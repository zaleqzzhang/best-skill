# Pipeline 参考指南

## 概述

本文档是 code-patent-writing skill 的 Stage 参考文档，说明 16 个 Stage（Stage 00-15）的输入输出关系、各 Stage 的 I/O Contract 定义、输出目录映射、以及与 DOCX 构建引擎的对接方式。

**重要**：本 skill 由 AI 智能体直接执行。智能体按 SKILL.md 的指示逐 Stage 撰写各章节 .md 文件，辅助脚本负责代码上下文提取和 DOCX 组装。

> **注意**：逻辑 Stage 编号（00-15）与物理目录编号（`stage-01` 到 `stage-12`）不同。物理目录名保持固定以兼容辅助脚本。

## 16 Stage 概览

| 逻辑 Stage | 功能 | 物理输出目录 | 关键输出文件 | 执行者 |
|------------|------|-------------|-------------|--------|
| **00** | **环境前置检查与依赖安装** | `$WORK_DIR/` | `package.json` | 辅助脚本（强制，Stage 00 必须首先执行） |
| 01 | 代码上下文提取 | `ideal/` | `code_context.md` | 辅助脚本（强制） |
| 02 | 创新点分析与 Ideal 生成 | `ideal/` | `ideal_output.md` | 智能体 |
| 03 | 目录初始化 + 发明范围 | `patent_run/stage-01/` | `goal_text.md` | 辅助脚本 + 智能体 |
| 04 | 现有技术分析 | `patent_run/stage-02/` | `prior_art.md` | 智能体 |
| 05 | **联网文献收集（强制）** | `patent_run/stage-03/` | `references.md`, `web_search_results.json` | 智能体 + 本地 Playwright |
| 06 | 关键术语 | `patent_run/stage-04/` | `key_terms.md` | 智能体 |
| 07 | 发明构思 | `patent_run/stage-05/` | `concept.md` | 智能体 |
| 08 | 背景技术 | `patent_run/stage-06/` | `background.md` | 智能体 |
| 09 | 发明内容 | `patent_run/stage-07/` | `invention_content.md` | 智能体 |
| 10 | **UI 原型与 Playwright 截图（强制）** | `patent_run/stage-08/` | `screenshots/*.png`, `figure_registry.json` | 智能体 + 本地 Playwright |
| 11 | **技术图表生成（强制，≥4 类 PNG）** | `$WORK_DIR/charts/` | `*.png`（≥4 张） | 智能体 + Mermaid CLI / image_gen |
| 12 | 专利评审 | `patent_run/stage-09/` | `reviews.md` | 智能体 |
| 13 | 专利修订 | `patent_run/stage-10/` | `revised_*.md` | 智能体 |
| 14 | 质量门禁 | `patent_run/stage-11/` | `quality_report.json` | 智能体 |
| 15 | DOCX 组装与打包（含图片嵌入） | `patent_run/stage-12/` | `patent_draft.md`, `.docx` | 辅助脚本 |

## Stage 分级与容错

16 个 Stage **全部为强制执行**，无可选 Stage：

- **环境检查阶段**（Stage 00）：必须在所有其他 Stage 之前执行，强制安装 Playwright（本地 npm）+ Mermaid CLI + Python 依赖
- **代码分析阶段**（Stage 01→02）：Stage 01 必须通过辅助脚本执行，禁止跳过
- **核心撰写阶段**（Stage 03→04→05→06→07→08→09）：任何阶段失败应降级处理；**Stage 05 文献收集为强制**，必须通过本地 Playwright 无头浏览器联网检索
- **图文生成阶段**（Stage 10→11）：**Stage 10 UI 截图为强制**（使用本地 Playwright headless）；**Stage 11 技术图表为强制**（至少 4 类 PNG）
- **质量保障阶段**（Stage 12→13→14→15）：必须执行，如果 Stage 14 质量门禁返回 `revise`，需返回 Stage 13 修订后重试（最多 2 轮）。Stage 15 DOCX 必须包含图片嵌入

