# Component Reference

All 15 components. Each entry: HTML structure + CSS. Load this file when building specific components.

---

## 1. Top Navigation

```html
<nav class="top-nav">
  <div class="top-nav__container">
    <a href="/" class="top-nav__brand" aria-label="WeChat home">
      <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
        <path d="M8.5 3C4.4 3 1 5.8 1 9.3c0 2.1 1.3 4 3.3 5.2l-.7 2.3 2.6-1.4c.7.2 1.5.3 2.3.3h.2c-.1-.4-.2-.8-.2-1.2 0-3.4 3.2-6.1 7.1-6.1.3 0 .6 0 .9.1C15.7 5.4 12.4 3 8.5 3z" fill="#07c160"/>
        <path d="M15.4 9.9c-3.4 0-6.1 2.4-6.1 5.4s2.7 5.4 6.1 5.4c.7 0 1.3-.1 1.9-.3l2.1 1.1-.6-1.9c1.6-1 2.7-2.6 2.7-4.3 0-3-2.7-5.4-6.1-5.4z" fill="#07c160" opacity="0.55"/>
      </svg>
      <span>WeChat</span>
    </a>
    <ul class="top-nav__links scroll-fade-x" role="list">
      <li><a href="#" class="nav-link">Newsroom</a></li>
      <li><a href="#" class="nav-link">Safety Center</a></li>
      <li><a href="#" class="nav-link">Help Center</a></li>
    </ul>
    <div class="top-nav__actions">
      <a href="#" class="btn-text-link">Sign in</a>
      <a href="#" class="btn-primary">Get WeChat</a>
    </div>
  </div>
</nav>
```

```css
.top-nav {
  position: sticky; top: 0; z-index: 100;
  background: var(--color-canvas);
  border-bottom: 1px solid var(--color-hairline);
  height: 60px; display: flex; align-items: center;
  transition: box-shadow var(--motion-normal) var(--ease-standard);
}
.top-nav__container {
  max-width: 1200px; margin: 0 auto;
  padding: 0 var(--space-xl); width: 100%;
  display: flex; align-items: center; gap: var(--space-xl);
}
.top-nav__brand {
  display: flex; align-items: center; gap: var(--space-xs);
  text-decoration: none; color: var(--color-ink);
  font-size: 16px; font-weight: 600;
}
.top-nav__links {
  display: flex; gap: var(--space-sm);
  list-style: none; margin: 0; padding: 0; flex: 1;
  flex-wrap: nowrap; white-space: nowrap;
}
/* When links may overflow (many channels, narrow viewport), pair with
   .scroll-fade-x (see references/layout.md) instead of a bare overflow-x:
   <ul class="top-nav__links scroll-fade-x"> — never show a raw scrollbar. */
.nav-link {
  font-size: 14px; font-weight: 500; color: var(--color-muted);
  text-decoration: none; padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-sm);
  transition: color var(--motion-fast) var(--ease-standard), background var(--motion-fast) var(--ease-standard);
}
.nav-link:hover { color: var(--color-ink); background: var(--color-surface-soft); }
.top-nav__actions { display: flex; align-items: center; gap: var(--space-md); }
```

---

## 2. Buttons

