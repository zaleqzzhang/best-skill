---
name: multi-platform-sentiment-dashboard
description: 为游戏/产品运营团队搭建一套跨平台舆情分析 Dashboard。当用户需要把 Discord、Facebook、YouTube、Reddit、X(Twitter)、TikTok、Web Search 等多个社区平台的用户反馈、帖子、评论、视频集中采集并做情感分析时，使用本 skill。本 skill 包含从多源数据采集、统一 ETL、到 Dashboard 渲染（舆情总览 / 官方社区 / 外部舆情 / 关键词追踪）的完整实现路径。
description_zh: 跨平台舆情分析 Dashboard
description_en: Multi-Platform Sentiment Dashboard
disable: false
agent_created: true
---

# Multi-Platform Sentiment Dashboard

## When to use

**Use this skill when** the user wants to build a unified sentiment/voice-of-customer dashboard that ingests community data from multiple social or community platforms and presents it with:

- Cross-platform aggregate view (total messages, sentiment distribution, trend, top channels/keywords)
- Official community view (Discord-like forums with channels, threads, active users)
- External view (Facebook, YouTube, Web mentions with post/video-level analytics)
- Keyword tracking (frequency trends over time)
- A clean static-frontend web UI that the user can host on any static-file service

**Do NOT use** for: single-platform monitoring, social publishing tools, paid-media analytics, customer-support ticketing. The skill is focused on the *listening* side (what users are saying), not the *speaking* side (publishing responses).

Typical trigger phrases from the user:
- "建一个跨多个平台的舆情 dashboard"
- "把 Discord/Facebook/YouTube/Reddit 的用户反馈整合起来看"
- "社区运营需要一个能看情感趋势和关键词的看板"
- "我想做一个游戏舆情分析系统"

## What you get

This skill encodes a production-grade approach validated in a real CrossFire Legends (CFL) deployment with **4 platforms × 45 days × tens of thousands of messages** running daily on GitHub Actions and a static-site CDN. The output is a **frontend-only dashboard** (HTML + JS, no server) that consumes pre-aggregated JSON data files — easy to host, easy to extend, no backend maintenance.

## Prerequisites & data source contract

Before you start, decide and document these two things — they shape the entire pipeline:

### 1. Where does the raw data live, and who can read it?

The dashboard is a **static SPA** that reads JSON files via HTTP. The two common choices:

| Option | Pros | Cons |
|---|---|---|
| **GitHub repo** (public or private) | Free, version-controlled, easy `fetch()`, no rate limits for normal use | Public repos expose data to everyone; private repos need a PAT in the frontend (read-only) |
| **Internal file host** (OA Pages, S3+CloudFront, internal CDN) | Full control over ACL, fast on internal network | You need to set up auth/CDN yourself |

**CFL's choice:** a private GitHub repo (`tuohaicuncunzhang/XiaoK`) is the **single source of truth** for both raw fetcher output and the ETL'd daily JSON. The dashboard frontend fetches from that repo's Pages deployment (raw content is the same, Pages serves it anonymously). The deployment pipeline uses a **GitHub PAT** to push updated JSONs.

```text
GitHub repo (private, with PAT)
   ├── data/raw/discord/YYYY-MM-DD.json      ← fetchers write here
   ├── data/daily/{platform}_YYYY-MM-DD.json ← ETL writes here
   ├── data/index.json                       ← ETL writes the manifest
   └── (dashboard.html + assets/)            ← frontend reads from here
```

### 2. Authentication tokens you will need

| Token | Where it lives | Scope | Risk if leaked |
|---|---|---|---|
| `GH_TOKEN` (GitHub PAT) | Pipeline env, e.g. `os.environ['GH_TOKEN']` | `repo` (push JSON) | Attacker can push to the repo — **keep it server-side only** |
| `DEEPSEEK_API_KEY` *or your LLM key* | Frontend JS (read by `translate.js` / `page-ask-ai.js`) | LLM API access | Attacker can burn your LLM quota — **see hardening notes below** |

**Frontend key safety:** in production you should *not* ship LLM API keys in plain JS. The CFL setup does ship them in JS for prototype speed, and accepts the risk. For real production, route LLM calls through a tiny serverless proxy you control (e.g. Cloudflare Worker / SCF) and put the key in env there. The skill's LLM client template (`assets/templates/llm-client.js`) is structured so you can swap the direct-call path for a proxy URL by changing one constant.

