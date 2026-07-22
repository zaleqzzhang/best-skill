---
name: wechat-theme-frontend
description: 'This skill should be used when building frontend UI in the WeChat (微信) design style — landing pages, hero sections, safety-center feature grids, help-center category cards, newsroom article lists/detail pages, download/QR bands, or any page needing pure white/true-black theming, WeChat-green CTAs, rounded sans-serif typography, and matching functional motion. Covers light/dark mode via data-theme, and Chinese (zh-CN, primary) / English pages. When the request mentions "km" (km文章/km排版/km风格), constrain content to a narrower reading column (768px, or 1024px if "宽屏" is specified) while keeping all other styling unchanged.'
---

# WeChat Theme Frontend Skill

Build polished, on-brand frontend components following the WeChat (微信) official design language — covering design tokens, component patterns, motion, and page structure. Reference sources: wechat.com, newsroom.wechat.com, safety.wechat.com, cs.help.wechat.com.

**Detailed references live in `references/` — load only what the task needs. Do not duplicate their content here; this file holds only the always-on rules and a quick-lookup summary.**

| File | Contents |
|---|---|
| `references/tokens.md` | Authoritative `:root` token block, dark-theme overrides + theme switcher JS, typography classes, Chinese typography classes, font stack (no web-font import needed) |
| `references/components.md` | HTML + CSS for all 15 components (nav, buttons, icon feature grid, product entry grid card, news card, help category card, search bar, etc.) |
| `references/motion.md` | Scroll reveal, tactile press feedback, icon squircle hover, **product card three-element hover choreography** (card lift + multi-layer shadow + icon spring), notification pulse, nav scroll shadow |
| `references/brand-guidelines.md` | 微信官方品牌规范（来源 wechat.design）— 标志类型与背景色规则、最小尺寸与安全区域、错误使用禁忌、标准色板 5 色、官方字体（汉仪旗黑体/Myriad Pro）与 Web 系统等价物映射 |
| `references/layout.md` | Band pacing rules, section container, responsive breakpoints, KM article container (768px/1024px, opt-in) — points to `assets/scaffold-en.html` / `assets/scaffold-zh.html` for the full page skeleton |
| `assets/scaffold-en.html` | Ready-to-copy English page scaffold (head, nav, 5 bands, theme + reveal JS) |
| `assets/scaffold-zh.html` | Ready-to-copy Chinese (`lang="zh-CN"`) page scaffold — Chinese is the primary/default language for this theme |
| `assets/images/catalog.md` | WeChat 品牌配图目录（**仅作兜底资源**）— 2 个主题（`splash/` 启动页、`wechat/` 微信品牌），每主题 4 种比例（16:9、2.35:1、3:2、4:3）。默认优先用在线工具搜索/生成与内容匹配的真实配图；仅当在线搜索无合适结果、或需要 WeChat 品牌专用占位图时，才从这里挑选。 |

---

## Core Principles (always active)

**品牌理念 — 谨慎、优雅、超前：**
- **谨慎** — 全页仅一个主色绿（`#07c160`），动效微小（12px 位移），不滥用装饰性元素
- **优雅** — 系统无衬线字体 + 慷慨圆角（pill 按钮、squircle 图标），硬切分段而非渐变过渡
- **超前** — 真黑 `#191919` 暗色底（非过时深灰/藏青），`data-theme` 原生暗色模式
- 完整官方品牌规范（标志使用、色板、字体、禁忌）→ `references/brand-guidelines.md`

**Brand identity — non-negotiable:**
- Default canvas is pure white `#ffffff` in light mode; dark mode uses true dark `#191919` as page floor — **colder and cleaner** than warm-cream design systems, never off-white/cream
- WeChat Green `#07c160` is the sole primary accent in **both themes**: CTA buttons, active states, brand marks. Scarce and functional — never decorative
- Classic link blue `#576b95` is used for inline text links (mirrors the color used in 公众号/朋友圈 article links) — a **second, distinct accent** from the CTA green, never interchangeable with it
- Red `#fa5151` is reserved **exclusively** for notification dots, unread badges, and error/destructive states — never used decoratively
- **No display serif, no decorative web font.** Headlines and body both use the same unified sans-serif system stack (`--font-body`) — hierarchy comes from `font-weight` (600 for headings) and tight positive-tracking, not from a special typeface. This requires **zero Google Fonts import**
- Text is near-pure black `#1a1a1a` (post-2023 WeChat rebrand moved from dark-gray to true black) for headlines/primary text in light mode
- Roundness is expressed through **generous border-radius** (pill buttons, squircle icon chips) and the WeChat app-icon squircle language — not through font shape
- Dark true-black `#191919` surfaces carry footers and dark-mode page floors — flatter and colder than a "navy" dark theme