```css
/* Primary — WeChat green, pill shape is the default */
.btn-primary {
  display: inline-flex; align-items: center; justify-content: center;
  background: var(--color-primary); color: var(--color-on-primary);
  font-size: 14px; font-weight: 500; line-height: 1;
  padding: 0 22px; height: 40px;
  border-radius: var(--radius-pill); border: none; cursor: pointer; text-decoration: none;
  transition: background var(--motion-fast) var(--ease-standard), transform var(--motion-instant) var(--ease-standard);
}
.btn-primary:hover   { background: var(--color-primary-active); }
.btn-primary:active  { transform: scale(0.96); }
.btn-primary:disabled { background: var(--color-primary-disabled); color: #fff; cursor: not-allowed; transform: none; }

/* Secondary — white with hairline */
.btn-secondary {
  display: inline-flex; align-items: center; justify-content: center;
  background: var(--color-canvas); color: var(--color-ink);
  font-size: 14px; font-weight: 500; line-height: 1;
  padding: 0 22px; height: 40px;
  border-radius: var(--radius-pill); border: 1px solid var(--color-hairline);
  cursor: pointer; text-decoration: none;
  transition: border-color var(--motion-fast) var(--ease-standard), transform var(--motion-instant) var(--ease-standard);
}
.btn-secondary:hover  { border-color: var(--color-muted-soft); }
.btn-secondary:active { transform: scale(0.96); }

/* Secondary on dark surface */
.btn-secondary-dark {
  display: inline-flex; align-items: center; justify-content: center;
  background: rgba(255,255,255,0.08); color: var(--color-on-dark);
  font-size: 14px; font-weight: 500; line-height: 1;
  padding: 0 22px; height: 40px;
  border-radius: var(--radius-pill); border: 1px solid rgba(255,255,255,0.12);
  cursor: pointer; text-decoration: none;
  transition: background var(--motion-fast) var(--ease-standard);
}
.btn-secondary-dark:hover { background: rgba(255,255,255,0.14); }

/* Text link (nav / footer style, not inline article link) */
.btn-text-link {
  background: transparent; color: var(--color-ink);
  font-size: 14px; font-weight: 500;
  border: none; cursor: pointer; text-decoration: none; padding: 0;
  transition: color var(--motion-fast) var(--ease-standard);
}
.btn-text-link:hover { color: var(--color-primary); }

/* Icon circular */
.btn-icon-circular {
  display: inline-flex; align-items: center; justify-content: center;
  width: 36px; height: 36px; border-radius: var(--radius-full);
  background: var(--color-surface-soft); border: none;
  color: var(--color-ink); cursor: pointer;
  transition: background var(--motion-fast) var(--ease-standard), transform var(--motion-instant) var(--ease-standard);
}
.btn-icon-circular:hover  { background: var(--color-surface-strong); }
.btn-icon-circular:active { transform: scale(0.92); }

/* Inline text link — classic WeChat article blue, distinct from CTA green */
.text-link {
  font-size: 15px; color: var(--color-link); text-decoration: none;
  transition: color var(--motion-fast) var(--ease-standard);
}
.text-link:hover { color: var(--color-link-active); text-decoration: underline; }
```

---

## 3. Hero Band

```html
<section class="hero-band">
  <div class="hero-band__container">
    <div class="hero-band__content">
      <div class="badge-tag">1亿+ 用户在线</div>
      <h1 class="display-xl">连接你关心的<br>人、服务与品牌</h1>
      <p class="body-md">WeChat 提供聊天、通话与生活服务，让沟通更简单。</p>
      <div class="hero-band__actions">
        <a href="#" class="btn-primary">立即下载</a>
        <a href="#" class="btn-secondary">了解更多</a>
      </div>
    </div>
    <div class="hero-band__illustration">
      <!-- product mockup / QR code card here -->
    </div>
  </div>
</section>
```

```css
.hero-band { background: var(--color-canvas); padding: var(--space-section) 0; }
.hero-band__container {
  max-width: 1200px; margin: 0 auto; padding: 0 var(--space-xl);
  display: grid; grid-template-columns: 1fr 1fr;
  gap: var(--space-xxl); align-items: center;
}
.hero-band__content { display: flex; flex-direction: column; gap: var(--space-lg); }
.hero-band__actions { display: flex; gap: var(--space-md); flex-wrap: wrap; }

@media (max-width: 768px) {
  .hero-band__container { grid-template-columns: 1fr; }
  .hero-band__illustration { order: 2; }
  .display-xl { font-size: 28px; letter-spacing: 0; }
}
```

---

## 4. Icon Feature Grid (Safety Center style)

Squircle icon chips with tinted-green background — the core visual motif of `safety.wechat.com`.

