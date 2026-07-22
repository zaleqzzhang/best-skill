# Brand Guidelines Reference

微信官方品牌设计规范摘要，来源：[wechat.design/brand/main-brand](https://wechat.design/brand/main-brand)。本文件记录官方品牌层面的规范（标志、标准色、字体、使用禁忌），与 `tokens.md`（CSS 设计令牌）配合使用。

---

## 品牌理念

> 微信品牌形象基于微信的产品理念，包含于客户端各平台设计、相关网页设计、品牌设计、周边产品设计中。与传统品牌不同，微信是一个相对抽象、无形、但又无处不在的互联网产品。微信的品牌设计不仅要告诉用户这是微信，还要传达微信的理念和态度。

**三个关键词：谨慎、优雅、超前。** 前端实现中的体现：
- **谨慎** — 色彩克制（全页仅一个主色绿），动效微小（12px 位移），不滥用装饰
- **优雅** — 系统无衬线字体 + 慷慨圆角，而非花哨字体；硬切分段，而非渐变过渡
- **超前** — 真黑 `#191919` 暗色底（而非过时的深灰/藏青），`data-theme` 原生暗色模式

---

## 标志（Logo）类型

| 类型 | 用途 | 说明 |
|---|---|---|
| 中文标志 | 中文版页面、中文宣传材料 | "微信"中文字 + 图形标志组合 |
| 英文标志 | 英文版页面、国际宣传材料 | "WeChat" 英文字 + 图形标志组合 |
| 手机客户端标志 | App 图标、移动端推广 | 绿色气泡图标（squircle 圆角方形） |
| PC 客户端标志 | 桌面端 App 图标 | 同手机图标，适配桌面尺寸 |

> **Web 前端实现：** 本 skill 的 `scaffold-zh.html` / `scaffold-en.html` 中已内嵌一个简化版 WeChat SVG 图标（两个绿色对话气泡），可直接用于导航栏 `.top-nav__brand`。如需官方完整标志，请从 [wechat.design/brand](https://wechat.design/brand) 下载资源包。

---

## 标志背景色规则

官方规范使用 K 值（黑色百分比）划分背景明暗等级：

| 背景类型 | K 值范围 | 推荐标志形式 | 说明 |
|---|---|---|---|
| 白色 / 极浅 | K0 | 全彩标志 或 单色黑标志 | 最佳识别环境 |
| 浅灰 | K10–K40 | **禁止使用全彩标志** → 改用单色标志 | 全彩标志的白色气泡轮廓在浅灰底上不清晰 |
| 中灰 | K20–K50 | 单色白标志 | 白色单色标志在中灰底上对比度最佳 |
| 深灰 / 黑 | K50–K100 | 单色白标志 | 深色底上仅用白色单色标志 |

**单色标志两种变体：**
- **80% 黑色** — 用于浅色/有色/图片背景（透明度 80% 的黑色）
- **纯白** — 用于深色 / K50+ 背景

**前端映射：**
- 白色画布 (`--color-canvas: #ffffff`) → 全彩绿色 SVG 图标（默认）
- 浅灰面 (`--color-surface-soft: #f7f7f7`) → 全彩仍可用（K3 左右，远低于 K10 门槛）
- 暗色模式 (`--color-canvas: #191919`) → 切换为白色单色图标（通过 `fill="currentColor"` + `[data-theme="dark"]` 覆盖）

```css
/* 导航栏品牌图标默认全彩，暗色模式自动转白 */
.top-nav__brand svg path { fill: #07c160; }
[data-theme="dark"] .top-nav__brand svg path { fill: #ffffff; }
/* 第二个气泡保持半透明 */
.top-nav__brand svg path[opacity] { opacity: 0.55; }
```

---

## 标志最小尺寸与安全区域

| 场景 | 最小尺寸 |
|---|---|
| 印刷 | 8mm 宽 |
| 屏幕 | 24px 宽（绝对最小 16px） |

**安全区域（Clear Space）：** 标志周围需保留不小于标志高度 1/4 的留白，不可放置任何文字、图形或边框。

**前端映射：**
- 导航栏图标 22×22px — 接近最小值，仅用于导航栏紧凑场景
- 页脚图标 20×20px — 同上
- 如需大尺寸展示（如品牌区 hero），建议 48px 以上

---

## 标志错误使用（严禁）

| ❌ 禁止 | 说明 |
|---|---|
| 改变标志与文字的相对位置关系 | 标志图形和文字的组合比例固定 |
| 拉伸 / 压缩标志 | 必须等比缩放，`width` 和 `height` 同比例 |
| 在标志上附加文字 | 不得在标志图形旁自行添加标语或描述 |
| 修改标志颜色 | 绿色 `#07c160` 是唯一品牌色，不可替换 |
| 添加阴影 / 立体效果 / 渐变 | 标志必须保持平面，无任何特效 |
| 低质量使用 | 必须使用矢量 SVG，不用位图放大 |
| 修改标志细节 | 不可改变气泡形状、角度、比例 |

**前端实现注意：**
- SVG 图标不要加 `filter: drop-shadow()` 或 `text-shadow`
- 不要用 `transform: scale(1.1)` 以外的变形做 hover 效果（`scale` 等比缩放是安全的）
- 不要用 `filter: hue-rotate()` 改色

---

## 标准色板

来源：[wechat.design/brand/main-brand#标准色板](https://wechat.design/brand/main-brand)

| 色块 | HEX | RGB | 官方角色 | 本 skill 对应 token |
|---|---|---|---|---|
| 🟩 | `#07C160` | `rgb(7, 193, 96)` | 品牌主色（微信绿） | `--color-primary` |
| ⬛ | `#000000` | `rgb(0, 0, 0)` | 辅助色（纯黑） | `--color-brand-black`（新增） |
| 🟥 | `#7F7F7F` | `rgb(127, 127, 127)` | 辅助色（中灰） | `--color-brand-gray`（新增） |
| ⬜ | `#EDEDED` | `rgb(237, 237, 237)` | 背景色（浅灰） | `--color-hairline-soft` |
| ⬜ | `#F7F7F7` | `rgb(247, 247, 247)` | 背景色（极浅灰） | `--color-surface-soft` |

**说明：**
- 官方色板仅 5 色，极其克制——这印证了本 skill "全页仅一个主色" 的原则
- 官方纯黑 `#000000` 用于印刷品品牌标识；Web 前端使用 `#1a1a1a`（近黑）作为正文/标题色，因为纯黑在屏幕上对比度过强、在 OLED 屏上有锯齿感。两者不矛盾——`#000000` 是品牌标识色，`#1a1a1a` 是 Web 排版色
- 官方中灰 `#7F7F7F` 是品牌层面的中性灰，用于品牌物料；Web 排版使用 `#666666`（`--color-body-default`）和 `#888888`（`--color-muted`）做更细粒度的文字层级
- `#EDEDED` 和 `#F7F7F7` 已在本 skill 中作为 `--color-hairline-soft` 和 `--color-surface-soft` 使用

---

## 官方字体（品牌物料用，非 Web 前端）

wechat.design 站点引用的字体：

| 字体 | 用途 | 说明 |
|---|---|---|
| HYQiHeiX1-45W | 中文常规 | 汉仪旗黑体 45W（Light） |
| HYQiHeiX1-55W | 中文加粗 | 汉仪旗黑体 55W（Medium） |
| MyriadPro-Regular | 拉丁文常规 | Adobe Myriad Pro |
| MyriadPro-Light | 拉丁文细体 | Adobe Myriad Pro Light |
| Source Sans Pro | Web 后备 | 开源无衬线体 |
| Helvetica Neue | Web 后备 | 系统字体 |

**Web 前端策略（本 skill 已实现）：**
- **不引入任何 Web Font** — 品牌物料用的汉仪旗黑体和 Myriad Pro 是商业字体，不可用于 Web `@font-face`
- 使用系统等价物：PingFang SC（macOS/iOS）≈ 汉仪旗黑体的视觉风格；`-apple-system` / `Segoe UI` ≈ Myriad Pro 的人文无衬线风格
- `font-weight: 600` 模拟 HYQiHei 55W 的 Medium 字重
- 这使得页面零外部字体请求，同时保持品牌视觉一致性

---

## 客户端标志（App Icon）尺寸

官方提供以下屏幕显示尺寸：

| 尺寸 | 用途 |
|---|---|
| 256×256px | 高清展示 / App Store |
| 128×128px | 桌面端 |
| 96×96px | 大列表 |
| 64×64px | 中等列表 |
| 48×48px | 小列表 / 导航 |
| 32×32px | 最小显示 |

**前端映射：** 本 skill 的导航栏图标使用 22×22px（低于官方最小 32px），因为导航栏场景中图标与文字并排，视觉上可接受。如单独展示 App 图标，请用 48px 以上。

---

## 与本 skill 设计令牌的对照

| 官方规范 | 本 skill 实现 | 一致性 |
|---|---|---|
| 品牌绿 `#07C160` | `--color-primary: #07c160` | ✅ 完全一致 |
| 纯黑 `#000000` | `--color-brand-black: #000000`（品牌标识用）<br>`--color-ink: #1a1a1a`（Web 排版用） | ✅ 品牌层一致，排版层优化 |
| 中灰 `#7F7F7F` | `--color-brand-gray: #7f7f7f`（品牌层）<br>`--color-body-default: #666` / `--color-muted: #888`（排版层） | ✅ 品牌层一致，排版层细分 |
| 浅灰 `#EDEDED` | `--color-hairline-soft: #ededed` | ✅ 完全一致 |
| 极浅灰 `#F7F7F7` | `--color-surface-soft: #f7f7f7` | ✅ 完全一致 |
| 汉仪旗黑体 | `--font-body` → PingFang SC / Microsoft Yahei | ✅ 系统等价物 |
| Myriad Pro | `--font-body` → `-apple-system` / `Segoe UI` | ✅ 系统等价物 |
| 标志最小 24px | 导航 22px（紧凑场景例外） | ⚠️ 接近最小值 |
| 标志不可加阴影 | 本 skill 无 `drop-shadow` on logo | ✅ 一致 |
| 标志不可改色 | `fill: #07c160` 固定，暗色模式转白 | ✅ 一致 |
