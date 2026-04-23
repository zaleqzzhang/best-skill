# 主题与样式参考

AI 智能排版时的完整样式系统。详细技术约束见 `html-constraints.md`。

---

## 快速选色

| 主题名 | 强调色 | 强调浅色 | 风格 |
|--------|--------|----------|------|
| 默认（蓝） | `#3b82f6` | `#effbff` | 轻亮清爽 |
| 墨韵 | `#1a73e8` | `#e8f0fe` | 经典商务 |

> 排版时只需选定一个主题名，全局统一使用其强调色。

---

## 色彩方案（亮色 / 暗色）

| 用途 | 亮色 | 暗色 | 变量名 |
|------|------|------|--------|
| 页面背景 | `#fafaf9` | `#0f0f11` | `--color-bg` |
| 卡片背景 | `#ffffff` | `#1a1a1f` | `--color-surface` |
| 主文字 | `#1c1917` | `#e4e4e7` | `--color-text` |
| 次要文字 | `#57534e` | `#a1a1aa` | `--color-text-secondary` |
| 辅助文字 | `#a8a29e` | `#71717a` | `--color-text-muted` |
| 强调色 | `#3b82f6` | `#60a5fa` | `--color-accent` |
| 强调浅色 | `#effbff` | `#1e3a5f` | `--color-accent-light` |
| 边框 | `#e7e5e4` | `#2e2e35` | `--color-border` |
| 代码块背景 | `#1e1e2e` | `#11111b` | `--color-code-bg` |
| 代码块文字 | `#cdd6f4` | `#cdd6f4` | `--color-code-text` |

## Callout 颜色

| 类型 | 左边框 | 亮色背景 | 暗色背景 |
|------|--------|----------|----------|
| 红色（警示） | `#ef4444` | `#fef2f2` | `#1c1111` |
| 绿色（总结） | `#22c55e` | `#f0fdf4` | `#0d1f12` |
| 黄色（提醒） | `#eab308` | `#fefce8` | `#1c1a0e` |
| 蓝色（引用/提示） | `#3b82f6` | `#effbff` | `#0f1a2e` |

## 代码高亮配色

为代码块手动上色时的参考色值（Catppuccin Mocha 风格）：

| 元素 | 色值 |
|------|------|
| 关键字 | `#cba6f7` |
| 字符串 | `#a6e3a1` |
| 注释 | `#6c7086` |
| 函数名 | `#89b4fa` |
| 数字 | `#fab387` |
| 背景 | `#1e1e2e` |
| 文字 | `#cdd6f4` |

---

## 布局容器

### 外层 section（每篇文章唯一的外层容器）

```
max-width: 100%; margin: 0; padding: 0;
```

> 微信公众号阅读器**自带左右留白（约 15-20px）**，外层 section **禁止设置任何左右 margin 和左右 padding**，否则内容区域会过窄。
> 如确需内边距，仅允许设置上下方向。

### 图片

```
width: 100%
display: block
margin: 0.8em auto
border-radius: 6px
```

---

## 字号层级

| 元素 | 字号 | 字重 | 行高 |
|------|------|------|------|
| H1 | 22px | bold | 1.5 |
| H2 | 19px | bold | 1.5 |
| H3 | 17px | bold | 1.5 |
| H4 | 16px | bold | 1.5 |
| 正文 p / span | 15px | normal | 1.9 |
| 表格 th/td | 14px | normal | 1.6 |
| 代码 code | 13px | normal | 1.7 |
| 注脚/辅助文字 | 13px | normal | 1.8 |

---

## 元素样式映射

以下为每个 HTML 元素应使用的具体样式，直接复制使用即可。

### 标题 H2

```
font-size: 19px; color: --color-text; font-weight: bold; line-height: 1.5; margin-top: 1.4em; margin-bottom: 0.4em; margin-left: 0; margin-right: 0;
```

### 标题 H3

```
font-size: 17px; color: --color-text; font-weight: bold; line-height: 1.5; margin-top: 1.2em; margin-bottom: 0.4em; margin-left: 0; margin-right: 0;
```

### 正文段落

```
font-size: 15px; color: --color-text; line-height: 1.9; margin-bottom: 0.8em; margin-left: 0; margin-right: 0;
```

### 加粗文字（强调词）

```
color: --color-accent; font-weight: bold;
```

### 无序列表（▸ 符号模拟）

> **禁止使用 `<ul>`/`<li>` 标签**——微信渲染 bug 会导致圆点与内容分离。用 `<p>` + `▸` 符号模拟。

```html
<p style="margin:0 0 6px 0;padding:0 0 0 16px;font-size:15px;color:#333333;line-height:1.9;text-indent:-16px;">▸ 列表项内容</p>
```

**要点：** `padding-left:16px` + `text-indent:-16px` 实现悬挂缩进；bullet 统一用 `▸`（U+25B8）。

### 有序列表（数字模拟）

> **禁止使用 `<ol>`/`<li>` 标签**——同上原因。用 `<p>` + 数字模拟。

```html
<p style="margin:0 0 6px 0;padding:0 0 0 20px;font-size:15px;color:#333333;line-height:1.9;text-indent:-20px;">1. 列表项内容</p>
```

