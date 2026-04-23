# 微信公众号 HTML 排版约束

AI 智能排版时，必须严格遵循以下约束，确保生成的 HTML 可直接粘贴到微信公众号后台且不被过滤。

---

## 允许的 HTML 标签

`p` `br` `strong` `em` `span` `img` `a` `blockquote` `section` `h1` `h2` `h3` `h4` `table` `thead` `tbody` `tr` `th` `td` `hr` `pre` `code` `svg`

~~`ul` `ol` `li`~~ **已禁止**——微信渲染 `<li>` 会导致圆点与内容分离，列表必须用 `<p>` + `▸`/数字 模拟（见下方「列表替代方案」）

## 允许的 inline style 属性

**文字：** `font-size` `font-weight` `color` `line-height` `letter-spacing` `text-align` `text-decoration` `text-indent`

**间距：** `margin` `margin-top` `margin-bottom` `margin-left` `margin-right` `padding` `padding-top` `padding-bottom` `padding-left` `padding-right`

**边框与背景：** `border` `border-left` `border-right` `border-top` `border-bottom` `border-radius` `border-color` `background-color` `background`

**图片：** `width`（仅 img，通常 100%）`height` `vertical-align`

**其他：** `box-shadow` `box-sizing` `display`（仅 block / inline-block / none）`overflow` `word-break` `white-space` `text-overflow` `max-width`（仅 img）

---

## 严格禁止

### 禁止的标签
`div` `article` `figure` `figcaption` `iframe` `video` `audio` `canvas` `form` `input` `button` `select` `textarea` `label`

### 禁止的全局属性
`class` `id` `data-*`

### 禁止的 CSS
- `display: flex` / `display: grid`
- `position` / `float`
- `animation` / `transform` / `transition` / `@keyframes`
- `:hover` / `:active` / `:focus` 等伪类
- `calc()` / CSS 变量（`var(--xx)`）
- `!important`
- **代码块内**：任何 `white-space` 属性（微信会吞换行，必须用 `<br>` 代替）

### 禁止的页面结构标签
`<!DOCTYPE>` `<html>` `<head>` `<body>` `<meta>` `<title>` `<link>` `<script>` `<style>`

### 禁止的输出格式
- ` ```html ``` ` 等代码块包裹
- Markdown 格式混合输出
- Emoji / 表情符号 / 非文本装饰字符

---

## 结构嵌套规则（微信特有坑）

微信公众号对标签嵌套有特殊限制，违反会导致渲染异常：

### 列表项（`<li>`）内部禁止块级元素

**这是最常见的问题，有两大坑：**

#### 坑 1：`<li>` 内部禁止块级元素

`<li>` 内部如果包含 `p` / `section` / `div` 等块级元素，**微信会把每个块级元素都当作一个列表项渲染**，产生多余的 bullet 点和异常间距。

```html
<!-- 错误写法 — 会多出空 bullet -->
<ul>
  <li>
    <p>第一段文字</p>
    <p>第二段文字</p>
  </li>
</ul>

<!-- 正确写法 — li 内只放纯文本或行内元素 -->
<ul>
  <li><span style="font-size:15px;color:#57534e;line-height:1.9;">第一段文字</span></li>
  <li><span style="font-size:15px;color:#57534e;line-height:1.9;">第二段文字</span></li>
</ul>

<!-- 如果需要多行内容，拆成多个 li -->
```

#### 坑 2（致命）：`<li>` 标签之间禁止换行/空白

**微信编辑器会把 `<li></li>` 标签之间的换行符或空白字符解析为空文本节点，每个空节点都会渲染成一个空 bullet 点！**

```html
<!-- 致命错误 — 每个换行都变成一个空 bullet -->
<ul>
<li>第一项</li>
<li>第二项</li>
<li>第三项</li>
</ul>

<!-- 微信实际渲染为：<ul> <li></li>(空!) <li>第一项</li> <li></li>(空!) <li>第二项</li> ... -->

<!-- 唯一正确的写法 — 所有 li 必须写在同一行，无任何换行/空白 -->
<ul><li><span style="...">第一项</span></li><li><span style="...">第二项</span></li><li><span style="...">第三项</span></li></ul>

<!-- ol 同理 -->
<ol><li><span style="...">第一步</span></li><li><span style="...">第二步</span></li></ol>
```

> **强制规则：生成 HTML 时，所有 `<ul>` 和 `<ol>` 内的 `<li>` 必须压缩到单行书写，标签之间不允许有任何换行或空白字符。**

**`<li>` 允许的子元素：**
- 纯文本
- `span`、`strong`、`em`、`code`、`a`、`br`、`img`
- **禁止：** `p`、`section`、`h1-h4`、`blockquote`、`pre`、`table`、任何块级元素

### 嵌套层级上限

| 元素 | 最大嵌套深度 | 说明 |
|------|-------------|------|
| `ul` / `ol` | **2 层** | 即最多 `ul > li > ul > li` |
| `table` | **1 层** | 不支持嵌套表格 |

---

## 输出要求

1. **纯 HTML 输出** — 不输出 Markdown、代码块标记或任何非 HTML 内容
2. **所有样式必须 inline** — 微信会剥离 `<style>` 标签和 `class`，唯一可靠的样式方式是 `style="..."` 内联
3. **手机端优先** — 短段落、多留白、字号 15-17px、行高 1.75-2.0
4. **图片必须** — `<img>` 有 `alt` 属性，宽度 `width: 100%`
5. **禁止外部链接（致命！）** — `<a>` 标签 **不得带有 `href` 属性**，否则草稿箱 API 返回 `invalid content`
   - 无 `href` 的 `<a>` 标签可以正常发布
   - 带 `href` 的 `<a>` 标签（无论指向什么 URL）一律被微信 API 拒绝
   - 如需引用网址，改为纯文本显示（如「登录微信公众平台查看」）

