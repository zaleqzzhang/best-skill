# Key Design Decisions

This document captures the **why** behind the choices, so future contributors (human or AI) can decide when to keep, evolve, or break the patterns.

## Decision 1 — Three-layer separation (fetcher / ETL / dashboard)

**What**: Raw data → ETL → Dashboard. Each layer is independent and only talks via files.

**Why**:
- Re-sentiment without re-fetching (try a new model, no API calls)
- Re-render without re-processing (change a chart, no data work)
- Each layer is testable in isolation
- Easy to onboard new contributors: "you only need to understand the contract for the layer you're working on"

**Alternatives considered**:
- **Single script that does fetch + process + render** — simpler initially, but couples everything
- **Microservices** — way too much overhead for a community-ops tool with < 1M messages/day
- **Stream processing (Kafka, etc.)** — overkill for batch daily cadence

**When to break this rule**: If you need real-time updates (< 1 min latency), the dashboard needs to subscribe to a stream. At that point, introduce a small backend that emits SSE or WebSocket events to the dashboard. Don't try to do real-time with file polling.

## Decision 2 — Static frontend, no backend in production

**What**: Dashboard is HTML + JS, served as static files. No Node.js / Python backend.

**Why**:
- **Cost**: $0 to host (Cloudflare Pages / GitHub Pages / internal Pages)
- **Speed**: CDN delivery, <100ms TTFB globally
- **Versioning**: Every deploy is a git commit
- **Security**: Read-only data, no attack surface

**Alternatives considered**:
- **Next.js with API routes** — adds Node.js runtime, build complexity, deployment friction
- **Flask + React** — needs a server, ongoing maintenance
- **VuePress / Docusaurus** — fine, but they're blog-focused, not dashboard-focused

**When to break this rule**: If the dashboard needs **per-user** data (e.g., "my watchlist", "my saved searches"). At that point, add a tiny auth layer and a thin backend. Keep most of the dashboard static; only the personalized parts need a server.

## Decision 3 — Per-day, per-platform JSON files (not one big file)

**What**: `data/daily/{platform}_{date}.json` (small) + `data/index.json` (manifest)

**Why**:
- The dashboard only needs a small subset of dates (typically the last 30-90 days) to render trends. Loading only what's needed is fast.
- One big file with 45 dates × 4 platforms = 180 nested objects = 1-2 MB. Most of that goes to waste.
- Per-day files are easy to recompute, easy to backfill, easy to inspect

**Alternatives considered**:
- **One file per platform with all dates** — too granular at the data level, too coarse at the date level
- **SQLite** — adds dependency, breaks the "static" property
- **One file per day with all platforms** — works, but doubles download size when you only want one platform

**When to break this rule**: If your date range is bounded (e.g., "only last 30 days") and platform count is small (≤ 3), a single file per day may be simpler. We've kept per-platform split because it scales to 5+ platforms.

## Decision 4 — `feedback` as a separate sentiment (not just positive/negative/neutral)

**What**: Four sentiment buckets — positive, negative, feedback, neutral.

**Why**:
- A suggestion like "could you add a dark mode?" is NOT positive AND not negative. It's actionable feedback.
- Community ops cares about feedback as much as positive/negative. Mixing it with neutral hides the signal.
- The cost is one extra bucket in the schema — trivial.

**Alternatives considered**:
- **3 buckets (pos/neg/neu)** — simpler, but loses the actionable signal
- **5 buckets (pos/neg/neu/feedback/question)** — more granular, but `question` is hard to detect from text reliably
- **Score from -1 to +1** — more flexible, but harder to present visually (pie charts, percentage bars)

**When to break this rule**: If your audience is non-English-speaking and the feedback signals are different (e.g., "要望" vs "建议" vs "希望" in Chinese), you may want a 5th bucket like "question". Or, switch to a score.

## Decision 5 — Google News RSS for web search layer (no API key)

**What**: Use the free `https://news.google.com/rss/search?q=...` endpoint for the web/news layer.

**Why**:
- No API key needed
- Returns structured RSS XML (easy to parse)
- Includes a wide range of news sources
- Free, no quota

**Alternatives considered**:
- **SerpAPI** — $50/mo, but covers Google Search + Google News + Google Scholar
- **Bing Search API** — $7/1000 calls, decent quality
- **News API (newsapi.org)** — $449/mo for production, free tier too limited
- **Custom Google News scraper** — fragile, Google changes HTML often

**When to break this rule**: If you need >1000 results per query, or non-English sources that Google News RSS doesn't cover, switch to SerpAPI or Bing.

## Decision 6 — Hash router, not real URLs

**What**: URL is `dashboard.html#/home`, not `dashboard.html/home`. Browser back/forward works, but server doesn't need rewrite rules.

**Why**:
- Static hosts (Cloudflare Pages, GitHub Pages) work without configuration
- Easier to deploy — drop the folder, done
- No 404 handling for deep links

**Alternatives considered**:
- **Real URLs with server rewrites** — works on most hosts, but adds config
- **Search params (`?page=home`)** — works, but uglier URLs

