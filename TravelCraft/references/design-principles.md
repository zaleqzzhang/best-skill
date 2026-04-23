# Design Principles

Refined through multiple rounds of user feedback on the reference project. Follow these to avoid re-litigating settled decisions.

## Visual Identity: 宋式美学

The template is grounded in 宋代美学 — **restrained color, generous whitespace, fine lines, subtle patterns**. Not pure minimalism (素色 only) — 宋代 actually uses 天青 (汝窑)、酱釉 (建盏)、赭石 (丝绸) as accent colors on neutral grounds.

## Color Tokens

### Neutral base (always these)

```
--paper:    #F6F4F0   /* 米纸 background */
--card:     #FFFEFB   /* 月白 card */
--warm:     #FAF6F0   /* 暖米 XHS card */
--ink:      #2A2A2A   /* 墨 text */
--ink2:     #4A4A4A   /* secondary text */
--ink3:     #7A7A7A   /* tertiary */
--ink4:     #A8A8A8   /* label */
--line:     rgba(0,0,0,.06)  /* hairline */
```

### Accent (use sparingly as dots/bars, never large fills)

```
--rust:     #B07B5F   /* 赭石 — tags, XHS */
--indigo:   #5A7A9A   /* 靛蓝 — museum tag */
--bamboo:   #7A8B7A   /* 竹青 — free tag */
--plum:     #8B6F8B   /* 紫灰 */
```

## Visual Hierarchy via Background Color

The page uses **three background tiers** to distinguish info layers:

1. **Page background** = `--paper` (米纸).
2. **Card background** = `--card` (月白) — timeline, info cards.
3. **Summary background** = `bg-dN` (day-specific tint) — draws eye to "what's today about".
4. **XHS card** = `--warm` (暖米) — sits between card and paper.
5. **Warn block** = 粉红底 + 赭红左竖线.

When adding new sections: pick from this five-tier system, do not invent new background colors.

## Typography

- **Headings**: `'Noto Serif SC', serif` — classical feel for Chinese.
- **Body**: system UI stack — clean and legible.
- **Numbers (tl-time, etc.)**: sans-serif, small-caps feel.
- Letter-spacing matters: title 6–10px, labels 2–4px, body 0.
- Font sizes: base `14px` (desktop) → `16px` (export). Hero h1 `2.2em`. Summary title `.8em`. Body `.82em`.

## Line and Pattern Language

### Lines

- Hairlines (`1px` / `rgba(0,0,0,.06)`) as separators, not borders.
- Accent bars: 3–4px wide, use gradient fade to transparent.
- Underlines on active tab: centered, 24px wide, 2px thick.

### Patterns (SVG data URIs in CSS)

- **云雷纹** (hero BG): 48px tile, opacity `.1`, radial-mask transparent at center.
- **回字纹** (summary corner): 28px, opacity `.16`.
- **丝绸暗纹** (timeline corner): 120px, opacity `.04`.
- **缠枝纹** (photo default BG): 60px tile, opacity `.5`, hue 赭红.

Rule: patterns fill decorative spaces; they should NEVER compete with text or photos.

## Components That Work

These patterns emerged from iterations and should be kept:

- **Summary card** with colored tint + `::after` 回字纹 corner + 菱形 leading dot on `.st`.
- **Day accent** as a 4px vertical bar with circular caps top/bottom (like book binding).
- **Timeline connector** — 1.5px gradient line from `--ink4` fading to transparent.
- **Highlight timeline dot** — glowing ring using `box-shadow` spread.
- **XHS card brand dot** — 12×12 red gradient square before the "小红书" label.
- **Bottom nav items** — dual-line (大字 + 小标签) with colored active background.

## Anti-patterns (do NOT do)

Things that were tried and explicitly rejected:

| ❌ Don't | ✅ Do |
|----------|-------|
| Gradient dark banner at top, light content below | Warm→paper gradient hero, unified lightness throughout |
| Solid-filled color blocks for cards | White cards with subtle shadow, color only on accent bars |
| Leaflet/OSM interactive map | Static route map PNG |
| object-fit:cover everywhere (crops content) | Paired photos: 4:3 pre-cropped; single photos: height:auto |
| White image containers (look empty when loading) | Photo BG with 缠枝纹 pattern |
| Thick borders on every card | 1px hairlines only where absolutely needed |
| Giant hero photo | Text-focused hero with pattern BG |
| 折枝花 / floral decorations | 回字纹 / 云雷纹 / 丝绸暗纹 (geometric, scholarly) |
| Hotel price shown per day | Accommodation costs only in budget section |
| Chinese text + mixed bright promo tags | Muted tag colors in the ochre/indigo/bamboo palette |

## Decoration Rule

Every decorative element must answer: "Does this help read the content, or does it compete?" If the latter, reduce opacity, shrink, or remove.

Target opacity guidelines:

- Hero pattern: `.06`–`.10`.
- Corner ornaments: `.13`–`.16`.
- Background patterns (photo fallback): `.3`–`.5` (these can be stronger because they only show through gaps).
- Timeline / wrap decorations: `.03`–`.05`.

## Mobile-first Sizing

- Touch targets: ≥40×40px for any tappable element.
- Bottom nav items have `pointer-events:none` on children so taps resolve to parent.
- Hero title on mobile: `1.65em` + `6px` letter-spacing (smaller but still readable).
- Container padding on mobile: `14px` sides.
- Image captions: `.78em` on export (larger than `.68em` desktop default).

## Content Density

Rule of thumb: **a mobile screen (375×812) should show no more than 2 cards at a time**. Above that, visual density overwhelms. If content is too dense:

- Split long timelines across multiple `.tl-wrap` cards (e.g. morning/afternoon).
- Move non-critical info to `.info-card` below.
- Collapse food list into a single `.xhs` card rather than multiple entries.
