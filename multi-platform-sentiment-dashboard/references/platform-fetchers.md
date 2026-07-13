# Platform Fetchers

Each platform has a `fetch_{platform}.py` that:
1. Reads from the platform's API
2. Paginates, rate-limits, and persists
3. Outputs `data/raw/{platform}/{YYYY-MM-DD}.json` with **as much original context as possible**

The raw output is **not normalized**. The ETL does that. The fetcher's job is to capture everything the API gives, because you can never re-fetch historical data after a window closes.

## Generic shape

```python
def fetch(target_date: str, output_dir: str = "./data/raw", **opts) -> dict:
    """Fetch data for target_date, write raw JSON, return path."""
```

Common CLI:

```bash
python fetch_discord.py --date 2026-06-01 --output-dir ./data/raw
python fetch_facebook.py --date 2026-06-01 --output-dir ./data/raw
python fetch_youtube.py --date 2026-06-01 --output-dir ./data/raw
```

## Discord

**API**: Discord REST API (https://discord.com/developers/docs)
**Auth**: Bot token with `READ_MESSAGE_HISTORY` + `MESSAGE_CONTENT` intents
**Quota**: 5 requests/2s per route; 350 messages per channel per request

### Entity model
- **Server** (guild) → **Channel** → **Message**
- Cross-day split: a single fetch on 2026-06-01 may return messages from 2026-05-31 23:50 etc. Split by message `timestamp` date in the ETL.

### Implementation pattern

```python
import requests, time
from datetime import datetime, timezone

CHANNELS = ["general", "bug-reports", "suggestions", "events"]  # your channel names
TOKEN = os.environ["DISCORD_BOT_TOKEN"]
GUILD_ID = os.environ["DISCORD_GUILD_ID"]
BASE = "https://discord.com/api/v10"

def fetch_channel(channel_id, target_date):
    """Yield every message in channel_id (no date filter, ETL will split)."""
    headers = {"Authorization": f"Bot {TOKEN}"}
    url = f"{BASE}/channels/{channel_id}/messages?limit=100"
    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        msgs = r.json()
        if not msgs:
            return
        for m in msgs:
            yield m
        url = f"{BASE}/channels/{channel_id}/messages?before={msgs[-1]['id']}&limit=100"
        time.sleep(0.5)  # rate limit

def fetch_all():
    out = []
    for ch in CHANNELS:
        ch_id = resolve_channel_id(ch)  # look up from cache or /channels list
        for m in fetch_channel(ch_id, target_date):
            out.append({
                "id": m["id"],
                "user": f"{m['author']['username']}#{m['author']['discriminator']}",
                "content": m["content"],
                "channel": ch,
                "timestamp": m["timestamp"],
                "reactions": sum(r["count"] for r in m.get("reactions", [])),
                "reply_to": m.get("referenced_message", {}).get("id"),
                "attachments": len(m.get("attachments", []))
            })
    write_raw("discord", target_date, out)
```

### Pitfalls
- **Token leakage** — never commit the bot token; read from `DISCORD_BOT_TOKEN` env var
- **Permission bits** — bot must be in the guild with the right intents enabled in the developer portal
- **Message cap** — Discord returns max 100 per request; need `before`/`after` cursor
- **Time zone** — Discord timestamps are UTC ISO 8601; always convert with `datetime.fromisoformat(...).astimezone(timezone.utc)`
- **Threaded messages** — `referenced_message` may be null even when the message is a reply, if the parent was deleted

## Facebook

**API**: Graph API v19+ (https://developers.facebook.com/docs/graph-api)
**Auth**: Page access token (long-lived, ~60 days) or system-user token
**Quota**: 200 calls/hour per user; 4800 calls/day for a page

### Entity model
- **Page** → **Post** → **Comment**
- One Graph API call to fetch posts, another per post for comments. Capped at 100 posts and 5000 comments.

### Implementation pattern

```python
import requests, time

PAGE_ID = os.environ["FB_PAGE_ID"]
TOKEN = os.environ["FB_ACCESS_TOKEN"]
BASE = "https://graph.facebook.com/v19.0"

def fetch_posts():
    """Fetch posts from a Page (paged 100 at a time)."""
    posts = []
    url = f"{BASE}/{PAGE_ID}/posts?fields=id,message,created_time,comments.summary(true),reactions.summary(true)&limit=100"
    while url:
        r = requests.get(url, params={"access_token": TOKEN})
        r.raise_for_status()
        data = r.json()
        posts.extend(data.get("data", []))
        url = data.get("paging", {}).get("next")
        time.sleep(0.3)
    return posts

def fetch_comments(post_id):
    url = f"{BASE}/{post_id}/comments?fields=id,from,message,created_time,like_count,comment_count&limit=100"
    comments = []
    while url:
        r = requests.get(url, params={"access_token": TOKEN})
        r.raise_for_status()
        data = r.json()
        comments.extend(data.get("data", []))
        url = data.get("paging", {}).get("next")
        time.sleep(0.3)
    return comments
```

### Pitfalls
- **Token expiry** — long-lived tokens expire; renew via `/oauth/access_token?grant_type=fb_exchange_token`
- **Field expansion** — must explicitly request nested fields like `comments{...}` or they're null
- **Page vs User** — for community ops, fetch from a Page (public); for private groups you need a different approval process
- **Privacy** — only fetch public posts. The `privacy` field tells you, but a public page post is by definition public
- **Reaction vs Like** — `reactions.summary(true)` includes all reaction types (love, haha, angry, etc.). `like_count` on comments is separate

## YouTube

**API**: YouTube Data API v3 (https://developers.google.com/youtube/v3)
**Auth**: API key (free tier: 10,000 quota units/day; each `search.list` costs 100, each `videos.list` costs 1, each `commentThreads.list` costs 1)
**Quota**: design around the daily limit; one search costs 100 units → max 100 searches/day

### Entity model
- **Search query** → **Video** → **Comment**
- Three API calls per query: search → video stats → comment threads. ~102 units per query → ~98 queries/day on free tier.

### Implementation pattern

```python
import requests

API_KEY = os.environ["YT_API_KEY"]
BASE = "https://www.googleapis.com/youtube/v3"

QUERIES = [
    "CrossFire Legends update",
    "CrossFire Legends review",
    "CFL esports",
    # ...
]

def search_videos(query, published_after):
    """Step 1: find videos matching query."""
    r = requests.get(f"{BASE}/search", params={
        "key": API_KEY, "q": query, "part": "snippet",
        "type": "video", "order": "date", "maxResults": 50,
        "publishedAfter": published_after  # ISO 8601
    })
    r.raise_for_status()
    return [{
        "video_id": it["id"]["videoId"],
        "title": it["snippet"]["title"],
        "channel_id": it["snippet"]["channelId"],
        "channel_name": it["snippet"]["channelTitle"],
        "published_at": it["snippet"]["publishedAt"],
        "query": query
    } for it in r.json().get("items", [])]

def video_stats(video_ids):
    """Step 2: get view/like counts in one call."""
    r = requests.get(f"{BASE}/videos", params={
        "key": API_KEY, "id": ",".join(video_ids), "part": "statistics"
    })
    r.raise_for_status()
    return {it["id"]: it["statistics"] for it in r.json().get("items", [])}

def video_comments(video_id, max_comments=100):
    """Step 3: get top-level comments."""
    r = requests.get(f"{BASE}/commentThreads", params={
        "key": API_KEY, "videoId": video_id,
        "part": "snippet", "maxResults": max_comments, "order": "relevance"
    })
    r.raise_for_status()
    return [{
        "comment_id": it["id"],
        "user": it["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
        "content": it["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
        "published_at": it["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
        "like_count": it["snippet"]["topLevelComment"]["snippet"]["likeCount"],
        "video_id": video_id
    } for it in r.json().get("items", [])]
```

### Pitfalls
- **Quota exhaustion** — track quota usage in a counter; abort gracefully when near 10,000
- **Comments disabled** — some videos have comments off; handle the 403 gracefully
- **Channel ID vs handle** — use `channelId` from snippet for stable URL construction (`youtube.com/channel/UC...`). Don't confuse with `@handle` which can change.
- **Search relevance vs date** — `order=date` returns newest first, but only what matches the query. Combine with `publishedAfter` for time bounds
- **Top-level comments only** — `commentThreads` returns only top-level; use `comments.list` with `parentId` for replies (costs more quota, usually not needed)
- **`published_at` is the comment time, not the video time** — for sentiment trend, use the comment's `publishedAt`

## Web Search (optional)

For broader brand monitoring beyond owned social channels, a web search layer can pick up forum posts, blog articles, news mentions.

**Options**:
- **SerpAPI** (paid, $50/mo for 5k searches) — clean JSON results
- **Google News RSS** (free, no key) — `https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en` — limited to news only
- **Bing Web Search API** (paid, $7/1000 calls) — includes forums

### Pattern with Google News RSS

```python
import requests, xml.etree.ElementTree as ET

def fetch_news(query, language="en", region="US"):
    url = f"https://news.google.com/rss/search?q={query}&hl={language}-{region}&gl={region}&ceid={region}:{language.split('-')[0]}"
    r = requests.get(url, timeout=10)
    root = ET.fromstring(r.content)
    items = []
    for item in root.findall(".//item")[:30]:
        items.append({
            "title": item.find("title").text,
            "link": item.find("link").text,
            "pub_date": item.find("pubDate").text,
            "description": item.find("description").text,
            "source": item.find("source").text if item.find("source") is not None else "Google News",
            "query": query
        })
    return items
```

## Putting it together — a unified runner

```python
# run_fetchers.py
import argparse, sys
from datetime import datetime

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", default=datetime.utcnow().strftime("%Y-%m-%d"))
    p.add_argument("--output-dir", default="./data/raw")
    p.add_argument("--platforms", default="discord,facebook,youtube,web")
    args = p.parse_args()

    platforms = args.platforms.split(",")
    if "discord" in platforms:
        from fetch_discord import fetch as fetch_discord
        fetch_discord(args.date, args.output_dir)
    if "facebook" in platforms:
        from fetch_facebook import fetch as fetch_facebook
        fetch_facebook(args.date, args.output_dir)
    if "youtube" in platforms:
        from fetch_youtube import fetch as fetch_youtube
        fetch_youtube(args.date, args.output_dir)
    if "web" in platforms:
        from fetch_web import fetch as fetch_web
        fetch_web(args.date, args.output_dir)
```

Then the GitHub Action just calls:

```bash
python run_fetchers.py --date 2026-06-01
python etl_pipeline.py --date 2026-06-01 --input-dir ./data/raw --output-dir ./data
```
