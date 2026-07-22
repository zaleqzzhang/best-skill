# Motion Reference

All animation patterns for the WeChat design system. Motion is **fast, functional, and native-app-like** — quick settle, tactile press feedback, no editorial slowness.

---

## Motion Tokens (include in `:root`)

```css
:root {
  --motion-instant: 80ms;
  --motion-fast:   160ms;
  --motion-normal: 220ms;
  --motion-slow:   280ms;
  --motion-lazy:   360ms;
  --ease-standard: cubic-bezier(0.25, 0.1, 0.25, 1);   /* primary — native settle */
  --ease-spring:   cubic-bezier(0.34, 1.56, 0.64, 1);  /* decorative accents ONLY */

  --reveal-distance: 12px;
  --reveal-duration: var(--motion-slow);
  --reveal-ease:     var(--ease-standard);
  --reveal-stagger:  50ms;
}
```

---

## Scroll Reveal

Shorter travel and faster settle than editorial systems — WeChat motion is subtle, almost invisible, never a "wow" moment.

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

**Stagger rule:** Assign `data-delay="1"`, `"2"`, `"3"` sequentially across a grid row. Reset to `"1"` on the next row. Because `--reveal-stagger` is only 50ms, a 4-item row completes in ~200ms — feels instant, not choreographed.

---

## Tactile Press Feedback (core WeChat motion signature)

Every interactive element gives **immediate physical feedback** on press — this mimics native iOS/Android touch response and is the single most distinctive motion trait of the WeChat system (absent from most editorial/marketing sites).

```css
.btn-primary,
.btn-secondary,
.btn-icon-circular,
.category-card,
.theme-toggle-btn {
  transition: transform var(--motion-instant) var(--ease-standard), /* + other props */;
}
.btn-primary:active,
.btn-secondary:active,
.category-card:active {
  transform: scale(0.96);
}
.btn-icon-circular:active,
.theme-toggle-btn:active {
  transform: scale(0.92); /* smaller elements compress more, proportionally */
}
```

**Rule:** Any `<button>`, `<a class="btn-*">`, or tappable card MUST have an `:active` scale-down rule. Duration is always `--motion-instant` (80ms) — feedback must feel immediate, never eased-in slowly.

---

## Squircle Icon Hover (spring accent)

The one place a spring easing is allowed — icon chips inside feature/category cards pop slightly on card hover, echoing WeChat's playful app-icon bounce.

```css
.icon-chip {
  transition: transform var(--motion-fast) var(--ease-spring);
}
.feature-card:hover .icon-chip,
.category-card:hover .icon-chip {
  transform: scale(1.06);
}
```

Never apply `--ease-spring` to page-level reveals, band transitions, or anything larger than an icon — it reads as unserious at scale.

---

## Page Load Entry Sequence

Hero content enters on DOMContentLoaded — no scroll required. Below-fold uses scroll reveal. Faster and shorter than editorial equivalents.

**CSS:**

```css
@keyframes enter-up {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

.hero-band__content > * {
  animation: enter-up var(--motion-slow) var(--ease-standard) both;
}
.hero-band__content > *:nth-child(1) { animation-delay:  40ms; }
.hero-band__content > *:nth-child(2) { animation-delay: 100ms; }
.hero-band__content > *:nth-child(3) { animation-delay: 160ms; }
.hero-band__content > *:nth-child(4) { animation-delay: 220ms; }

.hero-band__illustration {
  animation: enter-up var(--motion-lazy) var(--ease-standard) both;
  animation-delay: 120ms;
}
```

Order: tag/badge → h1 → subtitle → CTA buttons. Illustration enters concurrently with subtitle. Total sequence completes under 500ms (editorial systems often run past 800ms) — WeChat pages feel "already there" rather than "arriving."

---

## Notification Dot Pulse

Reserved for the red notification/unread indicator only — communicates "something needs attention" without being a marketing flourish.

```css
@keyframes notif-pulse {
  0%   { box-shadow: 0 0 0 0   rgba(250, 81, 81, 0.35); }
  70%  { box-shadow: 0 0 0 6px rgba(250, 81, 81, 0); }
  100% { box-shadow: 0 0 0 0   rgba(250, 81, 81, 0); }
}
.badge-dot--pulse::after {
  animation: notif-pulse 1.8s var(--ease-standard) infinite;
}
```

Use sparingly — at most one pulsing indicator visible at a time.

---

## Search Bar Focus Expand

```css
.search-bar {
  transition: border-color var(--motion-fast) var(--ease-standard),
              background var(--motion-fast) var(--ease-standard),
              box-shadow var(--motion-fast) var(--ease-standard);
}
.search-bar:focus-within {
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
```

---

## Nav Scroll Shadow

```javascript
const nav  = document.querySelector('.top-nav');
const html = document.documentElement;
window.addEventListener('scroll', () => {
  const isDark = html.getAttribute('data-theme') === 'dark';
  nav.style.boxShadow = window.scrollY > 8
    ? (isDark ? '0 1px 12px rgba(0,0,0,0.5)' : '0 1px 8px rgba(0,0,0,0.06)')
    : '';
}, { passive: true });
```

Note the lower scroll threshold (8px vs 10px+ in editorial systems) and tighter shadow spread — WeChat's chrome reacts a beat faster.

---

## Hover Rules Summary

