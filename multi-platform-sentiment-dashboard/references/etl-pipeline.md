# ETL Pipeline

The ETL is the **contract enforcer**. It takes raw fetcher output and emits the unified schema. It is the only place where sentiment analysis, aggregation, and cross-day splitting happen.

## Inputs and outputs

```
data/raw/discord/2026-06-01.json       ─┐
data/raw/facebook/2026-06-01.json      ├─▶ etl_pipeline.py ─▶ data/daily/discord_2026-06-01.json
data/raw/youtube/2026-06-01.json       │                      data/daily/facebook_2026-06-01.json
data/raw/web/2026-06-01.json           ─┘                    data/daily/youtube_2026-06-01.json
                                                              data/daily/web_2026-06-01.json
                                                              data/index.json (updated)
```

## CLI

```bash
python etl_pipeline.py --date 2026-06-01 \
    --input-dir ./data/raw \
    --output-dir ./data
```

The pipeline is **one-call-per-date** and processes all platforms for that date. Re-running for the same date is safe — it overwrites the daily files and updates `index.json` in place.

## Pipeline stages

### Stage 1 — Load raw data per platform

```python
def load_raw(platform, date, input_dir):
    """Read data/raw/{platform}/{date}.json, return list of raw records."""
    path = Path(input_dir) / platform / f"{date}.json"
    if not path.exists():
        return []  # platform had no data for this date
    return json.loads(path.read_text(encoding="utf-8"))
```

### Stage 2 — Sentiment analysis

Choose a backend at config time:

```python
SENTIMENT_BACKEND = "keyword"  # or "hf" for Hugging Face

def analyze_sentiment(text: str) -> str:
    if SENTIMENT_BACKEND == "hf":
        return _hf_sentiment(text)
    return _keyword_sentiment(text)
```

The keyword backend is fast (microseconds per message) and dependency-free. The HF backend needs `transformers` + `torch` and gives better accuracy on nuanced text.

### Stage 3 — Cross-day splitting (Discord only)

Discord messages have a `timestamp` field. The fetcher returns every message visible on the target date, including some from the previous day (if they were recent) and excluding some from the target date (if they fell off the recent list). The ETL **must** split by the message's actual timestamp date:

```python
def split_by_date(messages, target_date):
    """Yield (date_str, message) for each message based on its timestamp."""
    for m in messages:
        msg_date = m["timestamp"][:10]  # YYYY-MM-DD
        yield msg_date, m
```

This means a single raw fetch for 2026-06-01 can produce entries in both `data/daily/discord_2026-05-31.json` AND `data/daily/discord_2026-06-01.json`. The ETL writes to **both** files when this happens.

Other platforms (FB, YT, Web) typically don't need this — their raw fetches are already aligned to the target date.

### Stage 4 — Aggregation per platform

For each platform, compute:

| Field | How |
|---|---|
| `total_messages` | `len(messages)` |
| `positive/negative/feedback/neutral` | `Counter(sentiment for m in messages)` |
| `active_users` | `len(set(m["user"] for m in messages))` |
| `channels` | `Counter(m.get("channel") or m.get("post_title") or "unknown")` then top 20 |
| `keywords` | tokenize → lowercase → drop stopwords → Counter → top 30 |
| `top_messages` | sort by engagement (likes/reactions), top 10 |
| `all_messages` | full list, capped at 500 most recent |
| `_platform_meta` | platform-specific extras (see data-schema.md) |

### Stage 5 — Build platform_meta

Each platform's `_platform_meta` is computed here. This is the **only platform-specific code** in the ETL:

```python
def build_meta(platform, messages, date):
    if platform == "facebook":
        return _facebook_meta(messages)
    elif platform == "youtube":
        return _youtube_meta(messages)
    elif platform == "web":
        return _web_meta(messages)
    return {}
```

See `@data-schema.md` for the shape of each meta object.

### Stage 6 — Write daily file and validate

```python
def write_daily(platform, date, agg_data, output_dir):
    out = Path(output_dir) / "daily" / f"{platform}_{date}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(agg_data, ensure_ascii=False, indent=2), encoding="utf-8")
    validate(agg_data)  # raises on schema violation
```

### Stage 7 — Update index.json

`index.json` must be a **merge** of all dates, not a per-day file. Re-running for one date should update just that date's entry, not blow away the rest:

```python
def update_index(date, per_platform_summaries, output_dir):
    idx_path = Path(output_dir) / "index.json"
    if idx_path.exists():
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
    else:
        idx = {"days": [], "platforms": [], "total_days": 0}
    
    # Remove existing entry for this date
    idx["days"] = [d for d in idx["days"] if d["date"] != date]
    
    # Compute merged day summary
    day_entry = {"date": date, "platforms": {}}
    for plat, summary in per_platform_summaries.items():
        day_entry["platforms"][plat] = summary
    day_entry["total_messages"] = sum(s["total_messages"] for s in per_platform_summaries.values())
    day_entry["positive"] = sum(s["positive"] for s in per_platform_summaries.values())
    # ... etc
    
    idx["days"].append(day_entry)
    idx["days"].sort(key=lambda d: d["date"])
    idx["total_days"] = len(idx["days"])
    idx["platforms"] = sorted({p for d in idx["days"] for p in d["platforms"]})
    idx["last_updated"] = datetime.utcnow().isoformat() + "Z"
    
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")
```

## Idempotency

The pipeline is **idempotent**: re-running for the same date produces the same output (assuming raw input hasn't changed). This is critical because:
- The GitHub Action may retry on transient failures
- You may want to re-sentiment with a better model without re-fetching
- Manual backfills must not corrupt existing data

Concrete rules:
- `data/daily/{platform}_{date}.json` is **overwritten**, not appended
- `index.json` is updated by **replacing** the date's entry, not duplicating
- Cross-day splits must be careful: if you re-run for 2026-05-31, the messages that originally came from a 2026-06-01 fetch are still there, and the 2026-05-31 file will still be correct.

## Sentiment model trade-offs

| Backend | Accuracy | Speed | Cost | Best for |
|---|---|---|---|---|
| Keyword lists | 60-70% | <1ms/msg | Free | Prototyping, low-resource |
| VADER (NLTK) | 70-75% | 5ms/msg | Free, no GPU | English-only, basic nuance |
| Twitter-RoBERTa | 85%+ | 50-100ms/msg (CPU) | 500MB model, 1GB RAM | Production English |
| ERNIE/ChatGLM | 90%+ | 200ms+/msg (GPU) | GPU needed | Multilingual, best quality |

**Recommended starting point**: keyword lists, upgrade to VADER in week 2, swap to RoBERTa when you have >100k messages/day.

## Keyword extraction

Simple approach (no extra dependencies):

```python
STOPWORDS = {"the", "a", "an", "and", "or", "but", "is", "are", "this", "that", "to", "of", "in", "for", "on", "with", "as", "it", "be", "was", "i", "you", "we", "they", "..."}

def extract_keywords(messages, top_n=30, min_len=3):
    counter = Counter()
    for m in messages:
        text = m.get("content", "").lower()
        for word in re.findall(r"\b[a-z]{3,}\b", text):
            if word in STOPWORDS:
                continue
            counter[word] += 1
    return [{"word": w, "count": c} for w, c in counter.most_common(top_n)]
```

Better: use a domain-specific stopword list. Generic English stopwords miss game-specific noise (e.g., "lol", "gg" appearing 5000 times).

## Cross-day splitting caveats

The Discord split by timestamp can create **double-counting** if you're not careful:
- A message from 2026-05-31 23:55 is fetched during the 2026-06-01 run → it gets written to `data/daily/discord_2026-05-31.json` (correct, that's its actual day)
- But on the 2026-05-31 run, that message **was not in the fetch** (it was off the recent list) → `data/daily/discord_2026-05-31.json` is missing it

To handle this, the ETL should also **re-aggregate the previous day** when processing today, since late-arriving messages may have shifted the previous day's counts. Practical implementation: on every run, the ETL re-reads `data/raw/discord/{yesterday}.json` and re-emits `data/daily/discord_{yesterday}.json`. This keeps both days correct.

For a small community (< 10k messages/day) this is fine. For larger, you may want a "rolling 7-day re-aggregate" pattern.

## Common errors and how the ETL surfaces them

| Error | Detection | Action |
|---|---|---|
| Raw file missing for expected platform | `path.exists()` | Skip platform silently; log "no data for {platform} on {date}" |
| Malformed raw JSON | `json.loads` raises | Log + skip platform, don't fail the whole run |
| Sentiment model crashed on a message | try/except per message | Fall back to `neutral`, log |
| `total_messages != sum(sentiments)` | `validate()` assert | Halt pipeline, emit error to user |
| `index.json` write fails | try/except | Halt, the daily files are still valid |
| Disk full | OSError on write | Halt, surface error |

## Putting it all together

The full pipeline is ~300 lines of Python. See `@assets/templates/etl_pipeline.py` for a reference implementation. The most important thing is the **stages are independent** — you can swap any of them (different sentiment model, different keyword extractor, different aggregation) without touching the others.
