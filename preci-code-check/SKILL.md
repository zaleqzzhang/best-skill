---
name: preci-code-check
description: 当用户需要进行代码规范检查、PreCI 检查、提交前检查代码、检查代码质量、或明确提及 preci/preci-code-check 时触发。适用于检查改动代码、已暂存代码、全量代码扫描等场景。
category: code-quality
tags: [preci, code-check, lint, quality, pre-commit]
version: 3.1.2
---

# PreCI 代码规范检查技能

## 概述

本技能提供完整的 PreCI 代码规范检查能力，封装了 PreCI 工具的调用、安装、扫描和自动修正逻辑。

**核心特性**：
- ✅ 自动安装 PreCI 工具
- ✅ 智能服务管理（检测/启动 PreCI Server）
- ✅ 多扫描模式（combined/diff/pre-commit/all）
- ✅ 代码文件白名单过滤
- ✅ 自动修正常见规范问题
- ✅ 多项目批量检查
- ✅ 标准化输出格式

## 技能基础路径解析

本技能的文件引用均使用相对路径。AI 执行时必须先确定技能的实际安装路径（`SKILL_BASE`）：

**路径发现顺序**（按优先级）：
1. 当前已加载的 SKILL.md 所在目录（首选，直接可用）
2. `~/.codebuddy/skills/preci-code-check/`
3. `~/.claude-internal/skills/preci-code-check/`
4. 兜底搜索：`find ~ -path "*/preci-code-check/SKILL.md" -type f 2>/dev/null | head -1`

确定 `SKILL_BASE` 后，所有 `read_file` 调用使用 `${SKILL_BASE}/<相对路径>` 格式。

## 使用方式

### 方式一：技能调用（推荐）

```
use_skill("preci-code-check")
```

然后通过参数对象指定检查配置：

```yaml
scan_mode: combined      # combined | diff | pre-commit | all
target_path: .           # 检查路径
max_retry: 3             # 最大重试次数
multi_project: false     # 是否多项目检查
init_if_needed: true     # 未初始化时是否自动初始化
```

### 方式二：自定义命令

```bash
preci:check              # 默认 combined 模式
preci:check -d           # diff 模式（未暂存）
preci:check -s           # staged 模式（已暂存）
preci:check -a           # all 模式（全量）
preci:check -m           # 多项目检查
```

## 🚨 分步执行强制约束

**核心原则：按需读取，逐步执行，禁止预读！**

### 执行规则【必须遵守】

1. **禁止一次性读取所有工作流文档**
   - ❌ 禁止在开始执行前读取全部 7 个工作流文档
   - ❌ 禁止"为了提高效率"批量读取多个步骤的文档
   - ✅ 只读取即将执行的下一步工作流文档

2. **严格的分步执行顺序**
   ```
   → 读取 workflows/01-env-check.md
   → 执行步骤 [1/7]
   → 输出步骤 [1/7] 结果
   
   → 读取 workflows/02-project-init.md
   → 执行步骤 [2/7]
   → 输出步骤 [2/7] 结果
   
   → 读取 workflows/03-file-filter.md
   → 执行步骤 [3/7]
   → 输出步骤 [3/7] 结果
   
   ... 依此类推 ...
   ```

3. **读取即执行**
   - 读取工作流文档后，必须立即执行该步骤
   - 禁止读取文档后不执行，直接跳到下一步
   - 禁止读取多个文档后再统一执行

### 读取时机参考表

| 步骤 | 触发时机 | 读取文档 | 执行内容 |
|-----|---------|---------|---------|
| [1/7] | 技能启动 | `workflows/01-env-check.md` | PreCI 路径检测、自动安装、Server 状态检测 |
| [2/7] | 步骤 1 完成 | `workflows/02-project-init.md` | 项目类型检测、配置解析、工作目录初始化 |
| [3/7] | 步骤 2 完成 | `workflows/03-file-filter.md` | 获取变更文件、白名单过滤、无代码文件判断 |
| [4/7] | 步骤 3 完成且有代码文件 | `workflows/04-scan.md` | 执行扫描（combined/diff/pre-commit/all） |
| [5/7] | 步骤 4 完成 | `workflows/06-review.md` | 问题分类、质量评估、结构化报告 |
| [6/7] | 步骤 5 完成且有问题 | `workflows/05-auto-fix.md` | 循环修正、重新扫描、验证结果 |
| [7/7] | 步骤 6 完成或无问题 | `workflows/07-report.md` | 最终汇总、建议输出、返回结果 |

