---
name: anthropic-report
description: Generate beautifully typeset technical reports with Anthropic-style diagrams, using configurable font schemes (Anthropic Sans, TencentSans, or open-source Inter). Integrates with the anthropic-diagram skill for inline architecture visuals. Outputs HTML + PDF.
version: 2.0.0
supports:
  - macos
  - linux
---

# Anthropic-Style Technical Report Generator

Generate beautifully typeset, magazine-quality technical reports that combine Anthropic-style architecture diagrams with rich prose content. Output as HTML (with live fonts) and optionally PDF.

> **⚠️ Font Licensing Notice — MANDATORY user-facing warning:**
>
> This skill uses **Anthropic Sans** (Styrene A, by Commercial Type) and optionally **TencentSans** (by Monotype for Tencent). Both are **proprietary commercial fonts**.
>
> **The agent MUST do ALL of the following:**
>
> 1. **Before generating the FIRST report in a session**, proactively warn the user in the chat message:
>    > ⚠️ 字体版权提醒：本次生成使用了 Anthropic Sans（Styrene A，Commercial Type 出品）字体，属于付费商业字体。当前输出仅适用于个人学习和内部交流。如需用于商业用途（广告、产品、对外发布等），请购买字体授权或切换到开源方案 C（Inter 字体）。
>
> 2. **In every generated HTML file**, include this comment before `</body>`:
>    ```html
>    <!-- ⚠️ Font License: Anthropic Sans (Styrene A) is a commercial font by Commercial Type. TencentSans is a proprietary font by Monotype/Tencent. This file is for non-commercial use only. For commercial use, purchase a license or switch to Inter (SIL Open Font License). -->
>    ```
>
> 3. **If the user mentions commercial use, distribution, or publishing externally**, the agent MUST immediately recommend switching to Scheme C (Inter) and explain why.
>
> **DO NOT skip the chat warning. DO NOT wait for the user to ask about licensing. Be proactive.**

**Integrates with**: `anthropic-diagram` skill — all inline diagrams follow the same design system. If the user asks to visualize code or draw architecture diagrams within a report, apply the `anthropic-diagram` skill's code-reading mode and diagram type rules.

## When to Use

Trigger this skill when the user asks to:
- Create a technical report or document with architecture diagrams
- Generate a "图文排版" (illustrated article) with diagrams
- Produce a professional document combining text analysis and visual diagrams
- Make an Anthropic-style report, article, or presentation-like page
- Convert research notes or discussion summaries into a polished document
- Any request mentioning "anthropic-report", "图文报告", "排版", or "带图的文档"

## Design System

### Fonts — User Preference (Ask First!)

Before generating the first report in a session, **ask the user which font scheme they prefer**:

| Scheme | Headings / Titles | Body / Prose | Diagrams (SVG) | Best For |
|--------|-------------------|--------------|----------------|----------|
| **A: Pure Anthropic** | Anthropic Sans | Anthropic Sans | Anthropic Sans | Anthropic brand feel, online |
| **B: Anthropic + Tencent** | Anthropic Sans | TencentSans | Anthropic Sans | Tencent internal, premium CJK |
| **C: Open Source Safe** | Inter (700) | Inter (400) | Inter | Free commercial use, max compat |

If the user has no preference or doesn't respond, use **Scheme A**.

#### ⚠️ Font Licensing & Distribution Rules

**CRITICAL — Read before generating any output:**

| Font | License | Can Bundle in ZIP? | Can Link CDN? | Can Reference Local? |
|------|---------|--------------------|---------------|---------------------|
| **Anthropic Sans** (Styrene A, by Commercial Type) | Paid commercial | ❌ NO | ⚠️ Anthropic CDN only, personal/internal use | ✅ Yes |
| **TencentSans** (by Monotype for Tencent) | Proprietary brand font | ❌ NO | ❌ NO | ✅ Yes (if installed) |
| **Inter** (by Rasmus Andersson) | SIL Open Font License | ✅ Yes | ✅ Yes | ✅ Yes |