**Required permissions checklist** (print this, tick as you go):

- [ ] GitHub repo created (private recommended)
- [ ] PAT generated with `repo` scope, stored as `GH_TOKEN` env var in CI
- [ ] LLM API key obtained (DeepSeek / OpenAI / Anthropic / any OpenAI-compatible endpoint)
- [ ] Static host chosen (GitHub Pages / Cloudflare Pages / internal OA Pages) and accessible to your team
- [ ] Local dev server (`python -m http.server`) works for testing

## Architecture overview

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Discord API  │   │ Facebook API │   │ YouTube API  │   │ Web Search   │
│  (channels,  │   │  (posts,     │   │  (videos,    │   │  (SerpAPI /  │
│  messages)   │   │  comments)   │   │  comments)   │   │   custom)    │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │                  │
       ▼                  ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ fetch_       │   │ fetch_       │   │ fetch_       │   │ fetch_       │
│ discord.py   │   │ facebook.py  │   │ youtube.py   │   │ web.py       │
│ (per-channel │   │ (per-page    │   │ (search→     │   │ (per-query   │
│  threading)  │   │  pagination) │   │  videos→     │   │  results)    │
│              │   │              │   │  comments)   │   │              │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │                  │
       │   raw JSON per date (per platform)  │                  │
       └──────────────────┬──────────────────┴──────────────────┘
                          ▼
                  ┌───────────────────┐
                  │  etl_pipeline.py  │
                  │  - normalize      │
                  │  - sentiment      │
                  │  - aggregate      │
                  │  - emit index     │
                  └────────┬──────────┘
                           ▼
            ┌──────────────────────────────┐
            │  data/                       │
            │  ├── index.json  (lightweight│
            │  │   per-day summary)        │
            │  └── daily/                  │
            │      ├── discord_2026-06-01  │
            │      ├── facebook_2026-06-01 │
            │      ├── youtube_2026-06-01  │
            │      └── web_2026-06-01      │
            └──────────────┬───────────────┘
                           ▼
            ┌──────────────────────────────┐
            │  Dashboard (static SPA)      │
            │  - dashboard.html            │
            │  - assets/state.js           │
            │  - assets/router.js          │
            │  - assets/page-*.js (4 pages)│
            └──────────────────────────────┘
```

Three layers, each independently testable:
1. **Fetchers** — pure I/O, output raw JSON to `data/raw/{platform}/{date}.json`
2. **ETL** — pure transform, output normalized JSON to `data/daily/{platform}_{date}.json` + `data/index.json`
3. **Dashboard** — pure render, consumes the normalized JSON

## Steps

### Step 1 — Decide platforms and data sources

Pick 2–5 platforms based on where the audience actually talks. For each platform, identify:
- **API access**: official API keys vs. scraping vs. RSS
- **Quota limits**: per-day request budget and pagination strategy
- **Entity hierarchy**: channel → message (Discord), page → post → comment (Facebook), search → video → comment (YouTube)

For platform-specific implementation details, see `@references/platform-fetchers.md`.

### Step 2 — Design the unified data schema

The most important decision. Every platform must produce the same shape so the dashboard can be platform-agnostic. See `@references/data-schema.md` for the full schema. The minimum required fields:

```json
{
  "date": "2026-06-01",
  "platform": "discord",
  "total_messages": 99,
  "positive": 9, "negative": 18, "feedback": 1, "neutral": 71,
  "active_users": 23,
  "channels": [{"name": "general", "count": 41}, ...],
  "keywords": [{"word": "event", "count": 12}, ...],
  "all_messages": [{"user": "...", "content": "...", "sentiment": "positive", "timestamp": "..."}],
  "top_messages": [{"content": "...", "likes": 5, "sentiment": "positive"}],
  "_platform_meta": { /* platform-specific extras */ }
}
```

`index.json` is a lightweight per-day summary (no `all_messages`) so the dashboard can list dates without loading every detail.

### Step 3 — Build the fetchers

For each platform, write a `fetch_{platform}.py` that:
1. Reads from the platform API
2. Paginates and rate-limits
3. Outputs `data/raw/{platform}/{date}.json` with **as much original context as possible** (don't drop fields the ETL might need)

See `@references/platform-fetchers.md` for the patterns used for Discord, Facebook, YouTube.

### Step 4 — Build the ETL pipeline

`etl_pipeline.py` is the contract enforcer. It:
1. Loads raw JSON for the target date
2. Runs **sentiment analysis** on each message (recommend a small model or keyword-based fallback)
3. Aggregates per day: totals, sentiment distribution, active users, channels, keywords
4. Emits normalized JSON per platform + a merged per-day entry
5. Updates `data/index.json` with the new date

Key design rules — see `@references/etl-pipeline.md`:
- One `etl_pipeline.py` call handles **all platforms** for a given date
- Discord messages can span multiple days (timestamps differ from fetch date) — split by actual date
- Sentiment model: a small Hugging Face model OR a keyword list for low-resource fallback
- Idempotent: re-running for the same date overwrites cleanly

### Step 5 — Build the dashboard frontend

A static SPA with 4 pages. Recommended file layout:

```
dashboard.html
assets/
  ├── state.js      — global STATE, loadAllData()
  ├── router.js     — hash-based router, render dispatch
  ├── utils.js      — chart helpers, esc, time formatters
  ├── page-home.js                 — 舆情总览 (cross-platform aggregate)
  ├── page-community-sentiment.js  — 官方社区 (Discord-style)
  ├── page-external-sentiment.js   — 外部舆情 (FB/YT/Web)
  └── page-keywords.js             — 关键词追踪
