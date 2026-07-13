# Dashboard Pages

The dashboard has 4 pages. Each page is a single JS file exporting a `render(main)` function. The router dispatches based on the URL hash.

## Page 1 — Home (舆情总览 / Cross-Platform Aggregate)

**Purpose**: One-page overview of what's happening across all platforms right now. This is the page every team member sees first thing in the morning.

**Data needs**:
- `STATE.index.days` (all dates with per-platform summaries)
- `STATE.daysData[date]` (details for the selected date)

**Layout**:
```
┌──────────────────────────────────────────────────┐
│ [KPI: 今日消息量] [KPI: 活跃用户] [KPI: 情感分布] │
│ [KPI: 跨平台趋势]                                 │
└──────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────┐
│ 📈 消息量趋势 (stacked bar, all platforms)       │
│   [date range filter: 7d / 30d / 90d]            │
└──────────────────────────────────────────────────┘
┌──────────────────────┬───────────────────────────┐
│ 🔥 热门频道 (top 10) │ 🏷️ 热门关键词 (top 20)    │
└──────────────────────┴───────────────────────────┘
┌──────────────────────────────────────────────────┐
│ 👥 用户活跃排行 (top 10)                          │
└──────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────┐
│ 💬 精选消息 (latest 5-10)                         │
│   [card with platform badge, sentiment, content] │
└──────────────────────────────────────────────────┘
```

**Key design decisions**:
- **No platform filter on home** — Home is the aggregate view. Platform-specific details go to community-sentiment / external-sentiment pages.
- **Trend chart uses stacked bars** when "all platforms" is selected, single-platform line when one is selected.
- **Top messages sorted by recency**, not by engagement — Home is "what's happening NOW", not "what was popular".

**Implementation sketch**:
```js
async render(main) {
  main.innerHTML = `
    <h1>舆情总览</h1>
    <div id="home-kpi-grid"></div>
    <div class="card"><canvas id="home-trend-chart"></canvas></div>
    <div id="home-channels-keywords"></div>
    <div id="home-top-users"></div>
    <div id="home-recent-messages"></div>
  `;
  this._renderKPIs();
  this._renderTrend();
  this._renderChannelsAndKeywords();
  this._renderTopUsers();
  this._renderRecent();
}
```

## Page 2 — Community Sentiment (官方社区舆情)

**Purpose**: Deep dive into the official community — Discord-like channels where the product team and players talk directly. Focus on **channels, threads, active users**.

**Data needs**:
- `STATE.daysData[date]` for the selected date
- Platform filter chips (default: "all", but commonly Discord-heavy)

**Layout**:
```
┌──────────────────────────────────────────────────┐
│ Platform chips: [全部] [Discord] [Reddit] [...]  │
└──────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────┐
│ [KPI: 消息量] [KPI: 活跃用户] [KPI: 情感分布]    │
└──────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────┐
│ 📈 消息量趋势 (stacked by channel)               │
│ 📈 活跃用户趋势 (line)                           │
└──────────────────────────────────────────────────┘
┌──────────────────────┬───────────────────────────┐
│ 💬 频道分布 (top 15) │ 👥 用户排行 (top 10)     │
└──────────────────────┴───────────────────────────┘
┌──────────────────────────────────────────────────┐
│ ⭐ 精选消息 (sorted by engagement)               │
│   [Discord/Reddit badge + sentiment + content]  │
└──────────────────────────────────────────────────┘
```

**Key design decisions**:
- **Channels are the primary axis** — the page is organized by channel because that's how Discord is organized
- **User ranking shows the most active posters** — community ops uses this to find power users
- **Top messages sorted by engagement** (replies, reactions) — these are the messages that resonated

## Page 3 — External Sentiment (外部舆情)

**Purpose**: What people are saying OUTSIDE the official community — Facebook posts, YouTube videos, web mentions, tweets. Focus on **post/video-level analytics**, not channels.

**Data needs**:
- `STATE.daysData[date]` for the selected date
- Heavy use of `_platform_meta` for post/video lists

**Layout**:
```
┌──────────────────────────────────────────────────┐
│ Platform chips: [全部] [Facebook] [YouTube] [...]│
└──────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────┐
│ [KPI: 帖子/视频数] [KPI: 评论数] [KPI: 互动量]  │
└──────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────┐
│ 📈 评论/点赞趋势 (per platform, line)            │
└──────────────────────────────────────────────────┘
┌──────────────────────┬───────────────────────────┐
│ 📺 视频/帖子排行     │ 🎬 创作者排行             │
│ (top 10, clickable   │ (top 10, with channel     │
│  links)              │  links)                   │
└──────────────────────┴───────────────────────────┘
┌──────────────────────────────────────────────────┐
│ ⭐ 精选评论 (sorted by likes)                    │
│   [video source badge + comment]                │
└──────────────────────────────────────────────────┘
```

**Key design decisions**:
- **Post/video tables, not channel lists** — the entity is the post (FB) or video (YT), not the channel
- **Clickable links to original content** — community ops needs to be able to click through and reply
- **Creator rankings are channel-level** — for YT, group videos by creator to see who the top voices are
- **YouTube 趋势三图**: 播放量趋势 / 视频数趋势 / 创作者趋势 (no sentiment trend for YT — sentiment is on the post level, not the channel level)

