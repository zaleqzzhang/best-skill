---
name: plan-eng-review-codebuddy
description: This skill should be used when the user requests an engineering manager-mode plan review — locking in architecture, data flow, edge cases, test coverage, and performance before implementation. Triggers on requests like "评审架构 / 工程评审 / 锁定计划 / review architecture / lock in the plan", and is the required Phase 4 reviewer in the openspec-integrated-superpowers workflow (review of `openspec/changes/[name]/` proposals before implementation). Walks through architecture / code-quality / tests / performance interactively, with one-issue-per-question format, opinionated recommendations, mandatory test-coverage diagram, and optional cross-model independent review via the proposal-challenger subagent.
---

# Plan Eng Review (CodeBuddy 版)

## Overview

工程经理模式的计划/提案评审 skill。在写代码之前,锁定架构、数据流、测试覆盖、性能。以"找漏洞而非走流程"为目标,以"一问一议"的方式与用户交互逐项落实。

本 skill 是从 gstack 的 `plan-eng-review` 移植并适配 CodeBuddy 的版本,**剥离全部 gstack/Claude Code 特有依赖**,完整保留核心评审方法论,并与 `openspec-integrated-superpowers` 工作流的 Phase 4 完美契合。

## When to Use

主动触发本 skill 的场景:

1. **OpenSpec Phase 4**(主要场景):用户使用 openspec-integrated-superpowers 工作流时,Phase 3 完成、Phase 4 启动,**必须**通过 `use_skill("plan-eng-review-codebuddy")` 进入本 skill,产出 `openspec/changes/<name>/review-report.md`。
2. **独立调用**:用户已有计划文档/设计文档,在编码前要求"评审架构"、"工程评审"、"锁定计划"、"review architecture"、"lock in the plan"、"tech review"、"plan engineering review" 等。
3. **proactive 建议**:用户描述了一个非平凡变更(>3 文件、新增组件、跨模块改动)且明显在编码前阶段时,应主动建议运行此 skill。

**不要**在以下场景触发本 skill:
- 简单 bug 修复或单文件改动
- 纯文档/配置改动
- 已经在编码中、要求"评审已写好的代码"(那是 code review,不是 plan review)

## Workflow Decision Tree

```
触发本 skill
    ↓
Step 0: 范围挑战(必做)
    ↓
检查复杂度阈值(8+ 文件 或 2+ 新服务)?
    ├─ 是 → 主动建议 scope reduction (ask_followup_question)
    │       ├─ 接受 → 范围按建议缩减,记入报告
    │       └─ 拒绝 → 范围按原提案锁定,后续严禁再提
    └─ 否 → 范围按原提案锁定
    ↓
顺序执行四节评审,每节内"一问一议":
  Section 1: 架构评审 → STOP/确认
  Section 2: 代码质量评审 → STOP/确认
  Section 3: 测试评审(包含 ASCII 覆盖率图,见 references/test-review-methodology.md) → STOP/确认
  Section 4: 性能评审 → STOP/确认
    ↓
Outside Voice 交叉评审(可选,默认询问)
  使用 proposal-challenger subagent 独立二次评审
    ↓
产出必需输出:
  - NOT in scope
  - What already exists
  - Failure modes
  - Worktree 并行化策略(如适用)
  - Completion Summary + STATUS
    ↓
OpenSpec 集成: 写入 openspec/changes/<name>/review-report.md
```

## Step 0: 范围挑战(Scope Challenge)

**评审任何东西之前**,先回答以下 6 个问题。这是评审的"地基",跳过会让后续节都失焦。

### 0.1 已有代码盘点

什么现有代码已部分或完全解决了各子问题?能否捕获现有流程的输出,而不是构建并行流程?

→ 输出会进入最终报告的「What already exists」章节(见 `references/output-format.md` 第 4.2 节)。

### 0.2 最小改动集

什么是达成既定目标的**最小改动集**?标记任何可推迟而不阻塞核心目标的工作。**对范围蔓延要严苛**。

### 0.3 复杂度检查(关键阈值)

