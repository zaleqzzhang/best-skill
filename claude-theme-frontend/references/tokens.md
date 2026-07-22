# Token Reference

Complete `:root` block — paste at the top of any `<style>` block.

```css
:root {
  /* ── Brand ─────────────────────────────── */
  --color-primary:               #cc785c;  /* coral CTA */
  --color-primary-active:        #a9583e;  /* hover/press */
  --color-primary-disabled:      #e6dfd8;  /* disabled state */

  /* ── Text ──────────────────────────────── */
  --color-ink:                   #141413;  /* headlines, primary */
  --color-body-strong:           #252523;  /* emphasized body */
  --color-body:                  #3d3d3a;  /* default body */
  --color-muted:                 #6c6a64;  /* nav links, secondary */
  --color-muted-soft:            #8e8b82;  /* captions, copyright */

  /* ── Surfaces — cream ──────────────────── */
  --color-canvas:                #faf9f5;  /* page floor (THE brand color) */
  --color-surface-soft:          #f5f0e8;  /* section dividers */
  --color-surface-card:          #efe9de;  /* feature cards */
  --color-surface-cream-strong:  #e8e0d2;  /* active tabs, emphasis */

  /* ── Surfaces — dark ───────────────────── */
  --color-surface-dark:          #181715;  /* code mockups, footer */
  --color-surface-dark-elevated: #252320;  /* panels inside dark */
  --color-surface-dark-soft:     #1f1e1b;  /* code block bg */

  /* ── Borders ───────────────────────────── */
  --color-hairline:              #e6dfd8;  /* 1px borders on cream */
  --color-hairline-soft:         #ebe6df;  /* subtle dividers */

  /* ── On-color text ─────────────────────── */
  --color-on-primary:            #ffffff;  /* text on coral */
  --color-on-dark:               #faf9f5;  /* text on dark (echoes canvas) */
  --color-on-dark-soft:          #a09d96;  /* secondary text on dark */

  /* ── Accents ───────────────────────────── */
  --color-accent-teal:           #5db8a6;  /* status dots, connection indicators */
  --color-accent-amber:          #e8a55a;  /* category badges, highlights */

  /* ── Semantic ──────────────────────────── */
  --color-success:               #5db872;
  --color-warning:               #d4a017;
  --color-error:                 #c64545;

  /* ── Fonts ─────────────────────────────── */
  /* Display: Latin serif only — falls back to --font-body for CJK (no Chinese glyphs in Cormorant Garamond) */
  --font-display: "Copernicus", "Tiempos Headline", "Cormorant Garamond", "EB Garamond", Georgia, serif;
  /* Body: unified system stack — used for all body text, both Latin and Chinese pages */
  --font-body:    system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Helvetica, Arial, "PingFang SC", "Microsoft Yahei", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
  --font-code:    "JetBrains Mono", ui-monospace, "Cascadia Code", monospace;

  /* ── Spacing (4px base unit) ───────────── */
  --space-xxs:     4px;
  --space-xs:      8px;
  --space-sm:      12px;
  --space-md:      16px;
  --space-lg:      24px;
  --space-xl:      32px;
  --space-xxl:     48px;
  --space-section: 96px;   /* between major page bands */

  /* ── Border radius ─────────────────────── */
  --radius-xs:   4px;     /* tiny accents */
  --radius-sm:   6px;     /* small buttons, dropdown items */
  --radius-md:   8px;     /* buttons, inputs, category tabs */
  --radius-lg:   12px;    /* feature cards, product cards */
  --radius-xl:   16px;    /* hero illustration container */
  --radius-pill: 9999px;  /* badge pills, tags */
  --radius-full: 9999px;  /* icon buttons, avatars */

  /* ── Motion ─────────────────────────────── */
  --motion-instant: 80ms;
  --motion-fast:   160ms;
  --motion-normal: 240ms;
  --motion-slow:   360ms;
  --motion-lazy:   500ms;
  --ease-out:     cubic-bezier(0.16, 1, 0.3, 1);   /* primary — settle */
  --ease-in-out:  cubic-bezier(0.4, 0, 0.2, 1);    /* state transitions */

  /* ── Scroll reveal ─────────────────────── */
  --reveal-distance: 20px;
  --reveal-duration: var(--motion-slow);
  --reveal-ease:     var(--ease-out);
  --reveal-stagger:  70ms;
}
```