| Element | Light theme hover | Dark theme hover |
|---|---|---|
| `.btn-primary` | `background` darkens (no scale on hover, only on `:active`) | same |
| `.btn-secondary` | `border-color` darkens | `border-color`/bg lightens |
| `.btn-icon-circular` | `background` fills to `--color-surface-strong` | same, dark equivalent |
| `.feature-card` / `.category-card` | `translateY(-2px)` + bg darken one step, icon-chip springs to `scale(1.06)` | same |
| `.news-card` | `translateY(-3px)` + soft shadow | same, deeper shadow |
| `.nav-link` | color darken + subtle bg fill | same |
| `.text-link` | color → `--color-link-active` + underline | lighter blue + underline |

**Key distinction from editorial motion systems:** hover states here are secondary — the primary feedback signal is the `:active` press-scale, because WeChat's design language originates from touch-first mobile products. Always implement `:active` before polishing `:hover`.

---

## Product Card Hover (three-element choreography)

The signature hover pattern for `.product-card` (the white square product-entry grid used on `weixin.qq.com` and similar product-matrix pages). **Three visual changes fire simultaneously** in one motion event:

| Element | Property | Resting | Hover | Duration | Easing |
|---|---|---|---|---|---|
| **Card** | `transform` | `translateY(0)` | `translateY(-4px)` | `--motion-slow` (280ms) | `--ease-standard` |
| **Card** | `box-shadow` | `0 0 0 transparent` (none) | `0 2px 4px / 0 8px 16px / 0 16px 32px` layered | `--motion-slow` (280ms) | `--ease-standard` |
| **Icon** | `transform` | `scale(1)` | `scale(1.10)` | `--motion-fast` (160ms) | `--ease-spring` |
| **Card (press)** | `transform` | `scale(1)` | `scale(0.96)` on `:active` | `--motion-instant` (80ms) | `--ease-standard` |
| **Icon (press)** | `transform` | `scale(1)` | `scale(0.94)` on `:active` | `--motion-instant` (80ms) | `--ease-standard` |

**Why this choreography works:**

1. **Shadow lives in hover state, not resting state** — the gray page floor (`--color-surface-soft`) provides card separation at rest, so the card appears flat and content-forward. Shadow only emerges on hover, which means the hover feels like a *lift toward the user* rather than a *shift in elevation*. This is the opposite of card-with-resting-shadow patterns (Material elevation 1, Bootstrap cards) and is the WeChat design distinction.

2. **Multi-layer shadow = soft, not crisp** — three shadows stacked (4px close + 16px medium + 32px far) at low opacities (0.04–0.06) produce a diffuse halo rather than a hard drop. This reads as "the card is gently floating" not "the card has a sticker edge."

3. **Icon spring is the personality** — the icon uses `--ease-spring` (the ONLY place springs are allowed in this component) with `scale(1.10)`, slightly larger than the feature-card's `scale(1.06)`. The spring overshoot of 1.10→1.0 gives the icon a tiny playful bounce that matches WeChat's "high-spirited product identity" — but is contained to the 40px icon, never the whole card.

4. **Card and icon use different durations** — the card moves on 280ms (slow, "weighty") while the icon moves on 160ms (fast, "snappy"). This produces a small perceived offset where the icon "leads" the card by ~120ms, making the whole interaction feel responsive without being jerky. Both reach their end states within 280ms (the longer of the two) so they appear synchronized at rest.

5. **Press feedback compresses both** — on `:active`, the card shrinks to `scale(0.96)` AND the icon to `scale(0.94)` simultaneously on an 80ms instant transition. The icon compresses proportionally more because it's a smaller visual element. This satisfies the "tactile press feedback" rule that all interactive WeChat elements must have.

**CSS:**

```css
.product-card {
  transition:
    transform    var(--motion-slow) var(--ease-standard),
    box-shadow   var(--motion-slow) var(--ease-standard);
  box-shadow: 0 0 0 rgba(0, 0, 0, 0);
  will-change: transform, box-shadow;
}
.product-card:hover {
  transform: translateY(-4px);
  box-shadow:
    0 2px 4px  rgba(0, 0, 0, 0.04),
    0 8px 16px rgba(0, 0, 0, 0.06),
    0 16px 32px rgba(0, 0, 0, 0.04);
}
.product-card:active {
  transform: scale(0.96);
  transition: transform var(--motion-instant) var(--ease-standard);
}

.product-card__icon {
  transition: transform var(--motion-fast) var(--ease-spring);
}
.product-card:hover  .product-card__icon { transform: scale(1.10); }
.product-card:active .product-card__icon { transform: scale(0.94); }
```

**Dark-mode shadow rule:** the same translateY(-4px) lift, but shadows shift from black at 0.04–0.06 to black at 0.3–0.4 (much stronger) because on a `#191919` floor, low-opacity black shadows are nearly invisible. The card background also shifts one step up (`--color-surface-card` → `--color-surface-strong`) to maintain the perception of lift.

**Anti-pattern — never do this on product cards:**

```css
/* ❌ WRONG — shadow resting + shadow hover double-animates,
   and box-shadow animation is the most expensive property to animate.
   Use transform + box-shadow together, but keep box-shadow as 0 at rest. */
.product-card { box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.product-card:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.12); transform: translateY(-2px); }

/* ❌ WRONG — single-layer shadow, hard edge, looks like a 2010s bootstrap card */
.product-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.15); transform: translateY(-4px); }

/* ❌ WRONG — spring on the whole card reads as unserious, bouncy, non-native */
.product-card:hover { transform: scale(1.05); transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
```

**Component reference:** HTML + full responsive + dark-mode CSS → `references/components.md` → §15 Product Entry Grid Card.