```html
<section class="feature-section">
  <div class="section-container">
    <h2 class="display-lg reveal">安全工具与保障</h2>
    <div class="feature-grid">
      <article class="feature-card reveal" data-delay="1">
        <div class="icon-chip"><!-- SVG icon --></div>
        <h3 class="feature-card__title">账号安全</h3>
        <p class="feature-card__body">多重验证机制，保护你的账号不被盗用。</p>
      </article>
      <article class="feature-card reveal" data-delay="2">...</article>
      <article class="feature-card reveal" data-delay="3">...</article>
      <article class="feature-card reveal" data-delay="4">...</article>
    </div>
  </div>
</section>
```

```css
.feature-section { background: var(--color-canvas); padding: var(--space-section) 0; }
.section-container { max-width: 1200px; margin: 0 auto; padding: 0 var(--space-xl); }
.feature-grid {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: var(--space-lg); margin-top: var(--space-xxl);
}
.feature-card {
  background: var(--color-surface-card); border-radius: var(--radius-lg);
  padding: var(--space-xl); display: flex; flex-direction: column; gap: var(--space-md);
  transition: transform var(--motion-normal) var(--ease-standard), background var(--motion-normal) var(--ease-standard);
}
.feature-card:hover { transform: translateY(-2px); background: var(--color-surface-strong); }

/* Squircle icon chip — the WeChat signature icon container */
.icon-chip {
  width: 48px; height: 48px; border-radius: var(--radius-xl);
  background: var(--color-primary-soft); color: var(--color-primary);
  display: flex; align-items: center; justify-content: center;
  transition: transform var(--motion-fast) var(--ease-spring);
}
.feature-card:hover .icon-chip { transform: scale(1.06); }

.feature-card__title { font-size: 17px; font-weight: 600; line-height: 1.4; color: var(--color-ink); margin: 0; }
.feature-card__body  { font-size: 15px; font-weight: 400; line-height: 1.6; color: var(--color-body-default); margin: 0; }

@media (max-width: 1024px) { .feature-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px)  { .feature-grid { grid-template-columns: 1fr; } }
```

---

## 5. News / Article Card (Newsroom list)

```html
<div class="news-grid">
  <article class="news-card reveal" data-delay="1">
    <div class="news-card__image"><!-- img --></div>
    <div class="news-card__body">
      <div class="news-card__tags">
        <span class="badge-pill">Innovation</span>
        <span class="badge-pill">Product</span>
      </div>
      <h3 class="news-card__title">The Art of the Polite Decline: WeChat's New "Ignore" Calls Feature</h3>
      <time class="news-card__date">April 1, 2026</time>
    </div>
  </article>
  <!-- repeat -->
</div>
```

```css
.news-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-lg); }
.news-card {
  background: var(--color-canvas); border: 1px solid var(--color-hairline);
  border-radius: var(--radius-lg); overflow: hidden; text-decoration: none;
  display: flex; flex-direction: column;
  transition: transform var(--motion-normal) var(--ease-standard), box-shadow var(--motion-normal) var(--ease-standard);
}
.news-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.08); }
.news-card__image { width: 100%; aspect-ratio: 16/9; background: var(--color-surface-soft); object-fit: cover; }
.news-card__body { padding: var(--space-lg); display: flex; flex-direction: column; gap: var(--space-sm); }
.news-card__tags { display: flex; gap: var(--space-xs); }
.news-card__title { font-size: 17px; font-weight: 600; line-height: 1.45; color: var(--color-ink); margin: 0; }
.news-card__date { font-size: 13px; color: var(--color-muted); }

@media (max-width: 1024px) { .news-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px)  { .news-grid { grid-template-columns: 1fr; } }
```

---

## 6. Help Center Category Card

```html
<div class="category-grid">
  <a href="#" class="category-card reveal" data-delay="1">
    <div class="icon-chip icon-chip--sm"><!-- SVG --></div>
    <div>
      <h4 class="category-card__title">手动操作教程</h4>
      <p class="category-card__body">自助服务指南：帮您安全重新登录账号</p>
    </div>
  </a>
  <!-- repeat -->
</div>
```

