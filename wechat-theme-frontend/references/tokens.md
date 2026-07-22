# Token Reference

Complete `:root` block — paste at the top of any `<style>` block.

```css
:root {
  /* ── Brand ─────────────────────────────── */
  --color-primary:               #07c160;  /* WeChat green — CTA, brand */
  --color-primary-active:        #06ad56;  /* hover/press */
  --color-primary-soft:          #e0f7ea;  /* tinted backgrounds, squircle icon chips */
  --color-primary-disabled:      #a8e6c2;  /* disabled state */

  /* Official brand palette tokens (from wechat.design/brand/main-brand)
     — used for brand-accurate elements (logo, brand marks), not general typography */
  --color-brand-black:           #000000;  /* official pure black — logo/brand marks only */
  --color-brand-gray:            #7f7f7f;  /* official medium gray — brand materials */

  --color-link:                  #576b95;  /* classic WeChat inline text-link blue */
  --color-link-active:           #46567a;  /* link hover/press */

  --color-accent-red:            #fa5151;  /* notification dots, badges, errors ONLY */
  --color-accent-amber:          #fa9d3b;  /* warning, highlight tag */

  /* ── Text ──────────────────────────────── */
  --color-ink:                   #1a1a1a;  /* headlines, primary — true black, not warm-gray */
  --color-body-strong:           #333333;  /* emphasized body */
  --color-body:                  #576b7a;  /* NOTE: default body text is cool gray, see below */
  --color-body-default:          #666666;  /* default body text (use this, not the muted-blue above) */
  --color-muted:                 #888888;  /* nav links, secondary */
  --color-muted-soft:            #b2b2b2;  /* captions, copyright, placeholders */

  /* ── Surfaces — light ──────────────────── */
  --color-canvas:                #ffffff;  /* page floor — pure white (THE brand floor) */
  --color-surface-soft:          #f7f7f7;  /* section alternation, help-center bg */
  --color-surface-card:          #f5f5f5;  /* category / feature cards */
  --color-surface-strong:        #ececec;  /* active tabs, pressed states */

  /* ── Surfaces — dark ───────────────────── */
  --color-surface-dark:          #191919;  /* footer, dark-mode floor */
  --color-surface-dark-elevated: #232323;  /* panels/cards inside dark mode */
  --color-surface-dark-soft:     #2c2c2c;  /* code / mockup chrome bg */

  /* ── Borders ───────────────────────────── */
  --color-hairline:              #e5e5e5;  /* 1px borders on white */
  --color-hairline-soft:         #ededed;  /* subtle dividers */

  /* ── On-color text ─────────────────────── */
  --color-on-primary:            #ffffff;  /* text on green */
  --color-on-dark:               #ffffff;  /* text on dark surfaces */
  --color-on-dark-soft:          #a3a3a3;  /* secondary text on dark */

  /* ── Semantic ──────────────────────────── */
  --color-success:               #07c160;  /* same as brand green */
  --color-warning:               #fa9d3b;
  --color-error:                 #fa5151;

  /* ── Fonts — pure system stack, no web-font import ──── */
  /* No separate display face: headings = body font at weight 600 */
  --font-body:    -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Segoe UI", "Microsoft Yahei", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
  --font-code:    ui-monospace, "SFMono-Regular", "Cascadia Code", Consolas, monospace;

  /* ── Spacing (4px base unit) ───────────── */
  --space-xxs:     4px;
  --space-xs:      8px;
  --space-sm:      12px;
  --space-md:      16px;
  --space-lg:      24px;
  --space-xl:      32px;
  --space-xxl:     48px;
  --space-section: 80px;   /* between major page bands — denser than editorial systems */

  /* ── Border radius — roundness is WeChat's visual signature ── */
  --radius-xs:   6px;      /* tiny accents, tags */
  --radius-sm:   8px;      /* small buttons, dropdown items */
  --radius-md:   10px;     /* inputs, small cards */
  --radius-lg:   16px;     /* feature cards, category cards */
  --radius-xl:   20px;     /* squircle icon chips, hero illustration container */
  --radius-pill: 9999px;   /* CTA buttons — the default button shape */
  --radius-full: 9999px;   /* avatars, icon buttons */

  /* ── Motion — fast and functional, not editorial ───────── */
  --motion-instant: 80ms;
  --motion-fast:   160ms;
  --motion-normal: 220ms;
  --motion-slow:   280ms;
  --motion-lazy:   360ms;
  --ease-standard: cubic-bezier(0.25, 0.1, 0.25, 1);   /* primary — native-app settle */
  --ease-spring:   cubic-bezier(0.34, 1.56, 0.64, 1);  /* decorative accents ONLY (dots, bubbles) */

  /* ── Scroll reveal — short travel, quick settle ────────── */
  --reveal-distance: 12px;
  --reveal-duration: var(--motion-slow);
  --reveal-ease:     var(--ease-standard);
  --reveal-stagger:  50ms;
}
```

