---
name: tencent-ppt
description: This skill should be used when the user asks to "create a presentation", "make slides", "generate PPT", "build a slide deck", "create Tencent slides", "make a PPT page", or discusses presentation generation, slide design, or deck creation. Generates web-based presentation pages following the official Tencent PPT Template design system with support for multimedia content.
version: 2.1.0
author: shiyicao
---

# Tencent PPT Slide Generator

Generate presentation slides as self-contained HTML pages that faithfully follow the official Tencent PPT Template design system. Each slide is a standalone web page at 16:9 aspect ratio (1920x1080px), using TencentSans brand fonts and the official Tencent color palette.

**Preview method**: Open `index.html` directly in browser via `file://` protocol (no HTTP server needed).

## Workflow

### 1. Gather Requirements

Ask the user about their presentation needs:

- **Topic**: What is the presentation about?
- **Audience**: Internal team, executive review, external client, conference?
- **Slide count**: How many slides are needed?
- **Content outline**: Key points or sections to cover?
- **Media assets**: Any images, videos, or GIFs to include? (Accept local file paths or URLs)
- **Color theme**: Blue monochrome (default) or multicolor?
- **Delivery context**: Screen reading only, or projector/conference presentation? (affects minimum font sizes — see Presentation Readability)

### 2. Present Slide Plan with Layout Options

Before generating, present the user with a structured plan. For each slide, offer layout choices.

**Content density rule**: Each slide should contain **at most one core topic or story**. If a slide has two or more independent themes, split it into separate slides. When in doubt, prefer more slides with focused content over fewer slides that feel cramped.

**Cover Slide Styles:**
| Style | Description |
|-------|-------------|
| `cover-grid` | Grid pattern overlay on dark background |
| `cover-blocks` | Block/square pattern overlay |
| `cover-stripes` | Stripe pattern overlay |
| `cover-light` | Light/gradient effect overlay |
| `cover-blue-solid` | Solid Tencent Blue background |
| `cover-photo` | Blue-tinted photo background |

**Content Slide Layouts:**
| Layout | Description |
|--------|-------------|
| `title-only` | Large centered title, no body content |
| `content-text` | Section header + body text area |
| `content-image-right` | Text left, image right (50/50 split) |
| `content-image-left` | Image left, text right |
| `content-full-image` | Full-bleed image with optional text overlay |
| `content-3-images` | Three images in a row with captions |
| `content-2-column` | Two-column text layout |
| `content-cards` | Card grid layout (2-4 cards) |
| `content-chart` | Chart area with title and description |
| `content-video` | Embedded video with title |
| `content-quote` | Large quote with attribution |
| `content-comparison` | Side-by-side comparison |
| `content-timeline` | Horizontal or vertical timeline |
| `content-stats` | Large numbers/statistics display |

**Structural Slides:**
| Type | Description |
|------|-------------|
| `toc` | Table of contents with numbered sections |
| `section-divider` | Section break with number and title |
| `ending-thanks` | "Thanks" ending page |

### 3. Generate HTML Slides

For each slide, generate a self-contained HTML file following these rules:

- **Viewport**: Fixed 1920x1080px canvas inside a `.slide-viewport` wrapper, auto-scaled to fill browser via JS `transform: scale()`
- **CRITICAL — scaling rule**: The `.slide` div must ALWAYS remain exactly `width: 1920px; height: 1080px`. NEVER resize it to match the viewport or screen size. NEVER use an `isFullscreen()` check that sets `transform: none` or changes width/height — this breaks all absolute-positioned layouts on non-16:9 screens (e.g., MacBook 16:10). The ONLY correct approach is `transform: scale(Math.min(vw/1920, vh/1080))` at ALL times, including fullscreen. NEVER use flexbox centering on `.slide-viewport` — `transform: scale()` does not change layout size, so a 1920px element in a smaller flex container will overflow and get clipped. Instead, use `position: absolute` on `.slide` with `transform-origin: 0 0`, and compute `left/top` in JS to center: `left = (vw - 1920*scale)/2`, `top = (vh - 1080*scale)/2`.
- **Fonts**: Load TencentSans-W3 (light) and TencentSans-W7 (bold) via `@font-face` from the `assets/fonts/` directory
- **Colors**: Use the Tencent brand palette (see design spec in `references/`)
- **CSS**: All styles must be **inline** (embedded in `<style>` within each HTML file). Do NOT use external CSS files — this ensures each slide is truly self-contained and works when opened via `file://`.
- **Media**: Support `<img>`, `<video>`, and animated GIF via standard HTML tags. See **Media Handling** section below for path rules.
- **Self-contained**: Each HTML file works standalone when double-clicked / opened directly in a browser via `file://`

