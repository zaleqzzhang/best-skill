#!/usr/bin/env python3
"""
fetch_discord.py — Reference Discord Fetcher
=============================================
Fetches messages from configured Discord channels and writes
data/raw/discord/{date}.json with as much original context as possible.

The ETL is responsible for normalization, sentiment, and aggregation.
"""
import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path


# ----- Configuration ---------------------------------------------------------

# Replace with your actual channel IDs
CHANNELS = {
    "general": "123456789012345678",
    "bug-reports": "123456789012345679",
    "suggestions": "123456789012345680",
}


# ----- API helpers -----------------------------------------------------------

def fetch_messages(channel_id, headers, base_url, limit=100):
    """Yield all messages from a channel, paginating with 'before' cursor."""
    url = f"{base_url}/channels/{channel_id}/messages?limit={limit}"
    while url:
        import requests
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        msgs = r.json()
        if not msgs:
            return
        for m in msgs:
            yield m
        last_id = msgs[-1]["id"]
        url = f"{base_url}/channels/{channel_id}/messages?limit={limit}&before={last_id}"
        time.sleep(0.4)  # rate limit (5 req / 2s)


def normalize_message(raw, channel_name):
    """Convert Discord API message to our internal shape."""
    author = raw.get("author", {})
    return {
        "id": raw["id"],
        "user": f"{author.get('username', '?')}#{author.get('discriminator', '?')}",
        "user_id": author.get("id"),
        "content": raw.get("content", ""),
        "channel": channel_name,
        "channel_id": raw.get("channel_id"),
        "timestamp": raw.get("timestamp"),
        "edited_at": raw.get("edited_timestamp"),
        "reactions": sum(r.get("count", 0) for r in raw.get("reactions", [])),
        "reply_to": (raw.get("referenced_message") or {}).get("id"),
        "attachments": len(raw.get("attachments", [])),
        "mentions": len(raw.get("mentions", [])),
        "pinned": raw.get("pinned", False),
        # Keep raw for debug / future re-extraction
        "_raw_type": raw.get("type"),
    }


# ----- Main ------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True, help="Target date YYYY-MM-DD")
    p.add_argument("--output-dir", default="./data/raw", help="Output root")
    args = p.parse_args()

    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN env var not set")
        return 1

    base_url = "https://discord.com/api/v10"
    headers = {"Authorization": f"Bot {token}"}

    import requests  # late import to fail fast if missing

    out_dir = Path(args.output_dir) / "discord"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.date}.json"

    all_messages = []
    for channel_name, channel_id in CHANNELS.items():
        print(f"  Fetching #{channel_name} ({channel_id})...")
        try:
            for raw in fetch_messages(channel_id, headers, base_url):
                msg = normalize_message(raw, channel_name)
                all_messages.append(msg)
        except requests.exceptions.HTTPError as e:
            print(f"    [WARN] {channel_name}: {e.response.status_code} {e.response.reason}")
            continue

    # Sort by timestamp ascending
    all_messages.sort(key=lambda m: m.get("timestamp") or "")

    out_path.write_text(
        json.dumps(all_messages, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n  Wrote {len(all_messages)} messages → {out_path}")
    return 0


if __name__ == "__main__":
    exit(main())
