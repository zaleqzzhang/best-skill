# Unified Data Schema

The schema is the **contract** between the ETL and the dashboard. Every platform produces the same shape. The dashboard never reads platform-specific fields except inside `_platform_meta`.

## Top-level per-day, per-platform file

**File**: `data/daily/{platform}_{YYYY-MM-DD}.json`

```json
{
  "date": "2026-06-01",
  "platform": "discord",
  "total_messages": 99,
  "positive": 9,
  "negative": 18,
  "feedback": 1,
  "neutral": 71,
  "active_users": 23,
  "channels": [
    { "name": "general", "count": 41 },
    { "name": "bug-reports", "count": 28 },
    { "name": "suggestions", "count": 18 }
  ],
  "keywords": [
    { "word": "event", "count": 12 },
    { "word": "update", "count": 9 },
    { "word": "crash", "count": 5 }
  ],
  "all_messages": [
    {
      "user": "Alice#1234",
      "content": "Great update today!",
      "sentiment": "positive",
      "channel": "general",
      "timestamp": "2026-06-01T10:23:00Z"
    }
  ],
  "top_messages": [
    {
      "content": "Great update today!",
      "likes": 5,
      "user": "Alice#1234",
      "sentiment": "positive"
    }
  ],
  "_platform_meta": {}
}
```

## Field semantics

| Field | Type | Required | Meaning |
|---|---|---|---|
| `date` | string `YYYY-MM-DD` | ✓ | The day these messages belong to (NOT the fetch day) |
| `platform` | enum | ✓ | `discord` / `facebook` / `youtube` / `web` / `<your_platform>` |
| `total_messages` | int | ✓ | `len(all_messages)` |
| `positive`, `negative`, `feedback`, `neutral` | int | ✓ | Counts by sentiment. **Must sum to `total_messages`.** |
| `active_users` | int | ✓ | Unique users who posted/commented that day |
| `channels` | array | ✓ | Where the messages came from. For Discord: channel names. For FB/YT/Web: post titles or video titles. |
| `keywords` | array | ✓ | Top N keywords with counts |
| `all_messages` | array | ✓ | Every message that day. Can be capped (e.g., 500 most recent) for size. |
| `top_messages` | array | ✓ | Top K messages by engagement (likes, replies, etc.) |
| `_platform_meta` | object | optional | Platform-specific extras (see below) |

## Sentiment field values

`sentiment` is one of:
- `"positive"` — explicit praise, thanks, hype, success stories
- `"negative"` — complaints, bugs, frustration, anger
- `"feedback"` — constructive suggestions, feature requests, balanced critique
- `"neutral"` — questions, factual statements, greetings, off-topic

The split is intentional: `feedback` is **separate from neutral** because feedback is *actionable* — community ops wants to see it in its own bucket.

## Sentiment implementation

Two practical options:

### Option A — keyword-based (no ML, instant, low quality)

```python
POSITIVE = {"love", "great", "amazing", "awesome", "thanks", "good", "best", "happy", "excellent", "感谢", "棒", "好", "支持"}
NEGATIVE = {"hate", "bad", "worst", "broken", "crash", "bug", "trash", "garbage", "awful", "差", "烂", "bug", "卡顿"}
FEEDBACK = {"should", "could", "would", "suggest", "recommend", "maybe", "希望", "建议", "能不能"}
```

Match on the lowercased text. Fall back to `neutral` if no match. Quality is ~60–70% accurate. Good enough for trend tracking.

### Option B — small Hugging Face model (better quality, +200MB)

`cardiffnlp/twitter-roberta-base-sentiment-latest` is a strong small model. Map its 3 labels to our 4:
- LABEL_0 (negative) → `negative`
- LABEL_1 (neutral) → `neutral`
- LABEL_2 (positive) → `positive`
- Detect "should/could/I wish" patterns separately to upgrade neutral→feedback

Runs in <100ms per message on a CPU. Use this if you can spare 1GB of disk and want >85% accuracy.

## `_platform_meta` extension points

### Facebook
```json
"_platform_meta": {
  "posts": [
    {
      "title": "Post title or first 80 chars",
      "comment_count": 45,
      "total_likes": 230,
      "top_comments": [
        { "user": "...", "content": "...", "sentiment": "negative", "likes": 12 }
      ]
    }
  ]
}
```

### YouTube
```json
"_platform_meta": {
  "videos": [
    {
      "title": "Video title",
      "video_id": "abc123",
      "video_url": "https://youtube.com/watch?v=abc123",
      "channel_id": "UC...",
      "channel_name": "ChannelName",
      "view_count": 12000,
      "like_count": 340,
      "comment_count": 45,
      "query": "CrossFire Legends update"  // which search query found this video
    }
  ],
  "channels": [
    {
      "name": "ChannelName",
      "channel_id": "UC...",
      "channel_url": "https://youtube.com/channel/UC...",
      "video_count": 3,
      "total_views": 45000,
      "total_likes": 980
    }
  ],
  "queries": [
    { "query": "CrossFire Legends update", "video_count": 5, "total_views": 80000 }
  ]
}
```

### Discord
`_platform_meta` is usually empty — Discord's `channels` field is rich enough.

## index.json — the lightweight manifest

**File**: `data/index.json`

```json
{
  "days": [
    {
      "date": "2026-06-01",
      "platforms": {
        "discord": { "total_messages": 99, "positive": 9, "negative": 18, "feedback": 1, "neutral": 71 },
        "facebook": { "total_messages": 45, "positive": 2, "negative": 5, "feedback": 0, "neutral": 38 }
      },
      "total_messages": 144,
      "positive": 11,
      "negative": 23,
      "feedback": 1,
      "neutral": 109
    }
  ],
  "total_days": 45,
  "platforms": ["discord", "facebook", "youtube", "web"],
  "last_updated": "2026-06-01T03:00:00Z"
}
```

This is the **only file the dashboard needs to render its date picker and trend chart**. Detail fields are loaded lazily per-day-per-platform.

## Schema validation

In production, the ETL runs a self-check after writing each file:

```python
def validate(d):
    assert d["date"] and d["platform"]
    sentiment_sum = d["positive"] + d["negative"] + d["feedback"] + d["neutral"]
    assert sentiment_sum == d["total_messages"], f"{d['date']} {d['platform']}: sentiment sum {sentiment_sum} != total {d['total_messages']}"
    assert len(d["all_messages"]) > 0 or d["total_messages"] == 0
    return True
```

Any failure → halt the ETL and emit an error. The dashboard should never receive a malformed file.

## What we intentionally do NOT include in the schema

- **User IDs** — community ops usually wants usernames, not IDs. Store display names. If you need stable IDs, add a separate `user_id` field, but don't make it the primary key.
- **Full message history** — `all_messages` is capped (recommend 500 most recent per day per platform) to keep file size reasonable. Older messages live in the raw archive.
- **Raw payloads** — keep them in `data/raw/`, not in the daily files. The dashboard never needs them.
- **Cross-day normalization** — each day is independent. Trend calculations are done at render time, not stored.
