---
name: claude-theme-frontend
description: 'This skill should be used when building frontend UI in the Claude style design system — landing pages, hero sections, feature grids, pricing tables, code windows, product cards, or any page needing warm cream/dark-navy theming, coral CTAs, slab-serif display type, and matching motion. Covers light/dark mode via data-theme, and English/Chinese (zh-CN) pages. When the request mentions "km" (km文章/km排版/km风格), constrain content to a narrower reading column (768px, or 1024px if "宽屏" is specified) while keeping all other styling unchanged.'
---

# Claude Theme Frontend Skill

Build polished, on-brand frontend components following the Claude/Anthropic editorial design system — covering design tokens, component patterns, motion, and page structure.

**Detailed references live in `references/` — load only what the task needs. Do not duplicate their content here; this file holds only the always-on rules and a quick-lookup summary.**

| File | Contents |
|---|---|
| `references/tokens.md` | Authoritative `:root` token block, dark-theme overrides + theme switcher JS, typography classes, Chinese typography classes, Google Fonts import, font substitution table |
| `references/components.md` | HTML + CSS for all 13 components (nav, buttons, cards, footer, etc.) |
| `references/motion.md` | Scroll reveal, page load sequence, dark-card entrance, typewriter, coral pulse |
| `references/layout.md` | Band pacing rules, section container, responsive breakpoints, KM article container (768px/1024px, opt-in) — points to `assets/scaffold-en.html` / `assets/scaffold-zh.html` for the full page skeleton |
| `assets/scaffold-en.html` | Ready-to-copy English page scaffold (head, nav, 5 bands, theme + reveal JS) |
| `assets/scaffold-zh.html` | Ready-to-copy Chinese (`lang="zh-CN"`) page scaffold |

---

## Core Principles (always active)

**Brand identity — non-negotiable:**
- Default canvas is `#faf9f5` (warm cream) in light mode; dark night mode uses `#181715` (dark navy) as page floor
- Coral `#cc785c` is the sole accent in **both themes**: scarce on individual buttons, generous on full-bleed callout bands
- Display headlines use Copernicus/Tiempos Headline (substitute: Cormorant Garamond) at **weight 400, never bold**, with negative letter-spacing. Cormorant Garamond has no CJK glyphs — Chinese headlines fall back to `--font-body` (the unified system stack)
- Body uses a single unified system font stack for both Latin and Chinese text (see Fonts below); code uses JetBrains Mono
- Dark navy `#181715` surfaces carry product chrome (code editors, model cards, footer) — in dark mode this becomes the page floor

**Theme system — `data-theme` attribute:**
- Light mode (default): omit `data-theme` or set `data-theme="light"` — warm cream canvas `#faf9f5`
- Dark mode: add `data-theme="dark"` to `<html>` — dark navy canvas `#181715`
- Respect `prefers-color-scheme: dark` on first visit; persist choice in `localStorage`
- All surface and text tokens are overridden via `[data-theme="dark"]` CSS block — see `references/tokens.md`
- Theme toggle button (`data-theme-toggle`) goes in the top nav actions area

**Surface pacing — three modes, never repeat consecutively:**

*Light mode:*
1. Cream canvas `#faf9f5` — hero, feature text, CTA wrapper
2. Cream card `#efe9de` — feature grids (per-card)
3. Dark navy `#181715` — product mockups, footer

*Dark mode (same structure, inverted floors):*
1. Dark navy `#181715` — hero, feature text, CTA wrapper
2. Dark elevated `#252320` — feature grids (per-card)
3. Cream section `#faf9f5` — doc cards, content detail (used sparingly)

**Band edges are hard cuts** — never use gradient divider elements between bands. Each section carries its own `background` + `padding: var(--space-section) 0` (96px). The hard edge IS the pacing rhythm.

**Motion is warm and editorial:**
- `ease-out: cubic-bezier(0.16, 1, 0.3, 1)` — all reveals
- Translate up 20px + fade, never bounce or spring
- Stagger: 70ms per item in grids
- Dark cards use 28px distance + 500ms duration (heavier feel)

---

## Design Tokens (quick reference)

Full `:root` block, dark-theme overrides, and theme-switcher JS live in `references/tokens.md` — copy from there, do not retype. Most-used tokens for quick lookup:

| Token | Value | Use |
|---|---|---|
| `--color-primary` | `#cc785c` | Coral CTA, sole accent in both themes |
| `--color-canvas` | `#faf9f5` (light) / `#181715` (dark) | Page floor |
| `--color-ink` | `#141413` (light) / `#faf9f5` (dark) | Headlines, primary text |
| `--color-surface-dark` | `#181715` | Product mockups, footer (both themes) |
| `--font-display` | `"Copernicus", "Tiempos Headline", "Cormorant Garamond", ...` | Display headlines, weight 400 only |
| `--font-body` | Unified system stack (incl. PingFang SC / Microsoft Yahei) | All body text, Latin + Chinese |
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | All reveal/motion transitions |
| `--space-section` | `96px` | Vertical padding between page bands |

