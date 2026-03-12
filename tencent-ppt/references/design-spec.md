# Tencent PPT Template - Complete Design Specification

## Slide Dimensions

- **Canvas**: 1920 x 1080 px (16:9 widescreen)
- **Original PPT EMU**: 12,192,000 x 6,858,000 EMU
- **Conversion factor**: 1 EMU = 0.15748 px (at 1920px width)

## Color Palette

### Tencent Blue (Primary Brand Color)

| Name | Hex | Usage |
|------|-----|-------|
| Tencent Blue | `#0052D9` | Primary brand color, section labels, headers |
| Tencent Blue Dark | `#0338D2` | Darkest chart color, accents |
| Tencent Blue Variant | `#0538D0` | Content page center title |
| Tencent Blue BG | `#0052DA` | Ending page solid background |

### Blue Gradient Scale (for charts and graphics)

| Step | Hex | Usage |
|------|-----|-------|
| 1 (darkest) | `#0338D2` | Primary data series |
| 2 | `#265CDA` | Secondary data series |
| 3 | `#5482E2` | Tertiary data series |
| 4 | `#6D94E4` | Quaternary data series |
| 5 | `#A5BFF1` | Light accent |
| 6 (lightest) | `#DFEBFA` | Background accent, light fill |

### Multicolor Palette (alternative theme)

| Name | Hex | Usage |
|------|-----|-------|
| Blue | `#0052D9` | Primary |
| Orange | `#FF7535` | Accent 1 |
| Green | `#9BCF3F` | Accent 2 |
| Cyan | `#3DC0DB` | Accent 3 |

### Neutral Colors

| Name | Hex | Usage |
|------|-----|-------|
| Viewport Dark | `#1a1a2e` | Slide viewport background, body background |
| Black | `#000000` | Body text (dark mode) |
| Dark Gray | `#44546A` | Secondary text |
| Medium Gray | `#797979` | TOC item text, muted text |
| Light Gray | `#D7D7D6` | Borders, subtle backgrounds |
| Lighter Gray | `#E7E6E6` | Background fills |
| Gray C3 | `#C3C3C3` | Decorative elements |
| White | `#FFFFFF` | Text on dark backgrounds, page backgrounds |

### Footer/Page Number Color

- 75% luminance-modulated white: `rgba(255, 255, 255, 0.75)` on dark backgrounds
- 75% luminance gray: `#BFBFBF` on light backgrounds

## Typography

### Font Family Stack

```css
/* Primary - TencentSans (loaded via @font-face) */
@font-face {
  font-family: 'TencentSans';
  src: url('assets/fonts/TencentSans-W3.ttf') format('truetype');
  font-weight: 300;
  font-style: normal;
}

@font-face {
  font-family: 'TencentSans';
  src: url('assets/fonts/TencentSans-W7.ttf') format('truetype');
  font-weight: 700;
  font-style: normal;
}

/* Fallback stack */
--font-primary: 'TencentSans', 'Microsoft YaHei', 'PingFang SC', sans-serif;
--font-body: 'Microsoft YaHei', 'PingFang SC', 'TencentSans', sans-serif;
```

### Type Scale

| Token | Size | Weight | Usage |
|-------|------|--------|-------|
| `--text-thanks` | 120px | 700 | Ending page "Thanks" text |
| `--text-cover-title` | 62px | 700 | Cover slide main title |
| `--text-content-center` | 66px | 700 | Content page large centered title |
| `--text-section-title` | 54px | 700 | Section divider main title |
| `--text-section-number` | 48px | 700 | Section divider number |
| `--text-cover-subtitle` | 44px | 700 | Cover slide subtitle |
| `--text-toc-title` | 26px | 700 | Table of contents section titles |
| `--text-slide-heading` | 42px | 700 | Content slide main heading |
| `--text-card-title` | 30px | 700 | Card title text |
| `--text-body` | 24px | 400 | Default body text |
| `--text-card-desc` | 22px | 400 | Card description text |
| `--text-toc-item` | 20px | 700 | TOC chapter items |
| `--text-section-label` | 20px | 700 | Small section labels on content slides |
| `--text-badge` | 16px | 700 | Badge numbers |
| `--text-footer` | 12px | 300 | Page number, footer text |

