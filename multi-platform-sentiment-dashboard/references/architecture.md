# Architecture

## Design principle: three independent layers

The dashboard is split into three layers that communicate **only through files on disk**:

```
Fetcher ──writes──▶ data/raw/ ──reads──▶ ETL ──writes──▶ data/daily/ + data/index.json ──reads──▶ Dashboard
```

Each layer can be:
- Tested in isolation
- Replaced without touching the others (swap a fetcher, change an aggregation, redesign a page)
- Re-run idempotently (re-running ETL for the same date produces the same output)

This is intentional. It is **not** a microservice architecture, **not** an event stream, **not** a database. It is a batch pipeline where the "queue" is the filesystem.

## Why frontend-only?

The dashboard is a **static SPA** with **no backend in production**:

1. **Cost** — Cloudflare Pages / GitHub Pages / internal OA Pages all serve static files for free or near-free. No server, no DB, no API gateway.
2. **Versioning** — Every dashboard version is a git commit. Easy to roll back, easy to diff, easy to audit.
3. **Speed** — JSON files load in tens of milliseconds from a CDN. No API roundtrip latency.
4. **Security** — Read-only data. No attack surface beyond the static host.

The trade-off: cannot do user-specific queries. The dashboard always shows the same data to everyone. This is fine for a team-internal community-ops tool.

## Why per-day, per-platform JSON files?

Consider the alternatives:

- **Single big JSON** with everything → too big, fetches too much
- **Database** (SQLite) → requires server, breaks the "static" property
- **One file per platform with all dates** → not granular enough for "show me June 1 only"
- **One file per date per platform** ✓ → small (5–50 KB each), fast to load, easy to recompute a single day

The `data/index.json` is a separate lightweight manifest that lists all available dates and their per-day summaries. The dashboard loads `index.json` first (a few KB), then lazily loads daily files only for the dates it needs.

## Why hash-based router?

The dashboard uses URL hashes (`#/home`, `#/community-sentiment`, etc.) instead of real URLs because:
- Static hosts don't need rewrite rules for SPA routing
- Browser back/forward works out of the box
- Links can be copy-pasted without server-side handling

The cost: no deep-linkable server-rendered pages. For a team-internal tool, this is fine.

## Why an ETL step instead of fetching directly into the dashboard format?

Two reasons:

1. **Fetcher changes are cheap.** If Discord's API changes, you change the fetcher, not the dashboard. The ETL absorbs the change into the unified schema.
2. **Re-sentiment is cheap.** Want to try a better sentiment model? Re-run the ETL on existing raw data, no need to re-fetch from APIs. This is the "data lake" idea applied at small scale.

The `data/raw/` directory is the long-term asset. The `data/daily/` files are derived. As long as raw is preserved, the daily files can always be regenerated.

## State management

The dashboard uses a single global `STATE` object (not Redux, not Vuex, just a plain object) because:

- The data graph is small (< 50 dates, < 4 platforms)
- Pages are independent — they don't need to subscribe to each other
- A re-render is cheap (no virtual DOM, just `innerHTML = ...`)

`loadAllData()` is called once on page load, fetches `index.json` + all daily files in parallel, populates `STATE`, then the router takes over. The total load is typically 50–200 KB and completes in under 1 second on a normal connection.

## Platform-agnostic core, platform-specific extensions

The unified schema has one escape hatch: `_platform_meta`. This is a free-form object that each platform can use to carry its own context:

- Discord: nothing extra needed (channels are first-class in the schema)
- Facebook: `_platform_meta.posts[]` (post-level aggregate: title, comment_count, total_likes, top_comments)
- YouTube: `_platform_meta.videos[]` (per-video stats: title, view_count, like_count, channel, query source), `_platform_meta.channels[]` (creator aggregate), `_platform_meta.queries[]` (search-term aggregate)
- Web: empty for now, but the field is there for future use

This is the **extension point** for any new platform. Add a fetcher, populate `_platform_meta`, render platform-specific widgets on the page that needs them.

## Trade-offs and alternatives considered

| Decision | Alternative | Why we didn't pick the alternative |
|---|---|---|
| Static SPA + JSON files | Next.js + API routes | More moving parts, needs Node.js server |
| Per-day, per-platform files | Single big JSON | Slow, can't filter by date |
| Frontend sentiment | Backend sentiment at fetch time | Locked in a single model, can't re-sentiment cheaply |
| Hash router | Real URLs | Needs server rewrite rules |
| Plain JS (no framework) | React/Vue | Smaller bundle, no build step, easier to deploy |
| Chart.js (where used) | D3 / ECharts | Chart.js is enough for 90% of needs and is much smaller |
| GitHub Actions for daily run | Cron on a VM | Free, versioned, audit-logged |
| Cloudflare Pages / OA Pages | Netlify (used previously) | Free tier limits, OA Pages is internal so faster |