**Typography scale** (all display uses `--font-display`, weight 400):

| Class | Size | Line-h | Tracking | Use |
|---|---|---|---|---|
| `display-xl` | 64px | 1.05 | -1.5px | Hero h1 |
| `display-lg` | 48px | 1.10 | -1px | Section h2 |
| `display-md` | 36px | 1.15 | -0.5px | Sub-heads |
| `display-sm` | 28px | 1.20 | -0.3px | CTA heads |
| `title-lg` | 22px/500 | 1.30 | 0 | Plan labels |
| `title-md` | 18px/500 | 1.40 | 0 | Card titles |
| `body-md` | 16px/400 | 1.55 | 0 | Body text |
| `body-sm` | 14px/400 | 1.55 | 0 | Footer |
| `caption-uppercase` | 12px/500 | 1.40 | 1.5px | Tags, badges |

---

## Google Fonts (display font substitute only)

Only the display headline font needs a web-font import. Body text uses the system font stack (`--font-body`) and requires no CDN. Authoritative import snippet lives in `references/tokens.md` (Google Fonts Import section) — copy from there.

---

## Chinese Page Support

Chinese pages (`lang="zh-CN"`) use the **same unified system font stack** as Latin pages — no separate Chinese font or CDN import is required. `--font-body` already includes `"PingFang SC"` and `"Microsoft Yahei"` for correct CJK rendering on macOS/iOS and Windows respectively.

Display headlines (`--font-display`, Cormorant Garamond) have no CJK glyphs, so Chinese headings render in the fallback system font automatically — this is expected and requires no override.

**Chinese typography adjustments (apply via `:lang(zh-CN)`):**

| Rule | Latin default | Chinese override | Why |
|---|---|---|---|
| Body line-height | 1.55 | **1.8** | CJK glyphs need more vertical air than Latin sans-serif |
| Body font-size | 16px | **17px** (desktop) | CJK strokes are denser at small sizes; 1px extra aids legibility |
| `caption-uppercase` letter-spacing | 1.5px | `0.08em` + no uppercase | Chinese has no case; micro tracking improves label texture |
| Word-break | default | `word-break: break-all` | Prevents CJK overflow |

Full CSS + mobile overrides → `references/tokens.md` (Chinese Typography Classes section).

---

## KM Format (opt-in — only when explicitly requested)

**Trigger condition:** apply this section ONLY when the user's request explicitly mentions "km文章" (or equivalent: "km排版", "发km", "km格式", "km主题"). Do NOT apply the width constraint by default — the standard container width remains 1200px (see `references/layout.md`).

**KM Format is Claude theme with exactly one difference: a narrower content column.** Every other design decision — colors, typography, spacing scale, radius, motion, band pacing, dark mode, components — stays byte-for-byte identical to the standard Claude theme. Do not introduce a separate "KM style"; simply swap the container width.

| KM variant | Trigger phrase | Max content width |
|---|---|---|
| Standard | "km文章" / "km排版" / "发km" (default when width not specified) | **768px** |
| Wide-screen | "km文章宽屏" / "km宽屏主题" / "wide" explicitly mentioned | **1024px** |

**The width limit applies to the full content column — not just text.** Every element inside the article body must fit within the constrained width, including tables, charts, images, flowcharts, code blocks, and embedded diagrams. Nothing may overflow or bleed wider than the container.

Full `.km-article-container` CSS (replaces `.section-container`, covers img/svg/video/table/pre/chart overflow handling) → `references/layout.md` (KM Article Container section).

---

## Do's and Don'ts

| ✅ Do | ❌ Don't |
|---|---|
| Cream canvas `#faf9f5` as light mode floor | Pure white or cool gray canvas in light mode |
| Dark navy `#181715` as dark mode floor | Jet black `#000000` as dark mode floor |
| Coral `#cc785c` for CTAs in **both themes** | Introduce a second accent color for dark mode |
| `data-theme="dark"` on `<html>` for dark mode | Separate CSS file or class toggle for theming |
| Respect `prefers-color-scheme` + persist to `localStorage` | Ignoring OS preference on first visit |
| Copernicus/Cormorant Garamond, weight 400 | Bold serif display text |
| Negative letter-spacing on all display sizes | Omit letter-spacing on display |
| Alternate cream → dark → cream bands | Repeat the same surface mode consecutively |
| Hard-cut band edges with padding | Gradient divider `<div>` elements between bands |
| `ease-out` translate-up reveals | Bounce, spring, or scale-down reveals |
| 70ms stagger per card in grids | 200ms+ stagger or no stagger |
| Dark cards: 28px / 500ms (heavier) | Same duration for cream and dark cards |
| `translateY` hover on dark cards (max -4px) | `scale()` hover on dark cards |

---

*For full component markup + CSS → read `references/components.md`*
*For motion patterns + JS → read `references/motion.md`*
*For band pacing + breakpoints → read `references/layout.md`*
*For the full page skeleton → copy `assets/scaffold-en.html` or `assets/scaffold-zh.html`*
*For dark theme token overrides + theme switcher → read `references/tokens.md`*