## 各 Stage I/O Contract 定义

每个 Stage 的输入输出文件必须严格遵循以下 Contract。**任何 Stage 的输出文件缺失或格式不符均视为该 Stage 执行失败。**

| Stage | 输入文件 | 输出文件 | 验收标准（DoD） |
|-------|---------|---------|----------------|
| 00 | （无） | `package.json` | Playwright + Chromium + Mermaid CLI 安装成功 |
| 01 | （无，由脚本从仓库提取） | `ideal/code_context.md` | 文件 ≥1000 字符 |
| 02 | `code_context.md` | `ideal/ideal_output.md` | ≥3 个创新点，每个含 (a)(b)(c) 三段式 |
| 03 | `ideal_output.md` | `patent_run/stage-01/goal_text.md` | 包含发明名称+技术领域+发明目标+技术路线+预期效果+适用范围 |
| 04 | `goal_text.md` | `patent_run/stage-02/prior_art.md` | 3-5 个现有技术+共性不足+技术空白 |
| 05 | `prior_art.md`, `ideal_output.md` | `patent_run/stage-03/references.md`, `web_search_results.json` | references.md ≥8 篇精选引用；JSON 含 ≥20 条原始结果且符合 schema |
| 06 | `ideal_output.md` | `patent_run/stage-04/key_terms.md` | 5-6 个术语，纯段落格式 |
| 07 | `ideal_output.md` | `patent_run/stage-05/concept.md` | 2.1 核心构思 + 2.2 创新点（2-3 个五段式） |
| 08 | `ideal_output.md`, `prior_art.md` | `patent_run/stage-06/background.md` | 3.1 + 3.2 子节，≤1200 字 |
| 09 | `ideal_output.md`, 前序所有章节 | `patent_run/stage-07/invention_content.md` | 4.1+4.2+4.3 齐全，≥2 场景，≥2 扩展方案 |
| 10 | `invention_content.md`, `ideal_output.md` | `patent_run/stage-08/screenshots/*.png`, `figure_registry.json`, `code/index.html` | ≥**12** 张高清截图（含场景A逐步+场景B逐步+总览+场景切换+技术+对比），每张≥50KB；JSON 含 7 字段 schema；figure_type 区分产品侧/技术侧 |
| 11 | `invention_content.md` | `$WORK_DIR/charts/*.png` | ≥4 张高清 PNG（架构图+流程图+时序图+数据流图），白色背景，每张≥30KB |
| 12 | 前序所有章节 | `patent_run/stage-09/reviews.md` | 9 项清单+总评分+最紧急 3 项 |
| 13 | `reviews.md`, 前序章节 | `patent_run/stage-10/revised_*.md` | ≥4 个修订文件 |
| 14 | 修订后章节 | `patent_run/stage-11/quality_report.json` | JSON 符合 20+ 字段 schema；score ≥7 为 proceed |
| 15 | 所有章节 + charts/ + screenshots/ | `patent_run/stage-12/patent_draft.md`, `*.docx` | DOCX >200KB，含嵌入图片 |

**JSON schema 详细定义**：

- `web_search_results.json` → 见 SKILL.md Stage 05
- `figure_registry.json`（7 字段） → 见 SKILL.md Stage 10
- `quality_report.json`（20+ 字段） → 见 SKILL.md Stage 14

## Ideal 文档注入策略

当 Stage 02 生成了 `ideal_output.md` 时，各 Stage 应按以下策略使用 Ideal 内容：

