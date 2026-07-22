# Component Reference

All 13 components. Each entry: HTML structure + CSS. Load this file when building specific components.

---

## 1. Top Navigation

```html
<nav class="top-nav">
  <div class="top-nav__container">
    <a href="/" class="top-nav__brand" aria-label="Claude home">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M10 1v18M1 10h18M3.22 3.22l13.56 13.56M16.78 3.22L3.22 16.78"
              stroke="#141413" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
      <span>Claude</span>
    </a>
    <ul class="top-nav__links" role="list">
      <li><a href="#" class="nav-link">Product</a></li>
      <li><a href="#" class="nav-link">Pricing</a></li>
      <li><a href="#" class="nav-link">Research</a></li>
    </ul>
    <div class="top-nav__actions">
      <a href="#" class="btn-text-link">Sign in</a>
      <a href="#" class="btn-primary">Try Claude</a>
    </div>
  </div>
</nav>
```

```css
.top-nav {
  position: sticky; top: 0; z-index: 100;
  background: var(--color-canvas);
  border-bottom: 1px solid var(--color-hairline);
  height: 64px; display: flex; align-items: center;
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
}
.nav-link {
  font-size: 14px; font-weight: 500; color: var(--color-muted);
  text-decoration: none; padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-md);
  transition: color var(--motion-fast) var(--ease-out);
}
.nav-link:hover { color: var(--color-ink); }
.top-nav__actions { display: flex; align-items: center; gap: var(--space-md); }
```

---

## 2. Buttons

```css
/* Primary — coral */
.btn-primary {
  display: inline-flex; align-items: center; justify-content: center;
  background: var(--color-primary); color: var(--color-on-primary);
  font-size: 14px; font-weight: 500; line-height: 1;
  padding: 12px 20px; height: 40px;
  border-radius: var(--radius-md); border: none; cursor: pointer; text-decoration: none;
  transition: background var(--motion-fast) var(--ease-out), transform var(--motion-fast) var(--ease-out);
}
.btn-primary:hover  { background: var(--color-primary-active); transform: scale(1.02); }
.btn-primary:active { transform: scale(0.99); }
.btn-primary:disabled { background: var(--color-primary-disabled); color: var(--color-muted); cursor: not-allowed; transform: none; }

/* Secondary — cream with hairline */
.btn-secondary {
  display: inline-flex; align-items: center; justify-content: center;
  background: var(--color-canvas); color: var(--color-ink);
  font-size: 14px; font-weight: 500; line-height: 1;
  padding: 12px 20px; height: 40px;
  border-radius: var(--radius-md); border: 1px solid var(--color-hairline);
  cursor: pointer; text-decoration: none;
  transition: border-color var(--motion-fast) var(--ease-out), transform var(--motion-fast) var(--ease-out);
}
.btn-secondary:hover { border-color: var(--color-muted-soft); transform: scale(1.02); }

/* Secondary on dark surface */
.btn-secondary-dark {
  display: inline-flex; align-items: center; justify-content: center;
  background: var(--color-surface-dark-elevated); color: var(--color-on-dark);
  font-size: 14px; font-weight: 500; line-height: 1;
  padding: 12px 20px; height: 40px;
  border-radius: var(--radius-md); border: 1px solid rgba(255,255,255,0.08);
  cursor: pointer; text-decoration: none;
  transition: background var(--motion-fast) var(--ease-out);
}
.btn-secondary-dark:hover { background: #2e2b27; }

/* Text link */
.btn-text-link {
  background: transparent; color: var(--color-ink);
  font-size: 14px; font-weight: 500;
  border: none; cursor: pointer; text-decoration: none; padding: 0;
  transition: color var(--motion-fast) var(--ease-out);
}
.btn-text-link:hover { color: var(--color-primary); }

/* Icon circular */
.btn-icon-circular {
  display: inline-flex; align-items: center; justify-content: center;
  width: 36px; height: 36px; border-radius: var(--radius-full);
  background: var(--color-canvas); border: 1px solid var(--color-hairline);
  color: var(--color-ink); cursor: pointer;
  transition: border-color var(--motion-fast) var(--ease-out), transform var(--motion-fast) var(--ease-out);
}
.btn-icon-circular:hover { border-color: var(--color-muted-soft); transform: scale(1.06); }

/* Inline text link */
.text-link {
  font-size: 16px; color: var(--color-primary); text-decoration: none;
  transition: color var(--motion-fast) var(--ease-out);
}
.text-link:hover { color: var(--color-primary-active); text-decoration: underline; }
```

---

## 3. Hero Band