```css
.category-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-md); }
.category-card {
  background: var(--color-surface-card); border-radius: var(--radius-lg);
  padding: var(--space-lg); display: flex; align-items: flex-start; gap: var(--space-md);
  text-decoration: none; color: inherit;
  transition: background var(--motion-fast) var(--ease-standard), transform var(--motion-instant) var(--ease-standard);
}
.category-card:hover  { background: var(--color-surface-strong); }
.category-card:active { transform: scale(0.98); }
.icon-chip--sm { width: 40px; height: 40px; border-radius: var(--radius-md); flex-shrink: 0; }
.category-card__title { font-size: 16px; font-weight: 600; color: var(--color-ink); margin: 0 0 4px; }
.category-card__body  { font-size: 14px; color: var(--color-muted); margin: 0; line-height: 1.5; }

@media (max-width: 768px) { .category-grid { grid-template-columns: 1fr; } }
```

---

## 7. Search Bar (Help Center)

```html
<div class="search-bar">
  <svg class="search-bar__icon" width="18" height="18" viewBox="0 0 18 18" fill="none">
    <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.6"/>
    <path d="M16 16l-3.2-3.2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
  </svg>
  <input type="text" class="search-bar__input" placeholder="搜索你需要的帮助">
</div>
```

```css
.search-bar {
  display: flex; align-items: center; gap: var(--space-sm);
  background: var(--color-surface-card); border-radius: var(--radius-pill);
  padding: 0 var(--space-lg); height: 48px; max-width: 560px;
  border: 1px solid transparent;
  transition: border-color var(--motion-fast) var(--ease-standard), background var(--motion-fast) var(--ease-standard);
}
.search-bar:focus-within { border-color: var(--color-primary); background: var(--color-canvas); }
.search-bar__icon  { color: var(--color-muted); flex-shrink: 0; }
.search-bar__input {
  flex: 1; border: none; outline: none; background: transparent;
  font-family: var(--font-body); font-size: 15px; color: var(--color-ink);
}
.search-bar__input::placeholder { color: var(--color-muted-soft); }
```

---

## 8. Download / QR Code Band

```html
<section class="qr-band">
  <div class="section-container qr-band__inner">
    <div class="qr-band__text">
      <h2 class="display-md">扫码下载 WeChat</h2>
      <p class="body-md">使用手机相机扫描二维码，快速安装。</p>
    </div>
    <div class="qr-band__code">
      <!-- QR code image -->
    </div>
  </div>
</section>
```

```css
.qr-band { background: var(--color-surface-soft); padding: var(--space-section) 0; }
.qr-band__inner {
  display: flex; align-items: center; justify-content: space-between; gap: var(--space-xxl);
  flex-wrap: wrap;
}
.qr-band__code {
  width: 140px; height: 140px; background: var(--color-canvas);
  border-radius: var(--radius-lg); border: 1px solid var(--color-hairline);
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}

@media (max-width: 768px) { .qr-band__inner { flex-direction: column; text-align: center; } }
```

---

## 9. Green CTA Callout Band

```html
<section style="background: var(--color-canvas); padding: var(--space-section) 0;">
  <div class="section-container">
    <div class="cta-band-green reveal">
      <div class="cta-band__inner">
        <h2 class="display-sm">开始使用 WeChat</h2>
        <p class="body-md">连接朋友、家人与你关心的一切。</p>
        <div class="cta-band__actions">
          <a href="#" class="btn-secondary">立即下载</a>
          <a href="#" style="color: rgba(255,255,255,0.85); font-size:14px; font-weight:500; text-decoration:none;">查看功能 →</a>
        </div>
      </div>
    </div>
  </div>
</section>
```

```css
.cta-band-green {
  background: var(--color-primary); border-radius: var(--radius-lg); padding: 56px;
}
.cta-band-green .display-sm,
.cta-band-green .body-md { color: var(--color-on-primary); }
.cta-band__inner {
  max-width: 800px; margin: 0 auto;
  display: flex; flex-direction: column; gap: var(--space-lg);
  text-align: center; align-items: center;
}
.cta-band__actions { display: flex; gap: var(--space-md); flex-wrap: wrap; justify-content: center; }

/* Dark variant (used sparingly — footer-adjacent bands only) */
.cta-band-dark { background: var(--color-surface-dark); border-radius: var(--radius-lg); padding: 56px; }
.cta-band-dark .display-sm,
.cta-band-dark .body-md { color: var(--color-on-dark); }

@media (max-width: 768px) {
  .cta-band-green, .cta-band-dark { padding: var(--space-xxl) var(--space-md); }
}
```