如果计划满足以下任一条件,视为**复杂度异味**,必须挑战:
- 触及 **8+ 文件**
- 引入 **2+ 个新类/新服务**

→ 主动通过 `ask_followup_question` 推荐 scope reduction:
- 解释什么被过度构建
- 提出达成核心目标的最小版本
- 询问用户是缩减范围还是按原计划继续

**关键铁律**:一旦用户接受/拒绝了 scope reduction,**完全 commit**——后续评审节中绝不再重提缩减建议,绝不静默缩减范围,绝不跳过计划好的组件。

### 0.4 搜索检查

对计划引入的每个架构模式、基础设施组件、并发方案:

- 运行时/框架是否有内置方案? `web_search "{framework} {pattern} built-in"`
- 当前最佳实践是什么? `web_search "{pattern} best practice {current year}"`
- 是否有已知 footgun? `web_search "{framework} {pattern} pitfalls"`

如 `web_search` 不可用,跳过此项并记录:"web_search 不可用——基于内置知识继续"。

如计划在已有内置方案的情况下自造方案,标记为 scope reduction 机会。

### 0.5 TODOS 交叉引用

读取项目根目录的 `TODOS.md`(若存在)。检查:
- 是否有遗留项阻塞此计划?
- 能否把遗留项**捎带**进此 PR 而不扩大范围?
- 此计划是否产生新的应被记录为 TODO 的工作?

### 0.6 完整性检查(Completeness Principle)

**这是 Boil-the-Lake 原则的核心应用**。

详见 `references/output-format.md` 第 3 节「ask_followup_question 格式约束」中的「完整度评分」与「效率参考表」。简言之:

- AI 辅助让"完整方案"几乎免费(15 分钟 vs 人工 1 周)
- 默认推荐 Completeness ≥8 的选项
- 如果计划提议的 shortcut 节省的是"人时"但 AI 辅助下只省"分钟",必须推荐完整版

**Step 0 触发结果分支**:

- 复杂度检查命中 → 主动 `ask_followup_question` 提议 scope reduction,等待用户答复后继续
- 复杂度检查未命中 → 把 Step 0 的 6 项发现以表格形式展示,然后直接进 Section 1

## Section 1: 架构评审

