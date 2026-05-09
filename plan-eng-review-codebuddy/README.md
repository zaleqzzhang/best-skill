# plan-eng-review-codebuddy

工程经理模式的计划/提案评审 Skill。在写代码之前，锁定架构、数据流、测试覆盖、性能。以"找漏洞而非走流程"为目标，以"一问一议"的方式与用户交互逐项落实。

本 Skill 是从 gstack 的 `plan-eng-review` 移植并适配 CodeBuddy 的版本，**剥离全部 gstack/Claude Code 特有依赖**，完整保留核心评审方法论，并与 `openspec-integrated-superpowers` 工作流的 Phase 4 完美契合。

---

## 目录

- [适用场景](#适用场景)
- [核心工作流](#核心工作流)
- [评审四节 + Step 0](#评审四节--step-0)
- [Outside Voice 交叉评审](#outside-voice-交叉评审)
- [OpenSpec 集成](#openspec-集成)
- [文件结构](#文件结构)
- [关联 Subagent](#关联-subagent)

---

## 适用场景

### 主动触发

| 场景 | 说明 |
|------|------|
| **OpenSpec Phase 4** | 用户使用 `openspec-integrated-superpowers` 工作流时，Phase 3 完成后**必须**通过 `use_skill("plan-eng-review-codebuddy")` 进入本 Skill，产出 `openspec/changes/<name>/review-report.md` |
| **独立调用** | 用户已有计划文档/设计文档，在编码前要求"评审架构"、"工程评审"、"锁定计划"、"review architecture"、"lock in the plan"、"tech review" 等 |
| **Proactive 建议** | 用户描述了一个非平凡变更（>3 文件、新增组件、跨模块改动）且明显在编码前阶段时，应主动建议运行此 Skill |

### 不应触发

- 简单 bug 修复或单文件改动
- 纯文档/配置改动
- 已经在编码中、要求"评审已写好的代码"（那是 code review，不是 plan review）

---

## 核心工作流

```
触发本 Skill
    ↓
Step 0: 范围挑战（必做）
    ↓
检查复杂度阈值（8+ 文件 或 2+ 新服务）？
    ├─ 是 → 主动建议 scope reduction（ask_followup_question）
    │       ├─ 接受 → 范围按建议缩减，记入报告
    │       └─ 拒绝 → 范围按原提案锁定，后续严禁再提
    └─ 否 → 范围按原提案锁定
    ↓
顺序执行四节评审，每节内"一问一议"：
  Section 1: 架构评审 → STOP/确认
  Section 2: 代码质量评审 → STOP/确认
  Section 3: 测试评审（ASCII 覆盖率图） → STOP/确认
  Section 4: 性能评审 → STOP/确认
    ↓
Outside Voice 交叉评审（可选，默认询问）
  使用 proposal-challenger subagent 独立二次评审
    ↓
产出必需输出：
  - NOT in scope
  - What already exists
  - Failure modes
  - Worktree 并行化策略（如适用）
  - Completion Summary + STATUS
    ↓
OpenSpec 集成: 写入 openspec/changes/<name>/review-report.md
```

---

## 评审四节 + Step 0

### Step 0: 范围挑战（Scope Challenge）

评审任何东西之前，先回答 6 个问题：

1. **已有代码盘点** — 现有代码是否已部分解决子问题？
2. **最小改动集** — 达成目标的最小改动是什么？
3. **复杂度检查** — 8+ 文件或 2+ 新服务？主动建议 scope reduction
4. **搜索检查** — 框架是否有内置方案？当前最佳实践？已知 footgun？
5. **TODOS 交叉引用** — 是否有遗留项阻塞？是否产生新 TODO？
6. **完整性检查** — AI 辅助让完整方案几乎免费，默认推荐 Completeness ≥8

**关键铁律**：一旦用户接受/拒绝了 scope reduction，**完全 commit**——后续评审节中绝不再重提缩减建议。

### Section 1: 架构评审

- 整体系统设计与组件边界
- 依赖图与耦合关注
- 数据流模式与潜在瓶颈
- 扩展性特征与单点故障
- 安全架构（认证、数据访问、API 边界）
- ASCII 图嵌入建议
- 分发架构（CI/CD 是否包含）

### Section 2: 代码质量评审

- 代码组织与模块结构
- DRY 违规（严苛）
- 错误处理模式与缺失边界情况
- 技术债热点
- 过度/欠工程化区域
- ASCII 图陈旧性检查

### Section 3: 测试评审

**目标：100% 覆盖**。完整方法论见 `references/test-review-methodology.md`。

核心步骤：
1. 检测项目测试框架
2. 追踪计划中每条代码路径（ASCII 执行图）
3. 映射用户流、交互边界、错误状态
4. 对照现有测试逐分支检查（★/★★/★★★ 评分）
5. E2E vs Unit 决策矩阵
6. 产出 ASCII 覆盖率图
7. 把缺失测试加入计划

**回归测试铁律**：识别出回归（之前能工作但本次 diff 弄坏）→ 必须把回归测试作为关键需求加入计划，不发起 ask_followup_question，不跳过。

### Section 4: 性能评审

- N+1 查询与数据库访问模式
- 内存使用关注点
- 缓存机会
- 慢或高复杂度代码路径

### STOP 规则（四节通用）

每节每个发现都**单独发起一次 ask_followup_question**，绝不打包。只有当本节所有问题都已被用户决策后，才进入下一节。

---

## Outside Voice 交叉评审

四节评审完成后，可选提供来自不同 AI 模型的独立第二意见。

### 核心定位

**评审对象是"提案材料"，不是代码。**

- **OpenSpec 场景**：`openspec/changes/<name>/` 下的四件套合集（proposal.md + design.md + specs/ + tasks.md）
- **独立调用场景**：用户传入的所有计划文档合集

`proposal-challenger` 的职责是对"提案材料"做独立二次评审，读代码**仅用于验证提案材料中的引用或假设**。

### 六道防线

| 防线 | 机制 |
|------|------|
| **防线 1** | 默认禁读代码，仅在触发器 A（显式引用代码）/ B（声明依赖现有能力）命中时才读；触发器 C（其他所有情况）禁止读代码 |
| **防线 2** | 工具白名单物理收紧：`read_file` / `codebase_search` / `search_content` / `list_dir` / `search_file`，禁止联网搜索 |
| **防线 3** | 开篇强制 Code Reading Plan：读代码前必须先声明计划读取项 |
| **防线 4** | 每条 finding 必带溯源标签：`[proposal-only]` / `[verified-by-code]` / `[verified-by-search]` |
| **防线 5** | 完成后强制 Code Reading Audit：计划 vs 实际对照 |
| **防线 6** | 反偷懒/反越权自检：不凭印象猜、不跨界评审代码质量 |

### 用户主权铁律

Outside Voice 的发现是**仅供参考**（informational），即使跨模型共识也**不得自动采纳到计划中**。每条 finding 必须单独 ask_followup_question，等待用户明示批准后才更新 review-report。

---

## OpenSpec 集成

### 输入

- `openspec/changes/<name>/proposal.md`
- `openspec/changes/<name>/design.md`
- `openspec/changes/<name>/specs/`
- `openspec/changes/<name>/tasks.md`

### 输出

**唯一产物**：`openspec/changes/<name>/review-report.md`

包含章节（顺序固定）：
1. 评审元信息
2. Step 0 范围挑战结论
3. Section 1: 架构评审
4. Section 2: 代码质量评审
5. Section 3: 测试评审（含 ASCII 覆盖率图）
6. Section 4: 性能评审
7. Outside Voice 评审（如运行）
8. NOT in scope
9. What already exists
10. Failure modes
11. Worktree 并行化策略（如适用）
12. Completion Summary
13. STATUS

### 硬门禁交付

| STATUS | 含义 | Phase 5 能否启动 |
|--------|------|----------------|
| `DONE` | 全部完成 | ✅ 可启动 |
| `DONE_WITH_CONCERNS` | 完成但有问题 | ⚠️ 用户必须在 Phase 4.5 决策每个 concern |
| `BLOCKED` / `NEEDS_CONTEXT` | 无法继续/缺信息 | ❌ 严禁启动 |

### 修改约束

**Phase 4 期间禁止修改 `openspec/changes/<name>/` 之外的任何文件。** 测试缺口仅在 review-report.md 中列出建议，由调用方在 Phase 5 启动前统一更新 tasks.md。

---

## 文件结构

```
plan-eng-review-codebuddy/
├── SKILL.md                              # 主 Skill 定义（工作流入口）
├── README.md                             # 本文档
└── references/
    ├── engineering-mindset.md            # 工程偏好 + 15 条认知模式 + ASCII 哲学
    ├── test-review-methodology.md        # 测试评审 7 步法 + E2E 矩阵 + 回归铁律
    └── output-format.md                  # 风格守则 + 置信度 + Completeness + 必需输出格式
```

### References 说明

| 文件 | 内容 | 使用时机 |
|------|------|---------|
| `engineering-mindset.md` | 6 条工程偏好、15 条工程经理认知模式、ASCII 图表文档哲学 | 评审推荐方案时作为论证依据 |
| `test-review-methodology.md` | 测试框架检测、7 步法、E2E vs Unit 决策矩阵、回归铁律、ASCII 覆盖率图格式、OpenSpec 集成约定 | Section 3 测试评审时必读 |
| `output-format.md` | 输出风格守则、置信度校准、ask_followup_question 格式约束、Completeness Principle、必需输出三件套、Unresolved Decisions、Escalation 升级协议 | 全评审过程参考 |

---

## 关联 Subagent

- **`proposal-challenger`**（位于 `~/.codebuddy/agents/proposal-challenger.md`）— 基于 GPT-5.3-Codex 模型的独立交叉评审 Subagent，Outside Voice 节使用。

  该 Subagent 与主 Claude 形成**跨模型视角**，专注发现主评审遗漏的 5 类盲区：逻辑漏洞、过度复杂、可行性风险、依赖排序、战略误判。
