# Active Memory 技能

AI 主动记忆的完整操作规范，提供记忆读写的详细流程、格式模板、记录示例和质量自检清单。

---

## 快速开始

### 何时使用此技能

- **Rule 层检测到记忆操作需求时**：由 `active-memory-recording.mdc` 规则自动调度
- **显式命令触发时**：`/memory:remember`、`/memory:remember-long`、`/memory:remember-daily`、`/memory:tidy`
- **自主判断写入时**：AI 根据对话内容主动识别需要记忆的信息

### 基本使用流程

```
use_skill("active-memory")
```

技能加载后，根据操作类型读取对应的规范文件：

| 操作类型 | 需要读取的规范文件 |
|---------|------------------|
| 读取记忆 | `flows/read-flow.md` |
| 写入记忆 | `flows/classify-flow.md` → `flows/write-flow.md` |
| 整理记忆 | `flows/write-flow.md` + `flows/classify-flow.md` |
| 首次/不确定格式 | 额外读取 `templates/examples.md` |

---

## 技能架构

### 文件结构

```
active-memory/
├── SKILL.md              ← 入口路由（技能主文件）
├── README.md             ← 使用说明（本文件）
├── flows/
│   ├── read-flow.md      ← 读取流程详细规范
│   ├── classify-flow.md  ← 分类决策流程（长期/近期划分标准）
│   └── write-flow.md     ← 写入流程 + 格式模板 + 错误处理
└── templates/
    └── examples.md       ← 记录示例 + 质量自检清单
```

### 核心流程

```
┌─────────────────────────────────────────────────────────┐
│  触发场景                                                │
│  • 显式命令 (/memory:remember*)                         │
│  • 自主判断写入                                          │
│  • 读取历史记忆                                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  use_skill("active-memory")                             │
│  加载技能，获取 SKILL_BASE 路径                          │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │ 读取路径 │  │ 写入路径 │  │ 整理路径 │
   └────┬────┘  └────┬────┘  └────┬────┘
        │            │            │
        ▼            ▼            ▼
   read-flow.md  classify-flow.md  write-flow.md
                 write-flow.md    classify-flow.md
                 examples.md      examples.md
```

---

## 详细使用指南

### 1. 读取记忆

**触发条件**：新会话开始、询问历史上下文、继续未完成任务、引用已有决策

**执行步骤**：

```
use_skill("active-memory")
read_file("${SKILL_BASE}/flows/read-flow.md")
按 read-flow.md 指引执行读取操作
```

**读取优先级**：
1. `.codebuddy/MEMORY.md`（长期记忆）
2. `.codebuddy/memory/<今天>.md`（当日日志）
3. `.codebuddy/memory/<昨天>.md`（昨日日志）
4. 最近 7 天的日志文件（按需）

---

### 2. 写入记忆

**触发条件**：方案确认、重要结论达成、架构认知突破、解决技术问题、关键决策记录

**执行步骤**：

```
use_skill("active-memory")

# Step 1: 分类判断
read_file("${SKILL_BASE}/flows/classify-flow.md")
判断："下次全新会话是否仍需要这条信息？"
  → YES → 长期记忆（可能双写）
  → NO  → 仅当日日志

# Step 2: 执行写入
read_file("${SKILL_BASE}/flows/write-flow.md")
按 write-flow.md 定义的流程执行写入

# 可选：参考示例
read_file("${SKILL_BASE}/templates/examples.md")
```

**双写场景**：

| 场景 | 日志写什么 | 长期记忆写什么 |
|------|-----------|--------------|
| 用户确认核心方案 | 完整讨论过程 + 确认细节 | 方案结论 + 选择理由（精简版） |
| 发现关键架构认知 | 分析过程 + 代码引用 | 架构认知结论（去掉推理过程） |
| 用户否决方案 | 否决讨论完整记录 | ❌ 被否决方案 + 原因（一行即可） |
| 确认项目约定 | 讨论上下文 | 约定本身（规则化表述） |

---

### 3. 整理记忆（Tidy）

**触发条件**：手动执行 `/memory:tidy` 命令

**执行步骤**：

```
use_skill("active-memory")
read_file("${SKILL_BASE}/flows/write-flow.md")      # 晋升流程
read_file("${SKILL_BASE}/flows/classify-flow.md")   # 晋升判断标准
read_file("${SKILL_BASE}/templates/examples.md")    # 格式示例
```

**整理阶段**：