---

## Dark Theme Token Overrides

Apply `data-theme="dark"` on `<html>` to activate night mode. Coral `#cc785c` is unchanged — it reads well on dark navy. All cream surfaces flip to dark navy equivalents.

```css
/* ── Dark theme (data-theme="dark") ───────────────────────── */
[data-theme="dark"] {
  /* Page floors — swap cream for dark navy */
  --color-canvas:                #181715;   /* page floor → dark navy */
  --color-surface-soft:          #1f1e1b;   /* section alt → dark soft */
  --color-surface-card:          #252320;   /* feature cards → dark elevated */
  --color-surface-cream-strong:  #2e2c29;   /* active tabs, emphasis */

  /* Text — flip dark ink to warm white */
  --color-ink:                   #faf9f5;   /* headlines → warm white */
  --color-body-strong:           #e8e4de;   /* emphasized body */
  --color-body:                  #c4bfb8;   /* default body */
  --color-muted:                 #8e8b82;   /* nav links, secondary */
  --color-muted-soft:            #6c6a64;   /* captions, copyright */

  /* Borders — visible dark dividers */
  --color-hairline:              rgba(255, 255, 255, 0.08);
  --color-hairline-soft:         rgba(255, 255, 255, 0.05);

  /* On-color — dark card text uses warm white (already was faf9f5) */
  --color-on-dark:               #faf9f5;   /* unchanged */
  --color-on-dark-soft:          #a09d96;   /* unchanged */

  /* Dark surfaces become elevated (was already defined — no flip needed) */
  /* --color-surface-dark, --color-surface-dark-elevated, --color-surface-dark-soft unchanged */
}

/* ── Dark theme nav ──────────────────────────────────────── */
[data-theme="dark"] .top-nav {
  background: #181715;
  border-bottom-color: rgba(255, 255, 255, 0.08);
}
[data-theme="dark"] .top-nav__brand  { color: var(--color-ink); }
[data-theme="dark"] .nav-link        { color: var(--color-muted); }
[data-theme="dark"] .nav-link:hover  { color: var(--color-ink); }
[data-theme="dark"] .btn-text-link   { color: var(--color-muted); }
[data-theme="dark"] .btn-text-link:hover { color: var(--color-ink); }

/* ── Dark theme feature cards ───────────────────────────── */
[data-theme="dark"] .feature-card {
  background: var(--color-surface-card);   /* #252320 */
  border-color: rgba(255, 255, 255, 0.06);
}
[data-theme="dark"] .feature-card:hover {
  background: #2e2c29;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

/* ── Dark theme model / pricing cards ───────────────────── */
[data-theme="dark"] .model-card {
  background: var(--color-surface-card);
  border-color: rgba(255, 255, 255, 0.06);
}
[data-theme="dark"] .pricing-card {
  background: var(--color-surface-card);
  border-color: rgba(255, 255, 255, 0.06);
}
[data-theme="dark"] .pricing-card--featured {
  background: var(--color-surface-dark-elevated);
  border-color: rgba(204, 120, 92, 0.40);   /* coral border for featured */
}

/* ── Dark theme CTA bands ──────────────────────────────── */
[data-theme="dark"] .cta-band-coral {
  /* coral background is brand — unchanged in dark mode */
}
[data-theme="dark"] .cta-band-dark {
  background: var(--color-surface-card);
  border-color: rgba(255, 255, 255, 0.06);
}

/* ── Dark theme code window ────────────────────────────── */
/* Code windows are already dark — no override needed.
   In dark mode, use a slightly brighter surface for contrast:    */
[data-theme="dark"] .code-window {
  background: #0f0e0c;
  border-color: rgba(255, 255, 255, 0.06);
}

/* ── Dark theme inputs ─────────────────────────────────── */
[data-theme="dark"] input,
[data-theme="dark"] textarea,
[data-theme="dark"] select {
  background: var(--color-surface-card);
  color: var(--color-ink);
  border-color: rgba(255, 255, 255, 0.12);
}
[data-theme="dark"] input:focus,
[data-theme="dark"] textarea:focus {
  border-color: var(--color-primary);
  background: var(--color-surface-dark-elevated);
}

/* ── Dark theme footer ─────────────────────────────────── */
/* Footer is already dark-navy — in dark mode it merges with page floor.
   Add a top border to visually separate it:                      */
[data-theme="dark"] .footer {
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

/* ── Dark theme display typography — ink token auto-applies ── */
/* .display-* classes use `color: var(--color-ink)` — auto flips to #faf9f5 */

/* ── Body transition on theme switch ───────────────────── */
body {
  transition:
    background var(--motion-normal) var(--ease-out),
    color     var(--motion-normal) var(--ease-out);
}
```

