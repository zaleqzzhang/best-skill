---
name: code-patent-writing
description: "从代码仓库自动生成符合规范的发明专利技术交底书（.docx格式）。由 AI 智能体直接执行代码分析和专利撰写，配合辅助脚本完成代码上下文提取和 DOCX 组装。内嵌三层质量保障体系（写作规范→自我评审→质量门禁）和 7 层输出清洗管道，确保输出质量不低于专业专利代理人水准。"
metadata:
  category: writing
  trigger-keywords: "patent,专利,交底书,code-patent,代码专利,专利撰写,发明专利,技术交底"
  applicable-stages: "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15"
  priority: "1"
  version: "2.1"
  allowed-commands: "python3,python,node,npm,npx,git"
  requires-approval: "false"
---

# 代码专利交底书自动生成（Code-Patent-Writing）

## 概述

本 skill 将代码仓库（本地路径或远程 Git URL）作为输入，由 AI 智能体通过 **15 个 Stage** 自动生成标准的发明专利技术交底书（.docx 格式）：

| 阶段 | Stage | 内容 | 执行者 |
|------|-------|------|--------|
| 代码分析 | 01-02 | 提取代码上下文（脚本结构化提取 + 智能体语义增强）→ 分析创新点 → 生成 Ideal 文档 | 辅助脚本 + 智能体 |
| 专利撰写 | 03-09 | 发明范围→现有技术→文献检索→术语→构思→背景→发明内容 | 智能体 |
| 图文生成 | 10-11 | **强制** Playwright UI 截图 + **强制** 4 类技术图表 PNG | 智能体 + 本地 Playwright |
| 质量保障 | 12-14 | 专利评审→修订→质量门禁（含重试循环，含图文完整性检查） | 智能体 |
| 文档输出 | 15 | DOCX 组装与打包（含图片嵌入） | 辅助脚本 |

**架构说明**：本 skill 完全独立运行，**不依赖外部 LLM API**。所有 LLM 推理由安装本 skill 的宿主智能体（如 CodeBuddy）自身完成。辅助脚本仅负责代码上下文提取（纯 Python stdlib）和 DOCX 文件组装。

**三层质量保障**：
- **预防层**：写作规范（AI 味黑名单 + 防膨胀约束 + 通俗化保障）→ 参考 [$SKILL_DIR/references/writing-style-guide.md](references/writing-style-guide.md)
- **检测层**：自我评审（16 维度）+ 质量门禁（13 维评分 + 16 条阻断规则）→ 参考 [$SKILL_DIR/references/quality-rubric.md](references/quality-rubric.md)
- **修复层**：输出清洗（7 层管道 + 89 种模式）→ 参考 [$SKILL_DIR/references/llm-output-cleaning-guide.md](references/llm-output-cleaning-guide.md)

## 路径规范

> **⚠️ 以下路径规则为强制约束，智能体不得自行更改目录结构。**

1. **SKILL_DIR**（skill 安装目录）：本 SKILL.md 文件所在的目录
   - 脚本位于：`$SKILL_DIR/scripts/`
   - 模板位于：`$SKILL_DIR/assets/`
   - 参考文档位于：`$SKILL_DIR/references/`

2. **REPO_PATH**（目标代码仓库路径）：用户指定的待分析代码仓库的本地路径（即 `orchestrate.py extract-context` 的 `<repo_path>` 参数）

3. **WORK_DIR**（专利工作目录）：**必须**位于 `$REPO_PATH/_patent_docx`
   - 示例：如果 REPO_PATH 为 `/home/user/myproject`，则 WORK_DIR 为 `/home/user/myproject/_patent_docx`
   - 所有专利任务共享同一个固定目录名 `_patent_docx`，不随发明名称变化
   - **禁止**将 WORK_DIR 放在 REPO_PATH 的上级目录、workspace 根目录或其他任意位置

4. **PLAYWRIGHT_DIR**（Playwright 安装目录）：**必须**固定在 `$REPO_PATH/_patent_playwright`
   - 该目录由所有专利任务共享，**不随 WORK_DIR 变化**
   - Playwright 只在此目录安装一次，后续复用
   - 所有 Playwright JS 脚本执行时必须通过 `NODE_PATH=$REPO_PATH/_patent_playwright/node_modules` 或 `cd $REPO_PATH/_patent_playwright && node <script>` 来引用已安装的 playwright 包

## 执行纪律（强制，智能体必须遵守）

> **🚫 以下规则的优先级高于智能体自身的任何优化判断。违反任何一条都将导致产出不合格。**

### 规则 1：Plan/Todo 必须严格对应 16 Stage

智能体在创建 Plan 或 Todo 时，**必须**为 Stage 00 到 Stage 15 各创建一个独立的 todo 条目（共 16 条），标题格式为 `Stage NN: {Stage 标题}`。

- **禁止合并**：不得将多个 Stage 合并为一个 todo（如 "Stage 03-04" 或 "Stage 06-09"）
- **禁止拆分**：不得将一个 Stage 拆分为多个 todo
- **禁止新增**：不得在 Stage 00-15 之外自行添加额外步骤（如 "code-explorer 分析" "MCP 检索"）
- **禁止重排**：必须按 Stage 00 → 01 → 02 → ... → 15 的顺序执行

### 规则 2：禁止使用 MCP Playwright

本 Skill 的所有 Playwright 操作（Stage 05 联网检索、Stage 10 UI 截图、Stage 11 技术图表截图）**必须**通过生成 `.js` 脚本然后用 `node` 命令执行的方式完成。

- **禁止**调用 MCP playwright 工具（如 `browser_navigate`、`browser_snapshot`、`browser_click` 等）
- **禁止**在 Plan 中引用 `[mcp:playwright]`
- 原因：MCP playwright 会弹出浏览器窗口或行为不可控，而本 Skill 要求 headless 模式的本地 Node.js 脚本

### 规则 3：禁止使用 SubAgent 替代 Skill Stage

Stage 01（代码上下文提取）和 Stage 02（创新点分析）的执行方式已在 Skill 中明确定义：
- Stage 01 包含两步：**步骤 1** 必须通过 `orchestrate.py extract-context` 辅助脚本执行结构化提取；**步骤 2** 由智能体自身阅读脚本产出并做语义增强（主题相关性过滤 + 深度补充读取）
- Stage 02 **必须**由智能体自身阅读增强后的 `code_context.md` 后直接分析

- **禁止**使用 `task code-explorer` subagent 替代 Stage 01 的任何步骤或 Stage 02
- **禁止**在 Plan 中引用 `[subagent:code-explorer]`
- 原因：Stage 01 步骤 1 的辅助脚本内置了 Git 归属判定、AST 签名索引等自动化逻辑，subagent 无法替代；Stage 01 步骤 2 的语义增强需要结合脚本产出的 AST 特征作为精准指引，subagent 缺乏这些结构化线索会盲扫

### 规则 4：Playwright 安装位置固定

Stage 00 安装 Playwright 时：
- **必须**安装在 `$REPO_PATH/_patent_playwright/`（不是 `$WORK_DIR/`）
- 如果 `$REPO_PATH/_patent_playwright/node_modules/playwright` 已存在，**跳过安装**
- 后续所有 JS 脚本中 `require('playwright')` 必须能从此固定路径解析

### 规则 5：禁止使用 --force 降级模式

Stage 15 执行 `build-docx` 时：
- **禁止**使用 `--force` 参数跳过全链路前置检查
- 如果 `build-docx` 因 preflight 失败而拒绝执行（exit 1），**必须**返回修复缺失的 Stage 产出后重新运行
- `--force` 仅供人工调试使用，智能体在正常流程中使用 `--force` 视为违规
- 原因：`--force` 会跳过截图数量、图表数量、figure_registry 完整性等硬守卫检查，导致最终 DOCX 缺失图片或内容不完整

### 规则 6：写入后验证（防 0 字节文件）

> **⚠️ 本规则解决的问题**：`write_to_file` 工具偶发写入 0 字节或内容不完整的文件，导致后续 Stage 连锁失败。所有文件写入操作后**必须验证**。

**强制验证流程**：每次通过 `write_to_file` 写入文件后，**必须立即执行以下验证之一**（选择最适合的方式）：

```bash
# 方式 1：快速验证（推荐，适合大多数文件）
wc -c <文件路径>
# 确认字节数 > 0 且符合预期

# 方式 2：深度验证（适合关键文件：JSON、大 HTML、核心章节 MD）
python3 $SKILL_DIR/scripts/orchestrate.py verify-write <文件路径> --min-size <最小字节数> [--json] [--md-markers "标记1,标记2"]
```

**验证失败时的处理**：
1. 如果文件为 0 字节或远小于预期大小 → **必须重写**
2. 重写策略：**先写到安全路径（`$PLAYWRIGHT_DIR/` 或 `/tmp/`），`wc -c` 确认非空后，`cp` 到目标路径**
3. 最多重试 **2 次**，仍然失败则报错并停止当前 Stage

**大文件安全写入规则**（HTML / JSON / 长 Markdown，预估 > 3000 字符）：

```bash
# 步骤 1：写入到安全路径（无中文、无特殊字符）
# write_to_file → $PLAYWRIGHT_DIR/{文件名}  或  /tmp/patent_{文件名}

# 步骤 2：验证写入成功
wc -c $PLAYWRIGHT_DIR/{文件名}
# 确认字节数 > 0

# 步骤 3：复制到目标路径
cp $PLAYWRIGHT_DIR/{文件名} <目标路径>

# 步骤 4：验证目标文件
wc -c <目标路径>
```

**各 Stage 关键文件的最小大小参考**：

| Stage | 文件 | 最小字节数 | 验证命令 |
|-------|------|-----------|---------|
| 02 | `ideal_output.md` | 8000 | `verify-write ... --min-size 8000 --md-markers "## 产品表现特征,## 附图设计建议"` |
| 05 | `references.md` | 500 | `verify-write ... --min-size 500` |
| 05 | `web_search_results.json` | 200 | `verify-write ... --min-size 200 --json` |
| 09 | `invention_content.md` | 5000 | `verify-write ... --min-size 5000 --md-markers "### 4.1,### 4.2,### 4.3"` |
| 10 | `code/index.html` | 5000 | `verify-write ... --min-size 5000` |
| 10 | `figure_registry.json` | 200 | `verify-write ... --min-size 200 --json` |
| 11 | `charts/tech_charts.html` | 3000 | `verify-write ... --min-size 3000` |

### 规则 7：Stage 串行执行纪律（禁止并行写入多 Stage）

> **⚠️ 本规则解决的问题**：一次性批量写入多个 Stage 的文件会导致章节间缺乏连贯性、中间验证被跳过、单个 Stage 失败引发连锁效应。

**强制串行流程**：

```
进入 Stage N
  → 执行 Stage N 的全部步骤（撰写 + 写入 + 验证）
  → 调用 preflight --stage N 确认 PASS
  → 只有 PASS 后才能进入 Stage N+1
```

**具体禁止行为**：
- **禁止**在一个工具调用批次中同时写入属于不同 Stage 的多个文件（如同时写 `goal_text.md` + `prior_art.md` + `key_terms.md`）
- **禁止**跳过 `preflight --stage N` 验证直接进入下一个 Stage
- **禁止**在某个 Stage 的 preflight 返回 FAIL 时继续执行后续 Stage

**允许的并行行为**（同一 Stage 内）：
- 同一 Stage 内的多个文件可以并行写入（如 Stage 05 的 `references.md` 和 `web_search_results.json`）
- 同一文件的写入和验证可以在同一批次中完成

**Stage 间过渡模板**：

```bash
# 完成 Stage N 的所有写入和验证后
python3 $SKILL_DIR/scripts/orchestrate.py preflight $WORK_DIR --stage N

# 如果 PASS → 进入 Stage N+1
# 如果 FAIL → 根据 fix_hint 修复后重新验证，不得继续
```

## 中断恢复（Stage 级幂等）

> **⚠️ 强制要求**：每个 Stage 开始前，必须先按下表的验证条件检查该 Stage 的产出是否已正确完成。验证通过则跳过，验证失败（文件不存在 **或** 存在但内容不完整）则重新执行。

**🔒 硬守卫机制**：所有跳过验证条件已脚本化为 `orchestrate.py preflight` 子命令。**智能体必须在进入每个 Stage 前调用 preflight 获得机器可读的 PASS/FAIL 判定**，禁止自行判断跳过条件：

```bash
# 检查单个 Stage 的产出是否合格
python $SKILL_DIR/scripts/orchestrate.py preflight $WORK_DIR --stage N

# 检查全部 Stage（0-15）的产出
python $SKILL_DIR/scripts/orchestrate.py preflight $WORK_DIR --all
```

输出为 JSON 格式：`{"stage": N, "status": "PASS"|"FAIL", "missing": [...], "details": {...}}`
- **PASS** → 该 Stage 产出已验证完整，可跳过
- **FAIL** → 该 Stage 产出不完整，必须重新执行（`missing` 列出具体缺失项）

**核心原则**：不是简单检查"文件是否存在且非空"，而是**复用每个 Stage 已定义的"执行后验证"条件**做完整性检查。文件存在但格式不符（schema 字段缺失、截图数量不足、章节结构残缺等）视为该 Stage 未完成，必须重新执行。

**执行逻辑**：
1. 进入 Stage N 前，运行 `preflight --stage N` 获取判定结果
2. **PASS** → 打印 `[SKIP] Stage N: 产出已验证完整`，跳过进入 Stage N+1
3. **FAIL** → 打印 `[REDO] Stage N: 产出不完整，重新执行`，正常执行该 Stage
4. Stage 00（环境检查）**永不跳过**，始终执行

**Stage 跳过验证条件速查表**：

| Stage | 关键输出 | 跳过条件（全部满足才可跳过） |
|-------|---------|------------------------|
| 00 | — | **永不跳过**，始终执行环境检查 |
| 01 | `ideal/code_context.md` | 文件存在且 ≥ 1000 字符，且包含 `## 智能体语义增强` 章节标题 |
| 02 | `ideal/ideal_output.md` | 文件存在且包含 `## 产品表现特征` 和 `## 附图设计建议` 两个章节标题 |
| 03 | `patent_run/stage-01/goal_text.md` | 文件存在且 ≥ 200 字符 |
| 04 | `patent_run/stage-02/prior_art.md` | 文件存在且 ≥ 500 字符 |
| 05 | `patent_run/stage-03/references.md` + `web_search_results.json` | `references.md` 含 ≥ 8 条带链接精选文献；`web_search_results.json` 存在且含 `results` 数组 ≥ 20 条（原始检索结果） |
| 06 | `patent_run/stage-04/key_terms.md` | 文件存在且包含 ≥ 5 个术语定义段落 |
| 07 | `patent_run/stage-05/concept.md` | 文件存在且包含 `2.1` 和 `2.2` 子节标记 |
| 08 | `patent_run/stage-06/background.md` | 文件存在且包含 `### 3.1` 和 `### 3.2` 子节标题 |
| 09 | `patent_run/stage-07/invention_content.md` | 文件存在且包含 `### 4.1`、`### 4.2`、`### 4.3` 三个子节标题 |
| 10 | `patent_run/stage-08/screenshots/*.png` + `figure_registry.json` | `screenshots/` 下 PNG 数量 ≥ `invention_content.md` 中 `<!-- FIGURE:xxx -->` 占位符数量（最低不少于 10 张），且每张 ≥ 50KB 且无内容哈希完全相同的重复对；`figure_registry.json` 存在且含 `product_output_preview` 和 `innovation_linkage` 类型条目 |
| 11 | `$WORK_DIR/charts/*.png` | `charts/` 下 ≥ 4 张 PNG 且每张 ≥ 30KB |
| 12 | `patent_run/stage-09/reviews.md` | 文件存在且包含 ≥ 3 个检查项标记（✅ / ⚠️ / ❌） |
| 13 | `patent_run/stage-10/revised_*.md` | 至少存在 1 个 `revised_*.md` 文件且 ≥ 500 字符 |
| 14 | `patent_run/stage-11/quality_report.json` | JSON 存在且包含 `score_1_to_10`、`verdict`、`dimension_scores` 三个必填字段 |
| 15 | `$WORK_DIR/deliverables/{发明名称}.docx` | deliverables/ 下存在 ≥ 200KB 的 .docx 文件 |