---

## 样式风格参考

AI 排版时可自由选择风格，以下为可选方向：

### 色彩方案（选一）
- **墨韵**：深色正文 `#333`，主色 `#1a73e8`，辅色 `#5f6368`，背景 `#fff`
- **暖橙**：深色正文 `#2d2d2d`，主色 `#e8710a`，辅色 `#9aa0a6`，背景 `#fffaf5`
- **竹青**：深色正文 `#263238`，主色 `#00796b`，辅色 `#78909c`，背景 `#f5f5f0`
- **黛蓝**：深色正文 `#1e293b`，主色 `#4f46e5`，辅色 `#94a3b8`，背景 `#f8fafc`

### 排版节奏
- 标题与正文间距 `margin-top: 1.5em; margin-bottom: 0.5em`
- 段落间距 `margin-bottom: 1.2em`
- 引用块左边框 `border-left: 3px solid 主色` + 浅底色
- 代码块：多行用暗色背景 `#282c34` + 语法高亮，短代码可用浅色底 + 语言标签栏（见 themes.md）
- 分割线细线 `border: none; border-top: 1px solid #e5e7eb`

### 装饰元素（可选，使用 SVG 或 inline style 实现）
- 分割线 / 分隔符
- 引用块装饰
- 主副标题搭配
- 文字阴影（`text-shadow`，仅标题）
- 底色卡片（`background-color` + `padding` + `border-radius`）
- 边框卡片（`border` + `padding`）
- 文末互动引导区

### 关键句处理
- 底色高亮：`background-color: 浅主色; padding: 2px 6px; border-radius: 3px`
- 下划线强调：`border-bottom: 2px solid 主色; padding-bottom: 1px`
- 颜色强调：`color: 主色; font-weight: bold`

---

## 验证清单

输出前自检：

- [ ] 无 `class` / `id` / `data-*` 属性
- [ ] 无 `<style>` / `<script>` 标签
- [ ] 无 `div`，布局全靠 `p` / `section` / `span` + inline style
- [ ] 无 flex / grid / position / float
- [ ] 所有样式均为 inline
- [ ] 图片有 alt 且 width: 100%
- [ ] 无 Emoji / 表情符号
- [ ] 纯 HTML 输出，无代码块标记
- [ ] **禁止使用 `<ul>`/`<ol>`/`<li>` 标签——微信渲染 `<li>` 存在严重 bug：即使 `<li>` 独占一行且内部只有行内元素，微信仍会将圆点和内容分离（圆点单独一行，内容另起一行）。所有列表必须用 `<p>` 段落模拟（见下方「列表替代方案」）**
- [ ] **`<a>` 标签不得带 `href` 属性（否则 API 返回 invalid content）**
- [ ] **代码块内容必须用 `<br>` 替换 `\n`，禁止 `white-space: pre-wrap` / `white-space: pre`**
- [ ] **多行代码块必须使用暗色背景 + 语法高亮配色（见 themes.md「代码块」章节）**
- [ ] **代码块标题栏禁止使用 `display: flex`，用简单 `padding` + `<span>` 即可**
- [ ] **外层 section 禁止设置左右 margin / 左右 padding（微信自带留白）**
- [ ] **所有元素禁止设置 margin-left / margin-right，禁止用 calc() 缩减宽度——微信阅读器自带约 15-20px 左右留白，直接 width:100% 即可**
- [ ] **减少大表格的使用——超过 2 行内容的对比/示例场景，优先使用带背景色的 section 卡片（红/绿对比）或 blockquote 替代表格**
- [ ] **表格单元格内容强制限制：单个单元格内容不得超过 100 字，超出则必须拆分为 section 卡片或 blockquote，不得强行塞进表格**
- [ ] **表格内禁止嵌入 pre/code 代码块——会导致表格行高过大，影响阅读。表格内如需展示代码片段，改用行内 code 标签或直接纯文本描述**
- [ ] **每个 `<li>` 必须独占一行——禁止多个 `<li>` 写在同一行，否则微信解析器可能只显示圆点不显示内容**

## 列表替代方案（重要）

由于微信 `<li>` 渲染 bug（圆点与内容分离），所有列表必须用 `<p>` 段落模拟：

**无序列表（bullet ▸）：**
```html
<p style="margin:0 0 6px 0;padding:0 0 0 16px;font-size:15px;color:#333333;line-height:1.9;text-indent:-16px;">▸ 列表项内容</p>
<p style="margin:0 0 6px 0;padding:0 0 0 16px;font-size:15px;color:#333333;line-height:1.9;text-indent:-16px;">▸ 列表项内容</p>
```

**有序列表（数字）：**
```html
<p style="margin:0 0 6px 0;padding:0 0 0 20px;font-size:15px;color:#333333;line-height:1.9;text-indent:-20px;">1. 列表项内容</p>
<p style="margin:0 0 6px 0;padding:0 0 0 20px;font-size:15px;color:#333333;line-height:1.9;text-indent:-20px;">2. 列表项内容</p>
```

**要点说明：**
- `padding-left` 控制整体缩进，`text-indent` 为负值实现悬挂缩进（符号/数字突出，内容对齐）
- bullet 用 `▸` 符号（U+25B8），不使用 `•`（微信可能吞掉）
- 无序列表：`padding-left:16px` + `text-indent:-16px`
- 有序列表：`padding-left:20px` + `text-indent:-20px`（数字更宽）
- 列表项间距用 `margin-bottom:6px`，不要太大