### Presentation-Mode Minimum Sizes

When slides are intended for projection or conference presentation, apply these **minimums** to ensure readability at distance. These override the default type scale above when any value falls below the minimum:

| Element Type | Minimum | Applies to |
|-------------|---------|-----------|
| Slide heading | 38px | `--text-slide-heading` |
| Card / box title | 28px | `--text-card-title` |
| Body / description | 22px | `--text-card-desc`, `--text-body` |
| Labels / annotations | 18px | `--text-badge`, `--text-section-label` |
| Section label | 22px | `--text-section-label` |
| Section divider title | 48px | `--text-section-title` |

**Rule**: No visible text on a presentation slide (excluding page numbers) should be smaller than **18px**.

### Text Colors by Context

| Context | Color | Font |
|---------|-------|------|
| Cover title | `#FFFFFF` | TencentSans W7 |
| Cover subtitle | `#FFFFFF` | TencentSans W7 |
| Section divider title | `#0052D9` | TencentSans W7 |
| Section number | `#FFFFFF` | TencentSans W7 |
| Content center title | `#0538D0` | TencentSans W7 |
| Section label (small) | `#0052D9` | TencentSans W7 |
| Slide heading | `#0052D9` | TencentSans W7 |
| TOC section title | `#0052D9` | TencentSans W7 |
| TOC items | `#797979` | TencentSans W7 |
| Sub-labels | `#0052D9` | Microsoft YaHei |
| Body text | `#000000` | Microsoft YaHei |
| Footer / page number | `#BFBFBF` | Microsoft YaHei Light |
| White-on-blue text | `#FFFFFF` | TencentSans W7 |

## Layout Positioning (1920x1080 scale)

All positions below are translated from EMU to pixels at 1920x1080 resolution.

### Cover Slide

| Element | Position (x, y) | Size (w, h) |
|---------|-----------------|-------------|
| Background image | 0, 0 | 1920, 1080 |
| Pattern overlay | 0, 0 | 1920, 1080 |
| Tencent Logo | 117, 162 | 308, 42 |
| Title | 98, 262 | 1692, 158 |
| Subtitle | 98, 447 | 1424, 153 |

### Section Divider

| Element | Position (x, y) | Size (w, h) |
|---------|-----------------|-------------|
| Background | 0, 0 | 1920, 1080 |
| Section icon area | 92, 287 | 173, 151 |
| Section number | 138, 309 | 173, 101 |
| Title | 283, 305 | 838, 266 |
| Page indicator | 17, 1042 | 61, 44 |

### Content Page (with section header)

| Element | Position (x, y) | Size (w, h) |
|---------|-----------------|-------------|
| Badge circle | 59, 54 | 48, 48 |
| Section label | 112, 55 | 237, 49 |
| Main heading | 98, 110 | — | — |
| Content area | 98, 180 | 1724, 830 |
| Footer bar | 0, 1030 | 1920, 50 |
| Page number | 17, 1038 | 56, 41 |

### Table of Contents

| Element | Position (x, y) | Size (w, h) |
|---------|-----------------|-------------|
| Badge circle | 59, 54 | 48, 48 |
| Section label | 112, 55 | 237, 49 |
| TOC items start | 200, 250 | — | — |
| Item spacing | — | 60px vertical gap |

### Ending Page

| Element | Position (x, y) | Size (w, h) |
|---------|-----------------|-------------|
| Background (solid) | full | `#0052DA` |
| Pattern overlay | 0, 0 | 1920, 1080 |
| "Thanks" text | center | centered, y≈316 |
| Tencent Logo | 78, 975 | 231, 31 |

## CSS Custom Properties (Complete Set)

