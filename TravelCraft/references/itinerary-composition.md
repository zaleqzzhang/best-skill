# Itinerary Composition

Phase 3 playbook. Turn research scratchpad into a day-by-day itinerary.

## Day Structure

Every day follows the same three-layer pattern for consistent rhythm:

```
┌─ Day Header ────────────────────────────────┐
│  Day N · Date · Route: A → B → C            │
└─────────────────────────────────────────────┘
┌─ 今日看点 (Summary) — colored soft bg ──────┐
│  2–3 sentences answering:                   │
│  什么值得看 · 什么值得吃 · 什么值得逛       │
└─────────────────────────────────────────────┘
┌─ 小红书推荐 (XHS card) — warm bg ───────────┐
│  1–2 bloggers, like-count, key tips         │
└─────────────────────────────────────────────┘
┌─ 行程安排 (Timeline) — white card ──────────┐
│  6–10 time entries (see Timeline Tags)      │
│  Photos embedded inside highlight entries   │
└─────────────────────────────────────────────┘
```

## Pacing Rules

### Spots per day (by party type)

| Party | Max main spots | Max total entries |
|-------|----------------|-------------------|
| Solo young adult | 5 | 10 |
| Couple | 4 | 9 |
| Family with seniors | 3 | 7 |
| Family with young kids | 2 | 6 |

One "main spot" = 1.5–3h of actual visit time. Transfers, meals, rest do not count.

### Daily shape

- **Start**: 08:00–09:00 typical departure. Earlier if peak holiday (before 08:00 for 少林寺国庆).
- **First spot**: 9:00–11:30 — the most energy-demanding one, ideally the headline attraction.
- **Lunch**: 11:30–13:00, then a rest buffer (no walking-heavy spot right after).
- **Afternoon**: 13:30–17:00, 1–2 spots.
- **Evening**: food/walk/light activity. Avoid museum-style spots after dinner.
- **Check-in**: ideally 16:00–19:00, not 22:00+. Late-night arrivals kill the next day.

### Driving time budget

- Single-day driving total: **max 4h** (including in-city). More exhausts elderly/children.
- Single segment: **max 2h** without rest stop.
- Mountain/back-road distance: use 1.5× the map estimate.

## Timeline Entry Format

Each entry has: `time_window · title · description · tag`.

### Tag system (from template)

| Tag | When | Color |
|-----|------|-------|
| `tag-drive` | Driving segment | gray |
| `tag-museum` | Museum visit | indigo |
| `tag-heritage` | World heritage / 国保 site | 赭石 |
| `tag-free` | Free entry | 竹青 |
| `tag-food` | Meal | 赭红 |
| `highlight` class | The day's star attraction | glowing dot |

Mark 1–2 entries per day with `highlight` — no more, or nothing stands out.

### Entry wording

Titles: 2–5 Chinese characters + optional English. Verbs preferred for transfer entries: `→ 登封`, not `登封路段`.

Descriptions: 8–20 chars, one specific detail. Example:

- Good: `妇好墓 · 甲骨文厅 · 车马坑。必须预约`
- Bad: `参观殷墟博物馆了解殷商文化，非常有意义`

Time windows: use `HH:MM — HH:MM` with em dash. For single-point events use only start time.

## Summary Writing

2–3 sentences. Answer three implicit questions:

1. **什么值得看** — the headline experience and why.
2. **什么值得吃** — one concrete local food hint.
3. **什么值得逛** — one specific area / street / market.

Write like a friend whispering, not a brochure. Example:

> 赵国故都、成语之乡。博物馆新馆磁州窑精品和赵国文物值得细看，五一延时至21:00。晚上逛串城街，这条古街浓缩三千年历史。

Avoid brochure clichés: 美不胜收 / 值得一游 / 流连忘返 / 绝佳打卡地.

## 小红书 Card Format

One XHS card per day, 1–2 bloggers:

```
@博主名（XX赞）核心tip · 另一tip / @其他博主（XX赞）食物1 · 食物2
```

Show like-count as credibility marker. Use `·` between tips, `/` between bloggers.

## Photo Placement

Embed photos **inside the timeline entry** of the relevant spot, not in a gallery. Options:

- `.tl-photo` (single): 1 portrait or landscape photo with caption.
- `.tl-photos` (paired grid): 2 photos side-by-side — must be pre-cropped to 4:3.

For highlight entries use 2–4 photos; for regular entries use 0–1.

Photo captions (`.pc`): 4–10 chars, factual — `大佛洞造像`, `花砖细节`. Avoid 美图 / 打卡 / 绝美.

## Per-Day Theme Color

Assign each day one token from the palette (`--d1` through `--d6`). Suggested mapping:

| Day | Token | Hue | Fits |
|-----|-------|-----|------|
| D1 | `--d1` | 赭棕 | arrival, city orient |
| D2 | `--d2` | 竹青 | nature, heritage |
| D3 | `--d3` | 靛蓝 | museum, learning |
| D4 | `--d4` | 朱砂 | highlight / festival day |
| D5 | `--d5` | 紫灰 | contemplative / monument |
| D6 | `--d6` | 金黄 | departure, reflection |

Swap freely per trip feel; what matters is each day has a unique accent.

## Overview Section

Before day 1, include:

- Trip title + dates + party + total distance + total budget (in `hero .badges`).
- Route table (day # · primary activity · color dot).
- Static route map if available (`photos/route_map.png`). **Do NOT use Leaflet/OSM** — the map tiles are blocked in mainland China.
- Top reminders (reservations, IDs, discounts) — each in a `.card` block.
- Train/flight schedule.

## Budget Section

Final section in the HTML. Structure:

1. Per-category breakdown (交通, 租车, 门票, 住宿, 餐饮).
2. Sub-tables with line items; tickets show per-person split (你/母/父/计).
3. **合计 + 人均** in a highlighted card.
4. One-line optimization hint (e.g. `控制餐饮可至 ~¥9,800`).

Apply discount rules:
- 60–69 year olds: half-price at most attractions.
- 70+: free at almost all 国家级/省级 attractions (still need ID).
- Under 6 / under 1.2m: typically free.
- Students with valid ID: half-price at many.

Show these discounts inline in per-person columns, not buried in footnotes.