**Theme system — `data-theme` attribute:**
- Light mode (default): omit `data-theme` or set `data-theme="light"` — pure white canvas `#ffffff`
- Dark mode: add `data-theme="dark"` to `<html>` — true dark canvas `#191919` (WeChat's official 深色模式 is genuinely near-black, not navy)
- Respect `prefers-color-scheme: dark` on first visit; persist choice in `localStorage`
- All surface and text tokens are overridden via `[data-theme="dark"]` CSS block — see `references/tokens.md`
- Theme toggle button (`data-theme-toggle`) goes in the top nav actions area

**Surface pacing — functional, not editorial:**

*Light mode:*
1. White canvas `#ffffff` — hero, help-center search, article body
2. Light-gray surface `#f7f7f7` — section alternation, category card backgrounds
3. Green CTA band `#07c160` — download / conversion moments (used sparingly, at most once or twice per page)
4. Dark footer `#191919` — always the final band

*Dark mode (same structure, inverted floors):*
1. True dark canvas `#191919` — hero, article body
2. Dark elevated `#232323` — card backgrounds
3. Green CTA band (unchanged — green reads well on black)
4. Footer merges with page floor — add a 1px top hairline to separate

**Unlike editorial design systems, WeChat rarely alternates into a full dark band mid-page.** Dark is reserved for: (a) the whole page in dark mode, (b) the footer, (c) product/app mockup chrome. Keep marketing bands in white ⇄ light-gray rhythm, punctuated by the green CTA band.

**Band edges are hard cuts** — no gradient dividers. Each section carries its own `background` + `padding: var(--space-section) 0` (80px — more compact than editorial systems, reflecting WeChat's dense, functional layout).

**Horizontal scroll strips never show a raw scrollbar — and they never appear on PC at all.** Nav-link rows and tab bars follow a two-mode strategy: **desktop (≥1025px) uses `flex-wrap: wrap`** so extra items flow to a second line naturally (no scrollbar, no scroll affordance needed); **mobile/tablet (≤1024px) uses single-line horizontal scroll with the `.scroll-fade-x` mask** (hides native scrollbar, fades edges). For ad-hoc always-scrollable strips (chip filters, story reels), the standalone `.scroll-fade-x` utility is appropriate at every breakpoint. See `references/layout.md` → "Horizontal Scroll Containers".



**Motion is fast, snappy, and functional — not editorial:**
- `ease-standard: cubic-bezier(0.25, 0.1, 0.25, 1)` — all reveals and transitions (native-app settle, not a slow cinematic ease)
- Reveal travel is short: translate up **12px** (not 20px+) + fade — WeChat motion is subtle, almost imperceptible
- Stagger: 50ms per item in grids (tighter than editorial systems)
- Buttons/icons give **immediate tactile feedback**: `scale(0.96)` on `:active`, under 100ms — mimics native touch feedback
- A soft spring (`cubic-bezier(0.34, 1.56, 0.64, 1)`) is permitted **only** for small decorative accents (notification-dot pulse, chat-bubble pop-in) — never for page-level reveals

---

## Design Tokens (quick reference)

Full `:root` block and dark-theme overrides live in `references/tokens.md` — copy from there, do not retype. Most-used tokens for quick lookup:

| Token | Value | Use |
|---|---|---|
| `--color-primary` | `#07c160` | WeChat green — CTA, brand, sole primary accent |
| `--color-link` | `#576b95` | Inline text links (classic WeChat article link blue) |
| `--color-accent-red` | `#fa5151` | Notification dots, error states — scarce, functional only |
| `--color-canvas` | `#ffffff` (light) / `#191919` (dark) | Page floor |
| `--color-ink` | `#1a1a1a` (light) / `#ffffff` (dark) | Headlines, primary text — true black, not warm-gray |
| `--color-surface-dark` | `#191919` | Footer, dark-mode floor (both themes) |
| `--font-body` | Unified system sans-serif stack, PingFang SC-first | All text, headings and body — no web font needed |
| `--ease-standard` | `cubic-bezier(0.25, 0.1, 0.25, 1)` | All transitions/reveals |
| `--space-section` | `80px` | Vertical padding between page bands (denser than editorial 96px) |
| `--radius-pill` | `9999px` | CTA buttons — pill shape is the default button shape |

**Typography scale** (all headings use `--font-body`, weight 600 — no separate display font):

| Class | Size | Line-h | Tracking | Use |
|---|---|---|---|---|
| `display-xl` | 52px | 1.20 | -0.02em | Hero h1 |
| `display-lg` | 40px | 1.25 | -0.01em | Section h2 |
| `display-md` | 32px | 1.30 | 0 | Sub-heads |
| `display-sm` | 24px | 1.35 | 0 | Card/CTA heads |
| `title-lg` | 20px/600 | 1.40 | 0 | Category titles |
| `title-md` | 17px/600 | 1.45 | 0 | Card titles |
| `body-md` | 15px/400 | 1.60 | 0 | Body text |
| `body-sm` | 13px/400 | 1.60 | 0 | Meta, footer |
| `caption-uppercase` | 12px/500 | 1.40 | 0.05em | Tags, badges |

---

## Fonts — no web-font import required

WeChat's identity is **100% system sans-serif**. There is no separate display typeface — headline character comes from `font-weight: 600` + slightly tight positive tracking, and the perceived "roundness" of the 2023 rebrand comes from generous `border-radius` and the squircle icon language, **not from font shape**. This means:

- No Google Fonts `<link>`, no `@font-face` — the page loads instantly with zero font-CDN dependency
- `--font-body` resolves natively per OS: PingFang SC (macOS/iOS), Microsoft Yahei (Windows), with `-apple-system`/`Segoe UI` covering Latin text
- Full stack lives in `references/tokens.md`

---

## Chinese Page Support (Chinese is the PRIMARY language of this theme)

Unlike Latin-first design systems, WeChat's own site (`wechat.com/zh_CN`) treats **Chinese as the default, not a fallback**. Build Chinese (`lang="zh-CN"`) pages first; treat English as the secondary/translated variant.

**Chinese typography adjustments (apply via `:lang(zh-CN)`):**

| Rule | Latin default | Chinese override | Why |
|---|---|---|---|
| Body line-height | 1.60 | **1.75** | CJK glyphs need more vertical air |
| Body font-size | 15px | **15px** (unchanged — WeChat UI text stays compact even in Chinese) | Functional density is intentional; do not inflate size |
| `caption-uppercase` | uppercase, 0.05em | no uppercase, `0.02em` | Chinese has no case; near-zero tracking looks native |
| Word-break | default | `word-break: break-all` | Prevents CJK overflow |

Full CSS + mobile overrides → `references/tokens.md` (Chinese Typography Classes section).

---

## KM Format (opt-in — only when explicitly requested)

**Trigger condition:** apply this section ONLY when the user's request explicitly mentions "km文章" (or equivalent: "km排版", "发km", "km格式", "km主题"). Do NOT apply the width constraint by default — the standard container width remains 1200px (see `references/layout.md`).

**KM Format is WeChat theme with exactly one difference: a narrower content column.** Every other design decision — colors, typography, spacing scale, radius, motion, band pacing, dark mode, components — stays byte-for-byte identical to the standard WeChat theme.

| KM variant | Trigger phrase | Max content width |
|---|---|---|
| Standard | "km文章" / "km排版" / "发km" (default when width not specified) | **768px** |
| Wide-screen | "km文章宽屏" / "km宽屏主题" / "wide" explicitly mentioned | **1024px** |

**The width limit applies to the full content column — not just text.** Every element inside the article body must fit within the constrained width, including tables, charts, images, flowcharts, code blocks, and embedded diagrams.

Full `.km-article-container` CSS → `references/layout.md` (KM Article Container section).

---

## Do's and Don'ts

| ✅ Do | ❌ Don't |
|---|---|
| Pure white `#ffffff` as light-mode floor | Warm cream / off-white canvas |
| True dark `#191919` as dark-mode floor | Navy-tinted or warm-brown dark floor |
| WeChat green `#07c160` for CTAs in **both themes** | Use green for inline text links (that's `--color-link` blue) |
| Reserve red `#fa5151` strictly for badges/errors | Use red decoratively or as a second CTA color |
| Pure system sans-serif, weight 600 for headings | Import a decorative/serif Google Font for headlines |
| Pill buttons (`--radius-pill`) as the default CTA shape | Sharp-cornered buttons |
| `data-theme="dark"` on `<html>` for dark mode | Separate CSS file or class toggle for theming |
| White ⇄ light-gray band rhythm, green CTA as punctuation | Alternating full dark bands mid-page (reserve dark for footer/app-mockups only) |
| Short reveal travel (12px) + fast duration (~280ms) | 20px+ travel or 500ms+ "editorial" reveal timing |
| `scale(0.96)` tactile press feedback on buttons/icons | No active-state feedback (feels unresponsive) |
| 50ms stagger per card in grids | 200ms+ stagger |
| Squircle icon chips (`border-radius: 20px` on square box) with green-tint background | Circular icon badges with no background tint |
| Hard-cut band edges with padding | Gradient divider `<div>` elements between bands |
| `flex-wrap: wrap` on PC + `.scroll-fade-x` on mobile for nav links/tab bars | `overflow-x: auto` on PC (no useful scroll affordance) OR a bare `overflow-x: auto` that exposes a raw browser scrollbar |
| Logo SVG 用 `fill: #07c160` 固定色，暗色模式转 `currentColor`/白 | 给 logo 加 `drop-shadow`、`hue-rotate`、渐变或任何特效（官方严禁） |
| 导航栏 logo ≥ 22px，独立展示 ≥ 48px | logo 小于 16px（官方最小屏幕尺寸 24px） |
| 产品卡 hover：translateY(-4px) + 多层柔和阴影（0 2px / 0 8px / 0 16px 三层） + icon `scale(1.10)` 弹簧（160ms） | 单一硬阴影（如 `0 4px 12px rgba(0,0,0,0.15)`）— 看起来像过时的 Bootstrap 卡片 |
| 产品卡静止态无阴影，靠灰底分离 | 始终有静态阴影 — 弱化了 hover 的"浮起"感知 |
| 产品卡 icon 用 `color: currentColor` + 内联 `style="color:#xxx"` 注入品牌色 | 用 filter 改色、给 SVG 加渐变填充（违反官方品牌规范） |
| 卡片用 280ms 标准缓动做位移，icon 用 160ms 弹簧缓动做缩放（节奏错开 ~120ms） | 整张卡用弹簧 — 显得轻浮、脱离 native-app 节奏 |

---

*For full component markup + CSS → read `references/components.md`*
*For motion patterns + JS → read `references/motion.md`*
*For band pacing + breakpoints → read `references/layout.md`*
*For the full page skeleton → copy `assets/scaffold-en.html` or `assets/scaffold-zh.html`*
*For dark theme token overrides + theme switcher → read `references/tokens.md`*
*For official brand guidelines (logo, colors, fonts, usage rules) → read `references/brand-guidelines.md`*
*For fallback brand placeholder images (2 themes × 4 aspect ratios) — only when online image search finds nothing suitable → read `assets/images/catalog.md`*

---

## Image Strategy (配图策略)

构建 WeChat 主题页面需要配图时，**默认优先使用在线工具搜索/生成与页面内容语义匹配的真实配图**（产品截图、场景照片、插画等），而非一开始就用占位图。仅当在线搜索找不到合适图片、或场景本身就需要 WeChat 品牌专用占位图（如启动页 / 品牌标识演示）时，才回退到本 skill 自带的 `assets/images/` 素材。

**配图获取优先级（从高到低）：**

1. **在线搜索/生成优先** — 用可用的图片工具（如web 图片搜索、网络检索、`image_gen`）按页面文案关键词检索/生成真实配图。优先选择与内容语义贴合、风格干净、比例适配容器的图片；下载或生成后写入页面相对路径引用。
2. **自带品牌素材兜底** — 仅当在线搜索无合适结果、或场景本身就需要 WeChat 品牌占位图时，再从 `assets/images/` 选。

**兜底素材（仅当在线搜索无合适结果时）：**
- `splash/` — 手机 + 太空/地球壁纸，象征"首次启动 / 连接世界"（4 种比例）
- `wechat/` — 绿色背景 + 微信 logo + 人物剪影，品牌核心标识（4 种比例）

**兜底快速选择规则（使用自带素材时）：**
- **Hero 大插图**（`.hero-band__illustration`，4:3 容器）→ `4-3.jpg`
- **新闻/产品卡片**（`.news-card__image`，16:9 容器）→ `16-9.jpg`
- **超宽 banner**（页面顶部强调条、`.cta-band` 顶部）→ `2.35-1.jpg`
- **自由版面/轮播**（无 aspect-ratio 约束）→ `3-2.jpg`

**兜底主题映射：**
- 启动/连接/首次体验 → `splash/`
- 品牌/核心标识 → `wechat/`

**使用方式（自带素材兜底时）：**
```html
<!-- Hero 插图（4:3 容器） -->
<div class="hero-band__illustration">
  <img src="assets/images/wechat/4-3.jpg" alt="" loading="lazy"
       style="width:100%;height:100%;object-fit:cover;border-radius:var(--radius-xl);">
</div>

<!-- 新闻卡（16:9 容器） -->
<div class="news-card__image">
  <img src="assets/images/splash/16-9.jpg" alt="" loading="lazy"
       style="width:100%;height:100%;object-fit:cover;">
</div>
```

> **必须用 `object-fit: cover`**：无论在线配图还是自带素材，图源比例与容器比例仍可能有小数偏差，需用 cover 裁切而非拉伸。完整兜底选图指南、比例映射、场景决策树、暗色模式兼容性 → `assets/images/catalog.md`。
