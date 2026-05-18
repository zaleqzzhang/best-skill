# DOCX 公式插入指南（OMML）

## 概述

DOCX 文件不支持 LaTeX 或 Markdown 格式的公式渲染。在 Word 文档中插入数学公式需使用 **OMML (Office Math Markup Language)**，即 Office 原生数学标记语言。OMML 使用命名空间 `xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"`。

## 基本结构

公式包裹在 `<m:oMathPara>` (独立公式段) 或 `<m:oMath>` (行内公式) 中。

### 行内公式

行内公式直接嵌入在 `<w:p>` 段落的 run 中：

```xml
<w:p>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
    <w:t xml:space="preserve">其中损失函数定义为 </w:t>
  </w:r>
  <m:oMath>
    <!-- 公式内容 -->
  </m:oMath>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
    <w:t xml:space="preserve"> ，其中各参数含义如下。</w:t>
  </w:r>
</w:p>
```

### 独立公式段（居中显示，带右侧编号）

长公式使用独立段落居中显示，右侧带全局序号如（1）（2）。使用制表符将公式居中、编号右对齐：

```xml
<w:p>
  <w:pPr>
    <w:tabs>
      <w:tab w:val="center" w:pos="4153"/>
      <w:tab w:val="right" w:pos="8306"/>
    </w:tabs>
    <w:spacing w:beforeLines="50" w:afterLines="50"/>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
  </w:pPr>
  <w:r><w:tab/></w:r>
  <m:oMath>
    <!-- 公式内容 -->
  </m:oMath>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
    <w:tab/>
  </w:r>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
    <w:t>（1）</w:t>
  </w:r>
</w:p>
```

**说明**：`w:tab w:val="center" w:pos="4153"` 将公式居中于页面，`w:tab w:val="right" w:pos="8306"` 将编号右对齐。第一个 `<w:tab/>` 将公式推到中心制表位，第二个 `<w:tab/>` 将编号推到右侧制表位。编号使用全角括号（1）（2）（3）...，全文连续编号。

### 公式变量含义说明

每个独立公式后必须紧跟一段变量含义说明，格式为"其中，..."。

**关键规则：变量含义说明中的变量也必须使用 OMML 格式**。只要变量包含下标、上标、希腊字母等数学结构（如 y_i、ŷ_i、c_j），就必须用行内 `<m:oMath>` 嵌入，不能写成纯文本 `y_i`、`c_j` 这样的 Markdown 下标形式。纯英文字母或数字的简单变量（如 n、K、e）可以直接用 `<w:t>` 文本。

**正确示例**（包含下标变量的含义说明）：

```xml
<w:p>
  <w:pPr>
    <w:spacing w:beforeLines="50" w:afterLines="50"/>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
    <w:t xml:space="preserve">其中，n 为样本总数，</w:t>
  </w:r>
  <m:oMath>
    <m:sSub>
      <m:e><m:r><m:t>y</m:t></m:r></m:e>
      <m:sub><m:r><m:t>i</m:t></m:r></m:sub>
    </m:sSub>
  </m:oMath>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
    <w:t xml:space="preserve"> 为第 i 个样本的真实值，</w:t>
  </w:r>
  <m:oMath>
    <m:sSub>
      <m:e><m:r><m:t>ŷ</m:t></m:r></m:e>
      <m:sub><m:r><m:t>i</m:t></m:r></m:sub>
    </m:sSub>
  </m:oMath>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:sz w:val="20"/>
      <w:szCs w:val="20"/>
    </w:rPr>
    <w:t xml:space="preserve"> 为第 i 个样本的预测值。</w:t>
  </w:r>
</w:p>
```

**错误示例**（以下写法严禁使用）：
```xml
<!-- 错误！下标变量 y_i 不能作为纯文本放在 <w:t> 中 -->
<w:t>其中，n 为样本总数，y_i 为第 i 个样本的真实值</w:t>
```

## 常用公式元素

### 普通文本/变量 `<m:r>`