#### z-index Layering

All content slides must follow a consistent stacking order to prevent elements from being obscured by the footer:

| Layer | z-index | Elements |
|-------|---------|----------|
| Footer bar | `1` | `.slide-footer` |
| Overlapping content | `2` | Legends, bottom callout bars, any content positioned near the footer area (bottom < 120px) |

Always set `.slide-footer { z-index: 1; }` in every content slide. Any content element whose bottom edge is within 120px of the slide bottom must have `z-index: 2`.

#### Space Utilization

Content should fill the available area between the header (top ~180px) and the footer (bottom ~50px). Avoid large empty gaps:

- The gap between the lowest content element and the footer should not exceed **120px**.
- When content naturally doesn't fill the page, use these strategies: increase element padding/margins, add a bottom summary bar or callout, increase font sizes, or expand card/box heights.
- For multi-section layouts (e.g., paradigm boxes + data cards + quote bar), distribute spacing **evenly** between sections rather than leaving all whitespace at the bottom.

#### Section Divider Backgrounds

Use `section-block-bg.png` as the **default** background for section divider pages. The `section-stripe-bg.png` can cause text display issues at certain positions — only use it if explicitly requested and tested.

#### Custom Diagrams & Complex Layouts

When building custom visual layouts (cycle diagrams, flow charts, matrix grids) with absolute positioning:

- **Keep text concise**: Each node/label should be **4–6 characters** max. Long descriptions cause overlapping in constrained spaces.
- **Calculate collision zones**: Before positioning, verify that elements don't overlap by checking their bounding boxes (position + width/height + padding).
- **Prefer SVG for connectors**: Use SVG `<path>` elements for arrows and connecting lines rather than Unicode arrows or text characters — they scale cleanly and position precisely.

Consult **`references/design-spec.md`** for the complete color palette, typography scale, and spacing system.

Consult **`references/layout-patterns.md`** for HTML/CSS implementation patterns for each slide layout type.

Use **`assets/fonts/`** for TencentSans TTF font files.

Use **`assets/media/`** for Tencent logos and decorative pattern images extracted from the official template.

### 4. Output Structure

Generate slides into a project directory:

```
slides-output/
├── index.html              # Slideshow viewer (keyboard nav, fullscreen, gallery)
├── slide-01-cover.html
├── slide-02-toc.html
├── slide-03-section.html
├── slide-04-content.html
├── ...
├── slide-XX-ending.html
└── assets/
    ├── fonts/              # Copy of TencentSans fonts from skill assets
    └── media/              # Tencent logos and patterns from template
```

**Important — asset setup**: When creating a new slide project, **copy** (not symlink) the font files and media assets from the skill's `assets/` directory into `slides-output/assets/`. This ensures slides work independently of the skill installation path.

**No `styles/` directory**: All CSS is inlined in each HTML file. Do not create a separate `base.css`.

**No `assets/user-media/` directory**: User-provided media files are referenced via absolute path or URL directly (see Media Handling).

#### Slide Add/Remove Checklist

When adding, removing, or reordering slides, **all of the following must be updated in sync**:

1. **`index.html` slides array** — add/remove/reorder the file references
2. **`index.html` total count** — update the page indicator (e.g., "1 / 15" → "1 / 17")
3. **Page numbers** — update the `<span class="page-number">` in each affected slide's footer
4. **Section divider numbers** — update section numbers if sections were reordered
5. **Ending page filename** — ensure `index.html` references the correct ending file (e.g., after inserting slides, `slide-15-ending.html` might need to become `slide-17-ending.html`)

Failure to sync these causes silent failures (blank slides, wrong page numbers, missing ending page).

### 5. The `index.html` Slideshow Viewer

The `index.html` is a **slideshow viewer** (not a gallery grid). It:
- Loads all slides as iframes and shows one at a time, scaled to fill the viewport
- Supports **keyboard navigation** (when parent page has focus): ←/→ arrows, Space (next), Home/End
- Shows a **slide counter** (e.g., "3 / 15") in a bottom control bar
- Has **previous/next buttons** and a **fullscreen toggle** (F key)
- Has a **gallery mode** (G key) showing all slides as thumbnails — click to jump
- Has a **PDF export button** (P key or 📄 button) — see PDF Export section
- Controls auto-hide and appear on mouse hover
- **Fullscreen notification**: On `fullscreenchange` and `webkitfullscreenchange`, the viewer must call `iframe.contentWindow.postMessage('fitSlide', '*')` with delays (100ms, 300ms, 600ms) to notify the embedded slide to recalculate its scale. Also send this message in the iframe's `onload` callback with delays (50ms, 200ms, 500ms). This is critical for MacBook single-screen scenarios where Chrome fullscreen does not reliably trigger `resize` inside iframes.

**`file://` protocol limitation**: Under `file://`, browsers treat each file as a separate origin, so `iframe.contentDocument` access is blocked (cross-origin). This means:
- **Click-to-navigate inside slides does NOT work** (the injected script cannot be inserted into iframe)
- **Keyboard events when iframe has focus are NOT forwarded** to the parent
- **Workaround**: Users navigate via the bottom control bar buttons or by clicking outside the iframe first to give focus back to the parent page, then using keyboard shortcuts. This is an acceptable trade-off for the simplicity of not needing an HTTP server.
- **Workaround for fullscreen scaling**: Each slide listens for `postMessage('fitSlide')` from the parent and re-runs `fitSlide()`. A 500ms polling interval also catches any missed resize events as a safety net.

Each individual slide HTML file also works standalone when opened directly in a browser — it scales itself to fill the viewport using the `.slide-viewport` wrapper pattern.

### 6. Preview

After generating, open `index.html` directly in the browser:

```bash
# macOS
open slides-output/index.html

# Or just double-click index.html in Finder
```

No HTTP server is needed. The `file://` protocol supports all features including absolute-path media references, font loading, and the slideshow viewer (with the minor limitation noted above).

## Key Design Principles

- **Brand fidelity**: Match the official Tencent PPT Template exactly in colors, fonts, and proportions
- **Pixel-perfect**: Translate EMU-based PPT dimensions to CSS pixels at 1920x1080 scale
- **Media flexibility**: Accept images (PNG/JPG/SVG/WebP), animated GIFs, and videos (MP4/WebM) from local paths or URLs
- **Self-contained**: Each slide HTML file should work when opened directly via `file://`, with all styles inlined and minimal external dependencies (only font files and media assets in the `assets/` directory)
- **Progressive enhancement**: Base slides work without JavaScript; animations and interactivity are optional enhancements

## Presentation Readability

Slides often look fine on a desktop screen but become illegible when projected. Apply these minimum font sizes based on the delivery context:

### Font Size Minimums (Presentation / Projection Mode)

When the user indicates slides will be projected or presented to a group, enforce these minimums:

| Element Type | Minimum Size | Examples |
|-------------|-------------|---------|
| Slide heading | 38px | `.content-heading` |
| Card/box title | 28px | `.card-title`, `.mkt-logo` |
| Body / description | 22px | `.card-desc`, `.loop-text`, `.paradigm-desc` |
| Labels / annotations | 18px | `.stat-label`, `.timeline-date`, `.badge span` |
| Section label | 22px | `.section-label` |
| Section divider title | 48px | `.section-title` |
| Section divider desc | 28px | `.section-desc` |