**要点：** `padding-left:20px` + `text-indent:-20px`（数字比符号宽，需要更多缩进）。

### 列表项内 span

> 已废弃。列表不再使用 `<li>` + `<span>` 结构，改用 `<p>` 段落模拟（见上方「无序列表」和「有序列表」）。列表项内可直接使用 `<strong>`、`<code>` 等行内标签。

### 引用块 blockquote

```
border-left: 3px solid --color-accent; background-color: --color-accent-light; padding: 10px 14px; margin: 0.8em 0; font-size: 15px; color: --color-accent; line-height: 1.9;
```

> **注意：禁止设置 margin-left / margin-right，微信公众号自带左右留白。**

### 代码块（分两种场景）

#### 场景 A：多行大段代码（3 行以上）— 强制暗色主题 + 语法高亮

多行代码必须使用**暗色背景 + 语法高亮**，视觉区分于正文，提升可读性。

pre（外层容器）：
```
margin: 10px 0; padding: 12px 14px; background-color: #282c34; border-radius: 6px; overflow-x: auto;
```
code（内层文字）：
```
font-size: 12px; line-height: 1.7; color: #abb2bf; display: block; font-family: 'SFMono-Regular', Consolas, Monaco, 'Courier New', monospace;
```

语法高亮配色（One Dark Pro 风格，直接使用）：

| 元素 | 色值 | 适用场景 |
|------|------|---------|
| 关键字 / 命令 | `#c678dd` | export, import, def, if, return 等 |
| 字符串 | `#98c379` | 引号包裹的内容 |
| 注释 | `#7f848e` | # 开头、// 开头、/* ... */ |
| 函数名 | `#61afef` | 函数调用 |
| 数字 / 布尔 | `#d19a66` | 数字常量, true, false |
| 变量 / 属性名 | `#e06c75` | 标识符 |
| 正文默认色 | `#abb2bf` | 未匹配的普通文本 |

> **致命规则（微信兼容）：**
> - 代码内容中的每个换行符 `\n` **必须替换为 `<br>` 标签**
> - **禁止**使用 `white-space: pre-wrap`（微信会吞掉 `<pre>` 内原始换行）
> - **禁止**在 `<code>` 上设置任何 `white-*` 属性
>
> **排版步骤：**
> 1. 将代码文本中的 `\n` 全部替换为 `<br>`
> 2. 对关键字/字符串/注释等用 `<span style="color: xxx">` 包裹上色
> 3. 输出为 `<pre style="..."><code style="...">第1行<br>第2行<br>...</code></pre>`
>
> 示例输出：
> ```html
> <pre style="margin:16px 0;padding:14px 16px;background-color:#282c34;border-radius:6px;overflow-x:auto;">
> <code style="font-size:12px;line-height:1.7;color:#abb2bf;display:block;font-family:'SFMono-Regular',Consolas,Monaco,'Courier New',monospace;">
> <span style="color:#7f848e;"># 这是注释</span><br>
> <span style="color:#c678dd;">export</span> APP_NAME=<span style="color:#98c379;">"my-app"</span><br>
> <span style="color:#c678dd;">const</span> port = <span style="color:#d19a66">3000</span>;
> </code></pre>
> ```

#### 场景 B：行内 / 短代码（1-2 行）— 可选带语言标签栏

短代码可使用浅色背景 + 语言标签标题栏，更轻量。

外层容器 section：
```
margin: 10px 0; background-color: #f6f8fa; border-radius: 6px; overflow: hidden;
```
标题栏 section：
```
padding: 8px 14px; background-color: #eaecf0; border-bottom: 1px solid #dfe1e4;
```

> **注意：标题栏禁止使用 `display: flex`！** 用简单的 `text-align` + `padding` 即可。标签文字用一个 `<span>` 放在左侧即可。

标题栏内语言标签 span：
```
font-size: 13px; color: #5f6368;
```
pre：
```
margin: 0; padding: 14px; overflow-x: auto; background-color: #282c34;
```
code：
```
font-size: 13px; line-height: 1.75; color: #abb2bf; display: block; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
```

> 同样遵循 `\n → <br>` 规则。单行代码无需 `<br>`。

### 表格 table

> **禁止设置 margin-left / margin-right，禁止用 calc() 缩减宽度。直接 width:100%，微信会自动处理留白。**

table:
```
width: 100%; border-collapse: collapse; margin-bottom: 0.8em; margin-left: 0; margin-right: 0; font-size: 14px;
```
thead tr:
```
border-bottom: 2px solid #333333;
```
th:
```
border: none; border-bottom: 2px solid #333333; padding: 8px 10px; text-align: left; font-weight: bold; color: #1e293b;
```
> **禁止给表头设置背景色**——微信深色模式会自动反转浅色背景，导致浅色/深色模式显示不一致。表头统一用「无背景 + 加粗文字 + 粗底边框」区分，两种模式都能看清。
tbody tr:
```
border-bottom: 1px solid #e8eaed;
```
td:
```
padding: 10px 12px; color: #5f6368;
```

### 分割线 hr

```
border: none; border-top: 1px solid --color-border; margin: 1em 0;
```

> **禁止设置左右 margin，只用上下间距。**

### 底部注脚

```
font-size: 13px; color: --color-text-muted; line-height: 1.8; text-align: center;
```
