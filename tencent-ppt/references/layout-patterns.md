# Layout Patterns - HTML/CSS Implementation

This reference provides complete HTML/CSS patterns for every slide layout type in the Tencent PPT Template system.

## Base HTML Structure

Every slide file follows this base structure.

**CRITICAL: The `.slide` div must ALWAYS remain exactly 1920x1080px. NEVER resize it to match the viewport. NEVER set `transform: none` or change width/height based on fullscreen detection. Always use `transform: scale()` to fit any screen size. This is the only approach that preserves all absolute-positioned content layouts correctly across all screens (MacBook 16:10, external 16:9, etc.).**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide Title</title>
  <style>
    @font-face {
      font-family: 'TencentSans';
      src: url('assets/fonts/TencentSans-W3.ttf') format('truetype');
      font-weight: 300;
    }
    @font-face {
      font-family: 'TencentSans';
      src: url('assets/fonts/TencentSans-W7.ttf') format('truetype');
      font-weight: 700;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    html, body {
      width: 100%; height: 100%;
      overflow: hidden;
      background: #1a1a2e;
      margin: 0;
    }

    .slide-viewport {
      width: 100vw; height: 100vh;
      position: relative;
      background: #1a1a2e; overflow: hidden;
    }

    .slide {
      width: 1920px;
      height: 1080px;
      position: absolute;
      overflow: hidden;
      background: #FFFFFF;
      font-family: 'TencentSans', 'Microsoft YaHei', 'PingFang SC', sans-serif;
      transform-origin: 0 0;
    }
  </style>
  <script>
    /**
     * fitSlide: scale the fixed 1920x1080 slide to fill the viewport.
     *
     * IMPORTANT — NEVER change .slide width/height from 1920x1080.
     * NEVER set transform to 'none' or resize the slide div for fullscreen.
     * Always use transform: scale() so all absolute positions remain correct.
     * This works on ALL screens: MacBook (16:10), external monitors (16:9), etc.
     */
    function fitSlide() {
      var s = document.querySelector('.slide');
      if (!s) return;
      var vw = window.innerWidth || document.documentElement.clientWidth;
      var vh = window.innerHeight || document.documentElement.clientHeight;
      var scale = Math.min(vw / 1920, vh / 1080);
      var sw = 1920 * scale, sh = 1080 * scale;
      s.style.left = ((vw - sw) / 2) + 'px';
      s.style.top = ((vh - sh) / 2) + 'px';
      s.style.transform = 'scale(' + scale + ')';
    }
    window.addEventListener('resize', fitSlide);
    window.addEventListener('DOMContentLoaded', fitSlide);
    document.addEventListener('fullscreenchange', function() { setTimeout(fitSlide, 100); setTimeout(fitSlide, 300); });
    document.addEventListener('webkitfullscreenchange', function() { setTimeout(fitSlide, 100); setTimeout(fitSlide, 300); });
    window.addEventListener('message', function(e) { if (e.data === 'fitSlide') { setTimeout(fitSlide, 50); setTimeout(fitSlide, 200); } });
    /* Periodic self-check: catch any edge cases where resize events are missed */
    (function() {
      var lastW = 0, lastH = 0;
      setInterval(function() {
        var w = window.innerWidth || document.documentElement.clientWidth;
        var h = window.innerHeight || document.documentElement.clientHeight;
        if (w !== lastW || h !== lastH) { lastW = w; lastH = h; fitSlide(); }
      }, 300);
    })();
  </script>
</head>
<body>
  <div class="slide-viewport">
    <div class="slide">
      <!-- Slide content here -->
    </div>
  </div>
</body>
</html>
```

## Cover Slide Patterns

### Cover - Grid Pattern (`cover-grid`)

```html
<div class="slide cover">
  <!-- Pattern overlay -->
  <div class="cover-pattern">
    <img src="assets/media/pattern-grid.png" alt="" class="pattern-img">
  </div>
  <!-- Content -->
  <div class="cover-content">
    <img src="assets/media/tencent-logo-white.png" alt="Tencent" class="cover-logo">
    <h1 class="cover-title">Presentation Title</h1>
    <p class="cover-subtitle">Subtitle or date or department</p>
  </div>
</div>
```

```css
.cover { background: linear-gradient(135deg, #0a0a2e 0%, #0d1b3e 30%, #0052D9 100%); }
.cover-pattern { position: absolute; inset: 0; }
.pattern-img { width: 100%; height: 100%; object-fit: cover; mix-blend-mode: screen; opacity: 0.4; }
.cover-content { position: absolute; left: 98px; top: 162px; z-index: 2; }
.cover-logo { height: 42px; width: auto; margin-bottom: 58px; }
.cover-title {
  font-size: 62px; font-weight: 700; color: #FFFFFF;
  line-height: 1.2; max-width: 1692px; margin-bottom: 20px;
}
.cover-subtitle {
  font-size: 44px; font-weight: 700; color: #FFFFFF;
  max-width: 1424px; opacity: 0.9;
}
```

### Cover - Solid Blue (`cover-blue-solid`)

```html
<div class="slide cover-blue">
  <div class="cover-content">
    <img src="assets/media/tencent-logo-white.png" alt="Tencent" class="cover-logo">
    <h1 class="cover-title">Presentation Title</h1>
    <p class="cover-subtitle">Subtitle text here</p>
  </div>
</div>
```

```css
.cover-blue { background: #0052D9; }
.cover-blue .cover-title, .cover-blue .cover-subtitle { color: #FFFFFF; }
```

### Cover - Photo Background (`cover-photo`)

For user-provided background images:

```html
<div class="slide cover-photo">
  <img src="/path/to/user/background.jpg" alt="" class="cover-bg-img">
  <div class="cover-overlay"></div>
  <div class="cover-content">
    <img src="assets/media/tencent-logo-white.png" alt="Tencent" class="cover-logo">
    <h1 class="cover-title">Title Here</h1>
    <p class="cover-subtitle">Subtitle Here</p>
  </div>
</div>
```

```css
.cover-photo { position: relative; }
.cover-photo .cover-bg-img {
  position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;
}
.cover-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(0,82,217,0.85) 0%, rgba(3,56,210,0.7) 100%);
}
```

### Cover - Stripes Pattern (`cover-stripes`)

Same structure as `cover-grid`, but uses `pattern-stripes.png`:

```html
<div class="slide cover">
  <div class="cover-pattern">
    <img src="assets/media/pattern-stripes.png" alt="" class="pattern-img">
  </div>
  <div class="cover-content">
    <img src="assets/media/tencent-logo-white.png" alt="Tencent" class="cover-logo">
    <h1 class="cover-title">Presentation Title</h1>
    <p class="cover-subtitle">Subtitle text here</p>
  </div>
</div>
```

```css
/* Same CSS as cover-grid; only the pattern image file differs */
.cover { background: linear-gradient(135deg, #0a0a2e 0%, #0d1b3e 30%, #0052D9 100%); }
```

### Cover - Blocks Pattern (`cover-blocks`)

Same structure as `cover-grid`, but uses `pattern-blocks.png`:

```html
<div class="slide cover">
  <div class="cover-pattern">
    <img src="assets/media/pattern-blocks.png" alt="" class="pattern-img">
  </div>
  <div class="cover-content">
    <img src="assets/media/tencent-logo-white.png" alt="Tencent" class="cover-logo">
    <h1 class="cover-title">Presentation Title</h1>
    <p class="cover-subtitle">Subtitle text here</p>
  </div>
</div>
```

### Cover - Light Effect (`cover-light`)

Uses `pattern-light.png` for a softer, luminous look:

```html
<div class="slide cover cover-light">
  <div class="cover-pattern">
    <img src="assets/media/pattern-light.png" alt="" class="pattern-img">
  </div>
  <div class="cover-content">
    <img src="assets/media/tencent-logo-white.png" alt="Tencent" class="cover-logo">
    <h1 class="cover-title">Presentation Title</h1>
    <p class="cover-subtitle">Subtitle text here</p>
  </div>
</div>
```

```css
.cover-light { background: linear-gradient(135deg, #0a0f2c 0%, #0052D9 60%, #5482E2 100%); }
.cover-light .pattern-img { opacity: 0.5; mix-blend-mode: screen; }
```

## Table of Contents Pattern

```html
<div class="slide toc-slide">
  <!-- Header -->
  <div class="slide-header">
    <div class="badge"><span>1</span></div>
    <span class="section-label">目录</span>
  </div>

  <!-- TOC items -->
  <div class="toc-list">
    <div class="toc-item">
      <div class="toc-number">01</div>
      <div class="toc-text">
        <h3 class="toc-title">Section Title</h3>
        <p class="toc-desc">Brief description of this section</p>
      </div>
    </div>
    <div class="toc-item">
      <div class="toc-number">02</div>
      <div class="toc-text">
        <h3 class="toc-title">Section Title</h3>
        <p class="toc-desc">Brief description of this section</p>
      </div>
    </div>
    <!-- More items... -->
  </div>

  <!-- Footer -->
  <div class="slide-footer">
    <img src="assets/media/footer-bar.png" alt="" class="footer-bar">
    <span class="page-number">02</span>
  </div>
</div>
```

```css
.slide-header {
  position: absolute; left: 59px; top: 48px;
  display: flex; align-items: center; gap: 12px;
}
.badge {
  width: 48px; height: 48px; border-radius: 50%;
  background: #0052D9; display: flex; align-items: center; justify-content: center;
}
.badge span { color: #FFFFFF; font-size: 16px; font-weight: 700; }
.section-label { font-size: 20px; font-weight: 700; color: #0052D9; }

.toc-list {
  position: absolute; left: 200px; top: 250px;
  display: flex; flex-direction: column; gap: 60px;
}
.toc-item { display: flex; align-items: flex-start; gap: 30px; }
.toc-number { font-size: 48px; font-weight: 700; color: #0052D9; line-height: 1; }
.toc-title { font-size: 26px; font-weight: 700; color: #0052D9; margin-bottom: 8px; }
.toc-desc { font-size: 22px; color: #797979; }

.slide-footer { position: absolute; bottom: 0; left: 0; right: 0; height: 50px; z-index: 1; }
.footer-bar {
  position: absolute; bottom: 0; left: 0; width: 100%; height: 45px; object-fit: cover;
}
.page-number {
  position: absolute; bottom: 18px; left: 17px;
  font-size: 12px; font-weight: 300; color: #BFBFBF;
}
```

## Section Divider Pattern

```html
<div class="slide section-divider">
  <!-- Background decoration (use section-block-bg.png as default; section-stripe-bg.png may clip text) -->
  <img src="assets/media/section-block-bg.png" alt="" class="section-bg-decoration">

  <!-- Section content -->
  <div class="section-content">
    <div class="section-number-circle">
      <span class="section-num">01</span>
    </div>
    <h2 class="section-title">Section Title Here</h2>
  </div>

  <!-- Page number -->
  <span class="page-number">03</span>
</div>
```

```css
.section-divider { background: #FFFFFF; }
.section-bg-decoration {
  position: absolute; left: 0; top: 0; height: 100%;
  width: auto; opacity: 0.15;
}
.section-content {
  position: absolute; left: 92px; top: 287px;
  display: flex; align-items: flex-start; gap: 18px;
}
.section-number-circle {
  width: 80px; height: 80px; border-radius: 50%;
  background: #0052D9; display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.section-num { font-size: 48px; font-weight: 700; color: #FFFFFF; }
.section-title {
  font-size: 54px; font-weight: 700; color: #0052D9;
  line-height: 1.3; max-width: 838px; margin-top: 10px;
}
.section-divider .page-number {
  position: absolute; left: 17px; bottom: 20px;
  font-size: 12px; color: #BFBFBF; font-weight: 300;
}
```

## Content Slide Patterns

### Content - Text with Section Header (`content-text`)

```html
<div class="slide content-slide">
  <div class="slide-header">
    <div class="badge"><span>2</span></div>
    <span class="section-label">Section Name</span>
  </div>

  <h2 class="content-heading">Slide Title</h2>

  <div class="content-body">
    <p>Body text content goes here. Multiple paragraphs supported.</p>
    <ul>
      <li>Bullet point one</li>
      <li>Bullet point two</li>
    </ul>
  </div>

  <div class="slide-footer">
    <img src="assets/media/footer-bar.png" alt="" class="footer-bar">
    <span class="page-number">04</span>
  </div>
</div>
```

```css
.content-heading {
  position: absolute; left: 98px; top: 110px;
  font-size: 42px; font-weight: 700; color: #0052D9;
}
.content-body {
  position: absolute; left: 98px; top: 180px; right: 98px; bottom: 70px;
  font-size: 24px; color: #000000; line-height: 1.8;
  font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
  display: flex; flex-direction: column;
  justify-content: center;
  gap: 24px;
}
.content-body ul { padding-left: 24px; }
.content-body li { margin-bottom: 12px; }
```

### Content - Image Right (`content-image-right`)

```html
<div class="slide content-slide">
  <div class="slide-header">
    <div class="badge"><span>2</span></div>
    <span class="section-label">Section Name</span>
  </div>

  <h2 class="content-heading">Slide Title</h2>

  <div class="content-split">
    <div class="split-text">
      <p>Description text here...</p>
    </div>
    <div class="split-image">
      <img src="/path/to/user/photo.jpg" alt="Description">
    </div>
  </div>

  <div class="slide-footer">
    <img src="assets/media/footer-bar.png" alt="" class="footer-bar">
    <span class="page-number">05</span>
  </div>
</div>
```

```css
.content-split {
  position: absolute; left: 98px; top: 180px; right: 98px; bottom: 70px;
  display: flex; gap: 40px; align-items: stretch;
}
.split-text {
  flex: 1; font-size: 24px; color: #000000; line-height: 1.8;
  font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
  display: flex; flex-direction: column; justify-content: center;
}
.split-image { flex: 1; }
.split-image img {
  width: 100%; height: 100%; object-fit: cover; border-radius: 4px;
}
```

### Content - Image Left (`content-image-left`)

Mirror of `content-image-right` — image on the left, text on the right. Same CSS, just swap the HTML order:

```html
<div class="slide content-slide">
  <div class="slide-header">
    <div class="badge"><span>2</span></div>
    <span class="section-label">Section Name</span>
  </div>

  <h2 class="content-heading">Slide Title</h2>

  <div class="content-split">
    <div class="split-image">
      <img src="/path/to/user/photo.jpg" alt="Description">
    </div>
    <div class="split-text">
      <p>Description text here...</p>
    </div>
  </div>

  <div class="slide-footer">
    <img src="assets/media/footer-bar.png" alt="" class="footer-bar">
    <span class="page-number">05</span>
  </div>
</div>
```

Uses the same `.content-split`, `.split-text`, `.split-image` CSS as `content-image-right`. The visual difference comes from source order in HTML.

### Content - Two Columns (`content-2-column`)

```html
<div class="slide content-slide">
  <div class="slide-header">
    <div class="badge"><span>2</span></div>
    <span class="section-label">Section Name</span>
  </div>

  <h2 class="content-heading">Slide Title</h2>

  <div class="two-column">
    <div class="column">
      <h3 class="column-title">Column One</h3>
      <p>First column content...</p>
    </div>
    <div class="column-divider"></div>
    <div class="column">
      <h3 class="column-title">Column Two</h3>
      <p>Second column content...</p>
    </div>
  </div>

  <div class="slide-footer">
    <img src="assets/media/footer-bar.png" alt="" class="footer-bar">
    <span class="page-number">05</span>
  </div>
</div>
```

```css
.two-column {
  position: absolute; left: 98px; top: 180px; right: 98px; bottom: 70px;
  display: flex; gap: 0; align-items: stretch;
}
.column {
  flex: 1; padding: 0 40px;
  font-size: 24px; color: #000000; line-height: 1.8;
  font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
  display: flex; flex-direction: column; justify-content: center;
}
.column:first-child { padding-left: 0; }
.column:last-child { padding-right: 0; }
.column-title {
  font-size: 30px; font-weight: 700; color: #0052D9; margin-bottom: 20px;
  font-family: 'TencentSans', 'Microsoft YaHei', sans-serif;
}
.column-divider {
  width: 2px; background: #DFEBFA; flex-shrink: 0;
}
```

### Content - Chart (`content-chart`)

For data visualization slides. The chart area is a placeholder — use `<canvas>`, `<svg>`, or an `<img>` of a pre-rendered chart:

```html
<div class="slide content-slide">
  <div class="slide-header">
    <div class="badge"><span>2</span></div>
    <span class="section-label">Section Name</span>
  </div>

  <h2 class="content-heading">Chart Title</h2>

  <div class="chart-area">
    <!-- Option A: inline SVG chart -->
    <svg class="chart-svg"><!-- ... --></svg>

    <!-- Option B: pre-rendered chart image -->
    <!-- <img src="/path/to/chart.png" alt="Chart" class="chart-img"> -->
  </div>

  <p class="chart-caption">Source: Data source description</p>

  <div class="slide-footer">
    <img src="assets/media/footer-bar.png" alt="" class="footer-bar">
    <span class="page-number">08</span>
  </div>
</div>
```

```css
.chart-area {
  position: absolute; left: 98px; top: 180px; right: 98px; bottom: 110px;
  display: flex; align-items: center; justify-content: center;
  background: #FAFBFE; border-radius: 8px;
  padding: 24px;
}
.chart-svg, .chart-img {
  max-width: 100%; max-height: 100%; object-fit: contain;
}
.chart-caption {
  position: absolute; left: 98px; bottom: 72px;
  font-size: 16px; color: #797979;
}
```

### Content - Full Image (`content-full-image`)

```html
<div class="slide full-image-slide">
  <img src="/path/to/user/hero-image.jpg" alt="Description" class="full-img">
  <div class="image-overlay">
    <h2 class="overlay-title">Optional Title Overlay</h2>
  </div>
</div>
```

```css
.full-image-slide { background: #1a1a2e; }
.full-img { width: 100%; height: 100%; object-fit: cover; }
.image-overlay {
  position: absolute; bottom: 70px; left: 98px; right: 98px;
  background: linear-gradient(transparent, rgba(0,0,0,0.7));
  padding: 40px;
}
.overlay-title { font-size: 42px; font-weight: 700; color: #FFFFFF; }
```

### Content - Three Images (`content-3-images`)

```html
<div class="slide content-slide">
  <div class="slide-header">
    <div class="badge"><span>2</span></div>
    <span class="section-label">Section Name</span>
  </div>

  <h2 class="content-heading">Gallery Title</h2>

  <div class="image-grid-3">
    <div class="grid-item">
      <img src="/path/to/user/img1.jpg" alt="">
      <p class="grid-caption">Caption 1</p>
    </div>
    <div class="grid-item">
      <img src="/path/to/user/img2.jpg" alt="">
      <p class="grid-caption">Caption 2</p>
    </div>
    <div class="grid-item">
      <img src="/path/to/user/img3.jpg" alt="">
      <p class="grid-caption">Caption 3</p>
    </div>
  </div>

  <div class="slide-footer">
    <img src="assets/media/footer-bar.png" alt="" class="footer-bar">
    <span class="page-number">06</span>
  </div>
</div>
```

```css
.image-grid-3 {
  position: absolute; left: 98px; top: 180px; right: 98px; bottom: 70px;
  display: flex; gap: 28px; align-items: stretch;
}
.grid-item { flex: 1; display: flex; flex-direction: column; }
.grid-item img {
  width: 100%; flex: 1; object-fit: cover; border-radius: 4px;
}
.grid-caption {
  margin-top: 12px; font-size: 18px; color: #797979; text-align: center;
}
```

### Content - Cards (`content-cards`)

```html
<div class="slide content-slide">
  <div class="slide-header">
    <div class="badge"><span>2</span></div>
    <span class="section-label">Section Name</span>
  </div>
  <h2 class="content-heading">Slide Title</h2>

  <div class="card-grid">
    <div class="card">
      <div class="card-icon">01</div>
      <h3 class="card-title">Card Title</h3>
      <p class="card-desc">Card description text</p>
    </div>
    <div class="card">
      <div class="card-icon">02</div>
      <h3 class="card-title">Card Title</h3>
      <p class="card-desc">Card description text</p>
    </div>
    <div class="card">
      <div class="card-icon">03</div>
      <h3 class="card-title">Card Title</h3>
      <p class="card-desc">Card description text</p>
    </div>
  </div>

  <div class="slide-footer">
    <img src="assets/media/footer-bar.png" alt="" class="footer-bar">
    <span class="page-number">07</span>
  </div>
</div>
```

```css
.card-grid {
  position: absolute; left: 98px; top: 180px; right: 98px; bottom: 70px;
  display: flex; gap: 28px; align-items: stretch;
}
.card {
  flex: 1; padding: 32px;
  background: #F8F9FD; border-radius: 8px;
  border-left: 4px solid #0052D9;
  display: flex; flex-direction: column;
  justify-content: center;
}
.card-icon {
  font-size: 36px; font-weight: 700; color: #0052D9; margin-bottom: 16px;
}
.card-title {
  font-size: 30px; font-weight: 700; color: #000000; margin-bottom: 12px;
}
.card-desc { font-size: 22px; color: #797979; line-height: 1.6; }
```

### Content - Video (`content-video`)

```html
<div class="slide content-slide">
  <div class="slide-header">
    <div class="badge"><span>3</span></div>
    <span class="section-label">Section Name</span>
  </div>
  <h2 class="content-heading">Video Title</h2>

  <div class="video-container">
    <video controls autoplay muted loop>
      <source src="/path/to/user/demo.mp4" type="video/mp4">
    </video>
  </div>

  <div class="slide-footer">
    <img src="assets/media/footer-bar.png" alt="" class="footer-bar">
    <span class="page-number">08</span>
  </div>
</div>
```

```css
.video-container {
  position: absolute; left: 98px; top: 180px; right: 98px; bottom: 70px;
  display: flex; align-items: center; justify-content: center;
  background: #000000; border-radius: 4px; overflow: hidden;
}
.video-container video {
  width: 100%; height: 100%; object-fit: contain;
}
```

### Content - Animated GIF

Use the same pattern as images. GIFs play automatically in `<img>` tags:

```html
<img src="/path/to/user/animation.gif" alt="Animation" class="content-gif">
```

```css
.content-gif {
  max-width: 100%; max-height: 100%; object-fit: contain;
}
```

### Content - Quote (`content-quote`)

```html
<div class="slide quote-slide">
  <div class="quote-mark">"</div>
  <blockquote class="quote-text">
    The quote text goes here. Keep it impactful and concise.
  </blockquote>
  <p class="quote-attribution">— Attribution Name, Title</p>

  <div class="slide-footer">
    <img src="assets/media/footer-bar.png" alt="" class="footer-bar">
    <span class="page-number">09</span>
  </div>
</div>
```

```css
.quote-slide { background: #FFFFFF; display: flex; flex-direction: column; justify-content: center; padding: 0 200px; }
.quote-mark { font-size: 200px; color: #DFEBFA; line-height: 0.6; margin-bottom: 20px; }
.quote-text {
  font-size: 42px; font-weight: 700; color: #0052D9;
  line-height: 1.5; max-width: 1200px;
}
.quote-attribution {
  margin-top: 30px; font-size: 24px; color: #797979;
}
```

### Content - Statistics (`content-stats`)

```html
<div class="slide content-slide">
  <div class="slide-header">
    <div class="badge"><span>2</span></div>
    <span class="section-label">Section Name</span>
  </div>
  <h2 class="content-heading">Key Metrics</h2>

  <div class="stats-grid">
    <div class="stat-item">
      <span class="stat-number">98%</span>
      <span class="stat-label">User Satisfaction</span>
    </div>
    <div class="stat-item">
      <span class="stat-number">2.5M</span>
      <span class="stat-label">Daily Active Users</span>
    </div>
    <div class="stat-item">
      <span class="stat-number">150+</span>
      <span class="stat-label">Countries Served</span>
    </div>
  </div>

  <div class="slide-footer">
    <img src="assets/media/footer-bar.png" alt="" class="footer-bar">
    <span class="page-number">10</span>
  </div>
</div>
```

```css
.stats-grid {
  position: absolute; left: 98px; top: 180px; right: 98px; bottom: 70px;
  display: flex; gap: 60px; justify-content: center; align-items: center;
}
.stat-item { text-align: center; flex: 1; }
.stat-number {
  display: block; font-size: 72px; font-weight: 700; color: #0052D9; margin-bottom: 16px;
}
.stat-label { font-size: 24px; color: #797979; }
```

### Content - Timeline (`content-timeline`)

```html
<div class="slide content-slide">
  <div class="slide-header">
    <div class="badge"><span>2</span></div>
    <span class="section-label">Section Name</span>
  </div>
  <h2 class="content-heading">Project Timeline</h2>

  <div class="timeline">
    <div class="timeline-line"></div>
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-date">Q1 2024</div>
      <div class="timeline-content">
        <h4>Phase 1</h4>
        <p>Description of this phase</p>
      </div>
    </div>
    <!-- More items... -->
  </div>

  <div class="slide-footer">
    <img src="assets/media/footer-bar.png" alt="" class="footer-bar">
    <span class="page-number">11</span>
  </div>
</div>
```

```css
.timeline {
  position: absolute; left: 98px; top: 180px; right: 98px; bottom: 70px;
  display: flex; align-items: flex-start; gap: 0; padding-top: 40px;
}
.timeline-line {
  position: absolute; top: 50px; left: 0; right: 0;
  height: 3px; background: #DFEBFA;
}
.timeline-item {
  flex: 1; text-align: center; position: relative; padding: 0 20px;
}
.timeline-dot {
  width: 16px; height: 16px; border-radius: 50%;
  background: #0052D9; margin: 0 auto 20px;
  position: relative; z-index: 1;
}
.timeline-date { font-size: 18px; color: #0052D9; font-weight: 700; margin-bottom: 12px; }
.timeline-content h4 { font-size: 24px; font-weight: 700; color: #000; margin-bottom: 8px; }
.timeline-content p { font-size: 20px; color: #797979; line-height: 1.5; }
```

### Content - Comparison (`content-comparison`)

```html
<div class="slide content-slide">
  <div class="slide-header">
    <div class="badge"><span>2</span></div>
    <span class="section-label">Section Name</span>
  </div>
  <h2 class="content-heading">Before vs After</h2>

  <div class="comparison">
    <div class="comparison-side comparison-left">
      <h3 class="comparison-label">Before</h3>
      <div class="comparison-content">
        <!-- Text, image, or any content -->
      </div>
    </div>
    <div class="comparison-divider"></div>
    <div class="comparison-side comparison-right">
      <h3 class="comparison-label">After</h3>
      <div class="comparison-content">
        <!-- Text, image, or any content -->
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <img src="assets/media/footer-bar.png" alt="" class="footer-bar">
    <span class="page-number">12</span>
  </div>
</div>
```

```css
.comparison {
  position: absolute; left: 98px; top: 180px; right: 98px; bottom: 70px;
  display: flex; gap: 0;
}
.comparison-side { flex: 1; padding: 30px; display: flex; flex-direction: column; justify-content: center; }
.comparison-left { background: #F8F9FD; border-radius: 8px 0 0 8px; }
.comparison-right { background: #DFEBFA; border-radius: 0 8px 8px 0; }
.comparison-label {
  font-size: 24px; font-weight: 700; color: #0052D9; margin-bottom: 20px;
}
.comparison-divider { width: 2px; background: #0052D9; }
```

## Ending Slide Pattern

```html
<div class="slide ending-slide">
  <!-- Pattern overlay -->
  <img src="assets/media/ending-pattern-grid.png" alt="" class="ending-pattern">

  <!-- Thanks text -->
  <h1 class="thanks-text">Thanks</h1>

  <!-- Logo -->
  <img src="assets/media/tencent-logo-white.png" alt="Tencent" class="ending-logo">
</div>
```

```css
.ending-slide { background: #0052DA; }
.ending-pattern {
  position: absolute; inset: 0; width: 100%; height: 100%;
  object-fit: cover; mix-blend-mode: soft-light; opacity: 0.5;
}
.thanks-text {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  font-size: 120px; font-weight: 700; color: #FFFFFF; z-index: 1;
}
.ending-logo {
  position: absolute; left: 78px; bottom: 74px;
  height: 31px; width: auto; z-index: 1;
}
```

## Title-Only Slide Pattern

```html
<div class="slide title-only-slide">
  <h1 class="center-title">Large Centered Title</h1>

  <div class="slide-footer">
    <img src="assets/media/footer-bar.png" alt="" class="footer-bar">
    <span class="page-number">04</span>
  </div>
</div>
```

```css
.center-title {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  font-size: 66px; font-weight: 700; color: #0538D0;
  text-align: center; max-width: 1400px;
}
```

## Index / Slideshow Viewer Pattern

Generate an `index.html` that serves as a full-screen slideshow viewer with keyboard navigation. It loads all slides as iframes and displays one at a time. This replaces the old gallery grid.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>Presentation Title - Slideshow</title>
  <style>
    @font-face {
      font-family: 'TencentSans';
      src: url('assets/fonts/TencentSans-W7.ttf') format('truetype');
      font-weight: 700;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 100%; height: 100%; overflow: hidden; background: #1a1a2e; }
    body { font-family: 'TencentSans', 'Microsoft YaHei', sans-serif; }

    /* Slideshow container */
    .slideshow { position: relative; width: 100vw; height: 100vh; }
    .slide-frame {
      position: absolute; inset: 0;
      width: 100%; height: 100%;
      border: none; display: none;
      background: #1a1a2e;
    }
    .slide-frame.active { display: block; }

    /* Controls overlay */
    .controls {
      position: fixed; bottom: 0; left: 0; right: 0;
      height: 56px;
      background: linear-gradient(transparent, rgba(0,0,0,0.6));
      display: flex; align-items: center; justify-content: center;
      gap: 20px; z-index: 100;
      opacity: 0; transition: opacity 0.3s;
    }
    .slideshow:hover .controls,
    .controls:hover { opacity: 1; }

    .controls button {
      background: rgba(255,255,255,0.15); border: none; color: #fff;
      width: 40px; height: 40px; border-radius: 50%; cursor: pointer;
      font-size: 18px; display: flex; align-items: center; justify-content: center;
      transition: background 0.2s;
    }
    .controls button:hover { background: rgba(255,255,255,0.3); }

    .slide-counter {
      color: rgba(255,255,255,0.8); font-size: 14px;
      min-width: 60px; text-align: center;
    }

    /* PDF export progress overlay */
    .export-overlay {
      position: fixed; inset: 0; z-index: 300;
      background: rgba(0,0,0,0.85);
      display: none; flex-direction: column;
      align-items: center; justify-content: center; gap: 20px;
    }
    .export-overlay.active { display: flex; }
    .export-overlay h2 { color: #fff; font-size: 24px; }
    .export-progress { color: rgba(255,255,255,0.7); font-size: 16px; }
    .export-bar-bg { width: 320px; height: 6px; background: rgba(255,255,255,0.15); border-radius: 3px; overflow: hidden; }
    .export-bar-fill { height: 100%; background: #0052D9; border-radius: 3px; transition: width 0.3s; width: 0; }

    /* Gallery mode */
    .gallery-overlay {
      position: fixed; inset: 0; z-index: 200;
      background: rgba(0,0,0,0.95); overflow-y: auto;
      padding: 40px; display: none;
    }
    .gallery-overlay.active { display: block; }
    .gallery-header {
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 30px;
    }
    .gallery-header h1 { color: #fff; font-size: 24px; }
    .gallery-close {
      background: rgba(255,255,255,0.15); border: none; color: #fff;
      width: 40px; height: 40px; border-radius: 50%; cursor: pointer;
      font-size: 20px;
    }
    .gallery-grid {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 20px;
    }
    .gallery-card {
      background: #222; border-radius: 8px; overflow: hidden;
      cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;
    }
    .gallery-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,82,217,0.2); }
    .gallery-card-preview {
      width: 100%; aspect-ratio: 16/9; overflow: hidden; position: relative;
    }
    .gallery-card-preview iframe {
      width: 1920px; height: 1080px; border: none;
      transform-origin: 0 0;
      pointer-events: none;
    }
    .gallery-card-info { padding: 12px 16px; }
    .gallery-card-info h3 { font-size: 14px; color: #fff; margin: 0 0 2px; }
    .gallery-card-info p { font-size: 12px; color: #999; margin: 0; }
  </style>
</head>
<body>
  <div class="slideshow" id="slideshow">
    <!-- Iframes are inserted dynamically by JS -->
  </div>

  <div class="controls">
    <button id="btn-gallery" title="Gallery (G)">☰</button>
    <button id="btn-prev" title="Previous (←)">◀</button>
    <span class="slide-counter" id="counter">1 / 1</span>
    <button id="btn-next" title="Next (→)">▶</button>
    <button id="btn-fullscreen" title="Fullscreen (F)">⛶</button>
    <button id="btn-export" title="Export PDF (P)">📄</button>
  </div>

  <div class="gallery-overlay" id="gallery">
    <div class="gallery-header">
      <h1>All Slides</h1>
      <button class="gallery-close" id="gallery-close">✕</button>
    </div>
    <div class="gallery-grid" id="gallery-grid"></div>
  </div>

  <div class="export-overlay" id="export-overlay">
    <h2>Exporting PDF…</h2>
    <div class="export-progress" id="export-progress">Preparing…</div>
    <div class="export-bar-bg"><div class="export-bar-fill" id="export-bar"></div></div>
  </div>

  <script>
    // === CONFIGURE SLIDES HERE ===
    var SLIDES = [
      // { file: 'slide-01-cover.html', title: '01 - Cover', desc: 'Presentation cover' },
      // { file: 'slide-02-toc.html', title: '02 - Table of Contents', desc: 'Agenda' },
      // ...add all slides here
    ];

    var current = 0;
    var slideshow = document.getElementById('slideshow');
    var counter = document.getElementById('counter');
    var gallery = document.getElementById('gallery');
    var galleryGrid = document.getElementById('gallery-grid');

    // Build iframes
    SLIDES.forEach(function(s, i) {
      var iframe = document.createElement('iframe');
      iframe.className = 'slide-frame' + (i === 0 ? ' active' : '');
      iframe.src = s.file;
      iframe.loading = i < 3 ? 'eager' : 'lazy';
      iframe.addEventListener('load', function() {
        try { iframe.contentWindow.postMessage('fitSlide', '*'); } catch(e) {}
        setTimeout(function() { try { iframe.contentWindow.postMessage('fitSlide', '*'); } catch(e) {} }, 200);
        setTimeout(function() { try { iframe.contentWindow.postMessage('fitSlide', '*'); } catch(e) {} }, 500);
      });
      slideshow.appendChild(iframe);
    });

    // Notify all visible iframes to recalculate on fullscreen change
    function notifyIframesFit() {
      var frames = slideshow.querySelectorAll('.slide-frame');
      frames.forEach(function(f) {
        try { f.contentWindow.postMessage('fitSlide', '*'); } catch(e) {}
      });
    }
    document.addEventListener('fullscreenchange', function() {
      setTimeout(notifyIframesFit, 100);
      setTimeout(notifyIframesFit, 300);
      setTimeout(notifyIframesFit, 600);
    });
    document.addEventListener('webkitfullscreenchange', function() {
      setTimeout(notifyIframesFit, 100);
      setTimeout(notifyIframesFit, 300);
      setTimeout(notifyIframesFit, 600);
    });

    // Build gallery
    SLIDES.forEach(function(s, i) {
      var card = document.createElement('div');
      card.className = 'gallery-card';
      card.innerHTML =
        '<div class="gallery-card-preview">' +
          '<iframe src="' + s.file + '" loading="lazy" style="transform:scale(' + (320/1920) + ')"></iframe>' +
        '</div>' +
        '<div class="gallery-card-info"><h3>' + s.title + '</h3><p>' + (s.desc||'') + '</p></div>';
      card.addEventListener('click', function() { goTo(i); closeGallery(); });
      galleryGrid.appendChild(card);
    });

    function updateCounter() {
      counter.textContent = (current + 1) + ' / ' + SLIDES.length;
    }

    function goTo(index) {
      if (index < 0 || index >= SLIDES.length) return;
      var frames = slideshow.querySelectorAll('.slide-frame');
      frames[current].classList.remove('active');
      current = index;
      frames[current].classList.add('active');
      updateCounter();
    }

    function next() { goTo(current + 1); }
    function prev() { goTo(current - 1); }

    function openGallery() { gallery.classList.add('active'); }
    function closeGallery() { gallery.classList.remove('active'); }

    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(function(){});
      } else {
        document.exitFullscreen();
      }
    }

    // Button events
    document.getElementById('btn-next').addEventListener('click', next);
    document.getElementById('btn-prev').addEventListener('click', prev);
    document.getElementById('btn-fullscreen').addEventListener('click', toggleFullscreen);
    document.getElementById('btn-gallery').addEventListener('click', openGallery);
    document.getElementById('gallery-close').addEventListener('click', closeGallery);
    document.getElementById('btn-export').addEventListener('click', exportPDF);

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
      if (gallery.classList.contains('active')) {
        if (e.key === 'Escape') closeGallery();
        return;
      }
      switch(e.key) {
        case 'ArrowRight': case ' ': e.preventDefault(); next(); break;
        case 'ArrowLeft': e.preventDefault(); prev(); break;
        case 'Home': e.preventDefault(); goTo(0); break;
        case 'End': e.preventDefault(); goTo(SLIDES.length - 1); break;
        case 'f': case 'F': toggleFullscreen(); break;
        case 'g': case 'G': openGallery(); break;
        case 'p': case 'P': exportPDF(); break;
        case 'Escape': if (document.fullscreenElement) document.exitFullscreen(); break;
      }
    });

    // === PDF Export (pure frontend: html2canvas + jsPDF) ===
    var exportBusy = false;
    function loadScript(src) {
      return new Promise(function(resolve, reject) {
        var s = document.createElement('script');
        s.src = src; s.onload = resolve; s.onerror = reject;
        document.head.appendChild(s);
      });
    }
    async function loadLibsIfNeeded() {
      if (!window.html2canvas) await loadScript('https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js');
      if (!window.jspdf) await loadScript('https://cdn.jsdelivr.net/npm/jspdf@2.5.2/dist/jspdf.umd.min.js');
    }
    async function captureSlide(iframe) {
      var slideEl = iframe.contentDocument.querySelector('.slide');
      if (!slideEl) throw new Error('No .slide element found');
      // Temporarily reset transform so html2canvas captures at full 1920x1080
      var origTransform = slideEl.style.transform;
      var origLeft = slideEl.style.left;
      var origTop = slideEl.style.top;
      slideEl.style.transform = 'none';
      slideEl.style.left = '0px';
      slideEl.style.top = '0px';
      var canvas = await html2canvas(slideEl, { scale: 2, useCORS: true, allowTaint: true, width: 1920, height: 1080 });
      slideEl.style.transform = origTransform;
      slideEl.style.left = origLeft;
      slideEl.style.top = origTop;
      return canvas;
    }
    async function exportPDF() {
      if (exportBusy) return;
      // file:// fallback
      if (location.protocol === 'file:') { window.print(); return; }
      exportBusy = true;
      var overlay = document.getElementById('export-overlay');
      var progress = document.getElementById('export-progress');
      var bar = document.getElementById('export-bar');
      overlay.classList.add('active');
      progress.textContent = 'Loading libraries…';
      bar.style.width = '0%';
      try {
        await loadLibsIfNeeded();
        var jsPDF = window.jspdf.jsPDF;
        var pdf = new jsPDF({ orientation: 'landscape', unit: 'px', format: [1920, 1080], compress: true });
        var frames = slideshow.querySelectorAll('.slide-frame');
        for (var i = 0; i < SLIDES.length; i++) {
          progress.textContent = 'Slide ' + (i+1) + ' / ' + SLIDES.length;
          bar.style.width = ((i / SLIDES.length) * 100) + '%';
          // Ensure iframe is loaded and visible for capture
          var f = frames[i];
          f.style.display = 'block';
          f.contentWindow.postMessage('fitSlide', '*');
          await new Promise(function(r) { setTimeout(r, 300); });
          var canvas = await captureSlide(f);
          if (i !== current) f.style.display = 'none';
          var imgData = canvas.toDataURL('image/jpeg', 0.92);
          if (i > 0) pdf.addPage([1920, 1080], 'landscape');
          pdf.addImage(imgData, 'JPEG', 0, 0, 1920, 1080);
        }
        // Restore display state
        frames.forEach(function(f, idx) { f.style.display = idx === current ? 'block' : 'none'; });
        bar.style.width = '100%';
        progress.textContent = 'Saving…';
        var title = document.title.replace(/[\\/:*?"<>|]/g, '') || 'slides';
        pdf.save(title + '.pdf');
      } catch(e) {
        alert('PDF export failed: ' + e.message);
        console.error(e);
      } finally {
        overlay.classList.remove('active');
        exportBusy = false;
      }
    }

    updateCounter();
  </script>
</body>
</html>
```

**Key features:**
- **Keyboard navigation**: ←/→ arrows, Space (next), Home/End, Escape
- **Fullscreen**: Press F or click button
- **Gallery view**: Press G or click ☰ to see all slides as thumbnails; click a thumbnail to jump to that slide
- **PDF export**: Press P or click 📄 to export all slides as a PDF (requires HTTP server; falls back to print dialog under `file://`)
- **Slide counter**: Shows "3 / 15" style indicator
- **Auto-hide controls**: Controls fade in on hover
- **Lazy loading**: Only first 3 iframes load eagerly; rest are lazy-loaded

## Multicolor Theme Variations

For multicolor theme, replace the single blue palette with the multicolor accent system:

```css
/* Multicolor theme overrides */
.theme-multicolor {
  --accent-1: #0052D9;  /* Blue */
  --accent-2: #FF7535;  /* Orange */
  --accent-3: #9BCF3F;  /* Green */
  --accent-4: #3DC0DB;  /* Cyan */
}

/* Apply to cards, chart series, TOC numbers, etc. */
.theme-multicolor .card:nth-child(1) { border-left-color: var(--accent-1); }
.theme-multicolor .card:nth-child(2) { border-left-color: var(--accent-2); }
.theme-multicolor .card:nth-child(3) { border-left-color: var(--accent-3); }
.theme-multicolor .card:nth-child(4) { border-left-color: var(--accent-4); }

.theme-multicolor .toc-number:nth-child(1) { color: var(--accent-1); }
.theme-multicolor .toc-number:nth-child(2) { color: var(--accent-2); }
.theme-multicolor .toc-number:nth-child(3) { color: var(--accent-3); }
.theme-multicolor .toc-number:nth-child(4) { color: var(--accent-4); }
```

## Media Embedding Reference

User-provided media files should be referenced by **absolute path** (for local files) or **URL** (for remote files). Do NOT create an `assets/user-media/` directory.

### Local Image

```html
<!-- Use absolute path to the user's file -->
<img src="/absolute/path/to/photo.jpg" alt="Description">
```

### Remote Image (URL)

```html
<img src="https://example.com/image.jpg" alt="Description" crossorigin="anonymous">
```

### Animated GIF

```html
<img src="/absolute/path/to/animation.gif" alt="Animation description">
```

### Video (Local)

```html
<video controls autoplay muted loop playsinline>
  <source src="/absolute/path/to/video.mp4" type="video/mp4">
</video>
```

### Video (URL)

```html
<video controls autoplay muted loop playsinline>
  <source src="https://example.com/video.mp4" type="video/mp4">
</video>
```

### iframe Embed (YouTube, etc.)

```html
<div class="embed-container" style="position:relative;width:100%;padding-bottom:56.25%;height:0;overflow:hidden;">
  <iframe src="https://www.youtube.com/embed/VIDEO_ID"
    style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;"
    allowfullscreen></iframe>
</div>
```
