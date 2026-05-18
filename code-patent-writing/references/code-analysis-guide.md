# 代码分析与专利内容提取指南

## 概述

本指南说明 code-patent-writing 如何从代码仓库中提取专利创新点。分析工作由 AI 智能体（如 CodeBuddy）按以下四轮渐进式流程完成，辅助脚本 `repo_analyzer.py` 负责代码上下文提取（Git 操作、文件扫描、AST 分析），产出的 Ideal 文档作为后续专利撰写的输入。

## 自动分析流程（四个 Round）

### Round 1a — 概览扫描

输入 Git 仓库的 commit 记录和变更文件统计（`git diff --stat`），将文件分为：
- **创新文件**：实现独特算法、分析引擎、智能生成策略的核心文件
- **基础设施文件**：流水线调度、配置管理、CLI 解析等通用工程代码

产出 `scan_result.json`：含 `recommended_focus_files`（5-8 个重点文件）和 `preliminary_innovations`（初步创新方向）。

### Round 1b — 深度创新分析

传入创新相关文件的完整代码给 LLM，提取结构化 JSON：
- `invention_title`（中英双语发明名称）
- `innovations`（**2-4 个**创新点，严禁超过 4 个。根据 Round 1a 分类结果选择字段集）
- `bilingual_term_mapping`（8-15 个中英术语映射）
- `system_architecture`（分层架构、核心模块、模块交互、数据流）
- `product_interaction`（条件触发：仅当代码有 CLI/Web 交互时）
- `application_scenarios`（Before/After 对比场景）

#### 深度分析 JSON Schema（完整字段要求）

每个 `innovations[]` 对象根据创新层次选择**模块级字段集**或**系统级字段集**：

**模块级创新字段集**（适用于单模块算法创新）：

```json
{
  "name": "创新点名称（中文）",
  "name_en": "Innovation name in English",
  "innovation_level": "module",
  "problem_solved": "解决的技术问题（2-3句话，附 [file: xxx, func: yyy] 证据）",
  "concrete_example": "端到端案例（3-5句话，30秒规则：不懂编程的人能理解）",
  "technical_approach": "技术方案（先白话概括，再分步描述）",
  "advantage": "相比现有技术的优势（用案例对比）",
  "english_keywords": ["3-5个概念性英文术语，禁止代码函数名"],
  "quantitative_improvement": "量化改善（只保留最关键的2个精确数字）",
  "code_evidence": ["[file: path/to/file.py, func: core_function]"],
  "key_data_structures": ["CodeContext(repo_path, ...)"],
  "algorithm_pseudocode": "3-5行含参数和分支的伪代码"
}
```

**系统级创新字段集**（适用于多模块协同的产品级/系统级创新）：

```json
{
  "name": "创新点名称（中文）",
  "name_en": "Innovation name in English",
  "innovation_level": "system",
  "problem_solved": "解决的技术问题（2-3句话，从用户/产品角度描述）",
  "concrete_example": "端到端案例（3-5句话，30秒规则）",
  "technical_approach": "技术方案（先白话概括，再分步描述）",
  "advantage": "相比现有技术的优势（用案例对比）",
  "english_keywords": ["3-5个概念性英文术语"],
  "quantitative_improvement": "量化改善（端到端效果，如'从2周缩短到3小时'）",
  "system_evidence": ["[modules: module_a + module_b + module_c]"],
  "capability_description": "系统作为整体具备的前所未有的新能力（1-2句话）",
  "user_value_proposition": "Before/After 格式的用户价值变化描述"
}
```

> **选择规则**：2-4 个创新点中，至少 1 个应为系统级创新（`innovation_level: "system"`）。

#### 字段精确度对照表

| 字段 | 不合格示例 | 合格示例 |
|------|-----------|---------|
| `code_evidence` | `[file: ideal_generator.py]` | `[file: ideal_generator.py, func: _collect_full_diff]` |
| `key_data_structures` | "理想方案上下文对象" | `CodeContext(repo_path, is_git_repo, unpushed_commits, full_diff, ...)` |
| `algorithm_pseudocode` | "系统先分析再生成" | 3-5行含参数和分支的 Python 伪代码 |
| `quantitative_improvement` | "约3步减少到2步" | "单次改动正文最多保留 60000 字符，变更文件正文最多汇总 80000 字符" |
| `concrete_example` | "用户提交数据后系统处理并返回结果" | "工程师小李把仓库路径交给系统，系统先只看他未推送的改动..." |

#### 取证思维链（推荐）

深度分析输出建议以 2-3 行验证思路开头，例如：
```
先基于候选文件做二次取证，重点核对 ideal_generator、_ideal、_patent 中的实际函数与数据结构。
已确认两条主线有明确代码抓手：一条是"代码仓库→发明上下文→多阶段注入"，另一条是"专利文本→图表/UI原型→文档"。
```
这样可以提升深度分析输出中代码证据的准确性。

### Round 1.5 — 验证审查（专利授权性三问筛选）