---

## 10. Badges

```css
.badge-pill {
  display: inline-flex; align-items: center;
  background: var(--color-surface-strong); color: var(--color-body-default);
  font-size: 12px; font-weight: 500; line-height: 1.4;
  border-radius: var(--radius-pill); padding: 3px 10px;
}
.badge-tag {
  display: inline-flex; align-items: center;
  background: var(--color-primary-soft); color: var(--color-primary-active);
  font-size: 13px; font-weight: 500; line-height: 1.4;
  border-radius: var(--radius-pill); padding: 4px 12px;
}
/* Notification dot — red is reserved exclusively for this */
.badge-dot {
  position: relative; display: inline-block;
}
.badge-dot::after {
  content: ''; position: absolute; top: -2px; right: -2px;
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--color-accent-red);
  border: 1.5px solid var(--color-canvas);
}
.badge-count {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 18px; height: 18px; padding: 0 5px;
  background: var(--color-accent-red); color: #fff;
  font-size: 11px; font-weight: 600; border-radius: var(--radius-pill);
}
```

---

## 11. Text Input

```css
.text-input {
  background: var(--color-canvas); color: var(--color-ink);
  font-size: 15px; font-weight: 400; line-height: 1.6;
  padding: 10px 16px; height: 44px;
  border-radius: var(--radius-md); border: 1px solid var(--color-hairline);
  width: 100%; outline: none;
  transition: border-color var(--motion-fast) var(--ease-standard), box-shadow var(--motion-fast) var(--ease-standard);
}
.text-input:hover { border-color: var(--color-muted-soft); }
.text-input:focus { border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(7,193,96,0.12); }
```

---

## 12. Category Tabs

```html
<!-- Fixed/short tab sets: flex-wrap is fine. -->
<div class="tab-bar" role="tablist">
  <button class="category-tab category-tab--active" role="tab" aria-selected="true">全部</button>
  <button class="category-tab" role="tab">热门功能</button>
  <button class="category-tab" role="tab">账号安全</button>
</div>

<!-- Long/variable tab sets (news channels, category rails) that may overflow
     on mobile: use single-line + .scroll-fade-x instead of wrapping, so tabs
     stay on one row and scroll horizontally WITHOUT a visible scrollbar. -->
<div class="tab-bar tab-bar--scroll scroll-fade-x" role="tablist">
  <button class="category-tab category-tab--active" role="tab" aria-selected="true">推荐</button>
  <button class="category-tab" role="tab">要闻</button>
  <button class="category-tab" role="tab">科技</button>
  <button class="category-tab" role="tab">财经</button>
  <button class="category-tab" role="tab">体育</button>
  <button class="category-tab" role="tab">娱乐</button>
</div>
```

```css
.tab-bar { display: flex; gap: var(--space-xs); flex-wrap: wrap; }
/* Variant for long/variable tab sets: single line, horizontal scroll.
   Always pair with .scroll-fade-x (references/layout.md) — never a bare
   overflow-x, which exposes a raw browser scrollbar on mobile. */
.tab-bar--scroll { flex-wrap: nowrap; overflow-x: auto; padding-bottom: 2px; }
.tab-bar--scroll .category-tab { flex-shrink: 0; }
.category-tab {
  background: transparent; color: var(--color-muted);
  font-size: 14px; font-weight: 500; padding: 8px 16px;
  border-radius: var(--radius-pill); border: none; cursor: pointer;
  transition: background var(--motion-fast) var(--ease-standard), color var(--motion-fast) var(--ease-standard);
}
.category-tab:hover { background: var(--color-surface-soft); color: var(--color-ink); }
.category-tab--active { background: var(--color-primary-soft); color: var(--color-primary-active); font-weight: 600; }
```

---