详细维度参见 `references/engineering-mindset.md` 中的「15 条工程经理认知模式」(尤其 #3 默认无聊、#10 本质 vs 偶然复杂性、#11 两周嗅探)。

评估清单:
- 整体系统设计与组件边界
- 依赖图与耦合关注
- 数据流模式与潜在瓶颈
- 扩展性特征与单点故障
- 安全架构(认证、数据访问、API 边界)
- 哪些关键流程值得在计划/代码注释中嵌入 ASCII 图
- 对每条新代码路径或集成点,描述一个真实的生产失败场景,并检查计划是否考虑了它
- **分发架构**:若引入新构件(binary、package、container),如何构建、发布、更新?CI/CD 流水线是计划一部分还是被推迟?

**STOP 规则**:本节每个发现都单独发起一次 `ask_followup_question`,不打包。详见 `references/output-format.md` 第 3 节。

只有当本节所有问题都已被用户决策(选项 A/B/C 之一,或显式跳过)后,才进入下一节。

## Section 2: 代码质量评审

评估清单:
- 代码组织与模块结构
- DRY 违规——此处严苛
- 错误处理模式与缺失的边界情况(显式标出)
- 技术债热点
- 相对于工程偏好,过度工程化或欠工程化的区域
- 已触及文件中现有的 ASCII 图——本次改动后是否仍准确?

**STOP 规则**同上。

## Section 3: 测试评审

**完整方法论详见 `references/test-review-methodology.md`**。这是本 skill 最重的一节,目标 100% 覆盖。

核心步骤(精简版):
1. **Step 1**: 检测项目测试框架
2. **Step 2**: 追踪计划中每条代码路径(画出执行 ASCII 图)
3. **Step 3**: 映射用户流、交互边界情况、错误状态
4. **Step 4**: 对照现有测试逐分支检查(★/★★/★★★ 评分)
5. **Step 5**: 应用 E2E vs Unit 决策矩阵
6. **Step 6**: 产出 ASCII 覆盖率图(代码路径 + 用户流合并展示)
7. **Step 7**: 把缺失的测试加入计划

### 回归测试铁律

**当覆盖率审计识别出"回归"——之前能工作但本次 diff 弄坏的代码——必须把回归测试作为关键需求加入计划。不发起 `ask_followup_question`。不跳过。**

判断不确定时,默认写回归测试。详见 `references/test-review-methodology.md`「回归测试铁律」节。

### 测试评审产物的 OpenSpec 集成

按 `references/test-review-methodology.md`「OpenSpec 集成约定」节,测试评审产物**直接写入** `openspec/changes/<name>/review-report.md` 的「测试评审」章节,**不再单独产出 test-plan.md 文件**(符合 OpenSpec 单一产物原则)。

## Section 4: 性能评审

评估清单:
- N+1 查询与数据库访问模式
- 内存使用关注点
- 缓存机会
- 慢或高复杂度的代码路径

**STOP 规则**同上。

## Outside Voice — 独立交叉评审(可选,默认询问)

四节评审完成后,提供来自不同 AI 模型的独立第二意见。两个不同模型对计划达成共识,比一个模型的彻底评审是更强的信号。

### 核心定位

**Outside Voice 评审的对象是"提案材料",不是代码。**

"提案材料"(Proposal Materials)的定义:
- **OpenSpec 场景**:`openspec/changes/<name>/` 下的四件套合集(`proposal.md` + `design.md` + `specs/` + `tasks.md`)
- **独立调用场景**:用户传入的所有计划文档合集

proposal-challenger 的职责是对"提案材料"做独立二次评审,不是 code review。读代码仅用于**验证提案材料中的引用或假设**,不用于评审代码本身。

### 调用方式

通过 `task` 工具派发到 `proposal-challenger` subagent(基于 GPT 系 Codex 模型,与 CodeBuddy 主 Claude 形成跨模型视角):

```
task(
  subagent_name="proposal-challenger",
  description="独立交叉评审提案材料",
  prompt="""
  # 评审对象

  本次独立评审的"提案材料"(Proposal Materials)为以下合集(全部读完):
  - [列出具体路径,例如 openspec/changes/add-auth/proposal.md / design.md / specs/ / tasks.md]

  ## 主评审已完成的结论摘要
  [2-3 段摘要]

  # 你的职责

  你的工作是**找主评审遗漏的问题**,不要重复主评审。
  专注于 5 类盲区:逻辑漏洞、过度复杂、可行性风险、依赖排序、战略误判。

  # 六道防线(必须严格遵守,违反则评审作废)

  ## 防线 1:默认禁读代码,仅在触发器命中时才读

  - **触发器 A**:提案材料中**显式引用**代码(文件路径/类名/函数名/API 端点/表字段/行号) → MUST 读取验证
  - **触发器 B**:提案材料中**声明依赖**现有能力("复用现有 X"、"沿用项目 X"、"与已有 X 保持一致") → MUST 通过 codebase_search 验证存在性
  - **触发器 C**(其他所有情况):禁止读代码。架构合理性、业务逻辑、逻辑漏洞、战略误判等的评审,全部基于提案材料文本进行
  - **边界 1**(装饰性引用不读):仅当 finding 需要引用该代码作为论据时才读,纯装饰性引用不读
  - **边界 2**(兜底搜索限 3 次):如怀疑"可能已存在重复能力",允许主动 codebase_search 验证,但**每份评审最多 3 次**

  ## 防线 2:工具白名单

  允许 `read_file` / `codebase_search` / `search_content` / `list_dir` / `search_file`。禁止联网搜索（`web_search` 等）。

  `list_dir` 和 `search_file` 用于验证提案中引用的项目结构和文件路径，使用时**必须**在 Code Reading Plan 中声明使用意图，在 Code Reading Audit 中审计实际使用。

  ## 防线 3:开篇强制 Code Reading Plan

  在读任何代码前,必须先输出 `## CODE READING PLAN` 章节,逐项列出:
  - 触发器 A 命中项(附提案材料引用位置 + 计划读取的代码位置)
  - 触发器 B 命中项(附提案材料引用位置 + 计划搜索的 query)
  - 兜底搜索项(本次使用 N/3)
  - 末尾声明 "CONFIRMED: 读代码仅为验证以上 N 项。其他评审基于提案材料文本。"

  **没有 Code Reading Plan 就直接读代码 = 越权,对应 finding 全部作废。**

  ## 防线 4:每条 finding 必带溯源标签

  每条 finding 强制标注以下之一:
  - `[proposal-only]` — 仅基于提案材料文本判断。必须引用提案材料的具体段落
  - `[verified-by-code]` — 已 read_file 验证。必须列出文件路径 + 行号范围
  - `[verified-by-search]` — 已通过 codebase_search/search_content/list_dir/search_file 验证。必须列出 query/路径 + 命中结果

  **反作弊**:缺少必备字段的标签视为伪造,对应 finding 作废。

  ## 防线 5:完成后强制 Code Reading Audit

  输出末尾必须列 `## CODE READING AUDIT` 审计表:
  - 每项"计划读取"对照"实际是否读取"+ 验证结果 + 影响的 finding
  - 计划要读但没读 → 解释,对应 finding 降级为 [proposal-only]
  - 计划没读但实际读了 → 越权,超额 finding 作废
  - 兜底搜索使用次数(N/3)

  **无审计表 → 整份评审不合格。**

  ## 防线 6:反偷懒/反越权自检

  每条 finding 输出前,必须通过以下自检:
  - 不凭印象猜"可能有 X",必须验证后定论
  - 不跨界去评审"代码质量/命名/实现方式",那是 Phase 5 之后的事
  - 不读完一个文件后顺便扫相邻目录
  - 如果 finding 是"实现问题"而非"提案问题",直接丢弃

  # 输出格式

  严格按 proposal-challenger subagent 定义中的 `输出格式` 章节产出,不增不减。
  特别确保 `CODE READING PLAN` 和 `CODE READING AUDIT` 两个章节齐全。
  """
)
```

### 用户主权铁律

**Outside Voice 的发现是仅供参考(informational),即使跨模型共识也不得自动采纳到计划中。**

每条 Outside Voice finding,如果与主评审存在 tension(即两份评审结论冲突),必须:

1. 在报告中标记为 `CROSS-MODEL TENSION`
2. 单独发起一次 `ask_followup_question`,展示两份评审的分别立场
3. 给出推荐(说明哪边更有说服力及理由)
4. **等待用户明示批准后**才更新 review-report 或 tasks.md

即使你和 proposal-challenger 都同意某条修改,**也不得自动应用**。Cross-model agreement 是强信号,不是行动许可。

### Finding 可信度门禁

收到 proposal-challenger 的输出后,在采纳前做以下检查(任何一项失败 → 该 finding 视为作废,不进 review-report):

1. 输出是否包含 `CODE READING PLAN` 章节?
2. 输出是否包含 `CODE READING AUDIT` 章节?
3. 每条 finding 是否带溯源标签(`[proposal-only]` / `[verified-by-code]` / `[verified-by-search]`)?
4. `[verified-by-code]` 标签的 finding 是否列出了文件路径 + 行号?
5. `[verified-by-search]` 标签的 finding 是否列出了 query/路径 + 命中结果?
6. 兜底搜索次数是否 ≤3?

如 subagent 输出违反上述任何一项,**不要为了"显得完整"而采纳**——直接在主评审报告中记录:"Outside Voice 输出不符合防线要求,已跳过。" 并按用户主权铁律告知用户。

### 何时跳过

**Outside Voice 默认询问用户，AI 不得自行判断跳过。**

仅以下情况可跳过：
- 用户在 `ask_followup_question` 中明确选择跳过
- 用户在对话中显式输入"跳过评审"/"skip review"/"快速通过"/"skip outside voice" 等明确跳过指令

**AI 可建议但不可代决**：若 AI 判断提案规模较小（如单一 bug 修复、单文件改动、单一 API 端点），可在 `ask_followup_question` 的推荐中说明理由并建议跳过，但**必须等待用户明确选择后才能跳过**，禁止 AI 自主裁量直接跳过。

## 必需输出

评审完成后,**以下章节缺一不可**(详细格式见 `references/output-format.md`):

1. **NOT in scope** — 显式推迟的工作清单
2. **What already exists** — 现有代码盘点
3. **Failure modes** — 失败模式表 + critical gap 清单
4. **Worktree 并行化策略** — 仅在多条独立工作流时产出,否则一句话"顺序实施,无并行机会"
5. **Completion Summary** — 评审完成摘要表
6. **STATUS** — 四选一(DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT)

### Unresolved Decisions(未解决决策)

如用户跳过/打断/未答某 `ask_followup_question`,**绝不静默默认某选项**。在 Completion Summary 末尾单列「未解决的决策」章节。详见 `references/output-format.md` 第 7 节。

### Escalation(升级协议)

任务尝试 3 次失败 / 安全敏感不确定 / 范围超出可验证能力 → STOP 并升级,使用 STATUS: BLOCKED 或 NEEDS_CONTEXT 格式。**烂工作比没工作糟。**详见 `references/output-format.md` 第 8 节。

## OpenSpec 集成约定(Phase 4 专用)

当本 skill 在 openspec-integrated-superpowers 工作流的 Phase 4 被调用时,遵循以下额外约束:

### 输入

- `openspec/changes/<name>/proposal.md`
- `openspec/changes/<name>/design.md`
- `openspec/changes/<name>/specs/`
- `openspec/changes/<name>/tasks.md`

### 输出

**唯一产物**: `openspec/changes/<name>/review-report.md`

包含以下章节(顺序固定):
1. 评审元信息(被评审 change 名、评审时间、评审者)
2. Step 0 范围挑战结论
3. Section 1: 架构评审
4. Section 2: 代码质量评审
5. Section 3: 测试评审(含 ASCII 覆盖率图)
6. Section 4: 性能评审
7. Outside Voice 评审(如运行)
8. NOT in scope
9. What already exists
10. Failure modes
11. Worktree 并行化策略(如适用)
12. Completion Summary
13. STATUS

### 修改约束

**Phase 4 期间禁止修改 `openspec/changes/<name>/` 之外的任何文件。**

如果评审发现的测试缺口需要加入 tasks.md,**仅在 review-report.md 中列出建议**,由调用方(openspec-integrated-superpowers 工作流)在 Phase 5 启动前统一更新 tasks.md。

### 硬门禁交付

review-report 的 STATUS 字段是 openspec-integrated-superpowers Phase 4 → Phase 5 转换的硬门禁:

- `STATUS: DONE` → Phase 5 可启动
- `STATUS: DONE_WITH_CONCERNS` → 用户必须在 Phase 4.5 决策每个 concern,确认后方可进入 Phase 5
- `STATUS: BLOCKED` 或 `STATUS: NEEDS_CONTEXT` → Phase 5 严禁启动,必须先解决 blocking

详细 Phase 转换规则参见用户 rules 中的 `openspec-integrated-superpowers` 工作流定义。

## Resources

### references/

- **`engineering-mindset.md`** — 工程偏好 6 条 + 15 条工程经理认知模式 + ASCII 图表文档哲学。在评审推荐方案时作为论证依据。
- **`test-review-methodology.md`** — 测试评审 7 步法详解、E2E vs Unit 决策矩阵、回归测试铁律、ASCII 覆盖率图格式、OpenSpec 集成约定。Section 3 必读。
- **`output-format.md`** — 输出风格守则、置信度校准、ask_followup_question 格式约束(含 Completeness Principle 与效率参考表)、必需输出三件套格式、Unresolved Decisions 处理、Escalation 升级协议。

### 关联 subagent

- **`proposal-challenger`**(位于 `~/.codebuddy/agents/proposal-challenger.md`)— 基于 GPT 系 Codex 模型的独立交叉评审 subagent,Outside Voice 节使用。