> **与原代码 `--resume` 的区别**：原代码通过 `checkpoint.json` 记录最后完成的 Stage 编号，`--resume` 时按编号跳过——即使产出文件损坏也会跳过。Skill 版本更严格，按产出内容完整性判断，避免因中途崩溃导致的半成品被误认为已完成。

## 工作流程（16 Stage：Stage 00-15）

### Stage 00：环境前置检查与依赖安装（强制）

> **⚠️ 强制要求**：本 Stage **必须在所有其他 Stage 之前执行**。缺少任何依赖会导致后续 Stage 失败。

**步骤 1：检查 Node.js 环境**

```bash
node --version || { echo "❌ 需要安装 Node.js (>= 16.x)"; exit 1; }
npm --version || { echo "❌ 需要安装 npm"; exit 1; }
```

**步骤 2：强制安装 Playwright（固定目录，跨任务复用）**

```bash
# Playwright 固定安装在 $REPO_PATH/_patent_playwright/（所有专利任务共享）
# 如果已安装则跳过
PLAYWRIGHT_DIR="$REPO_PATH/_patent_playwright"
if [ ! -d "$PLAYWRIGHT_DIR/node_modules/playwright" ]; then
    mkdir -p "$PLAYWRIGHT_DIR"
    cd "$PLAYWRIGHT_DIR"
    npm init -y 2>/dev/null
    npm install playwright
    npx playwright install chromium
else
    echo "Playwright 已安装，跳过"
fi
```

验证：`cd $REPO_PATH/_patent_playwright && node -e "require('playwright')"` 无报错即成功。

> **注意**：后续所有 Stage 中的 Playwright JS 脚本必须在 `$REPO_PATH/_patent_playwright/` 目录下执行（`cd $REPO_PATH/_patent_playwright && node <script_path>`），或通过 `NODE_PATH=$REPO_PATH/_patent_playwright/node_modules node <script_path>` 确保能找到 playwright 包。

**步骤 3：推荐安装 Mermaid CLI（降级方案备用）**

```bash
npm install -g @mermaid-js/mermaid-cli
```

验证：`npx @mermaid-js/mermaid-cli --version` 有版本号输出即成功。**Mermaid CLI 为可选依赖**，若安装失败不阻断流程，Stage 11 将使用 HTML + Playwright 截图（优先方案）生成技术图表。

**步骤 4：检查 Python 依赖**

```bash
python3 -c "import defusedxml; import lxml" 2>/dev/null || {
    pip install defusedxml lxml
}
```

**执行后验证清单**：

| 依赖 | 验证命令 | 失败处理 |
|------|---------|---------|
| Node.js | `node --version` | 阻断，提示安装 |
| Playwright | `node -e "require('playwright')"` | 阻断，重新安装 |
| Chromium 浏览器 | `npx playwright install chromium` | 阻断，重新安装 |
| Mermaid CLI | `npx @mermaid-js/mermaid-cli --version` | 警告，Stage 11 使用 HTML + Playwright 方案（不阻断） |
| defusedxml + lxml | `python3 -c "import defusedxml; import lxml"` | 阻断，pip install |

### Stage 01：代码上下文提取（辅助脚本 + 智能体语义增强）

本 Stage 分两步执行：步骤 1 由辅助脚本做结构化提取（Git 归属、AST、依赖图），步骤 2 由智能体做语义理解和主题相关性过滤。两步缺一不可。

**步骤 1：辅助脚本结构化提取（强制）**

> **⚠️ 强制要求**：本步骤 **必须通过运行辅助脚本完成**，禁止跳过脚本直接自行读取代码文件进行分析。脚本内置了 Git 归属判定、AST 签名索引、Import 依赖图等自动化逻辑，手动读取无法替代。

```bash
python $SKILL_DIR/scripts/orchestrate.py extract-context <repo_path_or_url> \
    --name "发明名称" [--full]
# 脚本默认将 WORK_DIR 设为 <repo_path>/_patent_docx（本地路径时）
# 也可显式指定：--output <repo_path>/_patent_docx
```

**输出**：`$WORK_DIR/ideal/code_context.md`（基础版）— 包含 Git commit、diff、代码摘要、AST 签名等结构化上下文。

**步骤 1 验证**：确认 `$WORK_DIR/ideal/code_context.md` 文件存在且非空（至少 1000 字符），否则说明提取失败，需排查后重新执行。

**步骤 2：智能体语义增强（强制）**

> **⚠️ 强制要求**：步骤 1 完成后，智能体**必须**执行本步骤。目的是弥补脚本在"语义理解"和"主题相关性过滤"两方面的盲区，让 code_context.md 从"结构化原始数据"升级为"与发明主题高度相关的精炼上下文"。

智能体阅读步骤 1 产出的 `code_context.md`，结合**发明主题**执行以下 3 个子任务：

**子任务 A：主题相关性标注**

扫描 `code_context.md` 中的所有文件条目（代码摘要、AST 签名、变更文件等），对每个文件/模块标注与发明主题的相关性：

| 标注 | 含义 | 后续处理 |
|------|------|---------|
| 🔴 **高相关** | 直接实现发明核心功能的文件 | 步骤 2B 深度补充读取 |
| 🟡 **中相关** | 支撑核心功能的辅助模块 | 保留现有摘要，不补充 |
| ⚪ **低相关/无关** | 与发明主题无直接关系（如测试、配置、CI） | 在语义增强章节中标记为可忽略 |

**标注指引**（利用脚本已有的结构化信息）：
- AST 签名中标注了"探测到关键特征"（异步调度、复杂决策树、生成器/状态机）的文件 → **优先标注为 🔴 高相关**（需结合发明主题确认）
- Import 依赖图中 fan-in ≥ 2 的核心模块 → 优先考虑标注为 🔴 或 🟡
- 测试文件、配置文件、纯基础设施代码 → 通常标注为 ⚪

**子任务 B：深度补充读取**

对标注为 🔴 **高相关**但在步骤 1 中被截断（出现 `... (内容已截断) ...` 或 `... (truncated` 标记）的文件，使用 `read_file` 工具读取完整内容。

**补充规则**：
- 只补充 🔴 高相关且被截断的文件，不盲扫
- 每个文件最多读取 8000 字符（超过部分仍截断，但保留函数/类定义完整性）
- 总补充量不超过 5 个文件（避免上下文爆炸）
- 如果步骤 1 使用了 `--full` 模式且文件未被截断，则无需补充

**子任务 C：语义摘要生成**

为每个 🔴 高相关文件生成一段**面向专利的语义摘要**（100-200 字），包含：
- 该文件/模块解决什么技术问题
- 核心算法逻辑或数据处理流程的自然语言描述
- 与发明主题的关联说明（为什么这个文件对发明至关重要）

**输出格式**：将语义增强结果追加到 `code_context.md` 末尾，格式如下：

```markdown
## 智能体语义增强

> 发明主题：{发明名称}
> 增强时间：{ISO-8601 时间戳}

### 主题相关性标注

| 文件/模块 | 相关性 | 理由 |
|-----------|--------|------|
| researchclaw/ideal_generator.py | 🔴 高相关 | 直接实现从代码仓库提取创新点的核心功能 |
| researchclaw/pipeline/runner.py | 🟡 中相关 | 管线调度基础设施，非发明核心 |
| tests/test_xxx.py | ⚪ 无关 | 测试文件 |
| ... | ... | ... |

### 深度补充（被截断的高相关文件完整内容）

#### {文件路径1}

```{语言}
{补充读取的完整内容}
```

#### {文件路径2}
...

### 语义摘要

**{文件路径1}**：{100-200 字的面向专利的语义摘要}

**{文件路径2}**：{100-200 字的面向专利的语义摘要}
```

**执行后验证**：确认 `$WORK_DIR/ideal/code_context.md` 文件包含 `## 智能体语义增强` 章节标题，且该章节包含至少 1 个 🔴 高相关文件的语义摘要。

### Stage 02：创新点分析与 Ideal 文档生成（智能体）

阅读 `code_context.md`，按以下 4 轮渐进式分析提取创新点：

**Round 1a 概览扫描**：按以下**三级分类**对代码进行标注（优先级从高到低）：

**第一优先级 — 系统级创新**（多模块协同产生的涌现能力，不属于任何单个文件）：
- 项目作为整体提供的前所未有的端到端能力（如"纯代码→专利底稿+配套 UI 图"）
- 多个模块组合后产生的新价值，拆开任何一个模块都无法独立实现
- 用户视角的"Before/After"质变（参考 `code_context.md` 顶部的"项目价值分析提示"）
- **即使无法归属到单个代码文件，只要能指出协同工作的模块组合，就是有效的系统级创新**

**第二优先级 — 模块级创新**（单个模块的独特算法逻辑）：
- 独特算法逻辑、数据分析方法、智能生成策略、图文映射机制
- **利用 AST 特征探测信息**：`code_context.md` 的 AST 签名索引中，标注了"探测到关键特征"的文件（如异步调度、复杂决策树、生成器/状态机），这些文件**大概率包含模块级算法创新**，应优先深度分析

**第三优先级 — 基础设施代码**（不算独立创新）：
- 流水线调度、配置管理、CLI 参数解析、格式转换、数据序列化

> **关键原则**：系统级创新的优先级**高于**模块级创新。如果项目的核心价值是多模块协同产生的端到端能力，则应将其作为第一个创新点，再从支撑该能力的关键模块中提取 1-2 个模块级创新点作为补充。

- **工程实践硬排除**：以下改动即使涉及大量代码变更也**不得**作为独立创新点：
  - 纯粹为提升可维护性的代码重构（如拆分大函数、提取公共方法）
  - 框架/库的版本升级或迁移（如从 Flask 迁移到 FastAPI）
  - 增加单元测试、完善日志、增加监控
  - 纯 DevOps 改进（CI/CD 配置、Docker 化、部署脚本）

**Round 1b 深度分析**：提取 **2-4 个**核心创新点（严禁超过 4 个），根据 Round 1a 的分类结果选择对应字段集：

**模块级创新字段集**（适用于单模块算法创新）：

| 必填字段 | 精确度要求 |
|---------|----------|
| `code_evidence` | 精确到函数/类 `[file: xxx, func: yyy]` |
| `key_data_structures` | 列出 dataclass 字段或 dict schema |
| `algorithm_pseudocode` | 3-5 行含判断分支的伪代码 |
| `quantitative_improvement` | 精确到代码中的常量值 |
| `concrete_example` | 具体人+具体事的端到端案例（30 秒规则：让不懂编程的人理解） |

**系统级创新字段集**（适用于多模块协同的产品级/系统级创新）：

| 必填字段 | 精确度要求 |
|---------|----------|
| `system_evidence` | 列出协同工作的模块组合（如 `[modules: ideal_generator + pipeline_runner + patent_ui_experiment]`），不要求精确到单个函数 |
| `capability_description` | 描述系统作为整体具备的前所未有的新能力（1-2 句话） |
| `user_value_proposition` | 用 Before/After 格式描述对最终用户的价值变化 |
| `quantitative_improvement` | 精确到端到端效果的量化数据（如"从 2 周缩短到 3 小时"） |
| `concrete_example` | 具体人+具体事的端到端案例（30 秒规则） |

> **选择规则**：Round 1a 标注为"系统级创新"的使用系统级字段集；标注为"模块级创新"的使用模块级字段集。**2-4 个创新点中，至少 1 个应为系统级创新**（如果项目确实只有模块级创新则可豁免，但需在分析中说明理由）。
>
> **创新点价值锚定**（强制参考）：提取每个创新点时，必须参考 [$SKILL_DIR/references/writing-style-guide.md](references/writing-style-guide.md) 中"创新点价值锚定（专利可授权性导向）"一节的转化表，确保从**技术发明思维**而非**工程优化思维**出发描述创新。例如："复用已有管线，减少 70% 重复代码"应转化为"一种基于配置档案的跨领域管线适配方法"。

**Round 1.5 验证审查（专利授权性三问筛选）**：对每个创新点用以下三个问题做 PASS/REJECT/MERGE 判定：

> **三问筛选标准**（必须同时满足三问才能 PASS）：
> 1. **技术问题具体性**：该创新点是否解决了一个具体的技术问题，而非通用工程需求（如格式转换、文件导出、UI 美化）？
> 2. **方案区别性**：技术方案是否包含至少一个区别于现有方法的关键步骤或判断逻辑？
> 3. **效果可量化性**：是否产生了可量化或可观测的技术效果（如时间缩短、步骤减少、准确率提升）？

**通用工程实践排除清单**（以下类型作为**孤立功能**时必须 REJECT 或 MERGE 到其他创新点中）：
- 文件格式转换/导出（如 Markdown→DOCX、JSON→XML）— **但如果**格式转换是端到端自动化系统不可缺少的输出环节，且该端到端系统整体具备新颖性，则不排除系统级创新
- UI/Demo 自动生成 — **但如果**UI 自动生成涉及从非 UI 代码（如后端算法/纯代码仓库）自动推导界面结构和交互流程，属于"算法到界面的自动映射"创新，不排除
- 图表/可视化渲染 — **但如果**图表是从非可视化数据源（如代码仓库、文本文档）自动推导技术架构/流程并渲染，属于"结构化信息自动可视化"创新，不排除
- CLI 参数解析、配置管理、日志记录
- 标准化的数据序列化/反序列化

> **排除原则**：排除清单的目的是过滤**孤立的工程模块**，而非过滤**端到端系统的子组件**。判断标准：如果移除该模块后，系统的核心价值主张不受影响，则该模块是孤立的，应排除；如果移除后系统的端到端能力断裂，则不应排除。

**判定规则**：
- REJECT：不能同时满足三问，且属于通用工程实践排除清单
- MERGE：不能独立满足三问，但与另一个创新点组合后能满足。**MERGE 优先于 REJECT**
- PASS：同时满足三问，且有明确的技术问题→技术方案→代码证据链路
- **最终保留 2-3 个核心创新点（硬上限 3 个，硬下限 2 个）**

**工程优化 vs 技术发明区分（强制检查）**：

> 对每个 PASS 的创新点，必须额外执行以下检查。如果创新点的核心价值落入"工程优化"列，必须**重新锚定技术价值**后才能保留。

