# HTML Template Guide

The reference implementation at `assets/template/example-itinerary.html` is a complete, production-ready HTML that has been iteratively refined through many rounds of user feedback. **Do not rewrite it from scratch** — copy it and edit in place.

## How to Approach Editing

Unlike a skeletal template with `{{placeholders}}`, this is a filled-in example. To adapt it for a new trip:

1. Open the file.
2. Work top-down: title → hero → overview → day1 → day2 → ... → budget.
3. Replace text content, image paths, tab labels.
4. Add/remove day-sections to match the new trip's length.
5. Keep all CSS, JS, and structural markup untouched.

Use `replace_in_file` for targeted edits. Avoid `write_to_file` — rewriting the entire 1000+ line HTML risks losing carefully-tuned CSS.

## Sections to Edit (in order)

### 1. Document metadata

```html
<title>邯郸·安阳·登封·巩义 文化遗产自驾行程</title>
```

### 2. Hero

```html
<div class="hero">
  <div class="hero-deco">...</div>
  <h1>邯郸 · 安阳 · 登封 · 巩义</h1>      <!-- 主标题 -->
  <div class="sub">北朝石窟 · 殷商文明 · 天地之中 · 北宋皇陵</div>
  <div class="badges">
    <span class="badge">六天五晚</span>         <!-- 天数 -->
    <span class="badge">2026.4.28 — 5.3</span>   <!-- 日期 -->
    <span class="badge">自驾 ~650km</span>       <!-- 交通 -->
    <span class="badge">三人行</span>            <!-- 人数 -->
    <span class="badge">约 ¥10,700</span>        <!-- 预算 -->
  </div>
</div>
```

### 3. Tab bar + bottom nav

```html
<div class="tabs">
  <div class="tab active" data-day="overview">总览</div>
  <div class="tab" data-day="day1">壹 · 邯郸</div>    <!-- 每个 tab -->
  ...
</div>
```

```html
<nav class="bottom-nav"><div class="bnav">
  <a class="bi active" data-day="overview"><span class="n">览</span><span class="lbl">总览</span></a>
  <a class="bi" data-day="day1"><span class="n">壹</span><span class="lbl">邯郸</span></a>
  ...
</div></nav>
```

### 4. Overview day-section

Edit: route table, train/flight info, reminders, total budget.

Keep: the `.info-card` / `.card` structure.

### 5. Day sections (day1–day6)

Each follows:

```html
<div class="day-section" id="dayN">
  <div class="day-header">
    <div class="day-accent" style="background:var(--dN)"></div>
    <div class="day-header-text">
      <h2>Day N · 目的地</h2>
      <div class="date">四月廿X · 4/XX</div>
      <div class="route">A → B → C</div>
    </div>
  </div>

  <div class="summary bg-dN">
    <div class="summary-bar" style="background:linear-gradient(90deg,var(--dN),transparent)"></div>
    <div class="summary-body">
      <div class="st">今日</div>
      <p>2-3 句 summary</p>
    </div>
  </div>

  <div class="xhs">
    <div class="xt">小红书 · 话题</div>
    <div class="xc"><b>@博主</b>（XX赞）tip ...</div>
  </div>

  <div class="tl-wrap">
    <div class="tl-wrap-title">行程安排</div>
    <div class="timeline">
      <!-- entries -->
    </div>
  </div>
</div>
```

### 6. Timeline entry

```html
<div class="tl-item [highlight|drive|food]">
  <div class="tl-time">HH:MM — HH:MM</div>
  <div class="tl-title">标题</div>
  <div class="tl-desc">描述（可选）</div>
  <span class="tl-tag tag-[drive|museum|heritage|free|food]">标签</span>

  <!-- Single photo -->
  <div class="tl-photo">
    <img src="photos/xxx.jpg" onclick="openLightbox(this)">
    <div class="pc">说明</div>
  </div>

  <!-- OR paired photos (must be pre-cropped 4:3) -->
  <div class="tl-photos">
    <div class="tl-photo"><img src="photos/a.jpg" onclick="openLightbox(this)"><div class="pc">A</div></div>
    <div class="tl-photo"><img src="photos/b.jpg" onclick="openLightbox(this)"><div class="pc">B</div></div>
  </div>
</div>
```

### 7. Budget section (`id="budget"`)

Edit all tables and numbers. Keep the `.card` / `.total-card` wrappers.

## Color Token Assignment

