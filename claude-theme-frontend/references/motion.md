# Motion Reference

All animation patterns for the Claude design system. Motion is **warm and editorial** — confident settle-in, no bounce, no spring.

---

## Motion Tokens (include in `:root`)

```css
:root {
  --motion-instant: 80ms;
  --motion-fast:   160ms;
  --motion-normal: 240ms;
  --motion-slow:   360ms;
  --motion-lazy:   500ms;
  --ease-out:     cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out:  cubic-bezier(0.4, 0, 0.2, 1);

  --reveal-distance: 20px;
  --reveal-duration: var(--motion-slow);
  --reveal-ease:     var(--ease-out);
  --reveal-stagger:  70ms;
}
```

---

## Scroll Reveal

**CSS:**

```css
.reveal {
  opacity: 0;
  transform: translateY(var(--reveal-distance));
  transition:
    opacity var(--reveal-duration) var(--reveal-ease),
    transform var(--reveal-duration) var(--reveal-ease);
}
.reveal.is-visible { opacity: 1; transform: translateY(0); }

/* Stagger delays — assign data-delay="1"…"6" to grid items */
.reveal[data-delay="1"] { transition-delay: calc(var(--reveal-stagger) * 1); }
.reveal[data-delay="2"] { transition-delay: calc(var(--reveal-stagger) * 2); }
.reveal[data-delay="3"] { transition-delay: calc(var(--reveal-stagger) * 3); }
.reveal[data-delay="4"] { transition-delay: calc(var(--reveal-stagger) * 4); }
.reveal[data-delay="5"] { transition-delay: calc(var(--reveal-stagger) * 5); }
.reveal[data-delay="6"] { transition-delay: calc(var(--reveal-stagger) * 6); }

/* Dark cards feel heavier — override per-card */
.product-mockup-card.reveal,
.code-window-card.reveal,
.pricing-card--featured.reveal {
  --reveal-distance: 28px;
  --reveal-duration: var(--motion-lazy);
}
```

**JS (add before `</body>`):**

```javascript
const observer = new IntersectionObserver(
  (entries) => entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add('is-visible'); observer.unobserve(e.target); }
  }),
  { threshold: 0.15 }
);
document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
```

**Stagger rule:** Assign `data-delay="1"`, `"2"`, `"3"` sequentially across a grid row. Reset to `"1"` on the next row.

---

## Page Load Entry Sequence

Hero content enters on DOMContentLoaded — no scroll required. Below-fold uses scroll reveal.

**CSS:**

```css
@keyframes enter-up {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Hero content children */
.hero-band__content > * {
  animation: enter-up var(--motion-slow) var(--ease-out) both;
}
.hero-band__content > *:nth-child(1) { animation-delay:  60ms; }
.hero-band__content > *:nth-child(2) { animation-delay: 140ms; }
.hero-band__content > *:nth-child(3) { animation-delay: 220ms; }
.hero-band__content > *:nth-child(4) { animation-delay: 300ms; }

/* Hero illustration — deeper travel */
.hero-band__illustration {
  animation: enter-up var(--motion-lazy) var(--ease-out) both;
  animation-delay: 180ms;
}
```

Order: badge → h1 → subtitle → CTA buttons. Illustration enters concurrently with subtitle.

---

## Coral CTA Pulse

Use at most once per page — hero CTA button only.

```css
@keyframes coral-pulse {
  0%   { box-shadow: 0 0 0 0   rgba(204, 120, 92, 0.35); }
  70%  { box-shadow: 0 0 0 10px rgba(204, 120, 92, 0); }
  100% { box-shadow: 0 0 0 0   rgba(204, 120, 92, 0); }
}

.btn-primary--pulse {
  animation: coral-pulse 2.5s ease-out infinite;
  animation-delay: 2s; /* start after page settles */
}
```

Add class `btn-primary--pulse` to the single hero CTA only.

---

## Code Window Typewriter

For developer-focused hero sections. Replaces pre-rendered code text with a character-by-character reveal.

```javascript
function typewriterEffect(codeElement, options = {}) {
  const { speed = 18, startDelay = 600 } = options;
  const fullText = codeElement.textContent;
  codeElement.textContent = '';
  codeElement.style.opacity = '1';

  let i = 0;
  const timer = setTimeout(() => {
    const interval = setInterval(() => {
      codeElement.textContent += fullText[i];
      i++;
      if (i >= fullText.length) clearInterval(interval);
    }, speed);
  }, startDelay);

  return () => clearTimeout(timer); // call to cancel
}

// Usage:
// typewriterEffect(document.querySelector('.code-block code'));
```

Note: This overwrites `textContent` — syntax highlight `<span>` tags will be lost. Use only on plain-text code blocks, or run typewriter on a hidden copy and swap.

---

## Nav Scroll Shadow

```javascript
const nav  = document.querySelector('.top-nav');
const html = document.documentElement;
window.addEventListener('scroll', () => {
  const isDark = html.getAttribute('data-theme') === 'dark';
  nav.style.boxShadow = window.scrollY > 10
    ? (isDark ? '0 1px 16px rgba(0,0,0,0.40)' : '0 1px 12px rgba(20,20,19,0.07)')
    : '';
}, { passive: true });
```

---

## Hover Rules Summary

| Element | Light theme hover | Dark theme hover |
|---|---|---|
| `.btn-primary` | `background` darkens + `scale(1.02)` | same |
| `.btn-secondary` | `border-color` darkens + `scale(1.02)` | `border-color` lightens + `scale(1.02)` |
| `.btn-icon-circular` | `border-color` darkens + `scale(1.06)` | same with lighter border |
| `.feature-card` | `translateY(-3px)` | `translateY(-3px)` + darker bg |
| `.model-card` | `translateY(-3px)` + hairline border + soft shadow | `translateY(-3px)` + rgba border |
| `.pricing-card` | `translateY(-4px)` + shadow | `translateY(-4px)` + deeper shadow |
| `.product-mockup-card` | `translateY(-4px)` only | `translateY(-4px)` only |
| `.text-link` | color → `--color-primary-active` + underline | color → `#e8967a` + underline |

**Dark cards never use `scale()` — only `translateY`. This applies in both light and dark themes.**
