# code-patent-writing — 代码专利交底书自动生成

一个自包含的 AI 智能体技能（Skill），从代码仓库自动生成符合中国专利申请规范的发明专利技术交底书（`.docx` 格式）。

## 核心特性

- **端到端自动化**：输入代码仓库路径或远程 Git URL → 输出标准 .docx 交底书
- **智能发明代码提取**：基于 Git 状态自动区分"本地发明"与"开源现有技术"，支持 AST 签名索引、Import 依赖图分析
- **15 Stage 流水线**：代码提取→创新点分析→发明范围→现有技术→术语→构思→背景→内容→UI→流程图→评审→修订→质量门禁→DOCX 输出
- **图文并茂**：产品侧 ≥14 张高清 GUI 截图（含逐步交互图、场景切换对比图、产出物实例展示图、创新点联动总览图），技术侧 4+ 张高清技术图表（架构图、流程图、时序图、数据流图，内联 SVG 连线确保箭头100%渲染）
- **高清图表输出**：Mermaid 3x 缩放白色背景渲染、Playwright 2x 设备像素比截图、HTML 原型采用现代 UI 设计风格
- **三层质量保障**：写作规范（预防）→ 自我评审+质量门禁（检测）→ 输出清洗（修复）
- **12 条阻断规则 + 9 维加权评分**：严格的质量门禁体系（含截图数量、场景切换、文件大小检查）
- **19 词 AI 味黑名单 + 防膨胀硬约束**：确保输出无 AI 痕迹
- **占位符自动清洗**：修订标记（`===REVISED_*===`）和变更日志自动剥离，header 待填写字段自动填充

## 架构

```
智能体读取 SKILL.md
    ├── Stage 01: orchestrate.py extract-context → code_context.md
    │        └─ repo_analyzer.py（发明代码提取引擎）
    ├── Stage 02: 智能体自行分析代码 → ideal_output.md
    ├── Stage 03-10: 智能体按各 Stage 撰写 → patent_run/各章节.md
    ├── Stage 11: 智能体生成 Mermaid 流程图
    ├── Stage 12-14: 评审→修订→质量门禁（含重试循环）
    ├── Stage 15: orchestrate.py build-docx → 交底书.docx
    │        ├─ patent_to_json.py（MD→JSON 转换）
    │        ├─ patent_builder.py（DOCX 构建引擎）
    │        └─ office/（OOXML 工具包）
    └── 辅助: insert_image / gen_flowchart.sh / extract_content
```

## 发明代码提取逻辑

整个流水线的核心起点。由 `orchestrate.py` 进行归属判定，再调用 `repo_analyzer.py` 的 `extract_code_context()` 提取结构化上下文。

### 输入源解析（orchestrate.py）

用户输入可以是本地路径或远程 Git URL：

| 输入类型 | 行为 |
|---------|------|
| 本地路径（如 `/path/to/repo`） | 直接使用，无需拉取代码 |
| 远程 Git URL（`https://`、`git@` 等） | 先 `git clone --depth=1` 到本地临时目录，再进行后续分析 |

### 归属判定策略（orchestrate.py `_detect_repo_mode()`）

根据仓库 Git 状态，分为四种场景、两种模式：

| 仓库状态 | 判定模式 | 发明范围 |
|---------|---------|---------|
| 无 `.git`（普通目录） | `full_ownership` | 整个项目视为用户自有发明 |
| 有 `.git` + 无远端追踪分支 | `full_ownership` | 所有 commit 均视为用户自有发明 |
| 有 `.git` + 有远端追踪分支 + **无**未推送 commit | `full_ownership` | 整个项目视为用户自有发明 |
| 有 `.git` + 有远端追踪分支 + **有**未推送 commit | `diff_only` | 远端已推送代码视为"开源现有技术"，仅本地未推送的 commit 代表用户自己的发明 |

### 代码提取（repo_analyzer.py）

#### Git 仓库模式

`repo_analyzer.py` 检测到 `.git` 后调用 `_extract_git_context()`，提取以下内容：