### 特殊情况处理

**情况 1：无代码文件时**
```
[1/7] → [2/7] → [3/7] 检测到无代码文件
                      ↓
                直接跳到 [7/7] 输出报告
                （skipped=true, skipReason="无代码文件需要检查"）
```

**情况 2：扫描无问题时**
```
[1/7] → ... → [4/7] 扫描完成，无问题
                    ↓
              跳过 [5/7] 和 [6/7]
                    ↓
              直接执行 [7/7] 输出报告
```

### 自检清单（每步执行前必检）

执行每个步骤前，必须确认：
- [ ] 只读取了当前步骤的 1 个工作流文档？
- [ ] 没有提前读取后续步骤的文档？
- [ ] 当前步骤已执行完毕并输出结果？
- [ ] 准备读取下一步骤的文档？

## 执行前必读文档

AI 执行本技能时，**必须**严格遵循上述分步执行约束，按需读取以下工作流文档：

| 文档 | 说明 | 何时读取 |
|------|------|---------|
| `workflows/01-env-check.md` | 环境检测工作流 | 执行步骤 [1/7] 前 |
| `workflows/02-project-init.md` | 项目初始化工作流 | 执行步骤 [2/7] 前 |
| `workflows/03-file-filter.md` | 文件过滤工作流 | 执行步骤 [3/7] 前 |
| `workflows/04-scan.md` | 扫描执行工作流 | 执行步骤 [4/7] 前 |
| `workflows/06-review.md` | 结果审查工作流 | 执行步骤 [5/7] 前 |
| `workflows/05-auto-fix.md` | 自动修正工作流 | 执行步骤 [6/7] 前 |
| `workflows/07-report.md` | 输出报告工作流 | 执行步骤 [7/7] 前 |

**⚠️ 所有工作流文档包含完整的执行约束、输出格式和错误处理规范！**

## 标准执行工作流

PreCI 检查是一个标准化的 7 步工作流，**必须**严格按顺序执行：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 PreCI 代码检查开始
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 读取: workflows/01-env-check.md（仅此文档）
[1/7] 环境检测
      → 检测 PreCI 安装路径和版本
      → 检测 PreCI Server 状态
      ✅ 输出: PreCI 路径、版本号、Server 状态

🔴 读取: workflows/02-project-init.md（仅此文档）
[2/7] 项目初始化
      → 检测初始化标识文件
      → 自动初始化（如需要）
      ✅ 输出: 项目类型、配置参数、工作目录

🔴 读取: workflows/03-file-filter.md（仅此文档）
[3/7] 文件过滤
      → 获取变更文件列表
      → 过滤代码文件（白名单）
      → 判断是否有代码文件需要检查
      ✅ 输出: 代码文件列表、总数、是否跳过

🔴 读取: workflows/04-scan.md（仅此文档）
[4/7] 执行扫描
      → 根据 scan_mode 执行扫描
      → Combined 模式必须：[4.1] diff → [4.2] pre-commit → [4.3] 合并
      ✅ 输出: 扫描结果、问题列表

🔴 读取: workflows/06-review.md（仅此文档）
[5/7] 结果审查
      → 解析告警信息
      → 按类型分类统计
      → 生成结构化报告
      ✅ 输出: 问题分类、严重性统计、质量评估

🔴 读取: workflows/05-auto-fix.md（仅此文档）
[6/7] 自动修正
      → 循环修正（max_retry 轮）
      → 重新扫描验证
      ✅ 输出: 修正统计、剩余问题

🔴 读取: workflows/07-report.md（仅此文档）
[7/7] 输出报告
      → 最终汇总统计
      → 建议输出
      → 返回结果结构
      ✅ 输出: 完整的检查结果对象

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ PreCI 代码检查完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**⚠️ 强制约束**：
- 每个步骤前只读取该步骤的 1 个工作流文档
- 禁止一次性读取所有 7 个工作流文档
- 读取后立即执行该步骤，输出结果后再进入下一步

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `scan_mode` | string | `combined` | 扫描模式：`combined`、`diff`、`pre-commit`、`all` |
| `multi_project` | boolean | `false` | 是否扫描工作区内所有 Git 仓库 |
| `target_path` | string | `.` | 检查目标路径（相对或绝对） |
| `max_retry` | number | `3` | 自动修正最大重试次数 |
| `init_if_needed` | boolean | `true` | 未初始化时是否自动初始化 |