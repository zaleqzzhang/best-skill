> **注意**：本文档为 `patent_builder.py` 构建引擎的内部实现参考。正常撰写专利时，
> 所有内容通过 `patent_content.json` 声明式文件描述，由构建引擎自动完成 XML 编辑，
> **无需手动编写 Python 脚本操作 XML**。本文档仅供理解引擎内部逻辑或调试排错时参考。

# 专利交底书 DOCX 编辑指南

## 编辑方式：Unpack → Python 脚本编辑 XML → Repack

专利交底书模板是一个 .docx 文件（实质是 ZIP 包含 XML）。编辑流程：

```bash
# 1. 解压模板（模板在 $SKILL_DIR/assets/ 下，解压到 $WORK_DIR/unpacked/）
python $SKILL_DIR/scripts/office/unpack.py $SKILL_DIR/assets/发明专利技术交底书模板.docx $WORK_DIR/unpacked/

# 2. 编写 Python 脚本编辑 document.xml
#    重要：document.xml 通常有数千行，禁止使用 Read/Edit 工具直接读写！
#    必须编写 Python 脚本（使用 lxml 库）通过 XPath 定位并修改 XML 节点
python $WORK_DIR/edit_patent.py

# 3. 重新打包
python $SKILL_DIR/scripts/office/pack.py $WORK_DIR/unpacked/ $WORK_DIR/{发明名称}.docx --original $SKILL_DIR/assets/发明专利技术交底书模板.docx
```

## Python 脚本编辑 XML 的方法

使用 lxml 库解析和编辑 document.xml，通过 XPath 定位目标节点。以下是常用操作的代码模式：

### 基本结构

```python
from lxml import etree

# 命名空间映射
nsmap = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}

xml_path = '$WORK_DIR/unpacked/word/document.xml'
tree = etree.parse(xml_path)
root = tree.getroot()
body = root.find('.//w:body', nsmap)
```

### 定位章节标题段落

```python
def find_paragraph_containing_text(body, text):
    """查找包含指定文本的段落元素"""
    for p in body.findall('.//w:p', nsmap):
        full_text = ''.join(t.text or '' for t in p.findall('.//w:t', nsmap))
        if text in full_text:
            return p
    return None

# 示例：定位【关键术语】章节
section_p = find_paragraph_containing_text(body, '【关键术语】')
```

### 在指定位置插入内容段落

```python
def insert_after(parent, target, new_element):
    """在 target 元素之后插入 new_element"""
    idx = list(parent).index(target)
    parent.insert(idx + 1, new_element)

# 构建 XML 段落字符串，然后解析为元素插入
para_xml = '''<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:pPr>
    <w:spacing w:beforeLines="50" w:afterLines="50"/>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>
      <w:color w:val="000000"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:color w:val="000000"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
    <w:t>正文内容</w:t>
  </w:r>
</w:p>'''
new_para = etree.fromstring(para_xml)
insert_after(body, section_p, new_para)
```

### 删除蓝色提示文本和占位文字

**重要**：删除段落时必须检查父元素是否为表格单元格 `<w:tc>`。OOXML 规范要求每个 `<w:tc>` 至少包含一个 `<w:p>` 段落，如果删除后单元格为空，必须补一个空 `<w:p>`，否则 Word 会报"无法读取的内容"错误。

```python
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def _safe_remove_paragraph(p):
    """安全删除段落：如果段落在表格单元格内且是唯一段落，替换为空段落而非删除"""
    parent = p.getparent()
    if parent is None:
        return
    # 检查父元素是否为表格单元格 <w:tc>
    if parent.tag == f'{{{W}}}tc':
        # 统计该单元格中的 <w:p> 数量
        sibling_paragraphs = parent.findall(f'{{{W}}}p')
        if len(sibling_paragraphs) <= 1:
            # 这是单元格中唯一的段落，不能直接删除
            # 清空段落内容（保留 <w:pPr> 但移除所有 <w:r> 和文本）
            for child in list(p):
                if child.tag != f'{{{W}}}pPr':
                    p.remove(child)
            # 同时清除 pPr 中的蓝色颜色标记
            pPr = p.find(f'{{{W}}}pPr')
            if pPr is not None:
                for color in pPr.findall(f'.//{{{W}}}color'):
                    if color.get(f'{{{W}}}val', '').upper() == '0000FF':
                        color.getparent().remove(color)
            return
    parent.remove(p)

def remove_blue_hint_paragraphs(body):
    """删除蓝色提示文本段落（w:color w:val="0000FF"）"""
    to_remove = []
    for p in body.findall('.//w:p', nsmap):
        for color in p.findall('.//w:color', nsmap):
            if color.get(f'{{{nsmap["w"]}}}val', '').upper() == '0000FF':
                to_remove.append(p)
                break
    for p in to_remove:
        _safe_remove_paragraph(p)

def remove_placeholder_paragraphs(body):
    """删除包含占位文字的段落（如"流程图将在此处插入"）"""
    placeholder_keywords = ['流程图将在此处插入', '此处插入图片', '此处插入']
    to_remove = []
    for p in body.findall('.//w:p', nsmap):
        full_text = ''.join(t.text or '' for t in p.findall('.//w:t', nsmap))
        for kw in placeholder_keywords:
            if kw in full_text:
                to_remove.append(p)
                break
    for p in to_remove:
        _safe_remove_paragraph(p)
```