| 提取项 | 说明 |
|-------|------|
| 未推送 commit 列表 | `git log @{u}..HEAD --oneline`；无 upstream 则取全部 commit |
| Diff 统计 | `git diff @{u}..HEAD --stat` |
| 完整 Diff | `git diff @{u}..HEAD`，上限 60,000 字符 |
| 变更文件完整代码 | 从 diff stat 解析变更路径，读取完整文件（最多 30 文件，每文件 5,000 字符） |
| 文档摘要 | 扫描 root 和一级子目录的 .md 文件 |

变更文件按优先级排序：入口文件（main.py/app.py）> 源代码 > 配置 > 文档 > 测试。

> **注意**：在 `full_ownership` 模式下（无 upstream 或无未推送 commit），diff/变更文件可能为空。此时全量代码内容主要通过下面的 Full Analysis 模式补充。

#### 普通目录模式

无 `.git` 时调用 `_extract_dir_context()`，提取：目录树（3 层）、入口/配置文件（12 种）、核心代码摘要、文档摘要。

### Full Analysis 模式（`--full`，orchestrate.py 默认开启）

无论 Git 模式还是普通目录模式，均可叠加运行全量分析：

| 分析项 | 说明 |
|-------|------|
| **AST 签名索引** | Python `ast` 模块解析所有 .py 文件，提取 class/function 签名（含参数类型、返回值、装饰器） |
| **Import 依赖图** | 解析 import 关系，构建内部模块依赖图，识别核心模块（fan-in ≥ 2） |
| **测试覆盖提示** | 扫描 `test_*.py` 文件名，推断功能覆盖情况 |
| **全量代码扫描** | 40 个文件、每文件 5,000 字、总计 200,000 字符上限 |

> 在 `full_ownership` 模式下，全量代码扫描是发明代码的**主要来源**；在 `diff_only` 模式下，全量代码作为 diff 变更文件的**补充上下文**。

### 文件过滤规则

- **白名单后缀**：`.py`, `.js`, `.ts`, `.tsx`, `.go`, `.java`, `.kt`, `.swift`, `.c`, `.cpp`, `.rs`, `.md`, `.yaml`, `.json`, `.toml` 等 22 种
- **目录黑名单**：`node_modules`, `__pycache__`, `.git`, `dist`, `build`, `.venv`, `target`, `vendor` 等 14 个

## 目录结构

```
code-patent-writing/
├── SKILL.md                          # Skill 主定义文件（15 Stage 工作流程指南）
├── README.md                         # 本说明文档
├── assets/
│   └── 发明专利技术交底书模板.docx    # 交底书 Word 模板
├── references/                       # 参考文档（10 份）
│   ├── writing-style-guide.md        # 写作规范
│   ├── quality-rubric.md             # 质量评估规程
│   ├── llm-output-cleaning-guide.md  # 输出清洗规程
│   ├── ideal-injection-guide.md      # Ideal 注入策略指南
│   ├── code-analysis-guide.md        # 代码分析指南
│   ├── pipeline-integration-guide.md # Stage 参考指南
│   ├── json-content-guide.md         # patent_content.json 编写指南
│   ├── omml-formula-guide.md         # OMML 公式指南
│   ├── patent-template-format.md     # 模板格式参考
│   └── docx-editing-guide.md         # DOCX XML 编辑参考
└── scripts/                          # 辅助脚本
    ├── orchestrate.py                # 编排器（extract-context / init-patent-run / build-docx）
    ├── repo_analyzer.py              # 发明代码提取引擎（Git 归属判定 + AST + Import 图）
    ├── patent_to_json.py             # Markdown→JSON 桥接器（5 策略子节提取）
    ├── patent_builder.py             # DOCX 构建引擎（OOXML 操作）
    ├── insert_image.py               # 图片插入工具（PNG/JPEG，自动等比缩放）
    ├── extract_content.py            # 文档提取工具（PDF/DOCX/PPTX）
    ├── gen_flowchart.sh              # Mermaid 流程图渲染
    └── office/                       # OOXML 处理工具包
        ├── unpack.py                 # 解压 DOCX（pretty-print + merge runs）
        ├── pack.py                   # 打包 DOCX（XSD 校验 + 自动修复）
        ├── validate.py               # XSD 校验 CLI
        ├── soffice.py                # LibreOffice 沙箱辅助
        ├── helpers/                  # merge_runs / simplify_redlines
        ├── validators/               # DOCX/PPTX/Redlining 校验器
        └── schemas/                  # OOXML XSD schema 文件（ISO/ECMA/Microsoft）
```