由"严格专利审查员"角色审查每个创新点，使用**专利授权性三问**做 PASS / REJECT / MERGE 判定：

> **三问筛选标准**（必须同时满足三问才能 PASS）：
> 1. **技术问题具体性**：该创新点是否解决了一个具体的技术问题，而非通用工程需求？
> 2. **方案区别性**：技术方案是否包含至少一个区别于现有方法的关键步骤？
> 3. **效果可量化性**：是否产生了可量化或可观测的技术效果？

**通用工程实践排除清单**（以下类型作为**孤立功能**时必须 REJECT 或 MERGE）：
- 文件格式转换/导出（Markdown→DOCX、JSON→XML 等）— **但如果**格式转换是端到端自动化系统不可缺少的输出环节，且该端到端系统整体具备新颖性，则不排除系统级创新
- UI/Demo 自动生成 — **但如果**UI 自动生成涉及从非 UI 代码（如后端算法/纯代码仓库）自动推导界面结构和交互流程，属于"算法到界面的自动映射"创新，不排除
- 图表/可视化渲染 — **但如果**图表是从非可视化数据源（如代码仓库、文本文档）自动推导技术架构/流程并渲染，属于"结构化信息自动可视化"创新，不排除
- CLI 参数解析、配置管理、日志记录
- 标准化的数据序列化/反序列化

> **排除原则**：排除清单的目的是过滤**孤立的工程模块**，而非过滤**端到端系统的子组件**。判断标准：如果移除该模块后，系统的核心价值主张不受影响，则该模块是孤立的，应排除；如果移除后系统的端到端能力断裂，则不应排除。

REJECT 的创新点被移除，MERGE 的被合并。**最终保留 2-3 个核心创新点（硬上限 3 个，硬下限 2 个）**。

### Round 2 — 文档生成（3 段分段）

分 3 段生成完整的 Ideal 文档：
- **Segment A**：通俗概述、发明名称、核心创新点、检索关键词、应用场景
- **Segment B**（**必填，不可跳过**）：产品表现特征、附图设计建议
- **Segment C**：技术改进详细梳理（技术领域、背景技术、发明内容、技术方案架构）

最终拼接为 `ideal_output.md`。

#### Segment B 必填内容详细要求

**产品表现特征**（必填）：
1. 列出至少 2 个差异化使用场景，说明每个场景的主要用户、交互形式、主要输入/输出
2. 提供场景间 GUI 切换对比表（至少 6 个对比维度）
3. 描述 CLI 交互模式（如有），说明不同模式下的典型表现
4. 为每个创新点描述其 GUI 可视化体现

**附图设计建议**（必填，产品侧 5 张 + 技术侧 4 张 = 至少 9 张图的设计规范）：

每张图必须使用**四段式结构**：
- **图面内容描述**：该图展示什么、从什么视角
- **关键元素**：图中必须包含的核心元素清单
- **标注说明**：箭头含义、颜色区分、文字标注方式
- **产出物/联动要素**：该图中应嵌入哪些实际产出物预览或交叉引用标签

产品侧 5 张图：应用场景总览图 + GUI 交互流程图 + 场景切换对比图 + **产出物案例展示图** + **创新点联动总览图**
技术侧 4 张图：系统架构图 + 核心算法流程图 + 模块间时序图 + 数据流向图（技术图表连线必须使用内联 SVG 绘制）

末尾必须提供**附图组合建议**和篇幅受限时的裁剪策略。

#### Segment B 质量验收标准

- 产品表现特征不少于 500 字
- 附图设计建议中每张图不少于 100 字（四段式结构各段均需有实质内容）
- 附图设计建议不少于 9 张图的设计规范（产品侧5张 + 技术侧4张）
- 产出物案例展示图必须明确描述"本发明实际输出什么"（不能空洞描述"系统完成处理"）
- 缺少 Segment B 的 Ideal 文档视为**不合格**，需要补充后重新生成

## 输入源识别与代码归属判定

### 第一步：输入源识别

用户输入的 `repo_path` 支持两种形式：

| 输入形式 | 示例 | 处理方式 |
|---------|------|---------|
| **本地路径** | `/path/to/my-repo` | 直接使用，无需拉取 |
| **远程 Git URL** | `https://github.com/user/repo.git`、`git@github.com:user/repo.git` | 先 `git clone --depth=1` 到本地工作目录，再进入归属判定 |

远程 URL 的识别规则：以 `https://`、`http://`、`git://`、`git@` 开头即判定为远程 URL。

### 第二步：代码归属判定（四种情况）

确定本地路径后，根据 `.git` 目录和未推送 commit 状态判定代码归属：

```
repo_path
  ├─ 无 .git 目录 ──────────────────→ 情况 A：全量自有发明
  └─ 有 .git 目录
       ├─ 无远程追踪分支（@{u}）────→ 情况 B：全量自有发明
       ├─ 有 @{u}，无未推送 commit ─→ 情况 B：全量自有发明
       └─ 有 @{u}，有未推送 commit ─→ 情况 C：diff 发明模式
```