| 工程优化（被驳回风险高） | 技术发明（可授权性强） | 重新锚定方法 |
|---|---|---|
| "减少 N% 重复代码" | "通过配置档案实现跨领域管线适配" | 焦点从代码量转向动态任务切换的技术机理 |
| "节省 N 小时人工整理" | "自动界定发明的技术边界" | 焦点从省时间转向法律合规边界判定 |
| "去掉 AI 味 / 减少人工清理" | "面向专利法规范的多层级文本合规性处理" | 焦点从文本美化转向法律规范驱动的净化体系 |
| "自动生成 UI / 提高可读性" | "将后台算法逻辑自动映射为可视化交互原型" | 焦点从方便理解转向算法到界面的自动映射技术 |

> 参考 [$SKILL_DIR/references/writing-style-guide.md](references/writing-style-guide.md) 的「创新点价值锚定」章节获取完整的转化指导。

**Round 2 文档生成**：输出完整 Ideal 文档（`ideal_output.md`），每个创新点必须包含三段式结构：
- **(a) 技术原理描述**（250-400 字）：案例引入开头，纯自然语言，禁止代码标识符
- **(b) 代码证据附录**（50-100 字）：数据结构、伪代码、精确数值、代码文件路径
- **(c) 通俗理解**（80-120 字）：Before/After 小故事 + 日常类比

**Round 2 还必须生成以下两个附加章节**（缺一不可）：

**## 产品表现特征**（必填）：
- 列出本发明涉及的**差异化使用场景**（至少 2 个），说明每个场景的主要用户、交互形式、主要输入/输出
- 提供**场景间 GUI 切换对比表**（对比维度：主要用户、交互形式、主要输入、主要输出、页面复杂度、交互重点、是否需要场景切换）
- 为每个创新点描述其**可视化体现**（如何在界面上直观展示该创新点的价值）

**## 附图设计建议**（必填，产品侧 5 张 + 技术侧 4 张 = 9 张图设计规范）：

**动态附图策略判断**：
根据代码层级决定产品侧（图 1-5）的 UI 类型：
- **如果是前端/业务后端**：生成普通 App UI 或 Web GUI 交互图。
- **如果是底层代码（如中间件、网络层、基础算法）**：必须将 UI 设计降级为**"运维/监控大盘界面"**（如 Grafana 监控面板），展示 QPS 曲线、内存走势、连接数分布、状态大盘等，以符合底层技术的实际应用场景，避免生硬套用普通业务 UI。

每张图必须包含**四段式结构**：
1. **图面内容描述**：该图展示什么内容、从什么视角
2. **关键元素**：图中必须包含的核心元素清单（如图标、面板、箭头、标注、或监控图表组件）
3. **标注说明**：箭头含义、颜色区分、文字标注方式
4. **产出物/联动要素**（新增）：该图中应嵌入哪些实际产出物预览或交叉引用标签

产品侧 5 张图（根据上述动态策略适配为业务 GUI 或监控大盘）：
- **图 1 应用场景总览图**：展示多类用户或运维人员如何监控/使用本发明
- **图 2 交互/流转演示图**：展示主要场景的页面操作或监控数据流转步骤
- **图 3 场景切换/指标对比图**：对比不同场景的布局差异或核心监控指标的前后对比
- **图 4 产出物案例展示图**（新增，强制）：**以本发明主题自身的实际产出物为案例素材**，展示系统核心输出成果的高保真预览。例如：如果发明是"自动生成专利文档"，展示一份真实生成的交底书关键章节（标题、目录、核心段落缩略、配图缩略）；如果发明是"图像处理"，展示处理前后对比。**该图的核心价值是让读者直观看到"这个系统到底能产出什么"**
- **图 5 创新点联动总览图**（新增，强制）：作为产品侧与技术侧的桥梁，分三列展示"GUI操作 → 后台处理 → 创新点亮点"的端到端映射关系，三列间用箭头连接

技术侧 4 张图：
- **图 6 系统架构图**：展示分层架构，每层标注组件名称和职责。**右上角标注"支撑产品侧场景X"的溯源标签**
- **图 7 核心算法流程图**：展示核心处理链路，包含判断分支。**连线必须使用内联 SVG 绘制**
- **图 8 模块间时序图**：展示各模块的调用顺序和数据传递。**生命线和消息箭头必须使用内联 SVG 绘制**
- **图 9 数据流向图**：展示输入数据如何在系统内部逐步转化为输出。**不同链路用不同颜色区分**

末尾提供**附图组合建议**：优先级排序和篇幅受限时的裁剪策略。**产出物案例展示图和创新点联动总览图优先级高于场景切换对比图**。

完整的分析 JSON schema → 参考 [$SKILL_DIR/references/code-analysis-guide.md](references/code-analysis-guide.md)

### Stage 03：目录初始化 + 发明范围撰写（辅助脚本 + 智能体）

**步骤 1：初始化目录结构**（调用辅助脚本）

```bash
python $SKILL_DIR/scripts/orchestrate.py init-patent-run $WORK_DIR
```

**步骤 2：撰写发明范围**（→ `patent_run/stage-01/goal_text.md`）

以 `ideal_output.md` 为引导撰写专利发明范围说明书，包含：发明名称、技术领域、发明目标、技术路线概述、预期效果、适用范围。使用阶段差异化 Ideal 注入策略（参考 [$SKILL_DIR/references/ideal-injection-guide.md](references/ideal-injection-guide.md)）。
- 使用专利申请书的专业用语
- 技术描述要准确、具体，避免模糊表述
- 每句话必须能回答「具体做了什么」或「具体效果是什么」

### Stage 04：现有技术分析（→ `patent_run/stage-02/prior_art.md`）

基于发明主题撰写现有技术分析报告：

**前置步骤：项目依赖分析（强制）**

> 在撰写现有技术之前，**必须**先检查 Stage 01 提取的 `code_context.md` 中的 `## 项目入口/配置文件` 部分（即 `entry_files`），从中解析项目的核心依赖库。例如：
> - `requirements.txt` / `pyproject.toml` → Python 依赖（如 `langchain`、`celery`、`fastapi`）
> - `package.json` → Node.js 依赖（如 `express`、`playwright`、`redis`）
> - `go.mod` → Go 依赖（如 `gin`、`grpc`）
> - `pom.xml` / `build.gradle` → Java 依赖
>
> **将这些核心依赖库的原生机制作为"代表性现有技术"的首选来源**。例如：如果代码替换了 Redis 的某种用法，那么 Redis 原生的机制就是最好的现有技术（Prior Art）。这比盲目联网搜索更精准。

1. **技术发展脉络**：该领域的主要技术演进路线
2. **代表性现有技术**：列出 3-5 个最相关的现有技术方案（**优先从项目依赖中提炼**，再补充领域通用方案）
3. **共性不足**：归纳现有方案普遍存在的问题
4. **技术空白**：现有技术尚未覆盖的领域
5. **本发明的技术机会**：创新切入点

### Stage 05：文献收集与参考文献（强制，→ `patent_run/stage-03/`）

> **⚠️ 强制要求**：本 Stage **禁止跳过**。必须通过联网检索获取真实的现有技术文献，确保背景技术引用和参考文献章节包含可验证的真实来源。

**步骤 1：生成检索查询**

基于 Stage 04 现有技术分析报告中的技术关键词和 Ideal 文档中的创新点，生成中英双语检索 query：
- 中文 query：用于搜索中国专利数据库和中文学术资源
- 英文 query：用于搜索 Google Patents、arXiv、Semantic Scholar
- 组合检索式：`(核心技术术语1 OR 术语2) AND (patent OR 专利 OR specification)`

**步骤 2：联网检索（三级降级策略）**

**优先方案 A：本地 Playwright 无头浏览器脚本（推荐，数据最丰富）**

> **⚠️ 广撒网策略**：每个站点使用 **≥2 组不同 query** 检索，每组 query 提取 **≥5 条结果**（含翻页），最终汇总 **≥20 条原始文献**，再在步骤 3 中精选。

生成 Playwright Node.js 脚本，以无头浏览器模式访问以下站点：
- Google Patents（`https://patents.google.com/`）：**≥2 组 query**，每组提取前 5-10 条结果（专利号、标题、摘要、链接）
- arXiv（`https://arxiv.org/search/`）：**≥2 组 query**，每组提取前 5-10 条结果（论文标题、作者、arXiv ID、链接）
- Semantic Scholar（`https://www.semanticscholar.org/`）：**≥1 组 query**，提取前 5-10 条结果

**检索 query 设计要求**：
- 每个站点的多组 query 应覆盖不同维度：核心技术术语、应用场景、技术手段组合
- 例如对于"基于图数据库的知识推荐系统"：
  - query 1: `knowledge graph recommendation system`（宽泛）
  - query 2: `neo4j knowledge base intelligent retrieval`（具体技术栈）
  - query 3: `graph neural network content recommendation`（算法维度）

**执行方式**：智能体生成 `$WORK_DIR/playwright_search.js` 脚本，然后在 **Playwright 固定目录**下用 `node` 执行：