### Theme Switcher JS

```javascript
/* ── Theme: respect OS pref, persist to localStorage ── */
const html = document.documentElement;
(function initTheme() {
  const saved = localStorage.getItem('claude-theme');
  if (saved) {
    html.setAttribute('data-theme', saved);
  } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    html.setAttribute('data-theme', 'dark');
  }
})();

document.querySelector('[data-theme-toggle]')?.addEventListener('click', () => {
  const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  if (next === 'light') html.removeAttribute('data-theme');
  else html.setAttribute('data-theme', 'dark');
  localStorage.setItem('claude-theme', next);
});
```

### Theme Toggle Button HTML

Add to `.top-nav__actions` before the primary CTA:

```html
<button class="theme-toggle-btn" data-theme-toggle aria-label="Toggle theme">
  <!-- Sun: shown in dark mode → click to switch to light -->
  <svg class="theme-icon-sun" width="16" height="16" viewBox="0 0 16 16" fill="none">
    <circle cx="8" cy="8" r="3" stroke="currentColor" stroke-width="1.5"/>
    <path d="M8 1v2M8 13v2M1 8h2M13 8h2M3.22 3.22l1.42 1.42M11.36 11.36l1.42 1.42M3.22 12.78l1.42-1.42M11.36 4.64l1.42-1.42"
          stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  </svg>
  <!-- Moon: shown in light mode → click to switch to dark -->
  <svg class="theme-icon-moon" width="16" height="16" viewBox="0 0 16 16" fill="none">
    <path d="M14 10.5A6 6 0 016.5 3a6 6 0 000 10A6 6 0 0014 10.5z"
          stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
  </svg>
</button>
```

```css
.theme-toggle-btn {
  background: transparent; border: none; cursor: pointer;
  color: var(--color-muted); padding: 8px;
  border-radius: var(--radius-md);
  display: flex; align-items: center; justify-content: center;
  transition: color var(--motion-fast) var(--ease-out);
}
.theme-toggle-btn:hover { color: var(--color-ink); }

/* Light mode (default): show moon → click to go dark */
.theme-icon-sun  { display: none; }
.theme-icon-moon { display: block; }

/* Dark mode: show sun → click to go light */
[data-theme="dark"] .theme-icon-sun  { display: block; }
[data-theme="dark"] .theme-icon-moon { display: none; }
```

---

## Typography Classes

