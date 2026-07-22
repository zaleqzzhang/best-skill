# Layout Reference

Band pacing rules, section container, responsive breakpoints, and KM article container. For the full page skeleton, see `assets/scaffold-en.html` / `assets/scaffold-zh.html`.

---

## Full Page Scaffold

A ready-to-copy scaffold with `<head>` boilerplate, top nav with theme toggle, the 5-band structure (Hero → Dark Showcase → Features → Coral CTA → Dark Footer), theme-switch JS, and scroll-reveal JS is provided as a real file — do not retype it, copy it directly:

- **English (`lang="en"`)** → `assets/scaffold-en.html`
- **Chinese (`lang="zh-CN"`)** → `assets/scaffold-zh.html` (font-size 17px / line-height 1.8 body defaults, `word-break: break-all` baked in)

Both scaffolds leave five `/* N. ... */` comment placeholders inside `<style>` — paste in, in order: (1) `:root` tokens from `references/tokens.md`, (2) `[data-theme="dark"]` overrides from `references/tokens.md`, (3) base reset (already included), (4) motion utilities from `references/motion.md`, (5) component styles from `references/components.md`.

---

## Band Pacing Rules

The page alternates between three surface modes — **never repeat the same mode in two consecutive bands.**

| Mode | Light theme token | Dark theme token | Typical use |
|---|---|---|---|
| Primary canvas | `--color-canvas` (`#faf9f5`) | `--color-canvas` → overridden to `#181715` | Hero, feature text, CTA wrapper |
| Card surface | `--color-surface-card` (`#efe9de`) | `--color-surface-card` → `#252320` | Feature card backgrounds (per-card) |
| Dark navy | `--color-surface-dark` (`#181715`) | `--color-surface-dark` (`#181715`, unchanged) | Product mockups, code windows, footer |

**Typical rhythm (both themes):** primary-canvas Hero → dark-navy Showcase → primary-canvas Features → coral CTA band → dark-navy Footer

Each section carries its own `background` and `padding: var(--space-section) 0` (96px). **Band edges are hard cuts** — the direct color contrast IS the pacing rhythm.

```css
/* ✅ Correct — tokens auto-adapt to current theme */
.hero-section     { background: var(--color-canvas);       padding: var(--space-section) 0; }
.showcase-section { background: var(--color-surface-dark); padding: var(--space-section) 0; }

/* ❌ Never — gradient divider elements break editorial pacing */
/* <div class="band-transition"> ... </div> */
```

---

## Section Container

All content is centered in an 1200px max-width container:

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
| Mobile | `< 768px` | Hamburger nav; hero stacks; grids go 1-up; display type shrinks |
| Tablet | `768–1024px` | Feature cards 2-up; connector tiles 3-up |
| Desktop | `1024–1440px` | Full nav; 3-up feature cards; 4-up+ connector tiles |
| Wide | `> 1440px` | Same as desktop; content capped at 1200px |

**Global mobile overrides:**

```css
@media (max-width: 768px) {
  /* Display type scale-down — Latin */
  .display-xl { font-size: 32px; letter-spacing: -0.5px; }
  .display-lg { font-size: 28px; letter-spacing: -0.3px; }
  .display-md { font-size: 24px; letter-spacing: -0.2px; }

  /* Display type scale-down — Chinese (no letter-spacing) */
  :lang(zh-CN) .display-xl { font-size: 28px; letter-spacing: 0; line-height: 1.40; }
  :lang(zh-CN) .display-lg { font-size: 24px; letter-spacing: 0; line-height: 1.42; }
  :lang(zh-CN) .display-md { font-size: 20px; letter-spacing: 0; line-height: 1.45; }
  :lang(zh-CN) .display-sm { font-size: 18px; letter-spacing: 0; line-height: 1.50; }

  /* Hero */
  .hero-band { padding: var(--space-xxl) 0; }
  .hero-band__container { grid-template-columns: 1fr; padding: 0 var(--space-md); }
  .hero-band__illustration { order: 2; }

  /* Grids */
  .feature-grid          { grid-template-columns: 1fr; }
  .model-comparison-grid { grid-template-columns: 1fr; }
  .footer__columns       { grid-template-columns: 1fr 1fr; }

  /* CTA bands */
  .cta-band-coral, .cta-band-dark { padding: var(--space-xxl) var(--space-md); }

  /* Nav */
  .top-nav__links { display: none; } /* show hamburger menu instead */
}

@media (max-width: 1024px) {
  .feature-grid { grid-template-columns: repeat(2, 1fr); }
}
```

---

## KM Article Container (opt-in — only when user explicitly says "km文章")

**Do not apply by default.** This override only activates when the user's request explicitly references KM article formatting ("km文章", "km排版", "发km", "km主题", etc.). In all other cases, use the standard `.section-container` (1200px, see above).

**KM format is identical to the standard Claude theme in every respect — colors, typography, spacing, radius, motion, components, dark mode — except the content column width.** KM (internal knowledge management platform) articles render in a narrower reading column than a marketing landing page. Two variants:

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

**Usage:** swap `.section-container` for `.km-article-container` in the page scaffold's sections when the KM trigger phrase is present. Keep all other Claude-theme tokens (color, type, motion) unchanged — only the width constraint differs from the standard landing-page layout.

---

## Elevation Philosophy

Depth comes from **color contrast, not shadows**. The system is color-block first:

| Level | Treatment |
|---|---|
| Flat | No shadow, no border — body sections, nav, hero |
| Hairline | `1px var(--color-hairline)` — inputs, sub-nav |
| Cream card | `background: var(--color-surface-card)` — feature cards |
| Dark surface | `background: var(--color-surface-dark)` — product mockups |
| Hover lift | `translateY(-3px)` + `box-shadow: 0 4px 16px rgba(20,20,19,0.06)` — cards on hover only |

The only shadow used: `0 1px 3px rgba(20,20,19,0.08)` on rare elevated hover states. Never apply shadow as a default resting state.
