# patent_content.json 编写指南

## 概述

将 Stage 03-09 撰写的所有章节内容组织为 `$WORK_DIR/patent_content.json` 文件。该文件是纯声明式的，无需编写任何 Python 代码。

## JSON Schema

```json
{
  "header": {
    "交底书名称": "一种xxx的方法",
    "本发明涉及产品和技术": "...",
    "专利保护的目的": "..."
  },
  "sections": {
    "【关键术语】": [
      {"type": "text", "content": "术语1：定义..."},
      {"type": "text", "content": "术语2：定义..."}
    ],
    "【发明构思】": [
      {"type": "text", "content": "段落1..."}
    ],
    "3.1": [
      {"type": "text", "content": "..."}
    ],
    "3.2": [
      {"type": "heading", "content": "A、现有技术的缺点"},
      {"type": "text", "content": "..."},
      {"type": "heading", "content": "B、本专利技术方案可以解决的问题"},
      {"type": "text", "content": "..."}
    ],
    "4.1": [
      {"type": "text", "content": "..."}
    ],
    "4.2": [
      {"type": "text", "content": "步骤S1：..."},
      {"type": "formula", "omml": "<OMML XML>", "num": 1},
      {"type": "inline", "parts": ["其中，", {"omml": "<OMML>"}, " 为..."]},
      {"type": "image", "path": "flowchart_main.png", "width": 14, "caption": "图1 ..."},
      {"type": "empty"}
    ],
    "4.3": [
      {"type": "text", "content": "..."}
    ],
    "参考文献": [
      {"type": "text", "content": "无"}
    ]
  }
}
```

## 段落类型说明

| type | 必填字段 | 可选字段 | 说明 |
|------|---------|---------|------|
| `text` | `content` | — | 楷体 10pt 正文 |
| `heading` | `content` | — | 微软雅黑加粗 10pt |
| `formula` | `omml`, `num` | — | 居中公式 + 右侧编号"（N）" |
| `inline` | `parts` | — | 文本与行内公式混排 |
| `image` | `path` | `width`(默认14，单位cm), `caption` | 居中图片 + 标注 |
| `empty` | — | — | 空行 |

## 段落类型详解

- **`text`**：正文段落，楷体 10pt，黑色。`content` 为纯文本字符串。
- **`heading`**：标题段落，微软雅黑加粗 10pt。用于 3.2 章节中的"A、现有技术的缺点"等子标题。
- **`formula`**：独立数学公式段落。`omml` 为 OMML XML 片段（不含 `<m:oMath>` 外层标签），`num` 为公式编号（整数）。公式居中显示，右侧自动添加"（N）"编号。OMML 语法参考 [omml-formula-guide.md](omml-formula-guide.md)。
- **`inline`**：文本与行内公式混排段落。`parts` 是一个数组，元素可以是：
  - 字符串：普通文本
  - `{"omml": "<OMML XML>"}` 对象：行内公式
  - 示例：`["其中，", {"omml": "<m:sSub>...</m:sSub>"}, " 为变量"]`
- **`image`**：图片段落。`path` 为相对于 `$WORK_DIR/` 目录的图片路径。自动在图片前后插入空行，图片下方插入居中标注。
- **`empty`**：空行段落，用于段落之间的分隔。

## OMML 公式在 JSON 中的嵌入方式

OMML 公式以 XML 字符串形式直接写入 JSON 的 `omml` 字段。JSON 使用 `\"` 转义双引号，不会与中文引号冲突：

```json
{
  "type": "formula",
  "omml": "<m:sSub><m:e><m:r><m:t>S</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val=\"p\"/></m:rPr><m:t>entropy</m:t></m:r></m:sub></m:sSub><m:r><m:t>=</m:t></m:r>...",
  "num": 1
}
```

## 图片路径引用规则

图片 `path` 相对于 `patent_content.json` 所在目录解析。例如 `patent_content.json` 在 `$WORK_DIR/` 下，则 `"path": "flowchart_main.png"` 指向 `$WORK_DIR/flowchart_main.png`。

## 编辑规则

- `header` 中填入发明名称、涉及产品和技术、专利保护目的
- 头部表格中的撰写人、联络方式等个人信息**留空**（不在 JSON 中声明）
- `sections` 的 key 必须与模板 document.xml 中的章节标题文本匹配（如"【关键术语】""3.1""4.2""参考文献"等）
- 构建引擎会自动删除蓝色提示段落和"重要提醒"段落，无需手动处理
- 正文使用楷体 10pt（由引擎自动设置），标题使用微软雅黑加粗
- **禁止使用 Read/Edit 工具直接读写 document.xml**

## 引号使用规则

JSON 字符串值中的引号处理是常见的格式错误来源，必须严格遵守以下规则：

- **中文内容中的引号**：必须使用中文引号 `“”`（左引号 `“` 和右引号 `”`），**严禁**在中文语境下使用 ASCII 双引号 `"`，否则会导致 JSON 解析失败。
  - 正确：`"content": "这是“正确”的引号用法"`
  - 错误：`"content": "这是"错误"的引号用法"`（ASCII 双引号破坏 JSON 结构）
- **英文内容或必须使用 ASCII 引号的场景**：必须使用转义符 `\"` 表示双引号。
  - 正确：`"content": "The \"correct\" way to quote in English"`
  - 错误：`"content": "The "wrong" way to quote in English"`
- **OMML XML 属性中的引号**：XML 属性值中的 `"` 必须转义为 `\"`，这是 OMML 嵌入 JSON 时的必须要求（详见上方 OMML 示例）。
- **总结**：在 JSON 字符串内部，`"` 字符只能以 `\"` 形式出现；中文引用场景应统一改用 `""` 中文引号，从根本上避免转义问题。

## 数学公式处理

技术方案中涉及的数学公式**必须**使用 OMML 格式写入 `omml` 字段，**严禁将公式作为纯文本放在 `text` 类型的 `content` 中**。详细语法和 XML 模板参考 [omml-formula-guide.md](omml-formula-guide.md)，核心要点：
- **长公式**（含分数、求和、上下标等复杂结构）：使用 `formula` 类型，居中显示 + 右侧编号。
- **短公式**（单个变量、简单表达式如 `x_i`）：使用 `inline` 类型，在 `parts` 数组中以 `{"omml": "..."}` 嵌入。
- **判断标准**：只要表达式包含下标、上标、分数、求和∑、希腊字母、绝对值等数学符号，就必须用 OMML 格式。
