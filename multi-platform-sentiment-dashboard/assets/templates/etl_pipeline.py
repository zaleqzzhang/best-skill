#!/usr/bin/env python3
"""
ETL Pipeline — Reference Implementation
========================================
Reads data/raw/{platform}/{date}.json, applies sentiment, aggregates,
emits data/daily/{platform}_{date}.json + updates data/index.json.

This is a reference. Adapt the PLATFORMS list, sentiment backend, and
aggregation logic to your needs. See references/etl-pipeline.md for the
design rationale.
"""
import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path


# ----- Configuration ---------------------------------------------------------

PLATFORMS = ["discord", "facebook", "youtube", "web"]

# Keyword-based sentiment. For better accuracy, swap with HF transformers.
POSITIVE_WORDS = {
    "love", "great", "amazing", "awesome", "thanks", "good", "best", "happy",
    "excellent", "perfect", "wonderful", "fantastic", "推荐", "棒", "好",
    "支持", "感谢", "喜欢",
}
NEGATIVE_WORDS = {
    "hate", "bad", "worst", "broken", "crash", "bug", "trash", "garbage",
    "awful", "terrible", "差", "烂", "卡顿", "崩溃", "bug", "垃圾",
}
FEEDBACK_WORDS = {
    "should", "could", "would", "suggest", "recommend", "maybe", "wish",
    "希望", "建议", "能不能", "可否", "如果",
}

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "this", "that", "to",
    "of", "in", "for", "on", "with", "as", "it", "be", "was", "i", "you",
    "we", "they", "he", "she", "have", "has", "had", "do", "does", "did",
}


# ----- Sentiment -------------------------------------------------------------

def analyze_sentiment(text: str) -> str:
    """Return one of: positive, negative, feedback, neutral."""
    if not text:
        return "neutral"
    lower = text.lower()
    words = set(re.findall(r"\b\w+\b", lower))

    # Check in priority order: feedback first (most actionable)
    if words & FEEDBACK_WORDS:
        return "feedback"
    if words & NEGATIVE_WORDS:
        return "negative"
    if words & POSITIVE_WORDS:
        return "positive"
    return "neutral"


# ----- Aggregation -----------------------------------------------------------

def extract_keywords(messages, top_n=30):
    counter = Counter()
    for m in messages:
        text = (m.get("content") or m.get("message") or "").lower()
        for word in re.findall(r"\b[a-z]{3,}\b", text):
            if word in STOPWORDS:
                continue
            counter[word] += 1
    return [{"word": w, "count": c} for w, c in counter.most_common(top_n)]


def aggregate(platform, date, messages):
    """Build the per-day, per-platform aggregated structure."""
    sentiments = Counter(analyze_sentiment(m.get("content") or m.get("message") or "") for m in messages)

    # Channels: for Discord, the channel name; for FB/YT, the post/video title
    channel_counter = Counter()
    for m in messages:
        ch = m.get("channel") or m.get("post_title") or m.get("video_title") or "unknown"
        channel_counter[ch] += 1
    channels = [{"name": n, "count": c} for n, c in channel_counter.most_common(20)]

    keywords = extract_keywords(messages)

    # Top messages: sort by engagement (likes, reactions, replies)
    top = sorted(
        messages,
        key=lambda m: (m.get("likes") or m.get("reactions") or m.get("like_count") or 0),
        reverse=True,
    )[:10]
    top_messages = [{
        "content": m.get("content") or m.get("message") or "",
        "user": m.get("user") or m.get("from") or "unknown",
        "sentiment": analyze_sentiment(m.get("content") or m.get("message") or ""),
        "likes": m.get("likes") or m.get("reactions") or m.get("like_count") or 0,
    } for m in top]

    # Active users
    users = set()
    for m in messages:
        u = m.get("user") or m.get("from")
        if u:
            users.add(u)

    # All messages (capped at 500 most recent)
    all_messages = [{
        "user": m.get("user") or m.get("from") or "unknown",
        "content": m.get("content") or m.get("message") or "",
        "sentiment": analyze_sentiment(m.get("content") or m.get("message") or ""),
        "channel": m.get("channel") or m.get("post_title") or m.get("video_title"),
        "timestamp": m.get("timestamp") or m.get("created_time") or m.get("published_at"),
    } for m in messages[-500:]]

    return {
        "date": date,
        "platform": platform,
        "total_messages": len(messages),
        "positive": sentiments.get("positive", 0),
        "negative": sentiments.get("negative", 0),
        "feedback": sentiments.get("feedback", 0),
        "neutral": sentiments.get("neutral", 0),
        "active_users": len(users),
        "channels": channels,
        "keywords": keywords,
        "all_messages": all_messages,
        "top_messages": top_messages,
        "_platform_meta": build_meta(platform, messages),
    }