**Note on `--color-body`:** keep `--color-body-default` (#666666, neutral cool gray) as the token actually applied to `<body>` and paragraph text — it matches WeChat's help-center / newsroom body copy. The `--color-body` token above is kept only for naming parity with other theme systems; prefer `--color-body-default` in new components.

---

## Dark Theme Token Overrides

Apply `data-theme="dark"` on `<html>` to activate night mode. WeChat's own dark mode is genuinely near-black (not navy) — green is unchanged since it reads cleanly on true black.

```css
/* ── Dark theme (data-theme="dark") ───────────────────────── */
[data-theme="dark"] {
  /* Page floors — swap white for true dark */
  --color-canvas:                #191919;   /* page floor → true dark */
  --color-surface-soft:          #202020;   /* section alt */
  --color-surface-card:          #232323;   /* feature/category cards */
  --color-surface-strong:        #2c2c2c;   /* active tabs, pressed states */

  /* Text — flip true black to white */
  --color-ink:                   #ffffff;   /* headlines → white */
  --color-body-strong:           #e5e5e5;   /* emphasized body */
  --color-body-default:          #a3a3a3;   /* default body */
  --color-muted:                 #8a8a8a;   /* nav links, secondary */
  --color-muted-soft:            #666666;   /* captions, copyright */

  /* Link blue lightens slightly for contrast on dark */
  --color-link:                  #7a92c2;

  /* Green stays identical — brand color is theme-invariant */
  --color-primary-soft:          rgba(7, 193, 96, 0.16);

  /* Borders — visible dark dividers */
  --color-hairline:              rgba(255, 255, 255, 0.09);
  --color-hairline-soft:         rgba(255, 255, 255, 0.05);

  --color-on-dark:               #ffffff;
  --color-on-dark-soft:          #a3a3a3;
}

/* ── Dark theme nav ──────────────────────────────────────── */
[data-theme="dark"] .top-nav {
  background: #191919;
  border-bottom-color: rgba(255, 255, 255, 0.09);
}
[data-theme="dark"] .top-nav__brand  { color: var(--color-ink); }
[data-theme="dark"] .nav-link        { color: var(--color-muted); }
[data-theme="dark"] .nav-link:hover  { color: var(--color-ink); }
[data-theme="dark"] .btn-text-link   { color: var(--color-muted); }
[data-theme="dark"] .btn-text-link:hover { color: var(--color-ink); }

/* ── Dark theme feature / category cards ──────────────────── */
[data-theme="dark"] .feature-card,
[data-theme="dark"] .category-card,
[data-theme="dark"] .news-card {
  background: var(--color-surface-card);
  border-color: rgba(255, 255, 255, 0.06);
}
[data-theme="dark"] .feature-card:hover,
[data-theme="dark"] .category-card:hover {
  background: #2a2a2a;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
}

/* ── Dark theme squircle icon chip ─────────────────────────── */
[data-theme="dark"] .icon-chip {
  background: var(--color-primary-soft);
}

/* ── Dark theme CTA bands ──────────────────────────────────── */
[data-theme="dark"] .cta-band-green {
  /* green background is brand — unchanged in dark mode */
}
[data-theme="dark"] .cta-band-dark {
  background: var(--color-surface-card);
  border-color: rgba(255, 255, 255, 0.06);
}

/* ── Dark theme search bar / inputs ────────────────────────── */
[data-theme="dark"] .search-bar,
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

/* ── Dark theme footer ─────────────────────────────────────── */
/* Footer is already dark in both themes — add a hairline to separate from body when merged */
[data-theme="dark"] .footer {
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

/* ── Body transition on theme switch ───────────────────────── */
body {
  transition:
    background var(--motion-normal) var(--ease-standard),
    color     var(--motion-normal) var(--ease-standard);
}
```

### Theme Switcher JS

```javascript
/* ── Theme: respect OS pref, persist to localStorage ── */
const html = document.documentElement;
(function initTheme() {
  const saved = localStorage.getItem('wechat-theme');
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
  localStorage.setItem('wechat-theme', next);
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
  transition: color var(--motion-fast) var(--ease-standard),
              transform var(--motion-instant) var(--ease-standard);
}
.theme-toggle-btn:hover  { color: var(--color-ink); }
.theme-toggle-btn:active { transform: scale(0.92); }

/* Light mode (default): show moon → click to go dark */
.theme-icon-sun  { display: none; }
.theme-icon-moon { display: block; }

/* Dark mode: show sun → click to go light */
[data-theme="dark"] .theme-icon-sun  { display: block; }
[data-theme="dark"] .theme-icon-moon { display: none; }
```

---

## Typography Classes

No separate display font — headings use `--font-body` at weight 600, distinguished by size/tracking, not typeface.

```css
/* Display / headings — system sans-serif, weight 600 always */
.display-xl { font-family: var(--font-body); font-size: 52px; font-weight: 600; line-height: 1.20; letter-spacing: -0.02em; color: var(--color-ink); }
.display-lg { font-family: var(--font-body); font-size: 40px; font-weight: 600; line-height: 1.25; letter-spacing: -0.01em; color: var(--color-ink); }
.display-md { font-family: var(--font-body); font-size: 32px; font-weight: 600; line-height: 1.30; letter-spacing: 0;      color: var(--color-ink); }
.display-sm { font-family: var(--font-body); font-size: 24px; font-weight: 600; line-height: 1.35; letter-spacing: 0;      color: var(--color-ink); }

/* Title — weight 600, smaller scale */
.title-lg { font-family: var(--font-body); font-size: 20px; font-weight: 600; line-height: 1.40; color: var(--color-ink); }
.title-md { font-family: var(--font-body); font-size: 17px; font-weight: 600; line-height: 1.45; color: var(--color-ink); }
.title-sm { font-family: var(--font-body); font-size: 15px; font-weight: 600; line-height: 1.45; color: var(--color-ink); }

/* Body */
.body-md { font-family: var(--font-body); font-size: 15px; font-weight: 400; line-height: 1.60; color: var(--color-body-default); }
.body-sm { font-family: var(--font-body); font-size: 13px; font-weight: 400; line-height: 1.60; color: var(--color-muted); }

/* Labels */
.caption           { font-family: var(--font-body); font-size: 12px; font-weight: 500; line-height: 1.40; }
.caption-uppercase { font-family: var(--font-body); font-size: 12px; font-weight: 500; line-height: 1.40; letter-spacing: 0.05em; text-transform: uppercase; }

/* Inline text link — classic WeChat blue, not green */
.text-link { color: var(--color-link); text-decoration: none; transition: color var(--motion-fast) var(--ease-standard); }
.text-link:hover { color: var(--color-link-active); text-decoration: underline; }

/* Code */
.code { font-family: var(--font-code); font-size: 14px; font-weight: 400; line-height: 1.60; }
```

---

## Fonts — zero web-font import needed

Unlike serif-display design systems, WeChat requires **no `<link>` to Google Fonts and no `@font-face`**. Every typographic effect (hierarchy, roundness, character) is achieved with:
1. `font-weight: 600` for all headings (never a separate serif face)
2. Generous `border-radius` on buttons/cards/icon-chips (the actual source of WeChat's "rounded" feel post-2023 rebrand)
3. Slight negative/positive tracking per size (see typography scale)

This means pages using this theme load with **zero external font requests** — copy `--font-body` from the token block above and nothing else is required in `<head>`.

---

## Chinese Typography Classes

Chinese (`lang="zh-CN"`) is the **primary** language for this theme — build it first, not as a fallback.

```css
/* ── Chinese sizing/line-height tweaks — same font-family, denser text needs more air ─── */
:lang(zh-CN) .title-lg { font-size: 19px; line-height: 1.50; }
:lang(zh-CN) .title-md { font-size: 16px; line-height: 1.55; }
:lang(zh-CN) .title-sm { font-size: 15px; line-height: 1.55; }

:lang(zh-CN) .body-md  { font-size: 15px; line-height: 1.75; }
:lang(zh-CN) .body-sm  { font-size: 13px; line-height: 1.75; }

/* ── Chinese captions — no uppercase (CJK has no case), near-zero tracking ─ */
:lang(zh-CN) .caption-uppercase { letter-spacing: 0.02em; text-transform: none; }

/* ── Base reset for Chinese pages ────────────── */
:lang(zh-CN) {
  word-break: break-all;
  overflow-wrap: break-word;
  font-feature-settings: "kern" 1;
}

/* ── Mobile Chinese overrides ────────────────── */
@media (max-width: 768px) {
  :lang(zh-CN) .display-xl { font-size: 28px; line-height: 1.40; letter-spacing: 0; }
  :lang(zh-CN) .display-lg { font-size: 24px; line-height: 1.42; letter-spacing: 0; }
  :lang(zh-CN) .display-md { font-size: 21px; line-height: 1.45; letter-spacing: 0; }
  :lang(zh-CN) .display-sm { font-size: 18px; line-height: 1.50; letter-spacing: 0; }
}
```

---

## Reference Color Palette (source verification)

**Official brand palette** (来源：[wechat.design/brand/main-brand](https://wechat.design/brand/main-brand#标准色板))：

| 官方色块 | HEX | RGB | 官方角色 | 本 skill token |
|---|---|---|---|---|
| 🟩 | `#07C160` | `rgb(7,193,96)` | 品牌主色（微信绿） | `--color-primary` |
| ⬛ | `#000000` | `rgb(0,0,0)` | 辅助色（纯黑） | `--color-brand-black` |
| 🟥 | `#7F7F7F` | `rgb(127,127,127)` | 辅助色（中灰） | `--color-brand-gray` |
| ⬜ | `#EDEDED` | `rgb(237,237,237)` | 背景色（浅灰） | `--color-hairline-soft` |
| ⬜ | `#F7F7F7` | `rgb(247,247,247)` | 背景色（极浅灰） | `--color-surface-soft` |

> 官方色板仅 5 色。`#000000` 是品牌标识色（印刷/logo），Web 排版使用 `#1a1a1a`（`--color-ink`）以避免屏幕纯黑对比度过强。完整品牌规范 → `references/brand-guidelines.md`

**Extended web palette** (基于官方色板延伸的 Web 排版用色)：

| Color | Hex | Source / Use |
|---|---|---|
| WeChat Green | `#07c160` | Official brand primary — buttons, brand marks, success states |
| Link Blue | `#576b95` | Classic 公众号/朋友圈 inline article link color |
| Notification Red | `#fa5151` | Badge/unread-count red used across WeChat product UI |
| True Black text | `#1a1a1a` | Post-2023 rebrand headline/text color (previously dark gray) |
| Pure White floor | `#ffffff` | wechat.com, newsroom, safety-center light canvas |
| True Dark floor | `#191919` | WeChat native dark mode page floor |