### 保存修改

```python
tree.write(xml_path, xml_declaration=True, encoding='UTF-8', standalone=True)
```

## 模板 XML 结构

document.xml 的结构如下：

### 头部信息表格 `<w:tbl>`

表格有4行，每行包含标签单元格和内容单元格。

**定位方式**：搜索标签文本找到对应的 `<w:tc>` 标签单元格，其后紧跟的 `<w:tc>` 即为内容单元格。

| 标签文本 | 操作 |
|---------|------|
| `交底书名称` | 在同行右侧单元格的 `<w:p>` 中插入 `<w:r>` |
| `交底书撰写人` | 在同行右侧单元格的 `<w:p>` 中插入 `<w:r>` |
| `本发明涉及产品和技术` | 在同行右侧单元格的 `<w:p>` 中插入 `<w:r>` |
| `竞对或竞品名称` | 在同行右侧单元格的 `<w:p>` 中插入 `<w:r>` |
| `撰写人联络方式` | 在同行右侧单元格的 `<w:p>` 中插入 `<w:r>` |

**插入文本到空单元格的 XML 模式**（表格内容使用楷体）：
```xml
<w:p ...>
  <w:pPr>...</w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
    <w:t>填入的内容</w:t>
  </w:r>
</w:p>
```

### 正文章节

正文章节通过特征文本定位。每个章节标题后有若干空 `<w:p>` 段落用于填充内容。

**章节标题特征文本**：
- `【关键术语】` - 第1节
- `【发明构思】` - 第2节
- `【背景技术】` - 第3节
  - `3.1相关背景描述` - 子节3.1
  - `3.2现有技术的缺点` - 子节3.2
- `【发明内容】` - 第4节
  - `4.1产品侧` - 子节4.1
  - `4.2技术侧` - 子节4.2
  - `4.3专利方案所产生的有益效果` - 子节4.3
- `参考文献` - 第5节

**在章节中插入内容**：

找到章节标题段落后，在其后的空 `<w:p>` 中插入内容，或者在标题段落后追加新的 `<w:p>` 段落。

正文段落的标准 XML 模式（楷体 10pt 黑色，段前段后间距）：
```xml
<w:p>
  <w:pPr>
    <w:spacing w:beforeLines="50" w:afterLines="50"/>
    <w:autoSpaceDN w:val="0"/>
    <w:textAlignment w:val="center"/>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>
      <w:color w:val="000000"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:color w:val="000000"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
    <w:t>正文内容</w:t>
  </w:r>
</w:p>
```

**段落间距说明**：`<w:spacing w:beforeLines="50" w:afterLines="50"/>` 表示段前段后各半行间距，避免段落间距过小导致内容堆叠。

**加粗标题文本**（微软雅黑加粗，用于章节小标题）：
```xml
<w:r>
  <w:rPr>
    <w:rFonts w:ascii="微软雅黑" w:eastAsia="微软雅黑" w:hAnsi="微软雅黑" w:hint="eastAsia"/>
    <w:b/>
    <w:bCs/>
    <w:color w:val="000000"/>
    <w:sz w:val="20"/>
    <w:szCs w:val="20"/>
  </w:rPr>
  <w:t>加粗标题文本</w:t>
</w:r>
```

## 删除蓝色提示文本