| 逻辑 Stage | 注入强度 | 具体做法 |
|------------|---------|---------|
| 03 发明范围 | 🟢 软引导 | 参考 Ideal 中的发明名称和核心方向 |
| 04 现有技术 | 🔵 双语扩展 | 参考 Ideal 中的背景技术和检索关键词 |
| 05 文献收集 | 🔵 双语检索注入 | 从 Ideal 提取中英文检索关键词，生成跨语言检索 query |
| 06 关键术语 | 🟢 软引导 | 参考 Ideal 中的术语映射 |
| 07 发明构思 | 🟢 软引导 | 参考 Ideal 中的创新点 |
| 08 背景技术 | 🔴 强制提取 | 从 Ideal「二、背景技术」和「五、区别优势」提取素材 |
| 09 发明内容 | 🔴 全量注入 | 从 Ideal 提取创新点技术方案、应用场景、系统架构 |
| 10 UI 截图 | 🔴 强制约束 | 从 Ideal 提取产品交互描述和 GUI 可视化要求，强制生成页面原型 |
| 12 专利评审 | 🟡 对照清单 | 对照 Ideal 创新点检查覆盖率 |
| 13 专利修订 | 🟠 保护性+素材库 | 从 Ideal 提取补充材料填补评审发现的空缺 |
| 14 质量门禁 | 🔴 阻断级 | Ideal 创新点覆盖度 + 图文完整性作为阻断检查项 |

详细注入策略 → 参考 [ideal-injection-guide.md](ideal-injection-guide.md)

## 各 Stage 输出文件详解

### Stage 00 → `$WORK_DIR/package.json`
环境前置检查结果。Playwright + Chromium + Mermaid CLI 安装完成后，`$WORK_DIR/` 下会生成 `package.json` 和 `node_modules/`。

### Stage 01 → `ideal/code_context.md`
代码上下文：Git commit、diff、代码摘要、AST 签名等结构化上下文。由辅助脚本 `orchestrate.py extract-context` 生成。

### Stage 02 → `ideal/ideal_output.md`
创新点分析文档：智能体按 4 轮渐进式分析（概览扫描→深度分析→验证审查→文档生成）产出。

### Stage 03 → `patent_run/stage-01/goal_text.md`
发明范围说明书：发明名称、技术领域、发明目标、技术路线概述、预期效果、适用范围。

### Stage 04 → `patent_run/stage-02/prior_art.md`
现有技术分析报告：技术发展脉络、3-5 个现有技术方案、共性不足、技术空白、创新机会。

### Stage 05 → `patent_run/stage-03/references.md`, `web_search_results.json`
**强制联网文献收集**：通过本地 Playwright 无头浏览器检索 Google Patents / arXiv / Semantic Scholar 获取的真实文献列表。`references.md` 包含至少 8 篇精选格式化引用（专利号/DOI/标题/链接/相关性说明/精选理由）。`web_search_results.json` 包含 ≥20 条原始检索结果，符合 SKILL.md 定义的完整 JSON schema。

### Stage 06 → `patent_run/stage-04/key_terms.md`
关键术语定义：5-6 个核心术语，每个包含中英文名称、一句话定义、通俗类比。禁止表格格式。

### Stage 07 → `patent_run/stage-05/concept.md`
发明构思：2.1 核心构思（100-200 字）+ 2.2 核心创新点（2-3 个，五段式）。

### Stage 08 → `patent_run/stage-06/background.md`
背景技术：### 3.1 现有技术（2-3 种，每种≤300 字）+ ### 3.2 缺点（一句话痛点+具体场景）。≤1200 字。

### Stage 09 → `patent_run/stage-07/invention_content.md`
发明内容（最核心章节）：### 4.1 产品侧（≥2 场景，3-4 步）+ ### 4.2 技术侧（架构+算法+时序+数据流）+ ### 4.3 有益效果（2-3 段，≤400 字）+ 至少 2 个扩展方案。