```css
/* Display — Copernicus serif, weight 400 always, negative tracking required */
.display-xl { font-family: var(--font-display); font-size: 64px; font-weight: 400; line-height: 1.05; letter-spacing: -1.5px; color: var(--color-ink); }
.display-lg { font-family: var(--font-display); font-size: 48px; font-weight: 400; line-height: 1.10; letter-spacing: -1px;   color: var(--color-ink); }
.display-md { font-family: var(--font-display); font-size: 36px; font-weight: 400; line-height: 1.15; letter-spacing: -0.5px; color: var(--color-ink); }
.display-sm { font-family: var(--font-display); font-size: 28px; font-weight: 400; line-height: 1.20; letter-spacing: -0.3px; color: var(--color-ink); }

/* Title — system font stack, weight 500 */
.title-lg { font-family: var(--font-body); font-size: 22px; font-weight: 500; line-height: 1.30; color: var(--color-ink); }
.title-md { font-family: var(--font-body); font-size: 18px; font-weight: 500; line-height: 1.40; color: var(--color-ink); }
.title-sm { font-family: var(--font-body); font-size: 16px; font-weight: 500; line-height: 1.40; color: var(--color-ink); }

/* Body */
.body-md { font-family: var(--font-body); font-size: 16px; font-weight: 400; line-height: 1.55; color: var(--color-body); }
.body-sm { font-family: var(--font-body); font-size: 14px; font-weight: 400; line-height: 1.55; color: var(--color-muted); }

/* Labels */
.caption           { font-family: var(--font-body); font-size: 13px; font-weight: 500; line-height: 1.40; }
.caption-uppercase { font-family: var(--font-body); font-size: 12px; font-weight: 500; line-height: 1.40; letter-spacing: 1.5px; text-transform: uppercase; }

/* Code */
.code { font-family: var(--font-code); font-size: 14px; font-weight: 400; line-height: 1.60; }
```

---

## Google Fonts Import

Only the Latin display font needs a web font import. Body text uses the unified system stack (`--font-body`), which requires no CDN import on any platform — Latin or Chinese.

```html
<!-- Cormorant Garamond = Copernicus substitute (display headlines only) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
```

Chinese pages (`lang="zh-CN"`) use this exact same import — Cormorant Garamond has no CJK glyphs, so Chinese display headlines automatically fall back to `--font-body` (system stack, which already includes PingFang SC / Microsoft Yahei).

---

## Chinese Typography Classes

Chinese pages share the same font-family as Latin pages (`--font-display` for headlines with fallback to `--font-body`, `--font-body` for everything else). Only minor line-height, size, and text-transform adjustments are needed via `:lang(zh-CN)`:

```css
/* ── Chinese sizing/line-height tweaks — same font-family, denser text needs more air ─── */
:lang(zh-CN) .title-lg { font-size: 20px; line-height: 1.55; }
:lang(zh-CN) .title-md { font-size: 17px; line-height: 1.60; }
:lang(zh-CN) .title-sm { font-size: 16px; line-height: 1.60; }

:lang(zh-CN) .body-md  { font-size: 17px; line-height: 1.80; }
:lang(zh-CN) .body-sm  { font-size: 15px; line-height: 1.80; }

/* ── Chinese captions — no uppercase (CJK has no case) ─ */
:lang(zh-CN) .caption-uppercase { letter-spacing: 0.08em; text-transform: none; }

/* ── Base reset for Chinese pages ────────────── */
:lang(zh-CN) {
  word-break: break-all;
  overflow-wrap: break-word;
  font-feature-settings: "kern" 1;
}

/* ── Mobile Chinese overrides ────────────────── */
@media (max-width: 768px) {
  :lang(zh-CN) .display-xl { font-size: 28px; line-height: 1.40; }
  :lang(zh-CN) .display-lg { font-size: 24px; line-height: 1.42; }
  :lang(zh-CN) .display-md { font-size: 20px; line-height: 1.45; }
  :lang(zh-CN) .display-sm { font-size: 18px; line-height: 1.50; }
}
```

---

## Font Substitution

| Original (licensed) | Open-source substitute | Notes |
|---|---|---|
| Copernicus | Cormorant Garamond wght 400–500, tracking -0.02em | Closest match; Latin display headlines only |
| Copernicus | EB Garamond | Fallback |
| Tiempos Headline | Cormorant Garamond | Second substitute |
| StyreneB / body text (Latin + Chinese) | System font stack (`--font-body`) | No web font needed — resolves natively on every OS, includes PingFang SC / Microsoft Yahei for CJK |
| JetBrains Mono | JetBrains Mono | Free on Google Fonts |