## 13. Article Detail Header (Newsroom detail page)

```html
<header class="article-header">
  <a href="#" class="article-header__back">← 返回列表</a>
  <h1 class="display-lg">巧妙的拒绝之道：WeChat 全新"忽略"来电功能</h1>
  <div class="article-header__meta">
    <time class="body-sm">2026年4月1日</time>
    <span class="badge-pill">Innovation</span>
    <span class="badge-pill">Product</span>
  </div>
</header>
<article class="article-body">
  <p class="body-md">正文内容...</p>
</article>
```

```css
.article-header { max-width: 720px; margin: 0 auto; padding: var(--space-xxl) var(--space-xl) var(--space-lg); }
.article-header__back {
  display: inline-block; font-size: 14px; color: var(--color-muted);
  text-decoration: none; margin-bottom: var(--space-lg);
  transition: color var(--motion-fast) var(--ease-standard);
}
.article-header__back:hover { color: var(--color-ink); }
.article-header__meta { display: flex; align-items: center; gap: var(--space-sm); margin-top: var(--space-md); }
.article-body { max-width: 720px; margin: 0 auto; padding: 0 var(--space-xl) var(--space-xxl); }
.article-body .body-md { margin-bottom: var(--space-lg); }
.article-body a { color: var(--color-link); text-decoration: none; }
.article-body a:hover { text-decoration: underline; }
```

---

## 14. Footer

```html
<footer class="footer">
  <div class="footer__container">
    <div class="footer__brand">
      <svg><!-- WeChat mark --></svg>
      <span>WeChat</span>
    </div>
    <div class="footer__columns">
      <div>
        <h4 class="footer__heading">产品</h4>
        <a href="#">Weixin</a>
        <a href="#">微信支付</a>
      </div>
      <div>
        <h4 class="footer__heading">资源</h4>
        <a href="#">Newsroom</a>
        <a href="#">Safety Center</a>
        <a href="#">Help Center</a>
      </div>
      <!-- more columns -->
    </div>
  </div>
</footer>
```

```css
.footer { background: var(--color-surface-dark); color: var(--color-on-dark-soft); padding: 56px 0; }
.footer__container { max-width: 1200px; margin: 0 auto; padding: 0 var(--space-xl); display: flex; flex-direction: column; gap: var(--space-xxl); }
.footer__brand { display: flex; align-items: center; gap: var(--space-xs); font-size: 16px; font-weight: 600; color: var(--color-on-dark); }
.footer__columns { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-xxl); }
.footer__heading { font-size: 12px; font-weight: 600; color: var(--color-on-dark); text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 var(--space-md); }
.footer a { font-size: 14px; color: var(--color-on-dark-soft); text-decoration: none; line-height: 2; display: block; transition: color var(--motion-fast) var(--ease-standard); }
.footer a:hover { color: var(--color-on-dark); }
@media (max-width: 768px) { .footer__columns { grid-template-columns: 1fr 1fr; } }
```

---

## 15. Product Entry Grid Card (weixin.qq.com style)

方形白色入口卡片，参考微信公众平台 `weixin.qq.com` 产品矩阵：每张卡片是 1:1 方块，居中放置品牌图标 + 中文标签，按 4×N 网格排列。**核心特征是 hover 时三联动**：卡片上浮 + 阴影浮现 + 图标弹簧放大。

```html
<section class="product-section">
  <div class="section-container">
    <h2 class="display-lg reveal">微信生态产品</h2>
    <div class="product-grid">
      <a href="#" class="product-card reveal" data-delay="1">
        <div class="product-card__icon" style="color:#07c160;">
          <!-- 品牌色 SVG，viewBox 0 0 40 40 -->
          <svg viewBox="0 0 40 40" width="40" height="40" fill="currentColor"><!-- ... --></svg>
        </div>
        <span class="product-card__label">微信支付</span>
      </a>
      <a href="#" class="product-card reveal" data-delay="2">
        <div class="product-card__icon" style="color:#1657d5;">
          <svg viewBox="0 0 40 40" width="40" height="40" fill="currentColor"><!-- ... --></svg>
        </div>
        <span class="product-card__label">公众号</span>
      </a>
      <!-- 14 more cards, last one in a row can be a "more" placeholder -->
    </div>
  </div>
</section>
```