```css
:root {
  /* Dimensions */
  --slide-width: 1920px;
  --slide-height: 1080px;
  --slide-aspect: 16 / 9;

  /* Tencent Brand Colors */
  --tencent-blue: #0052D9;
  --tencent-blue-dark: #0338D2;
  --tencent-blue-title: #0538D0;
  --tencent-blue-bg: #0052DA;

  /* Blue Gradient Scale */
  --blue-1: #0338D2;
  --blue-2: #265CDA;
  --blue-3: #5482E2;
  --blue-4: #6D94E4;
  --blue-5: #A5BFF1;
  --blue-6: #DFEBFA;

  /* Multicolor Accents */
  --accent-orange: #FF7535;
  --accent-green: #9BCF3F;
  --accent-cyan: #3DC0DB;

  /* Neutrals */
  --viewport-dark: #1a1a2e;
  --black: #000000;
  --dark-gray: #44546A;
  --medium-gray: #797979;
  --light-gray: #D7D7D6;
  --lighter-gray: #E7E6E6;
  --gray-c3: #C3C3C3;
  --white: #FFFFFF;
  --footer-gray: #BFBFBF;

  /* Typography */
  --font-primary: 'TencentSans', 'Microsoft YaHei', 'PingFang SC', sans-serif;
  --font-body: 'Microsoft YaHei', 'PingFang SC', 'TencentSans', sans-serif;

  /* Type Scale */
  --text-thanks: 120px;
  --text-cover-title: 62px;
  --text-content-center: 66px;
  --text-section-title: 54px;
  --text-section-number: 48px;
  --text-cover-subtitle: 44px;
  --text-slide-heading: 42px;
  --text-card-title: 30px;
  --text-toc-title: 26px;
  --text-body: 24px;
  --text-card-desc: 22px;
  --text-toc-item: 20px;
  --text-section-label: 20px;
  --text-badge: 16px;
  --text-footer: 12px;

  /* Spacing */
  --page-margin-x: 98px;
  --page-margin-y: 48px;
  --header-height: 160px;
  --footer-height: 50px;
  --content-top: 180px;
  --content-bottom: 1030px;
}
```

## Background Patterns

The template includes several decorative pattern overlays for cover and ending slides. These are PNG images with transparency:

| Pattern | Asset File | Usage |
|---------|-----------|-------|
| Grid | `assets/media/pattern-grid.png` | Cover style A, Ending style A |
| Blocks | `assets/media/pattern-blocks.png` | Cover style B, Ending style B |
| Stripes | `assets/media/pattern-stripes.png` | Cover style C, Ending style C |
| Light effect | `assets/media/pattern-light.png` | Cover style D, Ending style D |
| Ending grid | `assets/media/ending-pattern-grid.png` | Ending page overlay |
| Ending blocks | `assets/media/ending-pattern-blocks.png` | Ending page overlay |

## Tencent Logo Assets

| File | Description |
|------|-------------|
| `assets/media/tencent-logo-white.png` | White logo for dark backgrounds |
| `assets/media/tencent-logo-white-2.png` | White logo variant |
| `assets/media/tencent-logo-blue.png` | Blue logo for light backgrounds |

## Section Divider Decorative Elements

| File | Description |
|------|-------------|
| `assets/media/section-block-bg.png` | Block pattern for section divider background (**recommended default**) |
| `assets/media/section-stripe-bg.png` | Stripe pattern for section divider background (may clip text at certain positions — use with caution) |
| `assets/media/footer-bar.png` | Decorative footer bar for content slides |

## z-index Layering Convention

All content slides must follow a consistent stacking order:

| Layer | z-index | Elements |
|-------|---------|----------|
| Base content | auto (0) | Normal slide content |
| Footer | `1` | `.slide-footer` and its children |
| Near-footer content | `2` | Legends, bottom callout bars, any absolutely-positioned content within 120px of the slide bottom |

This prevents the footer decorative bar from obscuring content elements like chart legends or summary bars.

## Space Utilization Guidelines

The usable content area spans from **top ~180px** (below header) to **bottom ~1030px** (above footer), giving **~850px** of vertical space.

- Maximum gap between the lowest content element and the footer: **120px**
- When content doesn't fill the area, prefer: expanding padding, increasing spacing between sections, adding a bottom callout/summary bar, or increasing font sizes
- For vertically stacked sections, distribute whitespace **evenly** between sections rather than accumulating at the bottom