```xml
<m:r>
  <m:rPr><m:sty m:val="p"/></m:rPr>
  <m:t>x</m:t>
</m:r>
```

`m:sty` 样式值：`p` 普通、`b` 粗体、`i` 斜体（变量默认）、`bi` 粗斜体。

### 分数 `<m:f>`

LaTeX: `\frac{a+b}{c}`

```xml
<m:f>
  <m:num>
    <m:r><m:t>a+b</m:t></m:r>
  </m:num>
  <m:den>
    <m:r><m:t>c</m:t></m:r>
  </m:den>
</m:f>
```

### 上标 `<m:sSup>`

LaTeX: `x^2`

```xml
<m:sSup>
  <m:e>
    <m:r><m:t>x</m:t></m:r>
  </m:e>
  <m:sup>
    <m:r><m:t>2</m:t></m:r>
  </m:sup>
</m:sSup>
```

### 下标 `<m:sSub>`

LaTeX: `x_i`

```xml
<m:sSub>
  <m:e>
    <m:r><m:t>x</m:t></m:r>
  </m:e>
  <m:sub>
    <m:r><m:t>i</m:t></m:r>
  </m:sub>
</m:sSub>
```

### 上下标 `<m:sSubSup>`

LaTeX: `x_i^2`

```xml
<m:sSubSup>
  <m:e>
    <m:r><m:t>x</m:t></m:r>
  </m:e>
  <m:sub>
    <m:r><m:t>i</m:t></m:r>
  </m:sub>
  <m:sup>
    <m:r><m:t>2</m:t></m:r>
  </m:sup>
</m:sSubSup>
```

### 根号 `<m:rad>`

LaTeX: `\sqrt{x+1}`

```xml
<m:rad>
  <m:radPr><m:degHide m:val="1"/></m:radPr>
  <m:deg/>
  <m:e>
    <m:r><m:t>x+1</m:t></m:r>
  </m:e>
</m:rad>
```

N 次根号（如 `\sqrt[3]{x}`）：

```xml
<m:rad>
  <m:deg>
    <m:r><m:t>3</m:t></m:r>
  </m:deg>
  <m:e>
    <m:r><m:t>x</m:t></m:r>
  </m:e>
</m:rad>
```

### 求和 `<m:nary>`

LaTeX: `\sum_{i=1}^{n} x_i`

```xml
<m:nary>
  <m:naryPr>
    <m:chr m:val="∑"/>
  </m:naryPr>
  <m:sub>
    <m:r><m:t>i=1</m:t></m:r>
  </m:sub>
  <m:sup>
    <m:r><m:t>n</m:t></m:r>
  </m:sup>
  <m:e>
    <m:sSub>
      <m:e><m:r><m:t>x</m:t></m:r></m:e>
      <m:sub><m:r><m:t>i</m:t></m:r></m:sub>
    </m:sSub>
  </m:e>
</m:nary>
```

积分：将 `m:chr` 改为 `∫`；连乘：改为 `∏`。

### 括号 `<m:d>`

LaTeX: `\left( x+1 \right)`

```xml
<m:d>
  <m:dPr>
    <m:begChr m:val="("/>
    <m:endChr m:val=")"/>
  </m:dPr>
  <m:e>
    <m:r><m:t>x+1</m:t></m:r>
  </m:e>
</m:d>
```

方括号：`m:begChr="["`, `m:endChr="]"`；大括号：`m:begChr="{"`, `m:endChr="}"`。

### 函数 `<m:func>`

用于 log、sin、cos、max、min 等函数名。函数名使用 `<m:fName>` 包裹，参数使用 `<m:e>` 包裹。

**示例1**：`log_2(N)` — 带下标的对数函数

```xml
<m:func>
  <m:fName>
    <m:sSub>
      <m:e>
        <m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>log</m:t></m:r>
      </m:e>
      <m:sub>
        <m:r><m:t>2</m:t></m:r>
      </m:sub>
    </m:sSub>
  </m:fName>
  <m:e>
    <m:d>
      <m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>
      <m:e>
        <m:r><m:t>N</m:t></m:r>
      </m:e>
    </m:d>
  </m:e>
</m:func>
```