```html
<section class="hero-band">
  <div class="hero-band__container">
    <div class="hero-band__content">
      <div class="badge-coral">New</div>
      <h1 class="display-xl">Meet your<br>thinking partner</h1>
      <p class="body-md">Claude is an AI assistant built for deep collaboration.</p>
      <div class="hero-band__actions">
        <a href="#" class="btn-primary btn-primary--pulse">Try Claude free</a>
        <a href="#" class="btn-secondary">See pricing</a>
      </div>
    </div>
    <div class="hero-band__illustration">
      <!-- product-mockup-card or hero illustration here -->
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
/* Hero content children animate on page load — see ref/motion.md */
.hero-band__actions { display: flex; gap: var(--space-md); flex-wrap: wrap; }

/* Display helpers */
.display-xl { font-family: var(--font-display); font-size: 64px; font-weight: 400; line-height: 1.05; letter-spacing: -1.5px; color: var(--color-ink); }
.display-lg { font-family: var(--font-display); font-size: 48px; font-weight: 400; line-height: 1.10; letter-spacing: -1px;   color: var(--color-ink); }
.display-md { font-family: var(--font-display); font-size: 36px; font-weight: 400; line-height: 1.15; letter-spacing: -0.5px; color: var(--color-ink); }
.display-sm { font-family: var(--font-display); font-size: 28px; font-weight: 400; line-height: 1.20; letter-spacing: -0.3px; color: var(--color-ink); }
.body-md    { font-family: var(--font-body);    font-size: 16px; font-weight: 400; line-height: 1.55; color: var(--color-body); }

@media (max-width: 768px) {
  .hero-band__container { grid-template-columns: 1fr; }
  .hero-band__illustration { order: 2; }
  .display-xl { font-size: 32px; letter-spacing: -0.5px; }
}
```

---

## 4. Feature Card Grid

```html
<section class="feature-section">
  <div class="section-container">
    <h2 class="display-lg reveal">What Claude can do</h2>
    <div class="feature-grid">
      <article class="feature-card reveal" data-delay="1">
        <div class="feature-card__icon"><!-- SVG --></div>
        <h3 class="feature-card__title">Deep analysis</h3>
        <p class="feature-card__body">Reason through complex documents and surface insights.</p>
      </article>
      <article class="feature-card reveal" data-delay="2">...</article>
      <article class="feature-card reveal" data-delay="3">...</article>
    </div>
  </div>
</section>
```

```css
.feature-section { background: var(--color-canvas); padding: var(--space-section) 0; }
.section-container { max-width: 1200px; margin: 0 auto; padding: 0 var(--space-xl); }
.feature-grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: var(--space-lg); margin-top: var(--space-xxl);
}
.feature-card {
  background: var(--color-surface-card); border-radius: var(--radius-lg);
  padding: var(--space-xl); display: flex; flex-direction: column; gap: var(--space-md);
  transition: transform var(--motion-normal) var(--ease-out);
}
.feature-card:hover { transform: translateY(-3px); }
.feature-card__icon  { width: 40px; height: 40px; color: var(--color-primary); }
.feature-card__title { font-size: 18px; font-weight: 500; line-height: 1.4; color: var(--color-ink); margin: 0; }
.feature-card__body  { font-size: 16px; font-weight: 400; line-height: 1.55; color: var(--color-body); margin: 0; }

@media (max-width: 1024px) { .feature-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px)  { .feature-grid { grid-template-columns: 1fr; } }
```

---

## 5. Code Window Card

```html
<div class="code-window-card reveal">
  <div class="code-window-card__header">
    <div class="code-window-card__dots">
      <span class="dot dot--red"></span>
      <span class="dot dot--yellow"></span>
      <span class="dot dot--green"></span>
    </div>
    <span class="code-window-card__filename">script.py</span>
  </div>
  <pre class="code-block"><code>
<span class="code-keyword">import</span> anthropic
client = anthropic.Anthropic()
message = client.messages.create(
    model=<span class="code-string">"claude-opus-4-5"</span>,
    max_tokens=<span class="code-number">1024</span>,
)
  </code></pre>
</div>
```

```css
.code-window-card { background: var(--color-surface-dark); border-radius: var(--radius-lg); padding: var(--space-lg); overflow: hidden; }
.code-window-card__header {
  display: flex; align-items: center; gap: var(--space-md);
  margin-bottom: var(--space-md); padding-bottom: var(--space-md);
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.code-window-card__dots { display: flex; gap: 6px; }
.dot { width: 12px; height: 12px; border-radius: 50%; }
.dot--red    { background: #ff5f57; }
.dot--yellow { background: #febc2e; }
.dot--green  { background: #28c840; }
.code-window-card__filename { font-family: var(--font-code); font-size: 12px; color: var(--color-on-dark-soft); }
.code-block { background: var(--color-surface-dark-soft); border-radius: var(--radius-sm); padding: var(--space-md); margin: 0; overflow-x: auto; }
.code-block code { font-family: var(--font-code); font-size: 14px; line-height: 1.6; color: var(--color-on-dark); white-space: pre; display: block; }
/* Syntax */
.code-keyword { color: #c792ea; }
.code-string  { color: #c3e88d; }
.code-number  { color: var(--color-accent-amber); }
.code-comment { color: var(--color-on-dark-soft); font-style: italic; }
.code-type    { color: var(--color-accent-teal); }
```