```css
.product-section { background: var(--color-surface-soft); padding: var(--space-section) 0; }

.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-lg);
  margin-top: var(--space-xxl);
}

/* ── Card base — flat, shadowless, 1:1 square ── */
.product-card {
  position: relative;
  background: var(--color-canvas);
  border-radius: var(--radius-md);
  aspect-ratio: 1 / 1;          /* enforce square regardless of label length */
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-md);
  text-decoration: none;
  color: var(--color-ink);
  /* Both transform AND shadow transition — see motion.md "Product Card Hover" */
  transition:
    transform var(--motion-slow) var(--ease-standard),
    box-shadow var(--motion-slow) var(--ease-standard);
  /* No default shadow — separation comes from the gray page floor */
  box-shadow: 0 0 0 rgba(0, 0, 0, 0);
  will-change: transform, box-shadow;
}

/* ── Hover state: lift + multi-layer soft shadow ── */
.product-card:hover {
  transform: translateY(-4px);
  box-shadow:
    0 2px 4px  rgba(0, 0, 0, 0.04),
    0 8px 16px rgba(0, 0, 0, 0.06),
    0 16px 32px rgba(0, 0, 0, 0.04);
}

/* ── Active state: tactile press-down (matches the WeChat motion signature) ── */
.product-card:active {
  transform: scale(0.96);
  transition: transform var(--motion-instant) var(--ease-standard);
}

/* ── Icon: brand-color, spring bounce on card hover ── */
.product-card__icon {
  display: flex; align-items: center; justify-content: center;
  /* Each product has its own color via inline `style="color:#xxx;"` */
  transition: transform var(--motion-fast) var(--ease-spring);
}
.product-card:hover .product-card__icon { transform: scale(1.10); }
.product-card:active .product-card__icon { transform: scale(0.94); }

/* ── Label: below icon, one-line truncation ── */
.product-card__label {
  font-size: 14px;
  font-weight: 400;
  line-height: 1.4;
  color: var(--color-ink);
  text-align: center;
  max-width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ── Responsive — drop to 3-col / 2-col ── */
@media (max-width: 1024px) { .product-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px)  { .product-grid { grid-template-columns: repeat(2, 1fr); } }

/* ── Dark mode: keep white card on a slightly elevated background, hover shadow darkens ── */
[data-theme="dark"] .product-section { background: var(--color-canvas); }
[data-theme="dark"] .product-card {
  background: var(--color-surface-card);
}
[data-theme="dark"] .product-card:hover {
  background: var(--color-surface-strong);
  box-shadow:
    0 2px 4px  rgba(0, 0, 0, 0.3),
    0 8px 16px rgba(0, 0, 0, 0.4);
}
```

**Use case:** open-platform product matrix, ecosystem overview pages, "more tools" grids, any dense icon-plus-label entry grid. Distinct from `.feature-card` (which has a left-aligned icon + multi-line body copy) and `.category-card` (which has a smaller icon chip + headline + body).

**Key visual rules:**
- Icon is `color: currentColor` and gets its hue from the parent — set per-card via `style="color:#xxx"` for each product's brand color (微信支付绿 `#07c160`、公众号蓝 `#1657d5`、小程序紫 `#7b5fc7`、视频号橙 `#fa9d3b`、表情包黄 `#fbbd08`、红包红 `#fa5151` 等)
- Default state has **no shadow** — the gray page floor provides separation, and shadow only emerges on hover (cleaner resting state than always-on shadow)
- **Three-element hover choreography** in one motion: card lifts (280ms standard), shadow fades in (280ms standard), icon springs (160ms spring). The spring on the icon is the only place `--ease-spring` is allowed in this component
- For the 16th "more" or empty slot in a 4×4 grid, use `<span class="product-card product-card--placeholder">` with reduced opacity and no hover effect

**Full motion breakdown** → `references/motion.md` → "Product Card Hover (three-element choreography)"