**Rules:**
1. **NEVER bundle Anthropic Sans or TencentSans font files** in any output, ZIP, or distributable package
2. **NEVER link TencentSans to any CDN** — only reference as local system font
3. Anthropic Sans CDN links (from anthropic.com) are acceptable for personal/internal use only
4. For commercial distribution, use **Scheme C** (Inter) exclusively
5. All schemes must include robust fallback stacks so the output degrades gracefully

#### Scheme A: Pure Anthropic

```css
@font-face {
  font-family: 'Anthropic Sans';
  src: url('https://cdn.prod.website-files.com/67ce28cfec624e2b733f8a52/69971a00a3295036497e1a28_AnthropicSans-Roman-Web.woff2') format('woff2');
  font-weight: 100 900;
  font-style: normal;
}
@font-face {
  font-family: 'Anthropic Sans';
  src: url('https://cdn.prod.website-files.com/67ce28cfec624e2b733f8a52/69971a016067bf14b9b8f48d_AnthropicSans-Italic-Web.woff2') format('woff2');
  font-weight: 100 900;
  font-style: italic;
}
```
- **All text**: `'Anthropic Sans', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Noto Sans SC', sans-serif`

#### Scheme B: Anthropic + TencentSans

```css
/* Anthropic Sans — from CDN */
@font-face {
  font-family: 'Anthropic Sans';
  src: url('https://cdn.prod.website-files.com/67ce28cfec624e2b733f8a52/69971a00a3295036497e1a28_AnthropicSans-Roman-Web.woff2') format('woff2');
  font-weight: 100 900;
  font-style: normal;
}
@font-face {
  font-family: 'Anthropic Sans';
  src: url('https://cdn.prod.website-files.com/67ce28cfec624e2b733f8a52/69971a016067bf14b9b8f48d_AnthropicSans-Italic-Web.woff2') format('woff2');
  font-weight: 100 900;
  font-style: italic;
}
/* TencentSans — local system font only, NO CDN, NO bundling */
```
- **Headings, section numbers, meta, footer**: `'Anthropic Sans', 'TencentSans', sans-serif`
- **Body text, prose, lists**: `'TencentSans', 'Anthropic Sans', -apple-system, 'PingFang SC', 'Noto Sans SC', sans-serif`
- **SVG diagram text**: `'Anthropic Sans', 'TencentSans', 'PingFang SC', sans-serif`

Note: Users without TencentSans installed will seamlessly fallback to the next font in the stack.

#### Scheme C: Open Source (Inter)

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
```
- **All text**: `'Inter', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Noto Sans SC', sans-serif`
- Safe for commercial distribution and any use scenario.

#### Offline / Self-Contained Mode
If the user needs fully offline output:
- Ask the user to provide their font files (woff2/ttf). Read and base64-encode them at generation time.
- For Scheme C (Inter), you may freely download and embed the font.
- **Never auto-download or auto-embed proprietary fonts without user's explicit instruction.**

### Page Layout

```css
:root {
  --bg: #faf9f7;           /* Page background */
  --text: #1a1a1a;         /* Primary text */
  --text-secondary: #6b6a66;
  --text-muted: #8c8b87;
  --border: #e0dfdb;
  --accent-blue: #1c5a82;
  --accent-red: #8c3b1a;
  --accent-green: #1a6b50;
  --card-bg: #f0efed;      /* Diagram wrapper background */
}
```

- **Max width**: 1060px, centered
- **Padding**: 80px top, 120px bottom, 40px sides
- **Section spacing**: 72px margin-bottom
- **Divider**: 1px solid `var(--border)`, 64px margin top/bottom

### Page Header

```
.eyebrow     → 12px, weight 500, letter-spacing 4, uppercase, muted
h1           → 42px Anthropic Sans, weight 700, letter-spacing -0.5
.subtitle    → 17px, secondary color, max-width 600px, centered
.meta        → 13px Anthropic Sans, muted, letter-spacing 0.5
```

### Section Structure

Each section follows this pattern:
```
.section-number  → "01" / "02" / "03" — 13px Anthropic Sans, muted, letter-spacing 3
h2               → 26px Anthropic Sans, weight 700
.lead            → 16px, secondary, max-width 720px, line-height 1.9
.diagram-wrapper → card-bg background, 18px radius, 8px padding, subtle shadow
.prose           → 15.5px body text, line-height 2
.callout         → white bg, left-accent border (blue/red/green), 8px radius
.insight-list    → arrow-prefixed list items
```