**When to break this rule**: If SEO matters (it doesn't for an internal tool), use real URLs. If you start getting requests for "shareable permalinks" with deep state (e.g., "send me the link to the dashboard for 2026-06-01 with platform=discord"), switch to search params: `?date=2026-06-01&platform=discord`.

## Decision 7 — Frontend sentiment, not backend

**What**: Sentiment analysis runs in the ETL step (Python), not in the dashboard (browser).

**Why**:
- The dashboard only displays pre-computed sentiments. Computing in browser is wasted work.
- Backend sentiment can use any model (HF transformers, VADER, custom). Frontend is limited to what's in JS.
- The schema's sentiment is the **contract** — the dashboard doesn't care how it was computed.

**Alternatives considered**:
- **Compute in browser via WebAssembly model** — possible, but slow and large bundle
- **Compute at fetch time in the platform API** — couples sentiment to fetcher, can't re-sentiment cheaply

**When to break this rule**: If you need real-time sentiment on user-typed text (e.g., a moderation layer), you'll need a backend. For the dashboard, ETL is correct.

## Decision 8 — Idempotent ETL, no append-only logs

**What**: Re-running ETL for the same date overwrites the daily file and updates the date's entry in `index.json`.

**Why**:
- The GitHub Action may retry on transient failures
- Re-sentiment with a better model requires re-running without data loss
- Manual backfills must be safe

**Alternatives considered**:
- **Append-only daily files** (`daily_2026-06-01_v1.json`, `_v2.json`) — safer in theory, but creates sprawl and complicates the dashboard (which one to load?)

**When to break this rule**: If you have a strict audit log requirement (regulated industry, GDPR right-to-erasure, etc.), keep append-only and add a separate cleanup job. The dashboard reads the latest version, but the audit log preserves history.

## Decision 9 — `STATE` global, not Redux/MobX/Zustand

**What**: Single global `STATE = { index, daysData, currentDate, currentPlatform, currentRoute }` plain object.

**Why**:
- The state graph is small (a few dozen fields, no deep nesting)
- Pages are independent and don't need to subscribe to each other
- Re-render is cheap — `main.innerHTML = ...` is fast for our content size
- Zero dependencies, zero learning curve

**Alternatives considered**:
- **Redux** — too much boilerplate for our needs
- **MobX** — fine, but adds a dependency
- **Zustand** — fine, but adds a dependency and a pattern
- **Component framework (React/Vue/Svelte)** — would change the whole structure; we kept plain JS for simplicity

**When to break this rule**: If the dashboard grows to 10+ pages with deep cross-page state (e.g., "selecting a keyword on Keywords page filters Home page"), consider Zustand. For 4 pages with simple state, plain object is enough.

## Decision 10 — `data/raw/` is preserved indefinitely

**What**: Raw fetcher output is never deleted. The daily files are derived and can be regenerated.

**Why**:
- Future sentiment model improvements can re-process historical data
- Bug investigation: "what did the raw Discord data look like on 2026-05-15 when the user complained?"
- Compliance: keep raw data for audit, even if normalized is wrong

**Alternatives considered**:
- **Delete raw after ETL** — saves disk, but loses re-processing ability
- **Compress and archive raw** — fine, but adds complexity

**When to break this rule**: Disk space pressure, or GDPR right-to-erasure (then both raw and normalized must be erasable). For most teams, raw is small (< 10MB/day), so keep it forever.

## Decision 11 — Cross-day splitting for Discord only

**What**: Discord raw fetches span multiple days, so the ETL splits by message timestamp. Other platforms (FB/YT/Web) don't need this.

**Why**:
- Discord fetches the "most recent N messages" from a channel, which can span days
- FB/YT/Web fetches are typically date-bounded at the API level (e.g., `publishedAfter`)
- Implementing it for FB/YT would be complexity for no benefit

**Alternatives considered**:
- **Always cross-day split** — robust, but adds code paths that never trigger
- **Never cross-day split** — simpler, but loses a few hours of late-day messages

**When to break this rule**: If you start using Reddit or X (Twitter) APIs, which also return time-windowed results, add cross-day splitting there too.

## Decision 12 — Platform-specific UI in `_platform_meta`, not in the schema

**What**: The unified schema has a `_platform_meta` field where each platform can put its own structure. Pages read it where needed.

**Why**:
- Keeps the core schema small and stable
- Adding a new platform doesn't require changing the schema, just adding meta structure
- Pages can `if (data._platform_meta.videos) renderVideoTable(...)` — opt-in

**Alternatives considered**:
- **Separate schema per platform** — clean per platform, but the dashboard has to handle 4 different shapes
- **One big schema with all possible fields** — most fields are null for most platforms, confusing

**When to break this rule**: If you find yourself adding the same field to `_platform_meta` for 3+ platforms (e.g., "share count"), promote it to the unified schema. The escape hatch is for one-off platform specifics.

---

## Summary table

| Decision | Why this and not the alternative |
|---|---|
| Three-layer separation | Re-sentiment without re-fetching |
| Static frontend | $0 hosting, no server, fast |
| Per-day per-platform files | Lazy load, easy backfill |
| 4 sentiment buckets (incl. feedback) | Actionable signal in its own bucket |
| Google News RSS | Free, no key, decent quality |
| Hash router | Static hosts, no rewrite rules |
| Backend sentiment | Re-sentiment possible, no model in browser |
| Idempotent ETL | Retry-safe, re-sentiment-safe |
| `STATE` global | Zero deps, small state graph |
| Keep `data/raw/` | Re-process, audit, debug |
| Cross-day split for Discord | Match real-world fetch behavior |
| `_platform_meta` escape hatch | Add platforms without schema changes |