注意：`<m:e>` 中的括号 `<m:d>` 内包含函数的所有参数（此处为 N），不能遗漏任何参数。函数名使用 `m:sty m:val="p"` 保持正体（不斜体）。

**示例2**：`max(a, b)` — 简单函数

```xml
<m:func>
  <m:fName>
    <m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>max</m:t></m:r>
  </m:fName>
  <m:e>
    <m:d>
      <m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>
      <m:e>
        <m:r><m:t>a,b</m:t></m:r>
      </m:e>
    </m:d>
  </m:e>
</m:func>
```

### 矩阵 `<m:m>`

LaTeX: `\begin{bmatrix} a & b \\ c & d \end{bmatrix}`

```xml
<m:d>
  <m:dPr>
    <m:begChr m:val="["/>
    <m:endChr m:val="]"/>
  </m:dPr>
  <m:e>
    <m:m>
      <m:mr>
        <m:e><m:r><m:t>a</m:t></m:r></m:e>
        <m:e><m:r><m:t>b</m:t></m:r></m:e>
      </m:mr>
      <m:mr>
        <m:e><m:r><m:t>c</m:t></m:r></m:e>
        <m:e><m:r><m:t>d</m:t></m:r></m:e>
      </m:mr>
    </m:m>
  </m:e>
</m:d>
```

### 上划线/下划线

上划线 (`\overline{x}`)：
```xml
<m:bar>
  <m:barPr><m:pos m:val="top"/></m:barPr>
  <m:e><m:r><m:t>x</m:t></m:r></m:e>
</m:bar>
```

### 希腊字母和特殊符号

在 `<m:t>` 中直接使用 Unicode 字符：

| 符号 | Unicode | LaTeX |
|------|---------|-------|
| α | α | \alpha |
| β | β | \beta |
| γ | γ | \gamma |
| δ | δ | \delta |
| θ | θ | \theta |
| λ | λ | \lambda |
| μ | μ | \mu |
| σ | σ | \sigma |
| ∞ | ∞ | \infty |
| ≤ | ≤ | \leq |
| ≥ | ≥ | \geq |
| ≠ | ≠ | \neq |
| ∈ | ∈ | \in |
| → | → | \rightarrow |

## 完整公式示例

### 示例1：均方误差（MSE）— 带编号的独立公式

LaTeX: `MSE = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2`

