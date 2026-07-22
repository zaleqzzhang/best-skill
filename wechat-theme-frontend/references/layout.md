# Layout Reference

Band pacing rules, section container, responsive breakpoints, and KM article container. For the full page skeleton, see `assets/scaffold-en.html` / `assets/scaffold-zh.html`.

---

## Full Page Scaffold

A ready-to-copy scaffold with `<head>` boilerplate (no web-font import needed), top nav with theme toggle, the 5-band structure (Hero → Icon Feature Grid → News/Category Grid → Green CTA → Dark Footer), theme-switch JS, and scroll-reveal JS is provided as a real file — do not retype it, copy it directly:

- **Chinese (`lang="zh-CN"`) — PRIMARY** → `assets/scaffold-zh.html` (build this first; Chinese is the default language for this theme)
- **English (`lang="en"`)** → `assets/scaffold-en.html`

Both scaffolds leave five `/* N. ... */` comment placeholders inside `<style>` — paste in, in order: (1) `:root` tokens from `references/tokens.md`, (2) `[data-theme="dark"]` overrides from `references/tokens.md`, (3) base reset (already included), (4) motion utilities from `references/motion.md`, (5) component styles from `references/components.md`.

---

## Band Pacing Rules

Unlike editorial systems that alternate cream/dark/cream, WeChat's pacing is **functional**: white and light-gray do most of the work, with the green CTA band as a rare punctuation mark and dark reserved almost exclusively for the footer.

| Mode | Light theme token | Dark theme token | Typical use |
|---|---|---|---|
| White canvas | `--color-canvas` (`#ffffff`) | overridden to `#191919` | Hero, article body, most sections |
| Light-gray surface | `--color-surface-soft` (`#f7f7f7`) | `#202020` | Section alternation, QR/download band |
| Card surface | `--color-surface-card` (`#f5f5f5`) | `#232323` | Feature/category card backgrounds |
| Green CTA | `--color-primary` (`#07c160`) | unchanged | Conversion moment — at most once or twice per page |
| Dark footer | `--color-surface-dark` (`#191919`) | unchanged (merges with floor) | Always the final band |

**Typical rhythm:** white Hero → white/light-gray Feature Grid → light-gray QR/Download band → white News/Category Grid → green CTA band → dark Footer

**Do not insert a full dark band mid-page** the way editorial systems do with product showcases — if a dark product-mockup moment is needed, keep it card-scoped (`.product-mockup-card` inside a white section) rather than a full-bleed dark section.