def build_meta(platform, messages):
    """Platform-specific extras. Override per platform."""
    if platform == "facebook":
        # Group by post
        posts = {}
        for m in messages:
            post_id = m.get("post_id") or m.get("parent_post")
            if not post_id:
                continue
            posts.setdefault(post_id, {
                "title": m.get("post_title", "")[:80],
                "comment_count": 0,
                "total_likes": 0,
                "top_comments": [],
            })
            posts[post_id]["comment_count"] += 1
            posts[post_id]["total_likes"] += m.get("likes", 0)
        return {"posts": list(posts.values())[:20]}

    if platform == "youtube":
        # Group by video
        videos = {}
        channels = {}
        for m in messages:
            vid = m.get("video_id")
            if not vid:
                continue
            videos.setdefault(vid, {
                "title": m.get("video_title", ""),
                "video_id": vid,
                "video_url": f"https://youtube.com/watch?v={vid}",
                "channel_name": m.get("channel_name", ""),
                "channel_id": m.get("channel_id", ""),
                "view_count": m.get("view_count", 0),
                "comment_count": 0,
            })
            videos[vid]["comment_count"] += 1

            ch_id = m.get("channel_id")
            if ch_id:
                channels.setdefault(ch_id, {
                    "name": m.get("channel_name", ""),
                    "channel_id": ch_id,
                    "channel_url": f"https://youtube.com/channel/{ch_id}" if ch_id else "",
                    "video_count": 0,
                    "total_views": 0,
                })
                channels[ch_id]["video_count"] += 1
                channels[ch_id]["total_views"] += m.get("view_count", 0)

        return {
            "videos": list(videos.values())[:20],
            "channels": list(channels.values())[:20],
            "queries": [],  # populated by fetcher if available
        }

    return {}


# ----- Validation ------------------------------------------------------------

def validate(d):
    """Raise if the daily file is malformed."""
    assert d["date"] and d["platform"], "missing date or platform"
    s = d["positive"] + d["negative"] + d["feedback"] + d["neutral"]
    assert s == d["total_messages"], (
        f"{d['date']} {d['platform']}: sentiment sum {s} != total {d['total_messages']}"
    )


# ----- Index management ------------------------------------------------------

def update_index(date, per_platform, output_dir):
    """Update data/index.json with the new date's entry."""
    idx_path = Path(output_dir) / "index.json"
    if idx_path.exists():
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
    else:
        idx = {"days": [], "platforms": [], "total_days": 0}

    # Remove existing entry for this date
    idx["days"] = [d for d in idx["days"] if d["date"] != date]

    # Build the day entry
    day = {
        "date": date,
        "platforms": {
            p: {
                "total_messages": d["total_messages"],
                "positive": d["positive"],
                "negative": d["negative"],
                "feedback": d["feedback"],
                "neutral": d["neutral"],
            }
            for p, d in per_platform.items()
        },
    }
    day["total_messages"] = sum(p["total_messages"] for p in day["platforms"].values())
    day["positive"] = sum(p["positive"] for p in day["platforms"].values())
    day["negative"] = sum(p["negative"] for p in day["platforms"].values())
    day["feedback"] = sum(p["feedback"] for p in day["platforms"].values())
    day["neutral"] = sum(p["neutral"] for p in day["platforms"].values())

    idx["days"].append(day)
    idx["days"].sort(key=lambda d: d["date"])
    idx["total_days"] = len(idx["days"])
    idx["platforms"] = sorted({p for d in idx["days"] for p in d["platforms"]})
    idx["last_updated"] = datetime.utcnow().isoformat() + "Z"

    idx_path.parent.mkdir(parents=True, exist_ok=True)
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")


# ----- Cross-day split (Discord only) ----------------------------------------

def split_by_date(messages):
    """Yield (date_str, message) for each message based on its timestamp."""
    for m in messages:
        ts = m.get("timestamp") or m.get("created_time") or ""
        if not ts:
            continue
        # ISO 8601: 2026-06-01T10:23:00Z → take first 10 chars
        yield ts[:10], m


# ----- Main ------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="ETL pipeline for sentiment dashboard")
    p.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    p.add_argument("--input-dir", default="./data/raw", help="Raw data directory")
    p.add_argument("--output-dir", default="./data", help="Output directory")
    p.add_argument("--platforms", default=",".join(PLATFORMS), help="Comma-separated platforms")
    p.add_argument("--migrate-legacy", action="store_true", help="Process yesterday too (for Discord late messages)")
    args = p.parse_args()

    platforms = args.platforms.split(",")
    dates_to_process = [args.date]
    if args.migrate_legacy:
        yesterday = (datetime.strptime(args.date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        dates_to_process.append(yesterday)

    in_dir = Path(args.input_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for date in dates_to_process:
        print(f"\n=== Processing {date} ===")
        per_platform = {}

        for platform in platforms:
            raw_path = in_dir / platform / f"{date}.json"
            if not raw_path.exists():
                print(f"  [{platform}] no raw data, skipping")
                continue

            messages = json.loads(raw_path.read_text(encoding="utf-8"))
            if not messages:
                print(f"  [{platform}] empty raw data, skipping")
                continue

            # Cross-day split (Discord)
            if platform == "discord":
                # Re-aggregate for the actual date of each message
                # For non-target dates, the file is still keyed by target_date
                # but the messages inside may belong to other dates
                pass  # see expanded logic in production etl_pipeline.py

            agg = aggregate(platform, date, messages)
            validate(agg)

            out_path = out_dir / "daily" / f"{platform}_{date}.json"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(agg, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  [{platform}] wrote {out_path} ({agg['total_messages']} msgs)")
            per_platform[platform] = agg

        if per_platform:
            update_index(date, per_platform, out_dir)
            print(f"  [index] updated {out_dir / 'index.json'}")

    print("\n✅ ETL complete")


if __name__ == "__main__":
    main()