### Callout Variants

```css
.callout           → border-left: 3px solid var(--accent-blue)   /* Info/insight */
.callout.warn      → border-left: 3px solid var(--accent-red)    /* Warning */
.callout.success   → border-left: 3px solid var(--accent-green)  /* Key takeaway */
```

Structure: `.callout-title` (14px, weight 600) + body text (14.5px, secondary)

### Footer

```
.page-footer → centered, border-top, 13px Anthropic Sans, muted, letter-spacing 0.5
```

## Embedded Diagram Design System

Diagrams are inline SVGs wrapped in `.diagram-wrapper`. Follow the **exact same design rules** as the `anthropic-diagram` skill.

**IMPORTANT**: If the `anthropic-diagram` skill is installed, defer to its full specification for:
- All 5 diagram types (architecture, flowchart, layer, comparison, sequence)
- Code-reading mode (auto-generate diagrams from source code)
- Color palette, node shapes, arrow markers, group containers
- Layout rules and sizing guidelines

If the user asks to "visualize the code" or "draw the architecture" within a report context, apply `anthropic-diagram`'s code-reading pipeline and embed the resulting SVG.

### Canvas
- Background: `#f0efed`, rounded corners `rx="22"`
- Default size: `960×540–640`, scale as needed

### Color Palette (STRICT — only these 5 groups)

| Role | Background | Title | Subtitle | Use For |
|------|-----------|-------|----------|---------|
| **Blue** | `#cce0f0` | `#1c5a82` | `#5a96b8` | Core processing, main pipeline |
| **Red/Warm** | `#f0d5c6` | `#8c3b1a` | `#b86a48` | Special, external, attention |
| **Green/Teal** | `#c8e8da` | `#1a6b50` | `#509878` | Results, output, final stages |
| **White** | `#ffffff` + stroke `#d8d7d3` | `#1a1a1a` | `#999999` | Input, neutral, user-facing |
| **Tag** | `#d4edda` | `#256b3a` | — | Labels, small identifiers |

### Node Shapes
- Standard: `rx="10"`, 120–140px wide, 56–62px tall, centered text
- Small tag: `rx="7"`, ~86px wide, 28–32px tall
- No stroke except White nodes

### Group Containers
- Dashed border: `stroke="#c4c3bf"`, `stroke-width="1.6"`, `stroke-dasharray="8,5"`
- Fill: `none` (transparent)
- `rx="12"`, label top-left (13px, muted)

### Arrows
- Stroke: `#b0afa9`, width `1.4`
- Open chevron marker (not filled):
```xml
<marker id="ah" viewBox="0 0 10 7" refX="9.5" refY="3.5"
  markerWidth="7" markerHeight="5.5" orient="auto">
  <path d="M 0 0.6 L 9.5 3.5 L 0 6.4" fill="none" stroke="#b0afa9" stroke-width="1.3" stroke-linejoin="round"/>
</marker>
```
- Orthogonal (90° turns) routing only. No diagonal lines.
- Use unique marker IDs per diagram (e.g. `ah1`, `ah2`, `ah3`) to avoid conflicts.

### Typography in SVG
- Title: 21px, weight 700, `#1a1a1a`, letter-spacing 4
- Node title: 14–16px, weight 600
- Node subtitle: 11–11.5px, weight 400
- Group label: 13px, weight 400, `#8c8b87`
- Hint/annotation: 12.5px, italic, `#aaa9a5`
- Footer note: 13px, `#8c8b87`, letter-spacing 0.8

**CRITICAL**: Each SVG must include its own `@font-face` declarations in `<defs><style>` for Anthropic Sans.

## Process