```xml
<!-- 公式段落：居中公式 + 右对齐编号 -->
<w:p>
  <w:pPr>
    <w:tabs>
      <w:tab w:val="center" w:pos="4153"/>
      <w:tab w:val="right" w:pos="8306"/>
    </w:tabs>
    <w:spacing w:beforeLines="50" w:afterLines="50"/>
  </w:pPr>
  <w:r><w:tab/></w:r>
  <m:oMath>
    <m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>MSE</m:t></m:r>
    <m:r><m:t>=</m:t></m:r>
    <m:f>
      <m:num><m:r><m:t>1</m:t></m:r></m:num>
      <m:den><m:r><m:t>n</m:t></m:r></m:den>
    </m:f>
    <m:nary>
      <m:naryPr><m:chr m:val="∑"/></m:naryPr>
      <m:sub><m:r><m:t>i=1</m:t></m:r></m:sub>
      <m:sup><m:r><m:t>n</m:t></m:r></m:sup>
      <m:e>
        <m:sSup>
          <m:e>
            <m:d>
              <m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>
              <m:e>
                <m:sSub>
                  <m:e><m:r><m:t>y</m:t></m:r></m:e>
                  <m:sub><m:r><m:t>i</m:t></m:r></m:sub>
                </m:sSub>
                <m:r><m:t>-</m:t></m:r>
                <m:sSub>
                  <m:e><m:r><m:t>ŷ</m:t></m:r></m:e>
                  <m:sub><m:r><m:t>i</m:t></m:r></m:sub>
                </m:sSub>
              </m:e>
            </m:d>
          </m:e>
          <m:sup><m:r><m:t>2</m:t></m:r></m:sup>
        </m:sSup>
      </m:e>
    </m:nary>
  </m:oMath>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>
      <w:sz w:val="20"/><w:szCs w:val="20"/>
    </w:rPr>
    <w:tab/>
  </w:r>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>
      <w:sz w:val="20"/><w:szCs w:val="20"/>
    </w:rPr>
    <w:t>（1）</w:t>
  </w:r>
</w:p>
<!-- 变量含义说明段落：下标变量必须使用行内 <m:oMath> -->
<w:p>
  <w:pPr>
    <w:spacing w:beforeLines="50" w:afterLines="50"/>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>
      <w:sz w:val="20"/><w:szCs w:val="20"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:sz w:val="20"/><w:szCs w:val="20"/>
    </w:rPr>
    <w:t xml:space="preserve">其中，n 为样本总数，</w:t>
  </w:r>
  <m:oMath>
    <m:sSub>
      <m:e><m:r><m:t>y</m:t></m:r></m:e>
      <m:sub><m:r><m:t>i</m:t></m:r></m:sub>
    </m:sSub>
  </m:oMath>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:sz w:val="20"/><w:szCs w:val="20"/>
    </w:rPr>
    <w:t xml:space="preserve"> 为第 i 个样本的真实值，</w:t>
  </w:r>
  <m:oMath>
    <m:sSub>
      <m:e><m:r><m:t>ŷ</m:t></m:r></m:e>
      <m:sub><m:r><m:t>i</m:t></m:r></m:sub>
    </m:sSub>
  </m:oMath>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:sz w:val="20"/><w:szCs w:val="20"/>
    </w:rPr>
    <w:t xml:space="preserve"> 为模型对第 i 个样本的预测值。MSE 值越小，表示预测值与真实值之间的偏差越小。</w:t>
  </w:r>
</w:p>
```

### 示例2：Softmax 函数 — 带编号的独立公式

LaTeX: `\sigma(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}`