---

## 6. Product Mockup Card (Dark)

```html
<div class="product-mockup-card reveal">
  <div class="badge-coral">Claude API</div>
  <h3 class="display-sm">Build with Claude</h3>
  <p class="product-mockup-card__body">Integrate Claude directly into your product.</p>
  <!-- product chrome / screenshots -->
</div>
```

```css
.product-mockup-card {
  background: var(--color-surface-dark); color: var(--color-on-dark);
  border-radius: var(--radius-lg); padding: var(--space-xl);
  display: flex; flex-direction: column; gap: var(--space-md);
  transition: transform var(--motion-slow) var(--ease-out);
}
.product-mockup-card:hover { transform: translateY(-4px); }
.product-mockup-card .display-sm { color: var(--color-on-dark); }
.product-mockup-card__body { font-size: 16px; line-height: 1.55; color: var(--color-on-dark-soft); }
```

---

## 7. Model Comparison Cards

```html
<div class="model-comparison-grid">
  <div class="model-card reveal" data-delay="1">
    <div class="badge-pill">Most capable</div>
    <h3 class="display-md">Claude Opus</h3>
    <p class="body-md">Best for complex analysis and nuanced reasoning.</p>
    <a href="#" class="text-link">Learn more →</a>
  </div>
  <!-- repeat for Sonnet, Haiku -->
</div>
```

```css
.model-comparison-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-lg); }
.model-card {
  background: var(--color-canvas); border: 1px solid var(--color-hairline);
  border-radius: var(--radius-lg); padding: var(--space-xl);
  display: flex; flex-direction: column; gap: var(--space-md);
  transition: border-color var(--motion-normal) var(--ease-out), transform var(--motion-normal) var(--ease-out), box-shadow var(--motion-normal) var(--ease-out);
}
.model-card:hover { border-color: var(--color-muted-soft); transform: translateY(-3px); box-shadow: 0 4px 16px rgba(20,20,19,0.06); }
@media (max-width: 768px) { .model-comparison-grid { grid-template-columns: 1fr; } }
```

---

## 8. Pricing Tier Cards

```html
<div class="pricing-grid">
  <div class="pricing-card reveal" data-delay="1">
    <h3 class="pricing-card__name">Free</h3>
    <div class="display-sm pricing-card__price">$0<span>/month</span></div>
    <ul class="pricing-card__features">
      <li>✓ Access to Claude</li>
    </ul>
    <a href="#" class="btn-secondary pricing-card__cta">Get started</a>
  </div>
  <!-- Featured tier: add class pricing-card--featured -->
  <div class="pricing-card pricing-card--featured reveal" data-delay="2">
    <div class="badge-coral">Most popular</div>
    <h3 class="pricing-card__name">Pro</h3>
    <div class="display-sm pricing-card__price">$20<span>/month</span></div>
    <ul class="pricing-card__features">
      <li>✓ Higher limits</li>
    </ul>
    <a href="#" class="btn-primary pricing-card__cta">Start free trial</a>
  </div>
</div>
```

```css
.pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: var(--space-lg); align-items: start; }
.pricing-card {
  background: var(--color-canvas); border: 1px solid var(--color-hairline);
  border-radius: var(--radius-lg); padding: var(--space-xl);
  display: flex; flex-direction: column; gap: var(--space-lg);
  transition: transform var(--motion-normal) var(--ease-out), box-shadow var(--motion-normal) var(--ease-out);
}
.pricing-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(20,20,19,0.08); }
/* Featured (dark) */
.pricing-card--featured { background: var(--color-surface-dark); border-color: transparent; color: var(--color-on-dark); }
.pricing-card--featured .pricing-card__name,
.pricing-card--featured .pricing-card__price { color: var(--color-on-dark); }
.pricing-card--featured .pricing-card__features { color: var(--color-on-dark-soft); }

.pricing-card__name { font-size: 22px; font-weight: 500; color: var(--color-ink); }
.pricing-card__price span { font-size: 16px; font-weight: 400; color: var(--color-muted); }
.pricing-card__features { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: var(--space-sm); font-size: 16px; color: var(--color-body); }
.pricing-card__cta { width: 100%; justify-content: center; }
```

---

## 9. Coral Callout Band