## 快速开始

### 环境准备

```bash
# 仅需安装 DOCX 组装依赖
pip install defusedxml lxml

# （可选）安装 Mermaid CLI（流程图渲染为 PNG）
npm install -g @mermaid-js/mermaid-cli
```

### 使用方式

本 skill 设计为由 AI 智能体加载执行。安装到 CodeBuddy 等智能体后，对话中提及"专利"、"交底书"、"代码专利"等关键词即自动触发。

智能体会按 SKILL.md 中的 15 Stage 流程自动执行：
1. 调用 `orchestrate.py extract-context` 提取代码上下文（Stage 01）
2. 分析代码创新点，生成 Ideal 文档（Stage 02）
3. 逐 Stage 撰写各章节（Stage 03-10）
4. 生成 Mermaid 流程图（Stage 11）
5. 评审→修订→质量门禁循环（Stage 12-14）
6. 调用 `orchestrate.py build-docx` 组装 DOCX（Stage 15）

### 手动分步执行

```bash
# 1. 提取代码上下文（支持本地路径或远程 Git URL）
python scripts/orchestrate.py extract-context /path/to/repo --name "发明名称" --full

# 2. 初始化 patent_run 目录
python scripts/orchestrate.py init-patent-run /path/to/_patent_发明名称

# 3. （由智能体完成各章节撰写后）组装 DOCX
python scripts/orchestrate.py build-docx /path/to/_patent_发明名称 --name "发明名称"
```

## DOCX 组装流水线

```
patent_run/ 各 stage 的 .md 文件
    │
    ▼  patent_to_json.py（5 策略子节提取）
patent_content.json（声明式章节描述）
    │
    ▼  office/unpack.py
解压后的 DOCX 模板目录
    │
    ▼  patent_builder.py（lxml 操作 OOXML）
填充后的 document.xml
    │
    ▼  office/pack.py（XSD 校验 + ZIP 打包）
最终 .docx 文件
```

## 输出物

运行完成后，所有最终交付物自动汇聚到 `deliverables/` 目录：

```
deliverables/
├── manifest.json                 # 交付物清单
├── patent_draft.docx             # 专利交底书 Word（含图表）
├── references.md                 # 参考文献（≥8 篇精选引用）
├── figure_registry.json          # 附图注册表
├── charts/                       # 高清技术图表（架构图+流程图+时序图+数据流图）
├── code/                         # 产品原型 HTML
├── sections/                     # 各章节最终版 Markdown
│   ├── key_terms.md
│   ├── concept.md
│   ├── background.md
│   └── invention_content.md
├── ideal/                        # Ideal 文档及代码上下文
│   ├── ideal_output.md
│   ├── code_context.md
│   └── context_metadata.json
└── screenshots/                  # 高清 GUI 截图（≥14 张，含产出物展示和创新点联动）
```

**patent_draft.docx** 包含：
- 头部表格（发明名称、涉及产品和技术、专利保护目的）
- 关键术语（5-6 个，含通俗类比）
- 发明构思（2-3 个创新点，五段式）
- 背景技术（3.1 技术演进 + 3.2 各方案缺点）
- 发明内容（4.1 产品侧含 ≥14 张 GUI 截图 + 4.2 技术侧含 6 子段深度模板 + 4.3 有益效果）
- 高清技术图表（架构图、流程图、时序图、数据流图，白色背景 3x 缩放）
- 高清 GUI 截图（2x 像素密度，含场景逐步交互图和场景切换对比图）
- 参考文献（≥8 篇精选引用）