**YouTube-specific quirk**: comments have their own `publishedAt` which is the actual comment time, NOT the video upload time. Use the comment's `publishedAt` for trend lines.

## Page 4 — Keywords (关键词追踪)

**Purpose**: Track specific keywords over time. Used for "is anyone talking about feature X?" or "is the word 'crash' spiking?"

**Data needs**:
- `STATE.daysData[date][platform].keywords` — but this is per-day, hard to trend
- Better: aggregate `keywords` across a date range at render time

**Layout**:
```
┌──────────────────────────────────────────────────┐
│ Date range: [last 7d ▼]                          │
│ Search: [type keyword]                           │
└──────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────┐
│ 📈 Keyword frequency trend (line chart)          │
│   [one line per matching keyword]                │
└──────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────┐
│ 🔥 Top keywords (table)                          │
│   [keyword, count, trend arrow]                  │
└──────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────┐
│ 💬 Matching messages (list, latest 50)           │
│   [highlight the keyword in content]             │
└──────────────────────────────────────────────────┘
```

**Key design decisions**:
- **Search-first interaction** — user types a word, dashboard shows trend + matching messages
- **No pre-defined keyword list** — let users search anything. Pre-defined lists become stale.
- **Highlight matched keywords in messages** — makes scanning easier
- **Trend across date range, not per-day** — the value is in seeing growth or decline over weeks

## Cross-page patterns

### State access

```js
// In any page, get the current data:
const data = STATE.daysData[STATE.currentDate];

// Or platform-filtered:
const platform = STATE.currentPlatform;  // 'all' | 'discord' | 'facebook' | ...
const filtered = platform === 'all' ? data : data[platform];
```

### Date navigation

The header has a date picker. When the user changes the date, the router re-renders the current page:

```js
// In state.js:
setDate(newDate) {
  STATE.currentDate = newDate;
  window.__reRenderCurrent();  // router.js exposes this
}
```

### Platform filter

Each page (except Home) has a platform chip row. The router resets `STATE.currentPlatform` on navigation:

```js
// router.js navigate():
if (route === 'community-sentiment') {
  STATE.currentPlatform = 'all';
} else if (route === 'youtube-ecosystem') {
  STATE.currentPlatform = 'youtube';  // default for YT-specific pages
} else {
  STATE.currentPlatform = 'all';
}
```

### Charts

Chart.js is the recommended library — small bundle (~60KB), easy to use, good defaults. For 90% of needs (line, bar, stacked bar, pie), it's enough. Only reach for ECharts/D3 when you need custom visualizations (heatmaps, force graphs, etc.).

**Common bug**: when navigating between pages, the previous page's chart instances must be destroyed, or the canvas keeps rendering in memory and the page leaks. Use `Utils.destroyAllCharts()` at the top of every page render.

### Empty states

Every page needs a graceful empty state for "no data for this date" or "filter matched 0 messages":

```html
<div class="empty-state">
  <div class="icon">🔍</div>
  <div>没有匹配的内容</div>
  <div class="hint">试试调整日期或筛选条件</div>
</div>
```

Don't show a broken page or a confusing `undefined` — always have a fallback.

### Loading state

If a page is slow (e.g., loading many daily files), show a spinner with a label, not just a blank area:

```html
<div class="loading">📊 加载中...</div>
```

## File-level rules

- **One page = one file** — `page-{name}.js` exporting `PageXxx.render(main)`. No bundler, no JSX, just plain ES6+.
- **No shared mutable state outside STATE** — if a page needs local state, use a module-level object. Don't pollute `window`.
- **All event listeners attached in render** — and cleaned up when the page is destroyed (use a simple `cleanup` pattern: `page.cleanup = () => { ... }` and call it in router).
- **No external API calls from the dashboard** — all data is in the JSON files. If you need a new data source, write a fetcher + ETL step, don't fetch from the browser.
- **Color palette** — use CSS variables from `styles.css`. Don't hardcode colors per page.

## Common bugs (from real production)

1. **Duplicate `const` declarations across pages** — e.g., two pages both declare `const isCN = ...`. Symptoms: only the first page works, others white-screen. **Rule**: namespace page-local consts under a per-page object, or use `let` and rename carefully.

2. **`<script>` tag order matters** — pages must load BEFORE `router.js` (which references them in `ROUTES`). Don't reorder alphabetically.

3. **`STATE.daysData[date]` is null on first load** — `loadAllData()` is async. Always null-check: `const data = STATE.daysData[date] || {}`.

4. **Cross-day UTC vs local time** — `new Date('2026-06-01').toISOString()` gives 2026-05-31 in negative-UTC timezones. Always construct with explicit time: `new Date('2026-06-01T00:00:00')` to avoid off-by-one days.

5. **Chart.js resize** — when the window resizes, charts must call `chart.resize()`. Use a single window-level resize listener that iterates all known charts, not one per chart.

6. **`<canvas>` height collapse** — if a canvas has no parent height, it renders at 0px. Always set explicit `height: 300px` on the parent.

7. **Long content overflow** — single very long messages (10k+ chars) can break layouts. CSS `overflow: hidden; text-overflow: ellipsis;` on content containers, with "show more" button for full text.

8. **Hash navigation triggering re-fetch** — clicking a nav link changes the hash, which triggers `hashchange`, which re-renders. Don't fetch in `render()` — fetch in `loadAllData()` once on page load, then render.