### Stage 10 → `patent_run/stage-08/screenshots/*.png`, `figure_registry.json`, `code/index.html`
**强制 UI 原型与 Playwright 高清截图**：基于产品侧描述和 Ideal 文档的「附图设计建议」生成包含 8 类视图的 HTML 原型页面（场景总览、场景A逐步、场景B逐步、**产出物实例展示**、状态转换、**创新点联动总览**、方案对比），使用本地 Playwright（headless，`deviceScaleFactor: 2`，viewport ≥ 1440px）按步骤自动截图。`screenshots/` 目录下至少 **14 张**高清 PNG 截图（每张≥50KB），必须包含场景切换截图、产出物展示截图和创新点联动截图。**禁止重复截图凑数**。HTML 页面采用现代 UI 设计风格，场景最后一步必须包含实际产出物预览区。`figure_registry.json` 符合 SKILL.md 定义的完整 7 字段 JSON schema，`figure_type` 枚举新增 `product_output_preview`（产出物展示）和 `innovation_linkage`（创新点联动）。每张产品侧截图包含创新点角标和技术图引用标注。

### Stage 11 → `$WORK_DIR/charts/*.png`（≥4 张）
**强制技术图表高清生成**：至少 4 类 PNG 图表（系统架构图、技术流程图、模块时序图、数据流图）。优先使用 **HTML + 内联 SVG 连线 + Playwright 截图**（节点用 CSS 布局，所有箭头和连线用 `<svg>` + `<line>` / `<polyline>` + `<marker>` 绘制，**禁止使用 CSS `::after` 伪元素画箭头**），降级使用 Mermaid CLI 或 image_gen。每张图表≥30KB。每张技术图表右上角标注场景溯源标签（如"支撑场景A步骤2"）。

### Stage 12 → `patent_run/stage-09/reviews.md`
专利评审：9 项清单检查 + 总体评分 + 最紧急 3 项修改。

### Stage 13 → `patent_run/stage-10/revised_*.md`
修订后各章节：分隔标记 `===REVISED_KEY_TERMS===` 等。

### Stage 14 → `patent_run/stage-11/quality_report.json`
质量评分 JSON：符合 SKILL.md 定义的完整 20+ 字段 schema（score + verdict + dimension_scores + fabrication_flags 等）。

## 与 DOCX 构建引擎的对接

`patent_to_json.py` 从 `patent_run/` 读取各章节 .md 文件，转换为 `patent_content.json`：

| 物理输入文件 | JSON section key |
|-------------|-----------------|
| `stage-04/key_terms.md` | `【关键术语】` |
| `stage-05/concept.md` | `【发明构思】` |
| `stage-06/background.md` → 3.1 | `3.1` |
| `stage-06/background.md` → 3.2 | `3.2` |
| `stage-07/invention_content.md` → 4.1 | `4.1` |
| `stage-07/invention_content.md` → 4.2 | `4.2` |
| `stage-07/invention_content.md` → 4.3 | `4.3` |
| `stage-03/references.md` | `参考文献` |

`patent_builder.py` 读取 JSON，写入 DOCX 模板 XML，`insert_image.py` 嵌入图片，`office/pack.py` 打包并校验修复。

### Stage 15 → `$WORK_DIR/deliverables/`（交付物汇聚）

DOCX 打包成功后，`orchestrate.py` 自动执行交付物汇聚，将最终产物拷贝到 `deliverables/` 目录：

| deliverables/ 内路径 | 来源 |
|---------------------|------|
| `patent_draft.docx` | `$WORK_DIR/{发明名称}.docx` |
| `references.md` | `patent_run/stage-03/references.md` |
| `charts/*.png` | `$WORK_DIR/charts/*.png` |
| `code/` | `patent_run/stage-08/code/` |
| `screenshots/` | `patent_run/stage-08/screenshots/*.png` |
| `sections/` | 优先 `stage-10/revised_*.md`，回退到原始 stage 文件 |
| `ideal/` | `$WORK_DIR/ideal/`（ideal_output.md、code_context.md、context_metadata.json） |
| `figure_registry.json` | `patent_run/stage-08/figure_registry.json` |
| `manifest.json` | 动态生成（含文件清单和时间戳） |