Each section carries its own `background` and `padding: var(--space-section) 0` (80px — tighter than editorial's 96px). **Band edges are hard cuts.**

```css
/* ✅ Correct — tokens auto-adapt to current theme */
.hero-section    { background: var(--color-canvas);      padding: var(--space-section) 0; }
.qr-section      { background: var(--color-surface-soft); padding: var(--space-section) 0; }

/* ❌ Never — gradient divider elements break the functional pacing */
/* <div class="band-transition"> ... </div> */
```

---

## Section Container

All content is centered in a 1200px max-width container:

```css
.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-xl); /* 32px side padding */
}
```

On mobile, reduce side padding:

```css
@media (max-width: 768px) {
  .section-container { padding: 0 var(--space-md); }
}
```

---

## Responsive Breakpoints

| Name | Width | Key changes |
|---|---|---|
| Mobile | `< 768px` | Hamburger nav; hero stacks; grids go 1-up; headings shrink; feature-grid → 1-up |
| Tablet | `768–1024px` | Feature/category cards 2-up; news cards 2-up |
| Desktop | `1024–1440px` | Full nav; 4-up feature cards; 3-up news cards |
| Wide | `> 1440px` | Same as desktop; content capped at 1200px |

**Global mobile overrides:**

```css
@media (max-width: 768px) {
  /* Heading scale-down — Latin */
  .display-xl { font-size: 28px; letter-spacing: 0; }
  .display-lg { font-size: 24px; letter-spacing: 0; }
  .display-md { font-size: 21px; letter-spacing: 0; }

  /* Heading scale-down — Chinese (identical values, tracking already 0) */
  :lang(zh-CN) .display-xl { font-size: 28px; line-height: 1.40; }
  :lang(zh-CN) .display-lg { font-size: 24px; line-height: 1.42; }
  :lang(zh-CN) .display-md { font-size: 21px; line-height: 1.45; }
  :lang(zh-CN) .display-sm { font-size: 18px; line-height: 1.50; }

  /* Hero */
  .hero-band { padding: var(--space-xxl) 0; }
  .hero-band__container { grid-template-columns: 1fr; padding: 0 var(--space-md); }
  .hero-band__illustration { order: 2; }

  /* Grids */
  .feature-grid    { grid-template-columns: 1fr; }
  .news-grid       { grid-template-columns: 1fr; }
  .category-grid   { grid-template-columns: 1fr; }
  .footer__columns { grid-template-columns: 1fr 1fr; }

  /* CTA bands */
  .cta-band-green, .cta-band-dark { padding: var(--space-xxl) var(--space-md); }
  .qr-band__inner { flex-direction: column; text-align: center; }

  /* Nav */
  .top-nav__links { display: none; } /* show hamburger menu instead */
}

@media (max-width: 1024px) {
  .feature-grid  { grid-template-columns: repeat(2, 1fr); }
  .news-grid     { grid-template-columns: repeat(2, 1fr); }
}
```

---

## Horizontal Scroll Containers (nav links, tab bars — no visible scrollbar)

**Problem:** Any row that can outgrow its container — nav link lists, category tab bars, chip filters — needs `overflow-x: auto` so it never wraps or breaks layout. But a bare `overflow-x: auto` renders the OS/browser scrollbar track on mobile web (and on desktop with a mouse), which reads as an unfinished, non-native UI element and breaks WeChat's flat, functional polish.

**Rule: any `overflow-x: auto` strip in this theme MUST use the `.scroll-fade-x` utility** — it hides the native scrollbar and replaces it with a soft edge fade that hints "more content this way" without any visible scrollbar chrome. This applies to `.top-nav__links`, `.tab-bar`, and any future horizontally-scrolling strip (filter chips, story reels, etc).

**Important device strategy — PC vs mobile:**

| Device | Nav links / tab bars | Why |
|---|---|---|
| **Desktop / PC** (≥1025px) | `flex-wrap: wrap` — let extra items flow to a second line naturally | PC viewports usually have room; wrapping keeps everything clickable and never needs a scrollbar |
| **Tablet / mobile** (≤1024px) | `.scroll-fade-x` — single line + horizontal scroll, edge-faded | Width is constrained; wrapping would create a tall "ladder" of items; horizontal scroll with edge fade is the mobile-native pattern |

**Never use `overflow-x: auto` on a desktop layout** — even with `.scroll-fade-x`, PC users get no useful scroll affordance (no touch swipe, no trackpad-on-horizontal-axis habit) and a wrapping layout is strictly better. The `.scroll-fade-x` utility is **mobile-only**.

```css
/* Default (PC): wrap to second line if too many items — never horizontal scroll. */
.top-nav__links,
.tab-bar { display: flex; gap: var(--space-xs); flex-wrap: wrap; }

/* Mobile / tablet (≤1024px): single line + scroll with edge fade. */
@media (max-width: 1024px) {
  .top-nav__links,
  .tab-bar {
    flex-wrap: nowrap;
    overflow-x: auto;
    scrollbar-width: none;        /* Firefox */
    -ms-overflow-style: none;     /* legacy Edge/IE */
    -webkit-overflow-scrolling: touch; /* momentum scroll on iOS */
    -webkit-mask-image: linear-gradient(to right, transparent, black 10px, black calc(100% - 10px), transparent);
            mask-image: linear-gradient(to right, transparent, black 10px, black calc(100% - 10px), transparent);
  }
  .top-nav__links::-webkit-scrollbar,
  .tab-bar::-webkit-scrollbar { display: none; height: 0; }
}
```

**Drop-in utility class** for ad-hoc horizontal strips (chip filters, story reels, etc.) that should be scrollable on all sizes — for those the edge fade IS appropriate at every breakpoint:

```css
.scroll-fade-x {
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
  -webkit-overflow-scrolling: touch;
  -webkit-mask-image: linear-gradient(to right, transparent, black 16px, black calc(100% - 16px), transparent);
          mask-image: linear-gradient(to right, transparent, black 16px, black calc(100% - 16px), transparent);
}
.scroll-fade-x::-webkit-scrollbar { display: none; height: 0; }

@media (max-width: 768px) {
  .scroll-fade-x {
    -webkit-mask-image: linear-gradient(to right, transparent, black 10px, black calc(100% - 10px), transparent);
            mask-image: linear-gradient(to right, transparent, black 10px, black calc(100% - 10px), transparent);
  }
}
```

**Nice-to-have (recommended for tab bars):** when a tab is selected via click/tap, scroll it into view so an off-screen active tab is never stranded:

```javascript
tab.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
```

**Anti-pattern — never do this on PC:**
```css
/* ❌ WRONG — applies scroll-fade-x to nav links at every breakpoint,
   forcing a PC user to discover a hidden horizontal scroll on a row
   that visually looks like a wrap-friendly nav. Either wrap (default)
   or scroll on mobile only. */
.top-nav__links { @apply .scroll-fade-x; }
```



---

## KM Article Container (opt-in — only when user explicitly says "km文章")

**Do not apply by default.** This override only activates when the user's request explicitly references KM article formatting ("km文章", "km排版", "发km", "km主题", etc.). In all other cases, use the standard `.section-container` (1200px, see above).

**KM format is identical to the standard WeChat theme in every respect — colors, typography, spacing, radius, motion, components, dark mode — except the content column width.** Two variants:

| Variant | Trigger | Max width |
|---|---|---|
| Standard KM article | "km文章" (no width qualifier) | **768px** |
| KM wide-screen article | "km文章宽屏" / "km宽屏主题" | **1024px** |

**Scope of the constraint — the whole content column, not just prose:** tables, charts, images, screenshots, flowcharts, embedded diagrams, and code blocks must all fit inside the same max-width. Nothing should force horizontal scroll on the page itself or bleed past the column edge.

```css
/* Replaces .section-container when building for KM */
.km-article-container {
  max-width: 768px;  /* use 1024px for the wide-screen variant */
  margin: 0 auto;
  padding: 0 var(--space-md);
}

@media (max-width: 768px) {
  .km-article-container { padding: 0 var(--space-sm); }
}

/* Force every content type to respect the column width */
.km-article-container img,
.km-article-container svg,
.km-article-container video,
.km-article-container canvas,
.km-article-container iframe {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Tables: don't let wide tables blow out the column — scroll internally instead */
.km-article-container table {
  display: block;
  max-width: 100%;
  overflow-x: auto;
  border-collapse: collapse;
}

/* Code blocks: wrap or scroll within the column, never overflow it */
.km-article-container pre {
  max-width: 100%;
  overflow-x: auto;
  box-sizing: border-box;
}

/* Charts / flowcharts / diagram wrappers */
.km-article-container .chart,
.km-article-container .flowchart,
.km-article-container .diagram {
  max-width: 100%;
  width: 100%;
  box-sizing: border-box;
}
```

**Usage:** swap `.section-container` for `.km-article-container` in the page scaffold's sections when the KM trigger phrase is present. Keep all other WeChat-theme tokens (color, type, motion) unchanged — only the width constraint differs from the standard landing-page layout.

---

## Elevation Philosophy

Depth comes from **subtle color-step contrast and thin borders, not heavy shadows** — reflecting WeChat's flat, functional visual language:

| Level | Treatment |
|---|---|
| Flat | No shadow, no border — body sections, nav, hero |
| Hairline | `1px var(--color-hairline)` — inputs, news cards, sub-nav |
| Card surface | `background: var(--color-surface-card)` — feature/category cards |
| Green surface | `background: var(--color-primary)` — CTA bands only |
| Hover lift | `translateY(-2px)` to `translateY(-3px)` + soft shadow — cards on hover only, never resting |

The only shadows used: `0 8px 24px rgba(0,0,0,0.08)` on news-card hover, `0 2px 12px rgba(0,0,0,0.06)` on search-bar focus. Never apply shadow as a default resting state — WeChat's depth language is color-step-first, shadow-second (even flatter than editorial systems, which occasionally use resting hairline + shadow combos).