### Font Size Minimums (Screen Reading Mode)

For slides intended only for on-screen reading or sharing as PDF, the default type scale in `design-spec.md` is sufficient.

### Audit Process

When asked to increase readability or enlarge fonts:
1. Read every slide file and catalog all `font-size` declarations
2. Compare each against the minimums table above
3. Apply increases proportionally — small text gets larger relative increases, already-large text gets smaller relative increases
4. Verify no text overflow or layout breaks after changes

## PDF Export

PDF export is built into the `index.html` slideshow viewer as a **pure-frontend feature** — no Node.js, Playwright, or local tooling required. Users click the 📄 button in the control bar (or press **P**) to export.

### How It Works

1. The viewer dynamically loads [html2canvas](https://html2canvas.hertzen.com/) and [jsPDF](https://github.com/parallax/jsPDF) from CDN on first use
2. For each slide, a hidden 1920×1080 iframe is created (or reused), `html2canvas` captures the `.slide` element at 2x resolution
3. Each canvas is added as a page to a jsPDF document (landscape A4 proportional to 1920×1080)
4. The assembled PDF is downloaded to the user's browser

### Requirements

- **Must run via HTTP** (e.g., `python3 -m http.server`). Under `file://`, cross-origin iframe restrictions prevent `html2canvas` from reading slide content. If `file://` is detected, the export button will fall back to `window.print()`.
- Internet access is needed on first export to load the CDN libraries (they are cached by the browser afterward).

### User Interaction

- A progress overlay shows "Exporting slide 3 / 17…" during capture
- Export typically takes 1–3 seconds per slide
- The PDF filename defaults to the `<title>` of index.html

### Implementation

The complete export logic is included in the `index.html` viewer template in `references/layout-patterns.md`. Key functions:

- `exportPDF()` — main entry point, orchestrates the capture loop
- `loadLibsIfNeeded()` — lazy-loads html2canvas + jsPDF from CDN
- `captureSlide(iframe)` — captures one iframe's `.slide` element via html2canvas. **Critical**: must temporarily reset `slideEl.style.transform/left/top` to `none/0px/0px` before capture and restore after, because `fitSlide()` applies `transform: scale()` which causes html2canvas to capture the scaled-down size instead of the full 1920×1080

## Media Handling

When the user provides media file paths or URLs:

1. **Local files**: Use the **absolute path** directly in `src` attributes (e.g., `src="/Users/username/Pictures/photo.jpg"`). Do NOT copy files into the project — this avoids duplicating large media (especially videos) and keeps the original file as the single source of truth. Absolute paths work correctly under `file://` protocol.
2. **URLs**: Use directly in `src` attributes. Note that remote URLs require internet access at viewing time.
3. **Supported formats**: PNG, JPG, SVG, WebP, GIF (animated), MP4, WebM
4. **Video embedding**: Use `<video>` tag with controls, autoplay, muted, loop attributes as appropriate
5. **Image sizing**: Preserve aspect ratio, fit within the designated layout area using `object-fit: cover` or `object-fit: contain`

**Trade-off note**: Using absolute paths means the slides are tied to the local machine's file system. If the slides need to be shared with others or archived as a portable package, copy the media files into the project directory and use relative paths instead.

## Additional Resources

### Reference Files

- **`references/design-spec.md`** — Complete Tencent PPT design specification: colors, fonts, dimensions, spacing
- **`references/layout-patterns.md`** — HTML/CSS patterns for every slide layout type, including the `index.html` viewer with built-in PDF export

### Asset Files

- **`assets/fonts/TencentSans-W3.ttf`** — TencentSans Light (body text)
- **`assets/fonts/TencentSans-W7.ttf`** — TencentSans Bold (headings, titles)
- **`assets/media/`** — Tencent logos and decorative pattern images from the official template