```javascript
// playwright_search.js — 智能体根据检索 query 动态生成
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const allResults = [];
  
  // 定义多组检索 query（智能体根据项目实际情况生成）
  const patentQueries = ['query_broad_1', 'query_specific_2'];
  const arxivQueries = ['query_algo_1', 'query_application_2'];
  const scholarQueries = ['query_combined_1'];
  
  // 1. 搜索 Google Patents — 多组 query
  for (const q of patentQueries) {
    await page.goto(`https://patents.google.com/?q=${encodeURIComponent(q)}`);
    await page.waitForTimeout(2000);
    // 提取搜索结果（前 10 条）...
    // allResults.push(...extractedItems);
  }
  
  // 2. 搜索 arXiv — 多组 query
  for (const q of arxivQueries) {
    await page.goto(`https://arxiv.org/search/?query=${encodeURIComponent(q)}&searchtype=all`);
    await page.waitForTimeout(2000);
    // 提取搜索结果（前 10 条）...
    // allResults.push(...extractedItems);
  }
  
  // 3. 搜索 Semantic Scholar — 补充检索
  for (const q of scholarQueries) {
    await page.goto(`https://www.semanticscholar.org/search?q=${encodeURIComponent(q)}`);
    await page.waitForTimeout(2000);
    // 提取搜索结果（前 10 条）...
    // allResults.push(...extractedItems);
  }
  
  // 去重（按 URL 去重）
  const seen = new Set();
  const uniqueResults = allResults.filter(r => {
    if (seen.has(r.url)) return false;
    seen.add(r.url);
    return true;
  });
  
  console.log(`检索完成: ${allResults.length} 条原始结果, 去重后 ${uniqueResults.length} 条`);
  
  // 输出结果到 JSON
  const output = {
    queries_used: [...patentQueries, ...arxivQueries, ...scholarQueries],
    results: uniqueResults,
    total_results: uniqueResults.length,
    search_timestamp: new Date().toISOString()
  };
  fs.writeFileSync(
    process.env.WORK_DIR + '/patent_run/stage-03/web_search_results.json',
    JSON.stringify(output, null, 2)
  );
  
  await browser.close();
})();
```

```bash
# 必须在 Playwright 固定目录下执行，确保 require('playwright') 能解析
cd $REPO_PATH/_patent_playwright && WORK_DIR="$WORK_DIR" node $WORK_DIR/playwright_search.js
```

> **注意**：Playwright 检索写入的 JSON 文件也须遵守规则 6（写入后验证），执行完脚本后用 `verify-write` 验证 `web_search_results.json` 非空且 JSON 合法。

**降级方案 B：使用宿主智能体的 `web_search` 工具**

若 Playwright 脚本执行失败（如 CAPTCHA 拦截、超时等），改用智能体内置的 `web_search` 工具：

1. 中文检索：`web_search(query="核心技术术语 专利 技术交底")`
2. 英文检索：`web_search(query="core_term patent specification method")`
3. 学术检索：`web_search(query="core_term arxiv OR 'semantic scholar'")`

从每次搜索结果中提取：标题、URL、摘要片段、来源类型。**至少执行 3 次不同 query 的搜索**。

**最终降级方案 C：基于项目依赖的智能体撰写**

若方案 A 和 B 均失败（如无网络环境），智能体可基于以下信息直接撰写参考文献：
- Stage 01 `code_context.md` 中的项目依赖（requirements.txt / package.json 等）
- Stage 04 现有技术分析报告中提及的技术方案
- Ideal 文档中的检索关键词

**方案 C 的额外要求**：
- 每条文献必须标注 `[待人工验证]` 后缀
- `web_search_results.json` 中 `source` 字段标记为 `"agent_knowledge"`
- 文献数量仍须 ≥ 8 条

**步骤 3：精选与整理输出**

> **广撒网精选流程**：步骤 2 的原始检索结果（≥20 条）全部保留在 `web_search_results.json` 中，然后按以下标准**精选 8-12 篇**写入 `references.md`。

**精选标准**（按优先级排序）：
1. **直接相关性**：与本发明解决的核心问题直接相关的专利/论文优先
2. **技术路线覆盖**：确保精选文献覆盖本发明涉及的所有关键技术模块（不能只集中在一个方向）
3. **来源多样性**：专利 ≥ 3 篇，学术论文 ≥ 3 篇，尽量三个站点都有代表
4. **时效性**：优先选择近 5 年内的文献
5. **权威性**：知名公司/机构的专利、高引用论文优先

**输出文件**：

- `patent_run/stage-03/references.md`：精选 **8-12 篇文献**的格式化引用列表，每篇包含：
  - 专利号或 DOI
  - 标题（中英文）
  - 来源链接（Google Patents / arXiv / Semantic Scholar URL）
  - 一句话相关性说明
  - **精选理由**（一句话说明为何入选，如"与本发明的图数据库建模方法直接相关"）
- `patent_run/stage-03/web_search_results.json`：**全部原始检索结果**的结构化 JSON（≥20 条，含未入选文献），**必须严格遵循以下 schema**：

```json
{
  "queries_used": ["中文检索词1", "english query 2"],
  "results": [
    {
      "title": "专利/论文标题",
      "url": "https://patents.google.com/patent/US20110231220A1",
      "snippet": "摘要或关键段落（≤200字）",
      "source": "google_patents | arxiv | semantic_scholar",
      "patent_id": "US20110231220A1",
      "arxiv_id": null,
      "doi": null
    }
  ],
  "total_results": 25,
  "search_timestamp": "2026-04-08T00:00:00+00:00"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `queries_used` | string[] | 是 | 实际使用的检索 query 列表（≥5 组） |
| `results` | object[] | 是 | 全部原始检索结果数组，≥20 条（含未精选文献） |
| `results[].title` | string | 是 | 专利/论文标题 |
| `results[].url` | string | 是 | 可访问的来源链接 |
| `results[].snippet` | string | 是 | 摘要片段 |
| `results[].source` | string | 是 | 枚举：`google_patents`/`arxiv`/`semantic_scholar` |
| `results[].patent_id` | string\|null | 否 | 专利号（如 US20110231220A1） |
| `results[].arxiv_id` | string\|null | 否 | arXiv ID（如 2603.10165） |
| `results[].doi` | string\|null | 否 | DOI 标识符 |
| `total_results` | int | 是 | 结果总数 |
| `search_timestamp` | string | 是 | ISO-8601 检索时间戳 |

**执行后验证**：确认 `references.md` 文件存在且包含至少 8 条带链接的精选文献引用，`web_search_results.json` 包含 ≥20 条原始检索结果，否则说明检索不充分，需增加检索 query 后重新执行。

**参考文献回填**：本 Stage 的文献列表存放在 `patent_run/stage-03/references.md`，`patent_to_json.py` 在 Stage 15 组装时会自动从 `stage-03`（优先）或 `stage-12` 读取并写入最终 `patent_content.json` 的「参考文献」章节。**严禁**最终参考文献为空。

### Stage 06：关键术语（→ `patent_run/stage-04/key_terms.md`）

撰写 **5-6 个**核心术语（严禁超过 6 个），每个术语用自然文本段落：
- **术语中文名称（English Term）**：一句话定义。在本发明中，指……。通俗理解：就像……一样。
- 类比必须用非技术人员熟悉的日常事物（食物、交通、家务），禁止用技术概念做类比
- **禁止使用表格格式**

### Stage 07：发明构思（→ `patent_run/stage-05/concept.md`）

包含两个子节：
- **2.1 核心发明构思**（100-200 字）：本质概括
- **2.2 核心创新点**（2-3 个，严禁超过 3 个）：每个用五段式 —— 痛点 / 现有不足 / 本发明方案 / 效果 / 通俗解释

通俗解释必须使用「假设你是XX（具体角色）」开头，说清 Before/After 对比和数字效果。

### Stage 08：背景技术（→ `patent_run/stage-06/background.md`）

必须使用 Markdown **三级标题**（###）标记子节，**禁止四级标题或加粗替代**：
- **### 3.1 相关背景描述，以及现有技术的技术方案**：描述 2-3 种最相近的现有技术（每种≤300 字）
- **### 3.2 现有技术的缺点或尚未解决的问题**：每种技术用「一句话痛点 + 具体场景表现」分析

整体不超过 1200 字。末尾用 1-2 句话过渡到本发明方案。

**Ideal 注入**：从 ideal_output.md 的「二、背景技术」和「五、与现有技术的区别」提取素材。

### Stage 09：发明内容（→ `patent_run/stage-07/invention_content.md`）

**这是最核心的章节**，必须包含以下子节（缺一不可，使用 ### 三级标题）：

**### 4.1 产品侧**（至少 2 个差异化场景，每个场景 2-3 步）

> **洋葱模型展示法（强制）**：产品侧采用"从外到内"三层递进展示，让不同角色的读者都能找到理解入口：
> - **最外层（UI 图）**：通过自动生成的 GUI 交互界面图，让非技术人员（法务、IP 管理人员）30 秒内理解"这个发明用在哪里、解决什么业务问题"
> - **中间层（交互流程）**：将 UI 上的用户操作翻译为系统指令序列，建立"界面动作→后台处理"的映射
> - **最内层（技术引导）**：在 4.1 末尾通过"映射关系引导语"将 UI 展示与 4.2 技术侧强绑定，指出 UI 只是应用场景的呈现，真正的技术创新在后台
>
> **设计初衷**：很多发明是纯后台算法或架构，没有天然的产品界面。系统自动生成的 GUI 交互图的核心价值是**让纯后台创新点被具象化理解**，而非展示 UI 设计本身。

- **步骤合并原则**：不要拆成碎步骤，每步必须包含完整的「用户输入 + 系统处理链路 + 输出结果」，使输入和输出更丰富
- **图位占位排版（强制 · 硬守卫）**：每个步骤描述后必须紧跟该步骤对应的**图位占位符**，格式为 `<!-- FIGURE:figure_type | 图注描述 -->`。**严禁写 Markdown 图片语法 `![]()`，严禁写截图文件路径**——截图尚未生成，路径由 Stage 10 决定、Stage 15 自动注入。占位符中的 `figure_type` 必须使用标准枚举值（见下方表格），`图注描述` 为中文简要说明。示例：
  ```markdown
  用户在主界面点击"新建项目"，系统弹出配置向导……（如图1所示）
  <!-- FIGURE:gui_a | 场景A步骤1：用户新建项目配置向导 -->
  ```
  **禁止先列完全部步骤文字再统一列占位符**——每个步骤文字后必须紧跟该步骤的占位符。
- **产品侧图位占位符 figure_type 枚举**：

  | figure_type | 用途 | 典型引用位置 |
  |-------------|------|-------------|
  | `scenario_overview` | 场景总览 | 4.1 开头，所有场景描述之前 |
  | `gui_a` | 场景A逐步截图 | 场景A的每个步骤之后 |
  | `gui_b` | 场景B逐步截图 | 场景B的每个步骤之后 |
  | `product_output_preview` | 产出物预览 | 最后一个场景的最后一步之后 |
  | `state_transition` | 状态转换 | 场景A与场景B之间的过渡段落 |
  | `innovation_linkage` | 创新点联动 | 4.1 末尾映射关系引导语之前或之后 |
  | `comparison` | 对比页 | 有益效果或场景描述中的旧方案对比 |

  **按需使用原则**：不是每种 figure_type 都必须出现。根据发明特点，只在叙事中有自然引用位置时才使用该类型占位符。场景逐步截图（`gui_a`、`gui_b`）为强制类型，其余为可选。
- **串行时间逻辑**：步骤之间必须有明确的时间或逻辑衔接词（如"接着"、"完成后"等），形成从用户实际操作视角的连贯流程
- 必须用「如图N所示」引用附图（图号在 Stage 15 自动按出现顺序编号，撰写时用 `图N` 占位即可）
- **严格 2-3 步，绝对禁止超过 3 步**
- **场景深度对等约束**：场景二的描述深度必须与场景一对等——每个步骤不少于 80 字，包含具体的角色名、操作细节、系统响应和量化数据。禁止场景二沦为场景一的简化复述

**4.1 末尾映射关系引导语（强制）**：

> 在 4.1 产品侧所有场景描述完毕后，**必须**插入一段过渡引导语，将前文的 UI 操作与后文的底层技术显式关联。格式模板如下（根据实际发明内容调整）：
>
> ---
> **底层技术支撑：** 为了实现上述图 1 至图 N 中展示的 [极简交互效果 / 自动化处理能力 / 一键生成功能]，本发明的底层技术采用了 [核心算法/架构的一句话概括]。上述产品界面仅为应用场景的呈现形式，真正的技术创新在于系统后台如何 [核心技术动作的一句话概括]。具体技术方案详见 4.2 节。
> ---

**### 4.2 技术侧**

> **定位提示（强制阅读指引）**：本节内容是支撑 4.1 中全部 UI 交互效果的"不可见"底层逻辑，是专利保护的真正核心。4.1 的 GUI 界面展示了用户看到什么；4.2 揭示了系统后台如何做到。审查重点应聚焦于本节的算法流程和架构设计。

- **术语降维（强制）**：技术描述中**严禁直接使用编程语言的数据结构名称**（如 dict、list、frozenset、tuple、dataclass 等）。必须将其替换为逻辑功能描述（如"键值映射关系"、"序列化集合"、"不可变状态集合"）。参考 [$SKILL_DIR/references/writing-style-guide.md](references/writing-style-guide.md) 的「术语映射规则（术语降维）」章节。
- **技术侧图文并茂（强制 · 硬守卫）**：4.2 技术侧的每个子节**必须**在描述末尾插入对应技术图表的占位符，格式与产品侧相同 `<!-- FIGURE:figure_type | 图注描述 -->`。4 个占位符缺一不可：

  | figure_type | 对应图表 | 插入位置 |
  |-------------|---------|---------|
  | `tech_architecture` | 系统架构图 | 4.2.1 系统架构描述末尾 |
  | `tech_flowchart` | 核心算法流程图 | 4.2.2 最后一个 S 步骤之后 |
  | `tech_sequence` | 模块间时序图 | 4.2.3 交互时序描述末尾 |
  | `tech_dataflow` | 数据流向图 | 4.2.4 数据流描述末尾 |

  示例：
  ```markdown
  本发明的系统架构分为三层：……（如图 N 所示）
  <!-- FIGURE:tech_architecture | 系统架构图：展示三层架构及核心组件 -->
  ```
  **每个占位符前必须有「如图 N 所示」引用**。占位符在 Stage 15 组装时自动替换为 `charts/` 目录下对应 PNG 图片。

- 4.2.1 系统技术架构：至少 3 层，每层至少 2 个组件。**精简度硬约束：每层描述不超过 80 字（层名 + 职责一句话 + 核心组件列表），全节不超过 400 字**。末尾必须插入 `<!-- FIGURE:tech_architecture | ... -->`
- 4.2.2 核心算法流程：用自然语言推导式描述，**禁止写伪代码、函数名、代码路径**。**每个步骤（S1-SN）必须包含以下 6 个子段（全部为强制必填，缺少任何一个子段即不合格）**：
  1. **问题动机**（1-2 句）：这一步要解决什么问题（用「如果不做这步会怎样」来解释）
  2. **技术动作**（**强制 ≤150 字，3-4 句**）：每句只说一个动作——判断条件、处理操作、输出结果。**禁止铺垫和解释性附加句**。参考 [$SKILL_DIR/references/writing-style-guide.md](references/writing-style-guide.md) 的「技术侧精简度规范」
  3. **输入数据样例**（强制）：用具体的字段名和示例值展示该步骤接收什么。格式示例：`仓库路径=/workspace/demo, 分支标识=feature/p1, 基线引用=origin/main`
  4. **输出数据样例**（强制）：用具体的字段名和示例值展示该步骤产出什么。格式示例：`候选变更集合=[file_a.py, file_b.py], 边界模式=远端对比`
  5. **关键参数**（强制）：列出该步骤涉及的核心配置项、阈值或约束条件及其具体取值
  6. **白话解释**（1 句，**≤40 字**）：用一句大白话总结这一步在做什么
  
  **S 步骤全部写完后**，必须插入 `<!-- FIGURE:tech_flowchart | ... -->`
- 4.2.3 模块间交互时序（**≤200 字**）：**必须提供独立于 S1-SN 步骤的新信息**（如模块间调用顺序、异步/同步关系、错误传播路径），禁止简单复述 S1-SN 的内容。**与 S1-SN 的句级重复率不得超过 30%**。末尾必须插入 `<!-- FIGURE:tech_sequence | ... -->`
- 4.2.4 数据流描述（**≤200 字**）：**必须聚焦数据格式的变换链路**（如输入为路径字符串→中间为结构化上下文对象→输出为 Markdown 文本），禁止与 S1-SN 或 4.2.3 高度重叠。**与 S1-SN 和 4.2.3 的句级重复率不得超过 30%**。末尾必须插入 `<!-- FIGURE:tech_dataflow | ... -->`

**### 4.3 有益效果**
- 围绕 2-3 个核心创新点，每个写 1 段 Before/After 对比（80-120 字）
- **全节不超过 400 字**
- **量化数据推导约束（强制）**：有益效果中出现的任何量化数据（如"复用率超过 70%"、"时间缩短 80%"），必须在同一段落或紧邻段落中给出推导过程或计算依据（如"23 个阶段中复用 16 个，复用率 = 16/23 ≈ 70%"）。无推导过程的量化数据视为不合格
- **有益效果角度转化（强制）**：有益效果**禁止以"省时间""省代码""省人工"作为首要卖点**。必须从技术效果和法律合规两个维度锚定价值。参考 [$SKILL_DIR/references/writing-style-guide.md](references/writing-style-guide.md) 的「有益效果转化指导」。效果表述的黄金公式：`技术手段的量化指标 + 该指标带来的技术/法律层面的直接收益`

**通俗化写作规范**（最高优先级）：
1. **30 秒规则**：每个段落首句让非技术人员 30 秒内理解
2. **先说人话，再说技术**：每个技术步骤先用日常类比开头
3. **精炼直接**：只描述核心技术要素，严禁啰嗦
4. **禁止一句话超过 40 个汉字**，超过必须拆分
5. 每个产品侧步骤 80-150 字（上限 150 字，超过即啰嗦），每个技术侧步骤 100-200 字

**技术方案完整性约束**：
- P1：权利要求的每项技术特征必须在发明内容中有对应详细描述
- P2：所有技术方案步骤必须基于上下文材料，严禁凭空编造
- P3：有益效果的量化数据必须来自 Ideal 文档或合理推理，不得捏造，且**必须有推导过程**
- P4：附图引用必须在文中注明（「如图N所示」）
- P5：**反重复约束**——4.2.3 和 4.2.4 必须各自提供独立的新视角信息，**与 S1-SN 步骤描述的句级重复率不得超过 30%**。检查方法：逐句对比 4.2.3/4.2.4 与 S1-SN，如果某句话仅是换了主语（如"编排器调用XX"→"S2 中系统调用XX"），视为重复

**图位占位符最低数量约束（强制 · 硬守卫）**：
- Stage 09 完成后，`invention_content.md` 中的 `<!-- FIGURE:xxx -->` 占位符总数**建议 14-18 个，最低不少于 14 个**（产品侧≥10 + 技术侧 4）
- **产品侧必需类型**：`scenario_overview`（≥1）、`gui_a`（≥2，场景A逐步）、`gui_b`（≥2，场景B逐步）、`product_output_preview`（≥1）、`state_transition`（≥1）、`innovation_linkage`（≥1）。`comparison` 为可选类型
- **技术侧必需类型（4 个，缺一不可）**：`tech_architecture`（1）、`tech_flowchart`（1）、`tech_sequence`（1）、`tech_dataflow`（1）
- 产品侧占位符不足 10 个或技术侧占位符不足 4 个时，**必须**在提交前补充缺失的占位符，不得进入 Stage 10
- 产品侧占位符数量决定 Stage 10 的截图数量；技术侧占位符在 Stage 15 自动映射到 `charts/` 目录下对应 PNG

**扩展方案（强制）**：
- 必须在 4.2 技术侧末尾或单独小节中提供至少 **2 个实质性扩展/替代方案**
- 每个扩展方案写清输入变化、处理变化、输出变化
- 示例：无远端基线场景、仅文档输入场景、仅 CLI 交互场景

**Ideal 注入**：从 ideal_output.md 提取创新点技术方案、应用场景 Before/After、系统架构信息。

### Stage 10：产品侧 UI 原型与 Playwright 截图（强制，→ `patent_run/stage-08/`）

> **⚠️ 强制要求**：本 Stage **禁止跳过**。无论发明是否涉及 GUI 交互，都必须为产品侧描述生成可视化的 UI 原型页面并截图，用于专利交底书的附图体系。

**步骤 0：解析图位需求清单（硬守卫 · 按需联动）**

> **核心原则**：截图数量和类型完全由 Stage 09 的 `invention_content.md` 中的 `<!-- FIGURE:xxx -->` 占位符决定。不多截、不少截、不凑数。

读取 `patent_run/stage-07/invention_content.md`（或修订版 `stage-10/invention_content.md`），用正则 `<!-- FIGURE:(\w+)\s*\|\s*(.+?)\s*-->` 提取所有占位符，生成**图位需求清单**：

```
图位需求清单示例：
  #1  figure_type=scenario_overview  caption=场景总览：多角色业务全景
  #2  figure_type=gui_a              caption=场景A步骤1：用户新建项目
  #3  figure_type=gui_a              caption=场景A步骤2：系统自动分析
  #4  figure_type=gui_a              caption=场景A步骤3：产出物预览
  #5  figure_type=gui_b              caption=场景B步骤1：批量导入
  ...
```

**硬守卫规则**：
- 如果清单为空（没有任何 `<!-- FIGURE:xxx -->` 占位符），说明 Stage 09 没有遵循图位占位规范，**必须中断并报错**，要求返回重写 Stage 09
- 清单中至少应包含 `gui_a` 和 `gui_b` 类型（场景逐步截图为强制），否则报警告

**步骤 1：生成多视图 HTML 原型**

> **🔒 强制模板引用**：生成 HTML 时**必须参考** [$SKILL_DIR/references/html-template-guide.md](references/html-template-guide.md) 中的「一、产品侧 UI 原型」章节，**原样复制**其中的 CSS 骨架到 `<style>` 标签中，并按其 HTML 结构骨架组织页面。**禁止自行设计 CSS 样式**——只允许在骨架基础上增加业务特定样式（如特定场景的额外卡片），不允许修改骨架中已定义的核心样式（导航栏配色、max-width、卡片圆角、字号等）。

基于**图位需求清单**和 Stage 09 产品侧（4.1 节）的场景描述，以及 Ideal 文档中的「产品表现特征」「附图设计建议」章节，**仅为清单中出现的 figure_type 生成对应视图**的 HTML 页面。**必须从用户实际操作产品的视角设计连贯的 UI 交互流程**。

各 figure_type 对应的视图设计规范：
- **`scenario_overview`（场景总览页）**：展示完整业务流程的概览，多角色/多场景的全局视图
- **`gui_a`（场景 A 逐步页）**：基础操作路径，**按用户操作的串行时间逻辑逐一展示**用户输入→系统处理→结果展示（每步一个独立视图状态，页面间要有明显的流程推进感）。**最后一步（结果展示步）必须包含实际产出物的内容预览区**——不是空洞的"完成"状态，而是真实展示系统输出了什么（如文档预览、图表缩略图、报告片段等），以**本发明主题自身的产出物作为案例素材**
- **`gui_b`（场景 B 逐步页）**：扩展操作路径，**同样按用户操作流程逐一展示**（不允许仅一张总览图，必须有每步独立状态）。**最后一步同样必须包含实际产出物预览**
- **`product_output_preview`（产出物实例展示页）**：**独立的产出物案例展示视图**，将本发明的核心输出成果以高保真方式呈现。该页面必须让读者直观看到"这个系统到底能产出什么东西"，而非仅停留在抽象概念描述
- **`state_transition`（状态转换页）**：展示场景 A 与场景 B 之间的**动态切换示意**，包含切换触发条件、共享元素和差异元素对比
- **`innovation_linkage`（创新点联动总览页）**：作为产品侧与技术侧的**桥梁视图**，展示"GUI 操作 → 后台处理模块 → 创新点"的端到端映射。**必须使用 5 列 Grid 布局**（左列=产品侧操作步骤，箭头列，中列=后台处理链路，箭头列，右列=创新点亮点），参考模板中的 `.linkage-grid` 样式
- **`comparison`（对比页）**：展示旧方案 vs 本发明方案的差异

页面必须包含：场景切换导航、步骤导航、当前场景/步骤标识、附图编号标注。**只生成图位需求清单中实际存在的视图类型**——清单没有的 figure_type 不要凑数生成。

**交叉引用标注规范（强制）**：
- 每张产品侧截图的**右上角或底部**必须包含创新点标签（如角标显示"🔷创新点1"），标注该视图主要体现哪个创新点
- 产品侧截图中涉及技术实现的区域，用虚线框+标注文字引导读者"详见技术侧图N"
- 技术侧图表在产品侧的"创新点联动总览页"中以缩略图形式嵌入，建立视觉关联

**HTML 页面视觉设计规范（强制 · 参考模板骨架）**：

> **⚠️ 以下规范的具体 CSS 实现已固化在** [$SKILL_DIR/references/html-template-guide.md](references/html-template-guide.md) 中，**必须原样复制使用**，不得自行重写。

- **导航栏**：**蓝底白字**（`background: #1a73e8; color: #fff`），胶囊形 tab（`border-radius: 20px`），品牌名带 emoji 前缀（如 `🔬 CodePatent {系统名}`）。**严禁白底导航栏**
- **视图容器宽度**：`max-width: 1400px`。**严禁缩小到 1200px 或更小**
- **卡片样式**：圆角卡片（`border-radius: 12px`）、轻微阴影（`box-shadow: 0 2px 8px rgba(0,0,0,0.08)`）、白色背景
- **字号清晰**：标题 20px+、正文 14px+、标签 12px+
- **布局整齐**：使用 CSS Grid 或 Flexbox 布局，卡片内容对齐，留白适当
- **图注标签**：每个视图底部必须有 `.fig-label`（居中、13px、灰色、加粗）标注图号和描述
- **字体**：使用系统中文友好字体栈 `'PingFang SC', 'Microsoft YaHei', -apple-system, sans-serif`

**生成后视觉自检清单（强制执行，参考 html-template-guide.md 第四节"禁止行为清单"）**：
1. 导航栏是否为蓝底白字？
2. `max-width` 是否为 1400px？
3. 联动页是否使用 5 列 `.linkage-grid`？
4. 差异对比页是否使用 `.diff-panel` 双栏布局？
5. 归属判定场景是否使用 `.attribution-bar` 比例条？
6. 每个视图底部是否有 `.fig-label` 图注？

将 HTML 文件保存到 `patent_run/stage-08/code/index.html`。

> **⚠️ 中文路径规避（强制）**：如果 `$WORK_DIR` 路径包含非 ASCII 字符，先将 HTML 写到 `$PLAYWRIGHT_DIR/`，用 `wc -c` 确认非空，然后**必须 `cp` 到 `$WORK_DIR/patent_run/stage-08/code/index.html`**。Stage 15 的 deliverables 汇聚依赖此路径。

**步骤 2：使用本地 Playwright 无头浏览器自动截图（高清模式）**

智能体生成 `$WORK_DIR/playwright_screenshot.js` 脚本，以无头模式对 HTML 页面逐步截图。**截图数量和顺序严格对应图位需求清单**：

```javascript
// playwright_screenshot.js — 智能体根据图位需求清单动态生成
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ headless: true });
  // 强制高清截图：2x 设备像素比 + 1440px 宽度
  const page = await browser.newPage({
    deviceScaleFactor: 2,
    viewport: { width: 1440, height: 900 }
  });
  
  // 打开本地 HTML 文件
  await page.goto('file://' + path.resolve('patent_run/stage-08/code/index.html'));
  
  // 严格按图位需求清单顺序截图（每个占位符对应一张截图）
  // 示例：清单 #1 → step_01_fig_scenario_overview.png
  await page.screenshot({ path: 'patent_run/stage-08/screenshots/step_01_fig_scenario_overview.png', fullPage: false });
  // ... 按清单逐一切换视图状态并截图 ...
  
  await browser.close();
})();
```

```bash
# 方式 1：在 Playwright 固定目录下执行（推荐）
cd $REPO_PATH/_patent_playwright && node $WORK_DIR/playwright_screenshot.js

# 方式 2：通过 NODE_PATH 指定 Playwright 安装路径（适用于非 cd 场景）
NODE_PATH=$REPO_PATH/_patent_playwright/node_modules node $WORK_DIR/playwright_screenshot.js
```

截图要求：
1. **必须 headless 模式**（`chromium.launch({ headless: true })`）
2. **必须高清模式**：`deviceScaleFactor: 2`（2 倍像素密度），`viewport` 宽度不小于 1440px
3. **截图数量 = 图位需求清单条目数**：每个 `<!-- FIGURE:xxx -->` 占位符精确对应一张截图，不多不少
4. 截图命名格式：`step_NN_fig_描述.png`，NN 从 01 递增，与图位需求清单顺序一致
5. 每张截图的视图状态必须有实质差异（内容不同或交互状态不同）

**Playwright 截图三层防护（强制 · 规则 6 扩展）**：

> **⚠️ 本防护解决上次执行中 HTML 0 字节 → 截图空白 → 后续全部中断的连锁故障。三层防护缺一不可。**

**第一层：HTML 预检（截图前）**

```bash
# 在执行 Playwright 截图脚本之前，必须先验证 HTML 文件非空
wc -c $WORK_DIR/patent_run/stage-08/code/index.html
# 如果 = 0 字节 → 中断，按规则 6 重写 HTML
# 如果 < 5000 字节 → 警告，HTML 内容可能不完整
python3 $SKILL_DIR/scripts/orchestrate.py verify-write $WORK_DIR/patent_run/stage-08/code/index.html --min-size 5000
```

**第二层：脚本内 DOM 检查（截图中）**

截图脚本**必须**在截图前加入 DOM 完整性检查：

```javascript
// 在 page.goto() 之后、screenshot() 之前，必须检查页面内容
await page.waitForTimeout(1000);
const bodyLen = await page.evaluate(() => document.body.innerHTML.length);
if (bodyLen < 100) {
  throw new Error(`HTML 未正确加载: body.innerHTML 仅 ${bodyLen} 字符`);
}
const idCount = await page.evaluate(() => document.querySelectorAll('[id]').length);
if (idCount < 3) {
  console.warn(`警告: 页面仅有 ${idCount} 个 ID 元素，可能未正确渲染`);
}
```

**第三层：PNG 后检（截图后）**

```bash
# 截图脚本执行完毕后，验证每张 PNG 的大小
ls -la $WORK_DIR/patent_run/stage-08/screenshots/*.png
# 每张 ≥ 50KB 才算有效，< 50KB 说明渲染失败需重新截图

# 使用 verify-write 逐一验证关键截图
python3 $SKILL_DIR/scripts/orchestrate.py verify-write $WORK_DIR/patent_run/stage-08/screenshots/step_01_fig_scenario_overview.png --png-min-kb 50

# 验证截图数量与预期一致
ls $WORK_DIR/patent_run/stage-08/screenshots/*.png | wc -l
# 数量必须 ≥ 图位需求清单条目数
```

截图保存到 `patent_run/stage-08/screenshots/`。

**步骤 3：生成附图注册表**

输出 `patent_run/stage-08/figure_registry.json`，**必须严格遵循以下 8 字段 schema**（新增 `placeholder_index` 字段用于与占位符精确对齐）：

```json
[
  {
    "figure_num": 1,
    "figure_id": "fig_scenario_overview",
    "figure_type": "scenario_overview",
    "caption_cn": "图1：应用场景总览图",
    "view_id": "view-scenario-overview",
    "screenshot_file": "step_01_fig_scenario_overview.png",
    "section_refs": ["4.1", "附图说明"],
    "placeholder_index": 0
  }
]
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `figure_num` | int | 是 | 图号，从 1 递增 |
| `figure_id` | string | 是 | 语义化 ID（如 `fig_scenario_overview`、`fig_gui_a_step0`） |
| `figure_type` | string | 是 | 枚举：`scenario_overview`/`gui_a`/`gui_b`/`state_transition`/`product_output_preview`/`innovation_linkage`/`tech_architecture`/`tech_flowchart`/`tech_sequence`/`comparison`/`flow_overview`/`product_demo` |
| `caption_cn` | string | 是 | 中文图注（如"图1：应用场景总览图"） |
| `view_id` | string | 是 | HTML 页面中对应视图的 ID（如 `view-scenario-overview`），无对应视图时为空字符串 |
| `screenshot_file` | string\|null | 是 | 截图文件名（如 `step_01_fig_scenario_overview.png`），技术图表无截图时为 null |
| `section_refs` | string[] | 是 | 关联的专利章节（如 `["4.1", "附图说明"]`） |
| `placeholder_index` | int | 是 | 对应 `invention_content.md` 中第几个 `<!-- FIGURE:xxx -->` 占位符（从 0 开始） |

**产品侧与技术侧配图分类标准**：
- **产品侧配图**（以 GUI 交互演示为重点）：`figure_type` 为 `scenario_overview`、`gui_a`、`gui_b`、`state_transition`、`product_output_preview`、`innovation_linkage`、`comparison`、`product_demo`
- **技术侧配图**（以技术方案展示为重点）：`figure_type` 为 `tech_architecture`、`tech_flowchart`、`tech_sequence`、`flow_overview`

**降级方案**：若本地 Playwright 截图失败，使用 `image_gen` 工具（多模态内容生成 skill）根据产品侧描述生成对应数量的场景示意图。

**执行后验证**：
1. `screenshots/` 目录下的 PNG 数量**必须等于**图位需求清单的条目数
2. `figure_registry.json` 的条目数**必须等于**图位需求清单的条目数
3. 每张截图文件大小不低于 **50KB**（过小说明内容空白或渲染失败）
4. `figure_registry.json` 中每个条目的 `placeholder_index` 必须连续且从 0 开始
5. **禁止重复截图凑数**——内容哈希（MD5）完全相同的截图对将被视为重复

### Stage 11：技术图表生成（强制，→ `$WORK_DIR/charts/`）

> **⚠️ 强制要求**：本 Stage **禁止跳过**。必须生成至少 4 类技术图表的 PNG 图片文件，用于技术侧的附图体系。

**必须生成的 4 类图表**：

1. **系统架构图**（`charts/system_architecture.png`）：展示系统分层架构，至少 3 层，每层标注组件名称和职责
2. **技术流程图**（`charts/technical_flowchart.png`）：展示核心算法的完整处理流程，包含判断分支。**必须基于 Stage 09（4.2.2）中提炼的主干控制流来绘制**，仅展示业务判断分支和数据转换步骤，不得包含错误处理、日志记录等非核心节点。每个步骤节点应与 S1-SN 一一对应
3. **模块时序图**（`charts/module_sequence.png`）：展示一次完整处理中各模块的调用顺序和数据传递
4. **数据流图**（`charts/data_flow_diagram.png`）：展示输入数据如何在系统内部逐步转化为输出

**可选生成的图表**（推荐生成）：
5. 场景对比图（`charts/scenario_illustration.png`）：Before/After 或新旧方案对比
6. 创新点高亮图（`charts/innovation_highlight.png`）：突出展示核心创新点

**生成方式（按优先级）**：

**优先方案 A：HTML + Playwright 截图（推荐，与 Stage 10 统一技术栈）**

智能体编写包含 4 类技术图表的 HTML 页面，使用与 Stage 10 相同的现代 UI 设计规范，然后通过 Playwright 无头浏览器高清截图。

**步骤 1：生成技术图表 HTML 页面**

> **🔒 强制模板引用**：生成技术图表 HTML 时**必须参考** [$SKILL_DIR/references/html-template-guide.md](references/html-template-guide.md) 中的「二、技术图表」章节，**原样复制**其中的 CSS 骨架到 `<style>` 标签中，并按其各图表 HTML 结构模板组织页面。**禁止自行设计图表 CSS 样式**。特别注意：
> - 架构图**必须使用水平标题**（`.arch-layer-title`），**严禁使用垂直文字标签**（`writing-mode:vertical-rl`）
> - **必须使用 SVG 连线**（参考模板中的 SVG marker 定义和连线示例），**严禁使用 `▼` / `→` 等文本字符代替箭头**
> - 时序图**必须使用 SVG 绘制生命线和消息箭头**，参考模板中的时序图 SVG 示例
> - `max-width` 必须为 `1400px`，与产品侧保持一致

基于 Stage 09 技术侧（4.2 节）的内容，生成 `$WORK_DIR/charts/tech_charts.html`，包含 4 个独立视图区域（每类图表一个），每个区域通过 HTML `id` 属性标识，便于逐一截图。

> **⚠️ 中文路径规避**：如果 `$WORK_DIR` 路径包含非 ASCII 字符（如中文发明名称），IDE 的文件写入工具可能偶发写入 0 字节文件。建议先将 HTML 写到 `$PLAYWRIGHT_DIR/tech_charts.html`（该目录不含中文）或 `/tmp/patent_tech_charts.html`，用 `wc -c` 确认文件非空后，再 `cp` 到 `$WORK_DIR/charts/tech_charts.html`。Playwright 截图脚本中 `page.goto()` 也应使用无中文路径的副本（如 `/tmp/` 中的文件）来避免 `file://` URL 编码问题。

**HTML 技术图表视觉设计规范（强制 · 参考模板骨架）**：

> **⚠️ 以下规范的具体 CSS 实现已固化在** [$SKILL_DIR/references/html-template-guide.md](references/html-template-guide.md) 中，**必须原样复制使用**，不得自行重写。

- **整体风格**：与 Stage 10 产品侧 UI 原型保持一致的现代设计风格
- **视图宽度**：`max-width: 1400px`。**严禁缩小到 1200px 或更小**
- **配色方案**：使用统一的专利配色体系（主色 `#1a73e8`、辅助色 `#34a853`/`#ea4335`/`#fbbc04`、背景色 `#f8f9fa`、边框色 `#dadce0`）
- **卡片样式**：圆角卡片（`border-radius: 12px`）、轻微阴影（`box-shadow: 0 2px 8px rgba(0,0,0,0.1)`）、白色背景
- **字号规范**：图表标题不小于 20px、节点/组件文本不小于 14px、标注/说明文本不小于 12px
- **布局方式**：CSS Grid / Flexbox 布局节点，**内联 SVG 绘制所有连线和箭头**
- **SVG 连线规范**：线宽不小于 `2px`（`stroke-width: 2`），箭头尺寸 `markerWidth: 10, markerHeight: 7`，主路径用主色（`#1a73e8`），次路径用灰色（`#5f6368`），错误路径用红色（`#ea4335`）
- **字体**：使用系统中文友好字体栈 `'PingFang SC', 'Microsoft YaHei', -apple-system, sans-serif`
- **架构图层标题**：**必须使用水平标题**（`.arch-layer-title`），**严禁垂直文字标签**（`writing-mode:vertical-rl`）

**4 类图表的 HTML 绘制指南**：

> **⚠️ 连线方案强制要求**：所有图表的箭头和连线**必须使用内联 SVG** 绘制（`<svg>` + `<line>` / `<polyline>` + `<marker>`），**禁止使用纯 CSS `::after` 伪元素**绘制箭头（CSS 伪元素在复杂布局中容易因元素高度/位置计算错误导致连线断裂或不显示）。节点仍然使用 CSS Grid/Flexbox 布局，连线使用覆盖在节点之上的 SVG 层绘制。

**SVG 箭头 marker 定义（全局复用，放在 HTML `<head>` 或图表区域开头）**：

```html
<svg width="0" height="0" style="position:absolute">
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#5f6368"/>
    </marker>
    <marker id="arrowhead-blue" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#1a73e8"/>
    </marker>
    <marker id="arrowhead-green" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#34a853"/>
    </marker>
  </defs>
</svg>
```

| 图表类型 | HTML 实现方式 | 关键要素 |
|---------|-------------|---------|
| 系统架构图 | CSS Grid 分层布局 + **内联 SVG 层间连线** | 每层用不同背景色区分，组件用圆角卡片表示。**层间连线用 `<svg>` 绝对定位覆盖层，`<line>` + `marker-end="url(#arrowhead)"` 绘制向下箭头**，确保连线100%渲染 |
| 技术流程图 | Flexbox 节点布局 + **内联 SVG 连线网格** | 处理节点用圆角矩形、判断节点用菱形（CSS `transform: rotate(45deg)` 或 SVG `<polygon>`）。**所有步骤间连线和分支箭头用 `<svg>` 覆盖层的 `<line>` / `<polyline>` 绘制**，Yes/No 分支用不同颜色 marker |
| 模块时序图 | CSS Grid 列布局 + **内联 SVG 消息箭头** | 每个模块占一列（顶部标题栏），**生命线用 SVG `<line>` 绘制垂直虚线（`stroke-dasharray: 5,5"`）**，**模块间调用用 SVG `<line>` + `marker-end` 绘制水平实线箭头**，消息文本用 SVG `<text>` 或 HTML 绝对定位标注在箭头上方 |
| 数据流图 | Flexbox 链式布局 + **内联 SVG 转换箭头** | 数据节点用椭圆或圆角卡片，**节点间转换箭头用 `<svg>` 覆盖层的 `<line>` + `marker-end` 绘制**，不同数据链路用不同颜色区分（蓝色/绿色/橙色），每个节点标注数据格式 |

**SVG 连线实现模式（参考代码）**：

```html
<!-- 在图表容器上设置 position:relative，SVG 覆盖层设置 position:absolute -->
<div style="position:relative">
  <!-- CSS 布局的节点 -->
  <div class="node" id="node-1">节点1</div>
  <div class="node" id="node-2">节点2</div>
  <!-- SVG 连线覆盖层 -->
  <svg style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1">
    <line x1="200" y1="60" x2="200" y2="120" stroke="#5f6368" stroke-width="2" marker-end="url(#arrowhead)"/>
  </svg>
</div>
```

**图表内容要求**：
- 节点文本使用中文
- 关键节点/步骤使用醒目颜色（主色或辅助色）高亮
- 每张图表包含标题栏（标注图号和中文标题）
- **连线/箭头必须使用内联 SVG 绘制**，关键路径使用加粗（`stroke-width: 3`）或彩色线条
- 判断分支标注条件文本（如"是/否"、"成功/失败"），用不同颜色 marker 区分
- **场景溯源标签（强制）**：每张技术图表的**右上角或标题栏旁**必须包含溯源标签（如"支撑场景A步骤2"、"支撑4.1产品侧全流程"），标注该图表支撑产品侧哪个操作场景/步骤
- **连线质量自检**：生成 HTML 后，智能体必须检查每张图表中的 SVG `<line>` / `<polyline>` 元素数量是否不少于节点数量减1（N个节点至少N-1条连线），连线数量为0视为渲染失败

**步骤 2：使用 Playwright 无头浏览器逐图截图（高清模式）**

> **🔒 强制使用元素级截图**：技术图表**必须**使用 `element.screenshot()` 对每个图表区域逐一截图，**严禁全页截图**。参考 [$SKILL_DIR/references/html-template-guide.md](references/html-template-guide.md) 中「三、Playwright 截图脚本模板」的 `playwright_charts.js` 模板。

智能体生成 `$WORK_DIR/charts/playwright_charts.js` 脚本，对 HTML 页面中的每个图表区域逐一截图：

```javascript
// playwright_charts.js — 智能体根据图表区域 ID 动态生成
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const browser = await chromium.launch({ headless: true });
  // 强制高清截图：2x 设备像素比 + 1440px 宽度
  const page = await browser.newPage({
    deviceScaleFactor: 2,
    viewport: { width: 1440, height: 2000 }
  });
  
  // 打开本地 HTML 文件（优先使用无中文路径的副本）
  const htmlPath = process.env.HTML_PATH || path.resolve('charts/tech_charts.html');
  await page.goto('file://' + htmlPath);
  await page.waitForTimeout(1500);
  
  // 第二层防护：DOM 完整性检查
  const bodyLen = await page.evaluate(() => document.body.innerHTML.length);
  if (bodyLen < 100) {
    throw new Error(`HTML 未正确加载: body.innerHTML 仅 ${bodyLen} 字符，请检查 HTML 文件是否非空`);
  }
  const allIds = await page.evaluate(() => Array.from(document.querySelectorAll('[id]')).map(e => e.id));
  console.log('页面中找到的 ID 元素:', JSON.stringify(allIds));
  
  // 逐个图表区域截图（含 fallback）
  const charts = [
    { id: '#chart-system-architecture', file: 'system_architecture.png' },
    { id: '#chart-technical-flowchart', file: 'technical_flowchart.png' },
    { id: '#chart-module-sequence', file: 'module_sequence.png' },
    { id: '#chart-data-flow', file: 'data_flow_diagram.png' }
  ];
  
  const outputDir = process.env.OUTPUT_DIR || 'charts';
  let successCount = 0;
  for (const chart of charts) {
    const element = await page.$(chart.id);
    if (element) {
      await element.screenshot({ path: path.join(outputDir, chart.file) });
      const size = fs.statSync(path.join(outputDir, chart.file)).size;
      console.log(`OK: ${chart.file} (${(size/1024).toFixed(1)}KB)`);
      successCount++;
    } else {
      // Fallback：尝试 locator 方式
      const loc = page.locator(chart.id);
      if (await loc.count() > 0) {
        await loc.screenshot({ path: path.join(outputDir, chart.file) });
        console.log(`OK (locator fallback): ${chart.file}`);
        successCount++;
      } else {
        console.error(`FAIL: 元素 ${chart.id} 未找到。可用 ID: ${JSON.stringify(allIds)}`);
      }
    }
  }
  
  console.log(`截图完成: ${successCount}/${charts.length} 成功`);
  if (successCount < charts.length) {
    process.exitCode = 1;
  }
  
  await browser.close();
})();
```

```bash
# 方式 1：在 Playwright 固定目录下执行（推荐）
cd $REPO_PATH/_patent_playwright && node $WORK_DIR/charts/playwright_charts.js

# 方式 2：通过 NODE_PATH 指定 Playwright 安装路径（适用于非 cd 场景）
NODE_PATH=$REPO_PATH/_patent_playwright/node_modules node $WORK_DIR/charts/playwright_charts.js
```

截图要求：
1. **必须 headless 模式**（`chromium.launch({ headless: true })`）
2. **必须高清模式**：`deviceScaleFactor: 2`（2 倍像素密度），`viewport` 宽度不小于 1440px
3. 使用元素级截图（`element.screenshot()`）而非全页截图，确保每张图表裁切精准
4. 每张截图 PNG 文件大小不低于 **30KB**（过小说明内容空白或渲染失败）

**Playwright 截图三层防护（强制 · 与 Stage 10 一致）**：

> **⚠️ 上次执行中 Stage 11 失败的根因链**：tech_charts.html 被写入 0 字节 → Playwright 打开空白页面 → `page.$('#chart-xxx')` 返回 null → 0 张图表 → 后续全部中断。

**第一层：HTML 预检（截图前）**

```bash
# 在执行截图脚本前，必须验证 HTML 非空
wc -c $WORK_DIR/charts/tech_charts.html
# 如果 = 0 字节 → 中断，按规则 6 重写（先写到 $PLAYWRIGHT_DIR/ 再 cp）
python3 $SKILL_DIR/scripts/orchestrate.py verify-write $WORK_DIR/charts/tech_charts.html --min-size 3000
```

**第二层：脚本内 DOM 检查（截图中）**

上述脚本模板已包含 `bodyLen` 和 `allIds` 检查。如果 `bodyLen < 100`，脚本会抛出异常并终止。

**第三层：PNG 后检（截图后）**

```bash
# 验证 4 张 PNG 均存在且 ≥ 30KB
ls -la $WORK_DIR/charts/*.png
python3 $SKILL_DIR/scripts/orchestrate.py verify-write $WORK_DIR/charts/system_architecture.png --png-min-kb 30
python3 $SKILL_DIR/scripts/orchestrate.py verify-write $WORK_DIR/charts/technical_flowchart.png --png-min-kb 30
python3 $SKILL_DIR/scripts/orchestrate.py verify-write $WORK_DIR/charts/module_sequence.png --png-min-kb 30
python3 $SKILL_DIR/scripts/orchestrate.py verify-write $WORK_DIR/charts/data_flow_diagram.png --png-min-kb 30
```

**降级方案 B：Mermaid CLI 渲染（高清模式）**

若 HTML + Playwright 截图失败（如 Playwright 未安装），使用 Mermaid CLI 渲染：

1. 基于技术方案用 Mermaid 语法生成 `.mmd` 文件（节点文本使用中文，换行用 `<br/>`）

2. **每个 .mmd 文件头部必须注入以下 init 配置**（确保高清、美观、中文友好）：
```
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '16px', 'fontFamily': 'PingFang SC, Microsoft YaHei, sans-serif', 'primaryColor': '#e8f0fe', 'primaryBorderColor': '#1a73e8', 'lineColor': '#5f6368', 'primaryTextColor': '#1a1a1a'}}}%%
```

3. **Mermaid 图表美观布局规范**：
   - 节点文本字号不小于 14px，关键节点使用加粗
   - 节点间距适当加大，避免文字重叠
   - 使用语义化颜色区分不同类型节点（如输入/处理/输出/判断）
   - 流程图使用 `TD`（从上到下）布局，时序图使用 `sequenceDiagram`
   - 节点文本控制在 20 字以内，超长时使用 `<br/>` 换行

4. 调用 Mermaid CLI 渲染为高清 PNG：
```bash
npx @mermaid-js/mermaid-cli -i chart.mmd -o chart.png -b white --scale 3 -w 1600
```

> **渲染参数说明**：`-b white` 白色背景（替代透明背景，避免嵌入 DOCX 后背景异常）；`--scale 3` 三倍缩放确保高清；`-w 1600` 宽度 1600px 确保图表不被压缩。

**降级方案 C：多模态内容生成**
若以上方案均不可用，使用 `image_gen` 工具（多模态内容生成 skill）生成技术图表：
- 为每类图表编写详细的文字描述 prompt
- 生成至少 4 张 PNG 图片

将所有 PNG 图表保存到 `$WORK_DIR/charts/` 目录。若使用方案 B，同时将 `.mmd` 源文件保存到 `$WORK_DIR/` 供参考。

**执行后验证**：确认 `$WORK_DIR/charts/` 目录下至少有 **4 张 PNG 文件**（架构图 + 流程图 + 时序图 + 数据流图），每张文件大小不低于 **30KB**，否则需切换到降级方案重新生成。

### Stage 12：专利评审（→ `patent_run/stage-09/reviews.md`）

以资深专利代理人视角，按以下 **16 项**清单逐项检查：

1. **结构完整性**：是否包含全部必备章节；是否存在论文体章节（讨论/结论/局限性）→ 必须删除
2. **多场景覆盖**：产品侧至少 2 个差异化场景；每个场景 2-3 步（严禁超过 3 步）；**场景二描述深度是否与场景一对等**（每步≥80 字）
3. **附图体系**：架构图/流程图/时序图/GUI 截图是否有引用
4. **技术深度**：核心算法有带示例数据的步骤描述；至少 3 层架构
5. **创新点表述**：痛点→现有不足→本方案→效果 四段式
6. **术语一致性**：全文术语统一
7. **可实施性**：技术方案足够详细到可实施
8. **扩展方案**：2-3 个实质性变形
9. **通俗可读性**：精炼直接；Before/After 量化对比
10. **6 子段完整性**：4.2.2 核心算法流程中每个 S 步骤是否完整包含 6 个子段（问题动机、技术动作、输入数据样例、输出数据样例、关键参数、白话解释），缺少任何子段标记为 ❌
11. **创新点举证充分性**：每个核心创新点（2-3 个）是否在 4.2.2 中有至少一个专门的 S 步骤为其提供完整技术方案举证，而非在泛化步骤中混合描述
12. **术语降维合规性**：搜索全文中是否存在裸露的编程语言数据结构名称（`dict`、`list`、`tuple`、`array`、`frozenset`、`set`、`dataclass`、`struct`、`callback`、`hook`、`regex`、`async`、`await`、`git log`、`git diff`、`JSON`、`YAML`、`TOML`、`API`、`endpoint`、`pipeline`、`AST`）。在正文叙述段落中出现任何一个即标记为 ❌，必须替换为逻辑功能描述。参考 writing-style-guide.md 的「术语映射规则（术语降维）」
13. **创新点可授权性检测**：对每个创新点执行"创造性自检三问"（技术问题具体性 / 方案区别性 / 效果非显而易见性）。如果创新点的核心价值表述为"减少代码量""提高开发效率""节省人工时间"等工程优化视角，标记为 ⚠️ 并建议从技术壁垒角度重新锚定（参考 writing-style-guide.md 的「创新点价值锚定」）
14. **UI-技术映射完整性**：检查 4.1 产品侧末尾是否存在"映射关系引导语"（将 UI 操作与 4.2 底层技术显式关联）；检查 4.2 技术侧开头是否存在"定位提示"（说明本节是支撑 4.1 界面效果的底层实现）。两者缺一标记为 ⚠️
15. **创新点层次适当性**：检查 2-3 个核心创新点中，是否至少有 **1 个**描述的是**系统级/产品级新能力**（多模块协同产生的涌现能力，如"从纯代码仓库端到端生成专利底稿+配套 UI 附图"），而非全部停留在单模块工程实现层面（如"Git 归属判定""文本清洗管道"）。如果全部创新点都是模块级实现细节，标记为 ❌ 并建议重新审视项目的核心价值命题
16. **技术侧图文结合度（新增）**：检查 4.2 技术侧是否包含 4 个技术图表占位符（`tech_architecture`/`tech_flowchart`/`tech_sequence`/`tech_dataflow`），且每个占位符前有「如图 N 所示」引用。缺少任何一个占位符标记为 ❌；有占位符但无图引用标记为 ⚠️。同时检查 4.2.1 每层描述是否≤80 字、4.2.2 技术动作子段是否≤150 字、4.2.3/4.2.4 是否各≤200 字

**对抗性评审模式（强制）**：
- 评审者**必须**找出至少 **3 个实质性弱点**和 **1 个建设性改进方向**
- 禁止所有检查项全部通过（如果 16 项检查中标记为 ✅ 的超过 13 项，必须重新审视是否存在评审盲区）
- 对于看起来"足够好"的内容，也必须从专利审核师的角度找出潜在的驳回理由

**内容真实性审核**：权利要求是否有未公开的技术特征、有益效果是否有无依据的量化数据（**量化数据必须有推导过程**）、附图引用是否一致。

**精简度检查**（强制）：关键术语>6个→🔴、产品侧>4步→🔴、技术侧出现代码→🔴、有益效果>400字→🔴、6子段不完整→🔴、编程语法裸露→🔴、创新点以"省时间/省代码"为首要卖点→🔴、缺少映射关系引导语→🔴、**技术动作子段>150字→🔴**、**4.2.3或4.2.4>200字→🔴**、**4.2缺少技术图表占位符→🔴**

对每项给出：✅ 通过 / ⚠️ 需修改 / ❌ 缺失 + 详细问题 + 修改建议。

### Stage 13：专利修订（→ `patent_run/stage-10/` 下各 `revised_*.md`）

根据 Stage 12 评审意见逐条修订：
- ✅ 通过的内容：原样保留
- ⚠️ 需修改的内容：按建议修改
- ❌ 缺失的内容：完整补充
- **背景技术保护规则**：3.1/3.2 只允许增补和术语修正，严禁精简或删减
- 修订后内容长度不得短于原文 80%

**修订版输出格式要求（强制）**：

> **⚠️ 每个 `revised_*.md` 文件必须包含该章节的完整内容（全文替换），而非仅修改的片段。**
>
> 修订流程：
> 1. 复制原始章节的完整内容到修订文件
> 2. 在完整内容中**原地修改**需要修订的部分
> 3. 在文件末尾附加修订日志
>
> **禁止**：仅输出修订增量片段（如"S3 步骤中，增加了……"），这会导致 DOCX 组装时原始内容丢失。
>
> **长度验证**：修订版文件字符数必须 ≥ 原始版字符数的 80%。如果修订版过短（< 原始版的 80%），preflight 检查将标记为 FAIL。

输出分隔标记格式（放在完整内容之前）：`===REVISED_KEY_TERMS===`、`===REVISED_CONCEPT===`、`===REVISED_BACKGROUND===`、`===REVISED_INVENTION_CONTENT===`

修订日志（放在完整内容之后）：`===REVISION_CHANGELOG===` + 逐条变更说明

**示例格式**：

```markdown
===REVISED_INVENTION_CONTENT===

# 发明内容

### 4.1 产品侧
（完整的 4.1 内容，含修订部分……）

### 4.2 技术侧
（完整的 4.2 内容，含修订部分……）

### 4.3 有益效果
（完整的 4.3 内容，含修订部分……）

===REVISION_CHANGELOG===
1. S3 补充归属模式对分析范围的限定逻辑
2. S4 输入数据样例增加具体文件签名数量
```

### Stage 14：质量门禁（→ `patent_run/stage-11/quality_report.json`）

输出**严格 JSON 格式**的质量评估，**必须遵循以下完整 schema**（满分 10 分）：

```json
{
  "score_1_to_10": 7.5,
  "verdict": "proceed",
  "dimension_scores": {
    "structure_completeness": 1.5,
    "multi_scenario": 1.5,
    "figure_coverage": 1.0,
    "technical_depth": 2.0,
    "innovation_focus": 1.0,
    "implementability": 1.0,
    "innovation_evidence": 1.0,
    "innovation_level_appropriateness": 1.0
  },
  "strengths": ["优点1", "优点2"],
  "weaknesses": ["缺陷1"],
  "critical_issues": ["阻断问题1"],
  "missing_sections": [],
  "has_paper_artifacts": false,
  "scenario_count": 2,
  "figure_ref_count": 10,
  "figure_desc_count": 10,
  "claims_present": true,
  "implementation_examples": 2,
  "extension_schemes": 3,
  "fabrication_flags": {
    "claim_unsupported": false,
    "effect_ungrounded": false,
    "figure_mismatch": false,
    "prior_art_fabricated": false,
    "overclaim": false,
    "details": ["检查说明1"]
  },
  "generated": "2026-04-08T00:00:00+00:00"
}
```

**字段定义**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `score_1_to_10` | float | 是 | 加权总分（0-10） |
| `verdict` | string | 是 | `"proceed"`（≥7 分）或 `"revise"`（<7 分） |
| `dimension_scores` | object | 是 | 8 维评分（见下表） |
| `strengths` | string[] | 是 | 优点列表 |
| `weaknesses` | string[] | 是 | 缺陷列表 |
| `critical_issues` | string[] | 是 | 阻断级问题列表 |
| `missing_sections` | string[] | 是 | 缺失的必备章节列表 |
| `has_paper_artifacts` | boolean | 是 | 是否残留论文体章节 |
| `scenario_count` | int | 是 | 产品侧场景数量 |
| `figure_ref_count` | int | 是 | 正文中"如图N"引用的总数 |
| `figure_desc_count` | int | 是 | 附图说明中的图号总数 |
| `claims_present` | boolean | 是 | 是否包含权利要求书 |
| `implementation_examples` | int | 是 | 实施例数量 |
| `extension_schemes` | int | 是 | 扩展方案数量 |
| `fabrication_flags` | object | 是 | 造假检测标志（5 项 bool + details） |
| `generated` | string | 是 | ISO-8601 生成时间戳 |

**dimension_scores 评分维度**：

| 评估维度 | 字段名 | 满分 |
|---------|--------|------|
| 结构完整性 | `structure_completeness` | 1.5 分 |
| 多场景覆盖 | `multi_scenario` | 1.5 分 |
| 附图引用 | `figure_coverage` | 1 分 |
| 技术深度 | `technical_depth` | 2 分 |
| 创新点聚焦 | `innovation_focus` | 1 分 |
| 可实施性 | `implementability` | 1 分 |
| **创新点举证充分性** | `innovation_evidence` | **1 分** |
| **创新点层次适当性** | `innovation_level_appropriateness` | **1 分** |

> **满分合计 = 10 分**，与 `score_1_to_10` 满分一致。`score_1_to_10 = 各维度得分之和`。

> **创新点举证充分性**评分标准：每个核心创新点在 4.2.2 中有完整 6 子段举证步骤 = 满分；缺少输入/输出数据样例 = 扣 0.5 分；创新点无专属步骤 = 0 分。

> **创新点层次适当性**评分标准：至少 1 个创新点为系统级/产品级创新（描述多模块协同的新能力）= 满分；全部创新点为模块级但有合理说明 = 0.5 分；全部创新点为工程实现细节且无系统级视角 = 0 分。

**9 条阻断规则**（任一触发 verdict 必须为 `revise`）：
1. 4.2.2 核心算法步骤为空或仅有占位文本
2. 步骤总数少于创新点数量
3. 缺少必备章节（4.1/4.2/4.3）
4. 存在论文体章节
5. 有益效果含无推导过程的精确百分比数字
6. 关键术语超过 6 个
7. **6 子段不完整**：4.2.2 任何 S 步骤缺少 6 子段中的任何一个（问题动机、技术动作、输入数据样例、输出数据样例、关键参数、白话解释）
8. **JSON 输出清洁度**：`patent_content.json` 中存在 `===REVISED_` 或 `===REVISION_CHANGELOG===` 残留标记，或 header 字段含"（待填写）"
9. **创新点层次偏差（新增）**：如果 ideal_output.md 中的**所有**创新点都属于"模块级工程实现"（即全部使用模块级字段集——有 `code_evidence` 和 `algorithm_pseudocode` 但无 `system_evidence` 或 `capability_description`），且项目 README/文档表明项目具备端到端系统级能力，则触发阻断，要求返回 Stage 02 重新分析创新点层次

**7 条图文阻断规则**（任一触发 verdict 必须为 `revise`）：
7. 参考文献为空或少于 3 篇真实引用（含专利号/DOI/链接）
8. 技术图表 PNG 文件数量少于 4 张（`$WORK_DIR/charts/` 目录）
9. UI 截图 PNG 文件数量少于 `invention_content.md` 中产品侧 `<!-- FIGURE:xxx -->` 占位符数量（最低 10 张）（`patent_run/stage-08/screenshots/` 目录）
10. **缺少场景切换/状态转换截图**：`figure_registry.json` 中不存在 `figure_type` 为 `state_transition` 的条目
11. **截图文件过小**：`screenshots/` 目录下存在任何 PNG 文件大小低于 **50KB**（说明内容空白或渲染失败，需重新截图）
12. **技术图表文件过小**：`charts/` 目录下存在任何 PNG 文件大小低于 **30KB**（说明图表内容不完整或渲染失败）
13. **技术侧无图引用（新增）**：`invention_content.md` 的 4.2 技术侧部分缺少 `tech_architecture`/`tech_flowchart`/`tech_sequence`/`tech_dataflow` 四种技术图表占位符中的任何一个，说明技术侧图文脱节，必须返回 Stage 09 补充
13. **图引用与图描述不一致**：`figure_ref_count`（正文"如图N"引用总数）与 `figure_desc_count`（附图说明图号总数）差值超过 2，说明技术图表在正文 4.2 中缺少"如图N所示"引用

verdict 取值：`proceed`（score ≥ 7）或 `revise`（score < 7）。如果 `revise`，返回 Stage 13 重新修订（最多 2 轮）。

**降级输出规则（2 轮仍未通过时）**：

> 如果经过 2 轮 Stage 13→14 循环后 score 仍 < 7，**不阻断流程**，按以下降级模式继续：

1. **verdict 改为 `proceed_degraded`**，在 `quality_report.json` 中追加以下字段：
   ```json
   {
     "verdict": "proceed_degraded",
     "degraded": true,
     "degraded_reason": "2 轮修订后质量评分仍为 X.X（< 7），降级输出",
     "revision_rounds": 2
   }
   ```
2. **Stage 15 正常执行**，但在最终 `patent_content.json` 的文档头部追加降级警告段落：
   ```
   ⚠️ 本文档经降级输出，质量门禁评分为 X.X（未达 7 分标准），建议人工复核后再提交。
   ```
3. **`deliverables/manifest.json`** 中追加 `"degraded": true` 标记，便于后续自动化流程识别

> **设计依据**：对齐原代码 `graceful_degradation=True` 的行为——原代码在质量门禁不通过时写入 `degradation_signal.json` 并以 `DONE(degraded)` 状态继续，不中断管线。Skill 版本采用相同策略，确保即使质量未达标也能产出可人工修正的交底书初稿，而非直接失败。

### Stage 15：DOCX 组装与打包（辅助脚本 + 图片嵌入）

> **⚠️ 强制要求**：最终 DOCX 必须包含所有技术图表和 UI 截图，参考文献章节必须包含 Stage 05 的文献列表。**严禁**输出无图或参考文献为空的 DOCX。

> **🔒 硬守卫已就位**：`build-docx` 命令在执行前会自动运行全链路前置检查（Stage 01-14 全部产出验证）。以下情况将**拒绝执行并 exit(1)**：
> - 截图不足 10 张 或 图表不足 4 张
> - figure_registry.json 缺失或缺少必需类型（product_output_preview / innovation_linkage）
> - ideal_output.md 或 invention_content.md 缺失
> - code_context.md 缺失
>
> **降级模式**：`--force` 参数可跳过前置检查，**仅供人工调试使用，智能体禁止使用**（参见执行纪律规则 5）。DOCX < 200KB 时仍返回 exit(2) 警告。
>
> ```bash
> # 默认严格模式（智能体必须使用此模式）
> python $SKILL_DIR/scripts/orchestrate.py build-docx $WORK_DIR --name "发明名称"
>
> # 降级模式（仅限人工调试，智能体禁止使用）
> python $SKILL_DIR/scripts/orchestrate.py build-docx $WORK_DIR --name "发明名称" --force
> ```

**步骤 0：参考文献回填**

`patent_to_json.py` 会自动从 `patent_run/stage-03/references.md`（优先）或 `patent_run/stage-12/references.md` 读取参考文献。确保 Stage 05 产出的文献列表已写入 `patent_run/stage-03/references.md`。如果两个位置都没有 references.md，最终参考文献将为空（不合格）。

**步骤 1：组装 DOCX**

```bash
python $SKILL_DIR/scripts/orchestrate.py build-docx $WORK_DIR --name "发明名称"
```

> **⚠️ `--name` 必须与 Stage 01 的 `--name` 完全一致**，即用户提供的完整原始主题字符串。

或手动分步执行：

```bash
# 1. 转换 MD → JSON
python $SKILL_DIR/scripts/patent_to_json.py \
    --run-dir $WORK_DIR/patent_run --work-dir $WORK_DIR --name "发明名称"

# 2. 解压模板
python $SKILL_DIR/scripts/office/unpack.py \
    $SKILL_DIR/assets/发明专利技术交底书模板.docx $WORK_DIR/unpacked/

# 3. 构建
python $SKILL_DIR/scripts/patent_builder.py \
    $WORK_DIR/patent_content.json $WORK_DIR/unpacked/

# 4. 打包（直接输出到 deliverables/）
mkdir -p $WORK_DIR/deliverables
python $SKILL_DIR/scripts/office/pack.py \
    $WORK_DIR/unpacked/ $WORK_DIR/deliverables/{发明名称}.docx \
    --original $SKILL_DIR/assets/发明专利技术交底书模板.docx
```

**步骤 2：图片嵌入（强制）**

在 DOCX 构建完成后，必须将技术图表和 UI 截图嵌入 Word 文档：

```bash
# 嵌入技术图表（charts/ 目录下所有 PNG）
for png in $WORK_DIR/charts/*.png; do
    python $SKILL_DIR/scripts/insert_image.py \
        $WORK_DIR/unpacked/ "$png" --width 14
done

# 嵌入 UI 截图（screenshots/ 目录下所有 PNG）
for png in $WORK_DIR/patent_run/stage-08/screenshots/*.png; do
    python $SKILL_DIR/scripts/insert_image.py \
        $WORK_DIR/unpacked/ "$png" --width 14
done

# 重新打包（输出到 deliverables/）
python $SKILL_DIR/scripts/office/pack.py \
    $WORK_DIR/unpacked/ $WORK_DIR/deliverables/{发明名称}.docx \
    --original $SKILL_DIR/assets/发明专利技术交底书模板.docx
```

**步骤 3：验证最终 DOCX**

检查最终 DOCX 文件：
- 文件大小应 > 200KB（含图片的 DOCX 通常远大于纯文本版本）
- 参考文献章节非空，包含至少 3 篇真实引用
- 技术图表和 UI 截图均已嵌入

**步骤 4：交付物汇聚（deliverables/）**

> 使用 `orchestrate.py build-docx` 时会自动执行此步骤。手动执行时无需额外操作。

DOCX 打包并验证成功后，`orchestrate.py` 自动将最终交付物汇聚到 `$WORK_DIR/deliverables/` 目录。用户只需关注此目录即可获取全部成果。

**deliverables/ 目录结构**：

```
deliverables/
├── manifest.json                 # 交付物清单（自动生成）
├── {发明名称}.docx               # 专利交底书 Word（含图表），使用实际发明名称命名
├── references.md                 # 参考文献列表
├── figure_registry.json          # 附图注册表（图号↔截图↔章节映射）
├── charts/                       # 技术图表 PNG（仅 *.png，不含 .html/.js 中间产物）
├── code/                         # 产品原型 HTML（index.html 等）
├── sections/                     # 各章节最终版 Markdown（带占位检测，不含占位文件）
│   ├── key_terms.md
│   ├── concept.md
│   ├── background.md
│   └── invention_content.md
├── ideal/                        # Ideal 文档及代码上下文
│   ├── ideal_output.md           # Ideal 分析文档（含产品表现特征+附图设计建议）
│   ├── code_context.md           # 代码上下文提取
│   └── context_metadata.json     # 上下文元数据
└── screenshots/                  # UI 截图（≥10 张高清 PNG，含产出物展示和创新点联动）
```

**manifest.json schema**：

```json
{
  "pipeline": "code-patent-writing",
  "topic": "发明名称",
  "files": ["{发明名称}.docx", "references.md", "charts/", "code/", "sections/", "screenshots/", "ideal/"],
  "generated": "ISO-8601 时间戳",
  "notes": {
    "{发明名称}.docx": "专利交底书 (Word 格式，含图表)",
    "references.md": "参考文献列表",
    "charts/": "技术图表 (流程图、架构图等)",
    "code/": "产品原型 Demo 代码",
    "sections/": "各章节最终版 Markdown",
    "screenshots/": "产品交互步骤截图",
    "ideal/": "Ideal 文档、代码上下文及元数据"
  }
}
```

> **注意**：`$WORK_DIR` 根目录下的 `patent_content.json`、`*.mmd`、`charts/` 等中间产物保留不动，不影响构建流程。`deliverables/` 是唯一的最终交付目录，DOCX 直接生成在此（无事后拷贝），`unpacked/` 构建中间目录在打包完成后自动清理。

## 撰写强制约束（防膨胀 + AI 味控制）

**以下约束在 Stage 03-10 所有章节撰写中必须严格遵守**：

### AI 味高频词黑名单（19 词，出现任何一个即不合格）

> 随着、近年来、不断发展、日益重要、显著、大幅、有效、高效、智能化、鲁棒性、可扩展性、此外、从而、进而、综上所述、综上、存在诸多不足、本发明具有以下有益效果、已成为……的重要课题

### 防膨胀硬约束

| 约束项 | 硬上限 |
|--------|--------|
| 关键术语 | 5-8 个（修订后≤6） |
| 4.1 产品侧步骤 | **严格 2-3 步**（绝对禁止超过 3 步） |
| 4.2 技术侧代码引用 | **0 处** |
| 4.2.1 架构描述每层 | **≤80 字** |
| 4.2.1 架构描述总字数 | **≤400 字** |
| 4.2.2 技术动作子段 | **≤150 字** |
| 4.2.3 模块间交互时序 | **≤200 字** |
| 4.2.4 数据流描述 | **≤200 字** |
| 4.2 技术侧图表占位符 | **4 个**（tech_architecture/tech_flowchart/tech_sequence/tech_dataflow） |
| 4.3 有益效果 | **2-3 段，≤400 字** |
| 发明构思创新点 | **2-3 个** |

### 反啰嗦规则（强制）

> **核心原则**：专利交底书追求精准表达，不是字数越多越好。每句话必须承载新信息，否则删除。

**禁止的啰嗦模式**：
1. **同义反复**：禁止在同一段落中用不同措辞重复表达相同意思（如"系统会自动检测……，也就是说系统自动发现……"）
2. **铺垫式开头**：禁止以"在当前……中"、"为了……"、"考虑到……"等铺垫句开头，直接说"系统做了什么"
3. **过度解释**：技术步骤描述后不要再用另一段话解释"这意味着什么"——读者能从前文理解
4. **修饰词堆砌**：禁止连续使用 2 个以上修饰词（如"高效精确自动化的智能处理"→"自动处理"）

**段落字数硬约束**：
| 章节 | 单段落上限 |
|------|-----------|
| 4.1 产品侧每步描述 | **≤150 字** |
| 4.2.1 架构每层描述 | **≤80 字** |
| 4.2.2 S 步骤的技术动作子段 | **≤150 字**（3-4 句，每句一个动作） |
| 4.2.2 S 步骤的白话解释子段 | **≤40 字** |
| 4.2.3 模块间交互时序（全节） | **≤200 字** |
| 4.2.4 数据流描述（全节） | **≤200 字** |
| 4.3 有益效果每段 | **≤150 字** |
| 背景技术每种现有技术描述 | **≤200 字** |

**精简度自检**：撰写每个段落后，检查是否能删掉 20% 的字而不损失信息量。如果能，说明原文太啰嗦。

### 通俗化三层保障

1. **30 秒规则**：每个创新点的场景引入必须让不懂编程的人在 30 秒内理解
2. **Before/After 故事**：每个创新点必须有具体角色（如"工程师小李"）的对比故事
3. **日常类比贯穿**：通俗概述（200 字）用一个类比（如"体检报告"）贯穿全段

### 代码标识符隔离

- 正文段落：**完全禁止**裸露的函数名、类名、Git 语法、`[代码参考: xxx]` 标记
- 代码引用：**仅允许**在 `(b) 代码证据附录` 子节中出现

## 质量保障体系

### 第一层：写作规范（预防）

撰写每个章节时严格遵守 [$SKILL_DIR/references/writing-style-guide.md](references/writing-style-guide.md)：
- 开门见山，禁止宏观背景铺垫
- 动词驱动叙述，少用抽象名词（"机制/策略/框架"→具体动作）
- 推导式逻辑（问题→根因→方案），非清单式罗列
- 短句拆分（>40 字必须拆分）
- 具体数字替代模糊表述

### 第二层：自我评审 + 质量门禁（检测）

撰写完成后按 [$SKILL_DIR/references/quality-rubric.md](references/quality-rubric.md) 执行：
1. **16 维度自我评审**：逐条检查，标记 ✅/🔴/🟡
2. **13 维加权评分**：总分 7 分以上为合格
3. **16 条阻断规则**（含图文阻断 + 术语降维 + 创新点可授权性）：任一触发必须修订
4. **5 组 CHECKLIST**：创新点覆盖/量化数据/步骤必填/权利要求/图文交付完整性
5. **反造假检查**：图引用一致性/权利要求支撑/术语使用率/降级信号/参考文献真实性

**质量门禁增强重试**（最多 2 轮）：定位缺陷 → 注入 Ideal 创新点素材 → 精确定向修订 → 重新评估

### 第三层：输出清洗（修复）

按 [$SKILL_DIR/references/llm-output-cleaning-guide.md](references/llm-output-cleaning-guide.md) 清洗：
1. 对话前缀清除（89+ 种中文输出噪声模式）
2. 技能/工具名泄漏清除
3. 代码块移除
4. Markdown 表格转自然语言
5. 运行时错误标记清除
6. 对话性垃圾清除
7. 工程/JSON 产物清除（CJK 比例 < 30% 时删除）

## patent_content.json 段落类型

| type | 必填字段 | 说明 |
|------|---------|------|
| `text` | `content` | 楷体 10pt 正文段落 |
| `heading` | `content` | 微软雅黑加粗 10pt 标题段落 |
| `formula` | `omml`, `num` | 居中独立公式 + 右侧编号 |
| `inline` | `parts` | 文本与行内 OMML 公式混排 |
| `image` | `path` | 居中图片，可选 `width` 和 `caption` |
| `empty` | — | 空行段落 |

## 各 Stage 输出目录映射

智能体撰写的各章节 .md 文件需要放到 `patent_run/` 下的指定目录，供 `patent_to_json.py` 读取。

> **注意**：逻辑 Stage 编号与物理目录编号不同。物理目录名（`stage-01` 到 `stage-12`）保持固定，以兼容辅助脚本。

| 逻辑 Stage | 物理输出目录 | 关键文件 | 说明 |
|------------|-------------|---------|------|
| 01 | `ideal/` | `code_context.md` | 代码上下文（脚本输出） |
| 02 | `ideal/` | `ideal_output.md` | 创新点分析文档（智能体输出） |
| 03 | `patent_run/stage-01/` | `goal_text.md` | 发明范围说明书 |
| 04 | `patent_run/stage-02/` | `prior_art.md` | 现有技术分析报告 |
| 05 | `patent_run/stage-03/` | `references.md`, `web_search_results.json` | **强制**联网文献收集 |
| 06 | `patent_run/stage-04/` | `key_terms.md` | 关键术语定义 |
| 07 | `patent_run/stage-05/` | `concept.md` | 发明构思 |
| 08 | `patent_run/stage-06/` | `background.md` | 背景技术 |
| 09 | `patent_run/stage-07/` | `invention_content.md` | 发明内容 |
| 10 | `patent_run/stage-08/` | `screenshots/*.png`, `figure_registry.json`, `code/index.html` | **强制** Playwright UI 截图 |
| 11 | `$WORK_DIR/charts/` | `*.png`（≥4 张）, `tech_charts.html` | **强制** 4 类技术图表 PNG（优先 HTML + Playwright 截图） |
| 12 | `patent_run/stage-09/` | `reviews.md` | 专利评审报告 |
| 13 | `patent_run/stage-10/` | `revised_*.md` | 修订后的各章节 |
| 14 | `patent_run/stage-11/` | `quality_report.json` | 质量评分 |
| 15 | `$WORK_DIR/deliverables/` | `{发明名称}.docx`, `manifest.json` | 最终专利文档（含嵌入图片）+ 交付物清单 |

## 参考文档索引

| 文档 | 用途 | 关键内容 |
|------|------|---------|
| [writing-style-guide.md](references/writing-style-guide.md) | 写作规范 | 19词黑名单、防膨胀约束、通俗化保障、代码隔离、反造假检查 |
| [quality-rubric.md](references/quality-rubric.md) | 质量评估 | 13维评分(含权重)、16维评审、16条阻断规则、5组CHECKLIST、增强重试流程 |
| [llm-output-cleaning-guide.md](references/llm-output-cleaning-guide.md) | 输出清洗 | 7层管道、89种前缀模式、CJK比例判断、Ideal消毒 |
| [ideal-injection-guide.md](references/ideal-injection-guide.md) | Ideal注入 | 11种阶段差异化策略、深度结构化提取、消毒规则 |
| [code-analysis-guide.md](references/code-analysis-guide.md) | 代码分析 | 4轮分析架构、输入源识别与归属判定 |
| [pipeline-integration-guide.md](references/pipeline-integration-guide.md) | Stage 参考 | 15 Stage 流程、输出目录映射 |
| [json-content-guide.md](references/json-content-guide.md) | JSON格式 | patent_content.json schema |
| [patent-template-format.md](references/patent-template-format.md) | 模板格式 | 交底书 DOCX 模板结构 |
| [docx-editing-guide.md](references/docx-editing-guide.md) | DOCX编辑 | OOXML 操作参考 |
| [omml-formula-guide.md](references/omml-formula-guide.md) | 公式 | OMML 数学公式语法 |
| [html-template-guide.md](references/html-template-guide.md) | **HTML模板** | **Stage 10/11 强制 CSS 骨架、HTML 结构模板、Playwright 截图脚本模板、禁止行为清单** |

## 依赖

### 必需依赖（Stage 00 自动安装）

- **Node.js** 16+：Playwright 和 Mermaid CLI 的运行环境
- **Playwright**（强制本地安装，固定在 `$REPO_PATH/_patent_playwright/`）：
  - 安装命令：`cd $REPO_PATH/_patent_playwright && npm install playwright && npx playwright install chromium`
  - 用于 Stage 05 联网检索（Google Patents / arXiv / Semantic Scholar）
  - 用于 Stage 10 产品侧 UI 原型截图
  - 用于 Stage 11 技术图表截图
  - **必须使用 headless 模式**（`chromium.launch({ headless: true })`）
  - **必须通过 `node` 命令执行本地 JS 脚本**，**禁止使用 MCP playwright 工具**
- **Mermaid CLI**（推荐，降级方案备用）：`npm install -g @mermaid-js/mermaid-cli`（Stage 11 降级方案 B 使用 Mermaid 渲染技术图表为 PNG）
- **Python 3.11+**
- **defusedxml**：`pip install defusedxml`
- **lxml**：`pip install lxml`

### 降级方案（仅当主方案不可用时）

- **web_search 工具**：Stage 05 Playwright 检索失败时的降级方案
- **image_gen 工具 / 多模态内容生成 skill**：Stage 11 HTML + Playwright 和 Mermaid CLI 均不可用时生成技术图表