| 情况 | 条件 | 归属判定 | 分析范围 |
|------|------|---------|---------|
| **A** | 本地路径，无 `.git` | 整个项目视为用户自有发明 | 扫描目录树、入口文件、核心代码 |
| **B** | 本地路径，有 `.git`，无未推送 commit（含无 upstream 的情况） | 整个项目视为用户自有发明 | 扫描全部代码文件 |
| **C** | 本地路径，有 `.git`，有未推送 commit | 远端已推送代码视为"开源现有技术"，仅本地未推送的 commit 代表用户自己的发明 | 通过 `git diff @{u}..HEAD` 提取变更 |
| **D** | 远程 Git URL | 克隆后等价于情况 B（浅克隆无未推送 commit） | 扫描全部代码文件 |

**关键说明**：
- 情况 B 涵盖"有 `.git` 但没有设置 upstream 追踪分支"的场景——这意味着代码从未推送到远端，全部属于用户自有
- 情况 C 中"未推送 commit"通过 `git rev-list @{u}..HEAD` 检测，返回非空即存在未推送 commit
- 情况 D 使用 `git clone --depth=1`（浅克隆）以减少网络传输和磁盘占用

## 主题聚焦筛选

当用户通过 `--name/-n`（orchestrate.py）指定发明主题时，系统在代码分析全链路中注入主题引导，防止大型仓库下无关代码占满上下文预算导致分析失焦。

### 工作机制

主题信号沿以下路径传递：

```
--name "一种基于XX的方法"
  → invention_name
  → config.research.topic
  → generate_ideal_doc(topic=...)
  → 所有 Round 的 system prompt + user prompt
```

### 各 Round 的主题注入

| Round | 注入位置 | 作用 |
|-------|---------|------|
| **Round 1a** 概览扫描 | system prompt 追加主题聚焦段 + user prompt 注入 `**发明主题**` | 引导 LLM 在文件分类时优先选择与主题相关的文件群组，`recommended_focus_files` 围绕主题筛选 |
| **Round 1b** 深度分析 | system prompt 追加主题约束 + user prompt 注入 `**发明主题**` | 要求创新点围绕主题提取，`invention_title` 与主题保持一致 |
| **Round 1.5** 验证审查 | 不注入（审查已聚焦的创新点） | — |
| **Round 2** 文档生成 | user prompt 注入 `**发明主题**` | 确保文档生成与用户主题一致 |

### 上下文预算保护

即使不指定主题，系统仍有以下硬限制防止上下文溢出：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| Git diff | 60,000 chars | 完整 diff 截断上限 |
| 变更文件 | 80,000 chars（30 文件 × 5K） | 变更文件总量 |
| Round 1b | 60,000 chars | 创新相关文件代码 |
| Round 2 | 20,000 chars | 文档生成阶段代码 |
| full_analysis | 150,000 chars | 合并代码上限 |

指定主题后，LLM 会在这些预算内优先选择与主题相关的文件，而非按文件名优先级盲选。

## `--desc-full` 增强模式

启用后额外执行：
- AST 静态分析（提取函数/类签名）
- Import 依赖图构建（模块间 fan-in/fan-out 分析）
- 测试覆盖提示（从测试文件名推断被测模块）
- 全代码库扫描（不仅限于 diff 涉及的文件）

## 从代码到专利的映射

| 代码元素 | 专利章节 | 提取方法 |
|---------|---------|---------|
| 项目 README/注释 | 发明构思 | 提炼核心技术思路 |
| 已有方案对比 | 背景技术 3.1 | 描述现有方案及其局限 |
| 解决的痛点 | 背景技术 3.2 | 分析代码解决了什么问题 |
| UI/API 接口 | 产品侧 4.1 | 描述用户可见的功能表现 |
| 核心算法/流程 | 技术侧 4.2 | 详细描述实现逻辑 |
| 性能/效果数据 | 有益效果 4.3 | 量化技术方案的优势 |

## 专利语言转换

| 代码术语 | 专利表述 |
|---------|---------|
| function/method | 方法/步骤 |
| class/module | 模块/装置/单元 |
| variable/parameter | 参数/数据 |
| if-else/switch | 判断/根据...确定... |
| for/while loop | 遍历/循环执行/迭代 |
| API call | 请求/调用/发送指令 |
| database query | 数据查询/数据检索 |
| cache | 缓存/临时存储 |
| request/response | 请求/响应/反馈 |
| render/display | 渲染/展示/呈现 |

## 产出物清单

分析完成后，`$WORK_DIR/ideal/` 目录下包含：

| 文件 | 说明 |
|------|------|
| `code_context.md` | 原始代码上下文 |
| `scan_result.json` | Round 1a 扫描结果 |
| `innovation_analysis.json` | Round 1b 分析结果 |
| `validation_result.json` | Round 1.5 验证结果 |
| `ideal_segment_a/b/c.md` | 三段中间产物 |
| `ideal_output.md` | **最终 Ideal 文档** |
| `metadata.json` | 生成元数据 |
