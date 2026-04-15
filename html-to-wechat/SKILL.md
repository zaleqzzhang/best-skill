---
name: html-to-wechat
description: Convert a full HTML page into WeChat Official Account (微信公众号) compatible format. Use when the user asks to convert HTML for WeChat, 公众号, or needs WeChat-compatible rich text output.
---

# HTML to WeChat (公众号) Converter

Convert a standard HTML page into a single HTML fragment with all styles inlined, compatible with WeChat Official Account's rich text editor.

## Workflow

1. Read the source HTML file
2. Apply all conversion rules below
3. Output a single `.html` file (no DOCTYPE/head/body) that can be opened in a browser, select-all, copy, and paste into the WeChat editor

## Conversion Rules

### Strip everything WeChat doesn't support

| Strip | Replacement |
|-------|-------------|
| `<style>` blocks | Inline all styles onto each element |
| `<link>` external resources | Remove (no external fonts) |
| `<script>`, JS event handlers | Remove entirely |
| `<svg>` elements | Replace with text or table-based alternatives |
| CSS classes (`class="xxx"`) | Resolve to inline `style=""` |
| CSS variables (`var(--xxx)`) | Replace with actual hex values |
| `::before` / `::after` pseudo-elements | Remove or recreate with real elements |
| `@keyframes` / animations | Remove |
| `@media` queries | Remove |

### Critical: `<section>` not `<div>` for styled containers

WeChat strips styles on `<div>` elements. **Use `<section>` for any element that needs background, border, or visual styling.**

```html
<!-- BAD: WeChat strips background on div -->
<div style="background:#f5f0e8; border-left:4px solid #c45d3e; padding:24px;">

<!-- GOOD: section preserves styles -->
<section style="background:#f5f0e8; background-color:#f5f0e8; border-left:4px solid #c45d3e; padding:24px;">
```

Always double-write background: `background:#xxx; background-color:#xxx;`

### CSS property compatibility

| Works | Doesn't work | Workaround |
|-------|-------------|------------|
| `background-color` (on `<section>`) | `linear-gradient` | Use solid color |
| `border`, `border-radius` | `box-shadow` (unreliable) | Remove or skip |
| `color` (hex only) | `rgba()` colors | Convert to hex |
| `font-size`, `font-weight` | `clamp()` | Use fixed `px` value |
| `padding`, `margin` | `vh`/`vw` units | Use `px` or `rem` |
| `text-align`, `line-height` | `position: absolute/fixed` | Use normal flow |
| `border-collapse` on `<table>` | `display: grid` | Use `<table>` |
| `display: inline-block` | `display: flex` (unreliable) | Use `<table>` |
| `vertical-align` | `background-clip: text` | Use solid color text |
| `letter-spacing` | `text-transform` (unreliable) | Manually transform text |

### Layout: use `<table>` instead of flex/grid

```html
<!-- BAD: flex doesn't work reliably -->
<div style="display:flex; gap:10px;">
  <span>Item 1</span>
  <span>Item 2</span>
</div>

<!-- GOOD: table layout is reliable -->
<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr>
    <td style="padding:10px;">Item 1</td>
    <td style="padding:10px;">Item 2</td>
  </tr>
</table>
```

### Dark background sections

```html
<!-- Use <section> with both background and background-color -->
<section style="background:#1f1a30; background-color:#1f1a30; padding:48px 32px; text-align:center;">
  <h2 style="color:#ffffff;">White text on dark background</h2>
  <!-- Use solid hex colors, never rgba -->
  <p style="color:#a0a0b0;">Muted text</p>
</section>
```

### Colored circle badges (numbered steps)

```html
<section style="width:28px; height:28px; border-radius:50%; background:#c45d3e; background-color:#c45d3e; color:#fff; font-size:13px; font-weight:600; text-align:center; line-height:28px;">1</section>
```

### Highlight / callout boxes

```html
<section style="background:#f5f0e8; background-color:#f5f0e8; border:1px solid #d4cfc4; border-left:4px solid #c45d3e; border-radius:0 6px 6px 0; padding:24px; margin:24px 0;">
  <p style="font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#c45d3e; margin:0 0 8px;">LABEL</p>
  <p style="font-size:16px; color:#1a1a2e; line-height:1.9; margin:0;">Content text here.</p>
</section>
```

### Blockquote-style left border

```html
<section style="font-size:18px; color:#1a1a2e; line-height:2; border-left:3px solid #c45d3e; padding-left:24px; margin:32px 0;">
  Quote text here.
</section>
```

### Font stacks (fallback for missing fonts)

Since external fonts won't load, use system font stacks:

- **Sans-serif**: `'Noto Sans SC', -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif`
- **Serif**: `'Noto Serif SC', Georgia, 'Songti SC', serif`
- **Monospace**: `'JetBrains Mono', Menlo, Monaco, Consolas, monospace`

### HTML entities

Replace HTML entities with actual Unicode characters where possible:
- `&middot;` → `·`
- `&rarr;` → `→`
- `&larr;` → `←`
- `&mdash;` → `—`

### Bullet lists without pseudo-elements

Since `::before` doesn't work, use inline colored dot characters:

```html
<div style="padding-left:20px; margin-bottom:13px; font-size:16px; color:#3d3d5c; line-height:1.75;">
  <span style="color:#c45d3e; margin-right:8px;">●</span>
  <strong style="color:#1a1a2e;">Bold label</strong> — Description text
</div>
```

### Dividers

```html
<hr style="border:none; border-top:1px solid #d4cfc4; margin:36px 0;">
```

## Output format

The output file should be a single `.html` file structured as:

```html
<div style="max-width:760px; margin:0 auto; font-family:'Noto Sans SC',sans-serif; color:#1a1a2e; line-height:1.8; font-size:16px;">

  <!-- All content here, fully inlined styles -->

</div>
```

No `<!DOCTYPE>`, no `<html>`, no `<head>`, no `<body>` tags. Just the content fragment.

## Quick checklist

- [ ] No `<style>` blocks (except optional Google Fonts `@import` at top)
- [ ] No CSS classes — all styles inline
- [ ] No CSS variables — all resolved to hex
- [ ] No `rgba()` — converted to hex
- [ ] No `linear-gradient` — solid colors only
- [ ] No `display:flex/grid` — use `<table>` for layout
- [ ] No SVG — use text alternatives
- [ ] No `position:absolute/fixed`
- [ ] No animations / pseudo-elements
- [ ] Styled containers use `<section>` not `<div>`
- [ ] Background colors double-written: `background:#xxx; background-color:#xxx`
- [ ] Dark sections have hex text colors, never `rgba`