模板中蓝色字体 (`w:color w:val="0000FF"`) 的段落是填写提示，应在填写内容后删除这些段落。搜索 `<w:color w:val="0000FF"/>` 定位这些段落。

**注意**：部分蓝色提示段落位于表格单元格 `<w:tc>` 内，且是该单元格的唯一段落。直接删除会导致单元格无 `<w:p>` 子元素，违反 OOXML 规范，Word 打开时会报"无法读取的内容"错误。必须使用上方的 `_safe_remove_paragraph` 函数安全删除。

同理，"重要提醒" 部分（在头部表格之后、正文之前）也应删除，可通过搜索 `重要提醒` 定位。

## 插入图片（流程图）

使用 `$SKILL_DIR/scripts/insert_image.py` 将图片插入到 unpacked DOCX 中：

```bash
python $SKILL_DIR/scripts/insert_image.py <unpacked_dir> <image.png> [--width WIDTH_CM] [--height HEIGHT_CM]
```

脚本会自动：
1. 复制图片到 `word/media/` 目录
2. 在 `word/_rels/document.xml.rels` 中添加关系条目
3. 输出关系 ID 和可直接粘贴到 `document.xml` 的 XML 段落

**使用步骤**：
1. 先运行脚本获取 XML 段落
2. 在 Python 编辑脚本中，将输出的 `<w:p>` 段落通过 `etree.fromstring()` 解析后插入到 `document.xml` 的目标位置（4.2 技术侧章节步骤描述之后）

**图片插入位置**：流程图一般插入在 4.2 技术侧章节的步骤描述之后。

**图片比例保持**：`insert_image.py` 自动读取图片原始尺寸并保持宽高比。如图片过长（如竖向长流程图），脚本会自动约束在 A4 页面范围内（最大 17cm×24cm）。XML 中使用 `<a:picLocks noChangeAspect="1"/>` 和 `<a:srcRect/>` 确保 Word 不会拉伸图片。只需指定 `--width` 参数，高度会自动按比例计算。

**图片标注段落**（居中，楷体，插在图片段落之后）：
```xml
<w:p>
  <w:pPr>
    <w:jc w:val="center"/>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>
      <w:color w:val="000000"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:color w:val="000000"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
    <w:t>图1 技术方案整体流程图</w:t>
  </w:r>
</w:p>
```

## 关键注意事项

1. **禁止使用 Read/Edit 工具直接读写 document.xml**：XML 文件通常有数千行，直接读取会消耗大量上下文导致会话不可用。必须编写 Python 脚本（使用 lxml）来操作 XML
2. **保持 XML 格式规范**：确保所有标签正确闭合
3. **使用正确的字体和字号**：标题使用微软雅黑，正文使用楷体，统一 10pt (sz=20)
4. **段落间距**：正文段落添加 `<w:spacing w:beforeLines="50" w:afterLines="50"/>` 避免段落堆叠
5. **空白处理**：文本首尾有空格时需添加 `xml:space="preserve"`
6. **不要修改模板结构**：只在空白位置填入内容或替换蓝色提示文本
7. **paraId 唯一性**：如新增段落需要 paraId，使用8位十六进制且不与已有值重复
8. **数学公式必须用 OMML 格式**：任何包含下标、上标、分数、求和、希腊字母等数学结构的表达式，必须使用 `<m:oMath>` OMML 格式写入，**严禁将公式作为纯文本放在 `<w:t>` 中**。行内引用的变量（如 c_j、x_i）和变量含义说明段落中的下标变量也必须使用行内 `<m:oMath>`。详见 [omml-formula-guide.md](omml-formula-guide.md)
9. **删除占位文字**：Python 脚本中必须删除所有包含方括号占位文本的段落（如"[流程图将在此处插入]"、"[此处插入图片]"等），这些文字不应出现在最终文档中
10. **表格单元格必须保留至少一个段落**：OOXML 规范要求每个 `<w:tc>` 至少包含一个 `<w:p>`。删除段落时（蓝色提示、占位文字等），如果被删段落是所在表格单元格的唯一段落，必须清空其内容而非删除该段落，否则 Word 会报"无法读取的内容"错误。使用上方的 `_safe_remove_paragraph` 函数处理此情况

## 数学公式

技术方案中的数学公式必须使用 OMML 格式。行内公式和独立公式的 XML 模板、语法详解和完整示例，请参考 [omml-formula-guide.md](omml-formula-guide.md)。