Each day has an accent color via `--dN` variable. Current palette (CSS variables in `:root`):

```css
--d1: #8B4513  /* 赭棕 */
--d2: #2E7D32  /* 竹青 */
--d3: #1565C0  /* 靛蓝 */
--d4: #C41E3A  /* 朱砂 */
--d5: #6A1B9A  /* 紫灰 */
--d6: #E65100  /* 金黄 */
```

And summary background tints:

```css
.summary.bg-d1{background:#F5EDE7}  /* 赭粉 */
.summary.bg-d2{background:#EBF2EC}  /* 竹绿 */
.summary.bg-d3{background:#E9EFF5}  /* 靛蓝 */
.summary.bg-d4{background:#F5EBEB}  /* 赭红 */
.summary.bg-d5{background:#EFEBF4}  /* 紫灰 */
.summary.bg-d6{background:#F5F0E6}  /* 暖黄 */
```

## Adapting Day Count

### Fewer days (e.g. 3-day trip)

1. Delete `day4`, `day5`, `day6` `<div class="day-section">` blocks.
2. Delete matching `.tab[data-day="day4"]` etc. entries.
3. Delete matching `.bi[data-day="day4"]` etc. bottom-nav entries.

### More days (e.g. 7-day trip)

1. Duplicate the `day6` block, change id to `day7`, update `data-day="day7"` references.
2. Add `<div class="tab" data-day="day7">柒 · 城市</div>` to the tab bar.
3. Add `<a class="bi" data-day="day7"><span class="n">柒</span><span class="lbl">城市</span></a>` to bottom nav.
4. Add a `--d7` CSS variable and matching `.summary.bg-d7` tint.

## Component Inventory

Use only these components (do not invent new ones):

- `.hero` — top banner with 云雷纹 pattern.
- `.tabs-wrap > .tabs` — horizontal tab nav.
- `.day-section` — full day container.
- `.day-header` with `.day-accent` — day title with color strip.
- `.summary` with `.summary-bar` and `.summary-body` — 今日看点 card.
- `.xhs` — 小红书 recommendation card.
- `.tl-wrap` with `.tl-wrap-title` + `.timeline` — timeline inside white card.
- `.tl-item` with modifiers `.highlight`, `.drive`, `.food`.
- `.tl-photo` / `.tl-photos` — photo containers with pattern BG.
- `.info-card` / `.card` — generic info blocks.
- `.warn` — pink warning/reminder block.
- `.table` — striped info table.
- `.total-card` — highlighted budget total.
- `.bottom-nav` with `.bi` — mobile bottom tab bar.
- `.lightbox` — full-screen photo viewer.

## Template Decorations (do NOT remove)

Traditional patterns baked into CSS:

- **云雷纹 (cloud-thunder)** on `.hero::before` — bronze-pattern, radial-mask fades toward center.
- **回字纹 (hui-pattern)** on `.summary-body::after` — corner ornament, opacity `.16`.
- **丝绸暗纹 (silk damask)** on `.tl-wrap::before` — bottom-right corner, opacity `.04`.
- **缠枝纹 (vine pattern)** on `.tl-photo` default background — shows only where image doesn't cover.

## JavaScript

The template's inline `<script>` handles:

- Tab + bottom-nav click switching using `ev.currentTarget.getAttribute('data-day')`.
- `.bi .n` and `.bi .lbl` have `pointer-events:none` to prevent child-element event issues.
- Lightbox open on img click.

Do NOT replace with a framework.

## Things That Were Tried and Rejected

Accumulated user feedback on the reference project — do NOT re-introduce:

- ❌ **Leaflet + OpenStreetMap** — tiles blocked in mainland China.
- ❌ **Hotel nightly price inside day timeline** — belongs only in budget section.
- ❌ **Text-overlay cover photos as main images** — look promotional.
- ❌ **折枝花卉 pattern corner** — too floral for contemplative tone.
- ❌ **Water-ink illustrations as main photos** — user wants real site photos.
- ❌ **Deep-color hero + light body** — looks top-heavy.
- ❌ **Floating rate-card for hotel prices per day** — noise.

## Responsive Breakpoints

- Desktop (>768px): tabs on top, no bottom nav, container max 720px.
- Mobile (≤768px): bottom nav visible, container 100%, font scales down slightly.
- Export mode (via `make_export_html.py`): container forced to 440px, font size 18px base, all sections expanded.