```xml
<!-- 公式段落：居中公式 + 右对齐编号 -->
<w:p>
  <w:pPr>
    <w:tabs>
      <w:tab w:val="center" w:pos="4153"/>
      <w:tab w:val="right" w:pos="8306"/>
    </w:tabs>
    <w:spacing w:beforeLines="50" w:afterLines="50"/>
  </w:pPr>
  <w:r><w:tab/></w:r>
  <m:oMath>
    <m:r><m:t>σ</m:t></m:r>
    <m:d>
      <m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>
      <m:e>
        <m:sSub>
          <m:e><m:r><m:t>z</m:t></m:r></m:e>
          <m:sub><m:r><m:t>i</m:t></m:r></m:sub>
        </m:sSub>
      </m:e>
    </m:d>
    <m:r><m:t>=</m:t></m:r>
    <m:f>
      <m:num>
        <m:sSup>
          <m:e><m:r><m:t>e</m:t></m:r></m:e>
          <m:sup>
            <m:sSub>
              <m:e><m:r><m:t>z</m:t></m:r></m:e>
              <m:sub><m:r><m:t>i</m:t></m:r></m:sub>
            </m:sSub>
          </m:sup>
        </m:sSup>
      </m:num>
      <m:den>
        <m:nary>
          <m:naryPr><m:chr m:val="∑"/></m:naryPr>
          <m:sub><m:r><m:t>j=1</m:t></m:r></m:sub>
          <m:sup><m:r><m:t>K</m:t></m:r></m:sup>
          <m:e>
            <m:sSup>
              <m:e><m:r><m:t>e</m:t></m:r></m:e>
              <m:sup>
                <m:sSub>
                  <m:e><m:r><m:t>z</m:t></m:r></m:e>
                  <m:sub><m:r><m:t>j</m:t></m:r></m:sub>
                </m:sSub>
              </m:sup>
            </m:sSup>
          </m:e>
        </m:nary>
      </m:den>
    </m:f>
  </m:oMath>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>
      <w:sz w:val="20"/><w:szCs w:val="20"/>
    </w:rPr>
    <w:tab/>
  </w:r>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>
      <w:sz w:val="20"/><w:szCs w:val="20"/>
    </w:rPr>
    <w:t>（2）</w:t>
  </w:r>
</w:p>
<!-- 变量含义说明段落：下标变量必须使用行内 <m:oMath> -->
<w:p>
  <w:pPr>
    <w:spacing w:beforeLines="50" w:afterLines="50"/>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>
      <w:sz w:val="20"/><w:szCs w:val="20"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:sz w:val="20"/><w:szCs w:val="20"/>
    </w:rPr>
    <w:t xml:space="preserve">其中，</w:t>
  </w:r>
  <m:oMath>
    <m:r><m:t>σ</m:t></m:r>
    <m:d>
      <m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>
      <m:e>
        <m:sSub>
          <m:e><m:r><m:t>z</m:t></m:r></m:e>
          <m:sub><m:r><m:t>i</m:t></m:r></m:sub>
        </m:sSub>
      </m:e>
    </m:d>
  </m:oMath>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:sz w:val="20"/><w:szCs w:val="20"/>
    </w:rPr>
    <w:t xml:space="preserve"> 为第 i 个类别的 Softmax 输出概率，</w:t>
  </w:r>
  <m:oMath>
    <m:sSub>
      <m:e><m:r><m:t>z</m:t></m:r></m:e>
      <m:sub><m:r><m:t>i</m:t></m:r></m:sub>
    </m:sSub>
  </m:oMath>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>
      <w:sz w:val="20"/><w:szCs w:val="20"/>
    </w:rPr>
    <w:t xml:space="preserve"> 为第 i 个类别的原始分数（logit），K 为类别总数，e 为自然对数的底数。所有类别的 Softmax 输出之和为 1。</w:t>
  </w:r>
</w:p>
```

## 命名空间声明

确保 `document.xml` 的根元素 `<w:document>` 包含 math 命名空间声明：

```xml
xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
```

如模板已有此声明则无需额外添加。

## 注意事项

1. **不要使用 LaTeX 或 Markdown 公式语法**，DOCX 无法渲染这些格式
2. 公式中的普通文本（如函数名 log, sin）使用 `<m:rPr><m:sty m:val="p"/></m:rPr>` 防止变为斜体
3. 希腊字母直接在 `<m:t>` 中使用 Unicode 字符
4. 复杂公式可嵌套组合上述基本元素
5. **严禁将数学公式作为纯文本放在 `<w:t>` 中**，即使公式看起来很简单（如 `y = ax + b`），只要包含变量下标、上标、分数、求和等数学结构，就必须使用 OMML 格式
6. **长公式**必须使用独立段落居中显示，右侧带全局编号（1）（2）...，公式后紧跟变量含义说明段落
7. **短公式**（如单个变量、简单表达式）直接嵌入行内文本，使用 `<m:oMath>` 行内公式
8. 公式编号全文连续递增，使用全角括号
9. **行内公式覆盖范围**：不仅独立公式段落中的公式要用 OMML，正文段落中引用的变量（如 c_j、x_i、log_2(N)）也必须使用行内 `<m:oMath>` 格式，禁止以纯文本下划线形式（如 `c_j`、`x_i`）出现在 `<w:t>` 中
10. **变量含义说明段落中的变量也必须用 OMML**：公式后的"其中，..."说明段落中，如果变量包含下标/上标/希腊字母等结构，必须用行内 `<m:oMath>` 嵌入，不能写成纯文本
11. **公式参数完整性**：OMML 公式中的每个变量和参数都必须完整写入，不能遗漏。例如 `log_2(N)` 中的 `N` 必须在 `<m:d>` 括号内的 `<m:e>` 中包含，`f(x)` 中的 `x` 必须在括号内