```html
<section style="background: var(--color-canvas); padding: var(--space-section) 0;">
  <div class="section-container">
    <div class="cta-band-coral reveal">
      <div class="cta-band__inner">
        <h2 class="display-sm">Start building with Claude today</h2>
        <p class="body-md">Join thousands of teams using Claude's API.</p>
        <div class="cta-band__actions">
          <a href="#" class="btn-secondary">Try Claude free</a>
          <a href="#" style="color: rgba(255,255,255,0.85); font-size:14px; font-weight:500; text-decoration:none;">View docs →</a>
        </div>
      </div>
    </div>
  </div>
</section>
```

```css
.cta-band-coral {
  background: var(--color-primary); border-radius: var(--radius-lg); padding: 64px;
}
.cta-band-coral .display-sm,
.cta-band-coral .body-md { color: var(--color-on-primary); }
.cta-band__inner {
  max-width: 800px; margin: 0 auto;
  display: flex; flex-direction: column; gap: var(--space-lg);
  text-align: center; align-items: center;
}
.cta-band__actions { display: flex; gap: var(--space-md); flex-wrap: wrap; justify-content: center; }

/* Dark variant */
.cta-band-dark { background: var(--color-surface-dark); border-radius: var(--radius-lg); padding: 64px; }
.cta-band-dark .display-sm,
.cta-band-dark .body-md { color: var(--color-on-dark); }

@media (max-width: 768px) {
  .cta-band-coral, .cta-band-dark { padding: var(--space-xxl) var(--space-md); }
}
```

---

## 10. Badges

```css
.badge-pill {
  display: inline-flex; align-items: center;
  background: var(--color-surface-card); color: var(--color-ink);
  font-size: 13px; font-weight: 500; line-height: 1.4;
  border-radius: var(--radius-pill); padding: 4px 12px;
}
.badge-coral {
  display: inline-flex; align-items: center;
  background: var(--color-primary); color: var(--color-on-primary);
  font-size: 12px; font-weight: 500; line-height: 1.4;
  letter-spacing: 1.5px; text-transform: uppercase;
  border-radius: var(--radius-pill); padding: 4px 12px;
}
```

---

## 11. Text Input

```css
.text-input {
  background: var(--color-canvas); color: var(--color-ink);
  font-size: 16px; font-weight: 400; line-height: 1.55;
  padding: 10px 14px; height: 40px;
  border-radius: var(--radius-md); border: 1px solid var(--color-hairline);
  width: 100%; outline: none;
  transition: border-color var(--motion-fast) var(--ease-out), box-shadow var(--motion-fast) var(--ease-out);
}
.text-input:hover { border-color: var(--color-muted-soft); }
.text-input:focus { border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(204,120,92,0.15); }
```

---

## 12. Category Tabs

```html
<div class="tab-bar" role="tablist">
  <button class="category-tab" role="tab">All</button>
  <button class="category-tab category-tab--active" role="tab" aria-selected="true">APIs</button>
</div>
```

```css
.tab-bar { display: flex; gap: var(--space-xs); flex-wrap: wrap; }
.category-tab {
  background: transparent; color: var(--color-muted);
  font-size: 14px; font-weight: 500; padding: 8px 14px;
  border-radius: var(--radius-md); border: none; cursor: pointer;
  transition: background var(--motion-fast) var(--ease-out), color var(--motion-fast) var(--ease-out);
}
.category-tab:hover { background: var(--color-surface-soft); color: var(--color-ink); }
.category-tab--active { background: var(--color-surface-card); color: var(--color-ink); }
```

---

## 13. Footer

```html
<footer class="footer">
  <div class="footer__container">
    <div class="footer__brand">
      <svg><!-- spike mark --></svg>
      <span>Anthropic</span>
    </div>
    <div class="footer__columns">
      <div>
        <h4 class="footer__heading">Product</h4>
        <a href="#">Claude</a>
        <a href="#">API</a>
      </div>
      <!-- more columns -->
    </div>
  </div>
</footer>
```

```css
.footer { background: var(--color-surface-dark); color: var(--color-on-dark-soft); padding: 64px 0; }
.footer__container { max-width: 1200px; margin: 0 auto; padding: 0 var(--space-xl); display: flex; flex-direction: column; gap: var(--space-xxl); }
.footer__brand { display: flex; align-items: center; gap: var(--space-xs); font-size: 16px; font-weight: 600; color: var(--color-on-dark); }
.footer__columns { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-xxl); }
.footer__heading { font-size: 12px; font-weight: 500; color: var(--color-on-dark); text-transform: uppercase; letter-spacing: 1.5px; margin: 0 0 var(--space-md); }
.footer a { font-size: 14px; color: var(--color-on-dark-soft); text-decoration: none; line-height: 2; display: block; transition: color var(--motion-fast) var(--ease-out); }
.footer a:hover { color: var(--color-on-dark); }
@media (max-width: 768px) { .footer__columns { grid-template-columns: 1fr 1fr; } }
```