```

For each page's design and code patterns, see `@references/dashboard-pages.md`.

### Step 6 — Automate with GitHub Actions

A daily cron workflow that:
1. Runs all fetchers in parallel
2. Runs `etl_pipeline.py --date $(date +%F)`
3. Commits the new `data/daily/*.json` and `data/index.json` back to the repo

Then the static-site host (Cloudflare Pages, GitHub Pages, Netlify, or internal OA Pages) auto-picks up the new commit and re-deploys.

### Step 7 — Deploy

The dashboard is **frontend-only** — any static host works. The CFL implementation deploys to an internal OA Pages instance. For external deployment: Cloudflare Pages (recommended, free) or GitHub Pages.

### Step 8 — (Optional) Add LLM-powered features

Two features dramatically improve a sentiment dashboard's usability and should be added once the data layer is stable:

1. **Selection-based translation** (`assets/translate.js`) — user selects any foreign text, a floating popup shows the Chinese translation. Useful for monitoring global communities.
2. **Data Q&A** (`assets/page-ask-ai.js`) — chat interface where the user asks natural-language questions; the LLM is given a system prompt injected with the same `data/index.json` + `data/daily/*.json` summaries the dashboard uses, so answers are grounded in real data.

Both features are **LLM-agnostic** — they call any OpenAI-compatible chat-completions endpoint (DeepSeek, OpenAI, Anthropic-via-proxy, local Ollama, internal gateway). The swap point is a single `LLM_ENDPOINT` + `LLM_API_KEY` pair, abstracted in `assets/templates/llm-client.js`. See `@references/ai-features.md` for design details, prompts, and security guidance.

## Pitfalls

These are real bugs hit during the CFL build. Skip them by following these rules:

- **Single-file JS parse error → whole dashboard white-screens.** All `<script>` tags are loaded in order; any syntax error in any file breaks everything. Always syntax-check after editing (`node -c assets/page-*.js`).
- **Don't repeat `const` declarations** (`isCN`, `STATE`, etc.). If two page files both declare `const STATE = ...`, the second one errors.
- **HTTP server required.** `file://` protocol is blocked by CORS for `fetch()`. Always serve via `python -m http.server` or any static server.
- **`data/index.json` is a SUMMARY only.** It has `total_messages / positive / negative / feedback / neutral / platforms` per day. Detail fields (`active_users`, `keywords`, `channels`, `all_messages`) are in `data/daily/{platform}_{date}.json`. Any code needing detail must read from the daily file with null guards.
- **Discord cross-day messages.** A raw fetch on 2026-06-01 can contain messages from 2026-05-31. The ETL must split them by the message's actual `timestamp` date, not the fetch date.
- **YouTube `published_at` vs `target_date`.** Comments have their own `published_at` — use that as the message timestamp, not the search target date.
- **Platform-specific view differences.** External pages (FB/YT) need post/video-level tables, not channel lists. Always show what the user can act on (e.g., the top 5 worst-rated videos), not just aggregates.
- **`<script>` tag order matters.** Pages must be loaded before `router.js` and `main.js`. Don't alphabetize.
- **IP-bound API tokens.** Some internal APIs (e.g., DataBrain) bind tokens to source IP. They will fail in CI from GitHub Actions. Document this; either run from a fixed IP or request an IP-free token.
- **Hash-router + `main.js` async.** If `loadAllData()` throws, the router never initializes and the page shows the loading spinner forever. Always wrap with try/catch and surface the error.
- **GitHub PAT in frontend = data leak.** A PAT with `repo` scope in any browser-served JS can be extracted and used to push malicious commits. **Never** put a write-capable PAT in `assets/`. Read-only fetches can use the `raw.githubusercontent.com` endpoint with no auth when the repo is public; if private, use a fine-grained read-only PAT and accept the small risk, or proxy through Cloudflare Worker.
- **LLM API key in frontend = quota leak.** Shipping `sk-...` keys in JS lets any user burn your quota. For prototypes this is acceptable; for production, route calls through a serverless proxy (Cloudflare Worker / SCF / Lambda) and keep the key server-side. The `llm-client.js` template is structured so the swap is one constant.

## Verification

After building, verify each layer in isolation:

1. **Fetchers** — output file exists, has expected raw fields
   ```bash
   python fetch_discord.py --date 2026-06-01 --output-dir ./data/raw
   ls data/raw/discord/2026-06-01.json
   ```

2. **ETL** — normalized file exists, schema validates, index is updated
   ```bash
   python etl_pipeline.py --date 2026-06-01 --input-dir ./data/raw --output-dir ./data
   python -c "import json; d=json.load(open('data/daily/discord_2026-06-01.json')); assert d['total_messages']==sum([d[k] for k in ['positive','negative','feedback','neutral']]); print('OK')"
   ```

3. **Dashboard** — starts cleanly, all 4 pages render, navigation works
   ```bash
   python -m http.server 8765
   # Open http://localhost:8765/dashboard.html
   # Click through all 4 nav items
   # Verify each shows real data, not empty states
   ```

4. **End-to-end** — run the GitHub Action, wait for commit, verify deployed dashboard

## File map

| File | Purpose |
|---|---|
| `SKILL.md` | This file — entry point, triggers, steps, pitfalls |
| `@references/architecture.md` | Deeper design rationale, why frontend-only, why per-platform files |
| `@references/data-schema.md` | Full unified schema, sentiment field semantics, `_platform_meta` extension points |
| `@references/platform-fetchers.md` | Per-platform fetching patterns: Discord threading, FB pagination, YT 3-step flow, Web search |
| `@references/etl-pipeline.md` | ETL design, sentiment analysis options, aggregation logic, idempotency |
| `@references/dashboard-pages.md` | Each of the 4 pages: data needs, layout, key interactions, common bugs |
| `@references/key-decisions.md` | Why we made the choices we did, alternatives considered |
| `@assets/templates/etl_pipeline.py` | Reference ETL implementation (with TODOs for sentiment backend) |
| `@assets/templates/fetch_discord.py` | Reference Discord fetcher |
| `@assets/templates/state.js` | Reference state manager |
| `@assets/templates/router.js` | Reference hash router |
| `@assets/templates/page-home.js` | Reference aggregate page |

## Extension points

After the base 4 pages are working, the same architecture cleanly extends to:

- **Market data** — add a `market` platform with its own fetcher (DAU/Revenue/etc.) and a new page reading from the same index
- **Esports tracking** — add an `esports` platform pulling tournament results, render as a new page
- **TikTok ecosystem** — TikTok Research API + video stats, treat as a special "video-only" platform
- **Sentiment model upgrade** — swap the keyword-based sentiment for a fine-tuned model without changing the schema
- **AI Q&A over data** — add a `state.summary` aggregation that an LLM can read to answer user questions

The schema's `_platform_meta` field exists precisely to absorb platform-specific extras without breaking the unified shape.