1. **Analyze** the user's content: identify key themes, arguments, data points, and what diagrams would best illustrate them
2. **Plan structure**: determine number of sections, diagram types, and narrative flow
3. **Write HTML**: produce a single self-contained HTML file following the design system exactly
4. **Add TOC page**: insert a rendered `<nav class="toc-page">` after `</header>` with all section links
5. **Embed diagrams**: create inline SVG diagrams within `.diagram-wrapper` divs
6. **Add prose**: write clear, insightful text around each diagram — this is a report, not just a diagram gallery
7. **Save as HTML**: write to the user's workspace as `.html`
8. **Preview**: use `preview_url` to show the HTML result
9. **Convert to PDF** (if requested): follow the 3-step pipeline below (SVG rasterization → Chromium PDF → pypdf bookmarks)

## HTML → PDF Conversion

When the user requests PDF output, follow this **3-step pipeline** to ensure clean Table of Contents (TOC) and sidebar bookmarks:

### Step 1: Built-in TOC Page (in HTML)

Always include a rendered TOC page inside the HTML, placed after `</header>`. This gives a visually polished TOC that is fully controlled and not affected by PDF reader auto-extraction bugs.

**Required CSS:**
```css
.toc-page { page-break-after: always; margin-bottom: 72px; }
.toc-title { font-size: 13px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 36px; }
.toc-list { list-style: none; padding: 0; }
.toc-item { display: flex; align-items: baseline; padding: 14px 0; border-bottom: 1px solid #edecea; text-decoration: none; color: var(--text); }
.toc-num { font-size: 13px; font-weight: 700; color: var(--accent-blue); letter-spacing: 1.5px; min-width: 42px; flex-shrink: 0; }
.toc-label { font-size: 16.5px; font-weight: 600; color: var(--text); flex: 1; }
.toc-desc { font-size: 13.5px; color: var(--text-muted); text-align: right; flex-shrink: 0; margin-left: 16px; max-width: 320px; }
```

**Required HTML (after `</header>`):**
```html
<nav class="toc-page">
  <div class="toc-title">Contents</div>
  <ul class="toc-list">
    <li><a class="toc-item" href="#sec-id">
      <span class="toc-num">01</span>
      <span class="toc-label">Section Title</span>
      <span class="toc-desc">Brief description</span>
    </a></li>
    <!-- repeat for each section -->
  </ul>
</nav>
```

Each `<h2>` MUST have a corresponding `id` attribute (e.g., `<h2 id="sec-overview">`).

### Step 2: SVG Diagram Rasterization (CRITICAL for clean PDF TOC)

**Problem**: Chromium's PDF engine extracts `<text>` elements from inline SVGs and pollutes the PDF sidebar outline/TOC with chart data labels (e.g., "2.1 KB", "4.8 KB +167%").

**Attempted fixes that DO NOT work:**
- `aria-hidden="true"` on SVG — Chromium PDF engine ignores it
- `role="img"` on SVG — ignored
- Playwright in-page JS `svg.replaceWith(img)` — PDF engine reads DOM before JS replacement
- Chromium `tagged: true` / `outline: true` — unreliable for CJK headings, sometimes generates partial/broken outlines

**Solution that works**: Rasterize SVGs to PNG **at the HTML source level** before PDF generation.

1. Use Playwright to screenshot each SVG element at 2x device scale:
   ```javascript
   const page = await browser.newPage({ deviceScaleFactor: 2 });
   const svgs = page.locator('.diagram-wrapper svg');
   for (let i = 0; i < await svgs.count(); i++) {
     const buf = await svgs.nth(i).screenshot({ type: 'png' });
     fs.writeFileSync(`diagram-${i+1}.png`, buf);
   }
   ```

2. Replace `<svg>...</svg>` in the HTML source with `<img>` tags:
   ```html
   <img src="diagram-1.png" alt="..." style="width:100%;height:auto;display:block;border-radius:14px;">
   ```

3. This completely removes SVG `<text>` nodes from the DOM, so the PDF engine cannot extract them.

### Step 3: Generate PDF + Inject Bookmarks with pypdf

**Generate the raw PDF** with Chromium — disable its outline generation to avoid duplicates:

```bash
cd /path/to/node/workspace && node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file:///path/to/report.html', { waitUntil: 'networkidle' });
  await page.waitForFunction(() => document.fonts.ready);
  await page.waitForTimeout(3000);
  await page.pdf({
    path: '/path/to/report-raw.pdf',
    format: 'A4',
    printBackground: true,
    tagged: false,   // MUST be false — Chromium's auto-outline is unreliable
    outline: false,  // MUST be false — we inject our own bookmarks with pypdf
    margin: { top: '12mm', bottom: '12mm', left: '8mm', right: '8mm' }
  });
  await browser.close();
})();
"
```

**Inject sidebar bookmarks** with Python `pypdf` (one-time install: `pip install pypdf`):

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("report-raw.pdf")
writer = PdfWriter()
writer.clone_document_from_reader(reader)

# Page index is 0-based
bookmarks = [
    ("Contents",           0),
    ("01 Section Title",   1),
    ("02 Section Title",   2),
    # ... add all sections
    ("References",         N),
]

for title, page_idx in bookmarks:
    writer.add_outline_item(title, page_idx)

with open("report.pdf", "wb") as f:
    writer.write(f)
```

This produces a PDF with:
1. A beautiful rendered TOC page (from HTML)
2. Clean sidebar bookmarks (from pypdf) — no duplicates, no SVG data pollution
3. Clickable navigation in the sidebar for all sections

### PDF Requirements
- Playwright and Chromium must be installed:
  ```bash
  cd /Users/zejianlei/.workbuddy/binaries/node/workspace && \
    npm install playwright && \
    npx playwright install chromium
  ```
- Python `pypdf` must be installed:
  ```bash
  pip install pypdf
  ```
- These are one-time setup. If already installed, skip.

## Quality Checklist

Before outputting, verify:
- [ ] User was asked for font scheme preference (A/B/C)
- [ ] Font `@font-face` declarations match the chosen scheme
- [ ] **NO proprietary font files (Anthropic Sans, TencentSans) are bundled or distributed**
- [ ] TencentSans is ONLY referenced as local system font (no CDN links)
- [ ] Fallback font stacks are present for all font-family declarations
- [ ] Page background is `#faf9f7`, diagram wrappers are `#f0efed`
- [ ] Only the 5 defined color groups used in diagrams
- [ ] All arrows use open chevron markers with unique IDs per diagram
- [ ] Dashed borders on group containers
- [ ] Text properly centered in diagram nodes
- [ ] Sections have number labels ("01", "02", etc.)
- [ ] Callouts use correct accent colors (blue/red/green)
- [ ] SVGs include their own `@font-face` in `<defs><style>` matching the chosen scheme
- [ ] HTML is fully self-contained (no external CSS/JS dependencies)
- [ ] Sufficient spacing, no clipping or overlapping
- [ ] **TOC**: Built-in `<nav class="toc-page">` present after `</header>`, with all sections linked
- [ ] **TOC**: Each `<h2>` has a unique `id` attribute matching the TOC `href`
- [ ] **PDF (if requested)**: SVG diagrams rasterized to PNG at source level (no inline SVG `<text>` in DOM)
- [ ] **PDF (if requested)**: Generated with `tagged: false, outline: false` (Chromium auto-outline disabled)
- [ ] **PDF (if requested)**: Sidebar bookmarks injected via pypdf, one clean set, no duplicates

## Example Section Template

```html
<section class="section">
  <div class="section-number">01</div>
  <h2>Section Title</h2>
  <p class="lead">A brief overview paragraph that sets context for the section.</p>

  <div class="diagram-wrapper">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" width="960" height="540">
      <!-- Full SVG diagram here -->
    </svg>
  </div>

  <div class="prose">
    <p>Analysis and insights about the diagram above.</p>
  </div>

  <div class="callout success">
    <div class="callout-title">Key Takeaway</div>
    The most important insight from this section.
  </div>
</section>
```

## Output Rules

1. **Always output HTML first**, preview with `preview_url`
2. **PDF is opt-in** — only generate when user explicitly asks for PDF
3. **File naming**: use descriptive kebab-case names (e.g., `agent-architecture-report.html`)
4. **Single file**: everything self-contained in one HTML file, no external dependencies
5. **Clean up**: remove any temporary scripts after PDF generation