| 参数 | 操作 |
|------|------|
| `--promote` | 扫描近期日志，将符合长期记忆标准的内容晋升到 MEMORY.md |
| `--compact` | 去重、合并相似条目、压缩冗余描述 |
| `--cleanup` | 删除超过 30 天且已晋升的日志文件 |
| `--all` | 依次执行：晋升 → 精简 → 清理 |

---

## 格式规范

### 当日日志格式

```markdown
## [主题] - [描述]
- ✅/❌/⏳ 结论内容（一句话）
```

**约束**：
- 每条记录 ≤ 3 行
- 使用状态标记：✅ 确认 / ❌ 否决 / ⏳ 待办
- 禁止 `###` 子标题展开

### 长期记忆格式

```markdown
## [模块] - [决策] (YYYY-MM-DD)
核心结论，一到两句话。

## [模块] - ❌ [否决方案] (YYYY-MM-DD)
否决结论 + 原因，一句话。
```

**约束**：
- 每个条目 ≤ 100 字
- 总条目 ≤ 30 条
- 禁止 `###` 子标题展开
- 已有同主题 → 原地更新，不新增重复

### 容量控制

| 项目 | 限制 | 超限处理 |
|------|------|---------|
| 单条日志记录 | ≤ 3 行 | 压缩为结论 + 状态标记 |
| 单日日志文件 | ≤ 50 行 | 合并同主题条目 |
| MEMORY.md 单条目 | ≤ 100 字 | 精简为规则化表述 |
| MEMORY.md 总条目 | ≤ 30 条 | 使用 `/memory:tidy --compact` 整理 |

---

## 命令参考

### 显式写入命令

| 命令 | 功能 | 写入位置 |
|------|------|---------|
| `/memory:remember <内容>` | AI 自主分类写入 | 日志 / 长期记忆 / 双写 |
| `/memory:remember-long <内容>` | 强制写入长期记忆 | MEMORY.md + 同步日志 |
| `/memory:remember-daily <内容>` | 强制写入当日日志 | 仅当日日志 |

### 查询与整理命令

| 命令 | 功能 |
|------|------|
| `/memory:memory-list` | 查看当前记忆内容 |
| `/memory:tidy [--promote\|--compact\|--cleanup\|--all]` | 整理优化记忆文件 |

---

## 最佳实践

### 应该记录什么

✅ **关键结论**：经分析、讨论、验证后得出的重要结论  
✅ **解决方案**：已确认的技术方案、架构决策、实现策略  
✅ **决策点**：用户的关键选择、确认/否决的方案及理由  
✅ **核心认知**：对项目架构、业务逻辑、技术栈的深入理解  
✅ **待办事项**：待实施的任务、待确认的疑问

### 不应该记录什么

❌ 临时搜索结果  
❌ 工具错误信息  
❌ 重复内容  
❌ 敏感信息（除非明确要求）

### 执行原则

1. **主动性**：不等用户要求，主动识别和记录
2. **及时性**：关键信息产生时立即记录
3. **简洁性**：提炼核心信息，避免冗余
4. **不干扰**：记录过程不打断当前任务流程
5. **协同性**：与 `<working_memory_files>` 系统规则协同

---

## 与规则层的协同

此技能由 `active-memory-recording.mdc` 规则统一调度：

- **通道 1（显式写入）**：`/memory:remember*` 和 `/memory:tidy*` 命令
- **通道 2（自主写入）**：AI 根据对话内容自主判断写入

**强制约束**：
- 每次执行显式命令前，必须调用 `use_skill("active-memory")`
- 严禁使用 `update_memory` 工具
- 仅使用 `read_file` + `replace_in_file` + `write_to_file`

---

## 故障排查

### 常见问题

**Q: 技能加载后如何确定文件路径？**  
A: 使用 `${SKILL_BASE}/<相对路径>` 格式，SKILL_BASE 由技能自动确定。

**Q: 如何区分长期记忆和当日日志？**  
A: 核心判断："下次全新会话是否仍需要这条信息？" → YES 长期记忆，NO 当日日志。

**Q: 格式不确定时怎么办？**  
A: 额外读取 `templates/examples.md` 获取正确示例。

**Q: MEMORY.md 超过 30 条怎么办？**  
A: 执行 `/memory:tidy --compact` 进行精简整理。

---

## 更新日志

| 日期 | 更新内容 |
|------|---------|
| 2026-03-12 | 初始版本：双通道机制 + 精简格式规范 |

---

## 相关文件

- **规则层**：`.codebuddy/rules/active-memory-recording.mdc`
- **命令层**：`.codebuddy/commands/memory/*.md`
- **记忆存储**：`.codebuddy/MEMORY.md` + `.codebuddy/memory/*.md`
