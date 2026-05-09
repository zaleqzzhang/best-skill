# PreCI 代码规范检查技能

专业的 PreCI 代码规范检查技能，支持单项目/多项目检查、自动安装、智能修正、多种扫描模式。

---

## 功能特性

| 特性 | 说明 |
|------|------|
| 🔧 **自动安装** | 自动检测并安装 PreCI 工具 |
| 🚀 **服务管理** | 智能检测/启动 PreCI Server |
| 📋 **多扫描模式** | combined / diff / pre-commit / all |
| 🎯 **智能过滤** | 代码文件白名单过滤，避免无效扫描 |
| 🛠️ **自动修正** | 自动修复常见规范问题（inner_ip_leak、code_style 等） |
| 📊 **批量检查** | 支持多项目批量检查 |
| 📈 **标准输出** | 结构化 JSON 输出，便于集成 |

---

## PreCI 安装

### 自动安装（推荐）

触发本技能时，步骤 [1/7] 会**自动检测并安装** PreCI，无需手动操作。

安装策略：直接从技能内置的 `scripts/PreCI/` 目录拷贝二进制文件到 `~/PreCI`，**完全绕过 `install.sh` 的交互式提示**，在 AI 非交互式执行环境中始终可靠。

```
[1/7] 环境检测
      [1.1] 检测 PreCI 命令路径...  → 未找到时自动触发安装
      [1.2] 开始安装 PreCI（非交互式直接拷贝模式）...
            源文件目录: .../scripts/PreCI
            安装目录  : ~/PreCI
            拷贝文件... ✅ 文件拷贝完成
      [1.3] 验证安装结果...  → 确认二进制可执行
```

### 手动安装（备选）

如需在 AI 环境之外手动安装，可直接执行安装脚本：

```bash
cd ~/.codebuddy/skills/preci-code-check/scripts/PreCI

# 默认安装到 ~/PreCI（推荐）
./install.sh

# 或指定安装目录
./install.sh /path/to/install
```

安装完成后使环境变量生效：

```bash
source ~/.bashrc    # bash 用户
source ~/.zshrc     # zsh 用户
```

验证安装：

```bash
preci version
```

> 参考文档：[PreCI 安装指南](https://doc.weixin.qq.com/doc/w3_AeAARwbsALACNbh6X086vTLuXiSS2?scode=AJEAIQdfAAoehWlEFYAeAARwbsALA)

### 安装注意事项

| 注意事项 | 说明 |
|---------|------|
| 📁 **安装位置** | 自动安装固定使用 `~/PreCI`，手动安装建议相同路径，避免权限和路径问题 |
| 🔐 **AnyDev 环境策略** | 在 AnyDev 云研发机器安装时，可能遇到网络策略限制。如提示策略不通，请根据反馈的目标 IP 申请策略：[AnyDev 申请访问 IDC 服务](https://iwiki.woa.com/p/4008772118) |

---

## 快速开始

### 方式一：技能调用（自然语言触发）

使用以下自然语言描述即可触发本技能：

| 触发关键字 | 示例 |
|-----------|------|
| "检查代码" | "请检查当前改动的代码" |
| "PreCI 检查" | "使用 PreCI 检查当前项目" |
| "代码规范检查" | "对当前代码进行规范检查" |
| "preci-code-check" | "使用 preci-code-check 技能检查代码" |
| "检查提交" | "检查我即将提交的代码" |

**触发示例**：

```
请使用 preci-code-check 检查当前改动的代码
```

```
帮我用 PreCI 检查一下这个项目的代码规范
```

```
检查当前目录的代码，使用 combined 模式
```

**参数配置示例**（如需指定参数）：

```yaml
use_skill: preci-code-check
scan_mode: combined      # 扫描模式
target_path: .           # 检查路径
max_retry: 3             # 最大重试次数
```

### 方式二：自定义命令([下载](https://git.woa.com/justinlai/open-ai-code/blob/master/commands/preci/check.md))

```bash
# 默认 combined 模式（推荐）
preci:check

# 指定扫描模式
preci:check -d    # diff 模式（未暂存文件）
preci:check -s    # staged 模式（已暂存文件）
preci:check -a    # all 模式（全量扫描）
preci:check -m    # 多项目检查
```

---

## 扫描模式说明

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **combined** ⭐ | 先扫描未暂存文件，再扫描已暂存文件，合并结果 | **默认推荐**，提交前检查 |
| diff | 仅检查未暂存文件（工作区修改） | 查看当前修改 |
| pre-commit | 仅检查已暂存文件 | 提交前最后检查 |
| all | 全量扫描整个项目 | 全面检查 |

---

## 工作流程

PreCI 检查遵循标准化的 7 步工作流：

```
┌─────────────────────────────────────────────────────────┐
│  [1/7] 环境检测  →  检测 PreCI 安装和 Server 状态       │
│  [2/7] 项目初始化 →  检测项目类型，自动初始化           │
│  [3/7] 文件过滤   →  获取变更文件，过滤代码文件         │
│  [4/7] 执行扫描   →  根据模式执行扫描                   │
│  [5/7] 结果审查   →  分类统计，质量评估                 │
│  [6/7] 自动修正   →  循环修正，重新验证                 │
│  [7/7] 输出报告   →  最终汇总，建议输出                 │
└─────────────────────────────────────────────────────────┘
```

---

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `scan_mode` | string | `combined` | 扫描模式 |
| `target_path` | string | `.` | 检查目标路径 |
| `max_retry` | number | `3` | 自动修正最大重试次数 |
| `multi_project` | boolean | `false` | 是否多项目检查 |
| `init_if_needed` | boolean | `true` | 未初始化时是否自动初始化 |

---

## 输出示例

```json
{
  "success": true,
  "scanMode": "combined",
  "summary": {
    "totalFiles": 5,
    "totalIssues": 12,
    "fixedIssues": 8,
    "remainingIssues": 4
  },
  "issuesByType": {
    "inner_ip_leak": 3,
    "code_style": 6,
    "unused_import": 3
  },
  "quality": {
    "level": "B",
    "fixRate": 0.67,
    "passThreshold": false
  }
}
```

---

## 自动修正能力

| 问题类型 | 修正策略 |
|----------|----------|
| inner_ip_leak | 添加 `@inner_ip_safe` 注释标记 |
| code_style | 自动格式化调整 |
| unused_import | 删除未使用的 import |
| naming_convention | 提示建议，谨慎修正 |

---

## 文件结构

```
preci-code-check/
├── SKILL.md              # 技能主文档（工作流引导）
├── README.md             # 本文件（使用说明）
└── workflows/            # 工作流文档
    ├── 01-env-check.md   # 环境检测
    ├── 02-project-init.md # 项目初始化
    ├── 03-file-filter.md # 文件过滤
    ├── 04-scan.md        # 扫描执行
    ├── 05-auto-fix.md    # 自动修正
    ├── 06-review.md      # 结果审查
    └── 07-report.md      # 输出报告
```

---

## 适用场景

- ✅ 代码提交前检查（pre-commit hook）
- ✅ CI/CD 流水线集成
- ✅ 主动代码质量检查
- ✅ 多项目批量扫描
- ✅ 代码审查辅助

---# PreCI 代码规范检查技能

专业的 PreCI 代码规范检查技能，支持单项目/多项目检查、自动安装、智能修正、多种扫描模式。

---

## 功能特性

| 特性 | 说明 |
|------|------|
| 🔧 **自动安装** | 自动检测并安装 PreCI 工具 |
| 🚀 **服务管理** | 智能检测/启动 PreCI Server |
| 📋 **多扫描模式** | combined / diff / pre-commit / all |
| 🎯 **智能过滤** | 代码文件白名单过滤，避免无效扫描 |
| 🛠️ **自动修正** | 自动修复常见规范问题（inner_ip_leak、code_style 等） |
| 📊 **批量检查** | 支持多项目批量检查 |
| 📈 **标准输出** | 结构化 JSON 输出，便于集成 |

---

## PreCI 安装

### 自动安装（推荐）

触发本技能时，步骤 [1/7] 会**自动检测并安装** PreCI，无需手动操作。

安装策略：直接从技能内置的 `scripts/PreCI/` 目录拷贝二进制文件到 `~/PreCI`，**完全绕过 `install.sh` 的交互式提示**，在 AI 非交互式执行环境中始终可靠。

```
[1/7] 环境检测
      [1.1] 检测 PreCI 命令路径...  → 未找到时自动触发安装
      [1.2] 开始安装 PreCI（非交互式直接拷贝模式）...
            源文件目录: .../scripts/PreCI
            安装目录  : ~/PreCI
            拷贝文件... ✅ 文件拷贝完成
      [1.3] 验证安装结果...  → 确认二进制可执行
```

### 手动安装（备选）

如需在 AI 环境之外手动安装，可直接执行安装脚本：

```bash
cd ~/.codebuddy/skills/preci-code-check/scripts/PreCI

# 默认安装到 ~/PreCI（推荐）
./install.sh

# 或指定安装目录
./install.sh /path/to/install
```

安装完成后使环境变量生效：

```bash
source ~/.bashrc    # bash 用户
source ~/.zshrc     # zsh 用户
```

验证安装：

```bash
preci version
```

> 参考文档：[PreCI 安装指南](https://doc.weixin.qq.com/doc/w3_AeAARwbsALACNbh6X086vTLuXiSS2?scode=AJEAIQdfAAoehWlEFYAeAARwbsALA)

### 安装注意事项

| 注意事项 | 说明 |
|---------|------|
| 📁 **安装位置** | 自动安装固定使用 `~/PreCI`，手动安装建议相同路径，避免权限和路径问题 |
| 🔐 **AnyDev 环境策略** | 在 AnyDev 云研发机器安装时，可能遇到网络策略限制。如提示策略不通，请根据反馈的目标 IP 申请策略：[AnyDev 申请访问 IDC 服务](https://iwiki.woa.com/p/4008772118) |

---

## 快速开始

### 方式一：技能调用（自然语言触发）

使用以下自然语言描述即可触发本技能：

| 触发关键字 | 示例 |
|-----------|------|
| "检查代码" | "请检查当前改动的代码" |
| "PreCI 检查" | "使用 PreCI 检查当前项目" |
| "代码规范检查" | "对当前代码进行规范检查" |
| "preci-code-check" | "使用 preci-code-check 技能检查代码" |
| "检查提交" | "检查我即将提交的代码" |

**触发示例**：

```
请使用 preci-code-check 检查当前改动的代码
```

```
帮我用 PreCI 检查一下这个项目的代码规范
```

```
检查当前目录的代码，使用 combined 模式
```

**参数配置示例**（如需指定参数）：

```yaml
use_skill: preci-code-check
scan_mode: combined      # 扫描模式
target_path: .           # 检查路径
max_retry: 3             # 最大重试次数
```

### 方式二：自定义命令([下载](https://git.woa.com/justinlai/open-ai-code/blob/master/commands/preci/check.md))

```bash
# 默认 combined 模式（推荐）
preci:check

# 指定扫描模式
preci:check -d    # diff 模式（未暂存文件）
preci:check -s    # staged 模式（已暂存文件）
preci:check -a    # all 模式（全量扫描）
preci:check -m    # 多项目检查
```

---

## 扫描模式说明

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **combined** ⭐ | 先扫描未暂存文件，再扫描已暂存文件，合并结果 | **默认推荐**，提交前检查 |
| diff | 仅检查未暂存文件（工作区修改） | 查看当前修改 |
| pre-commit | 仅检查已暂存文件 | 提交前最后检查 |
| all | 全量扫描整个项目 | 全面检查 |

---

## 工作流程

PreCI 检查遵循标准化的 7 步工作流：

```
┌─────────────────────────────────────────────────────────┐
│  [1/7] 环境检测  →  检测 PreCI 安装和 Server 状态       │
│  [2/7] 项目初始化 →  检测项目类型，自动初始化           │
│  [3/7] 文件过滤   →  获取变更文件，过滤代码文件         │
│  [4/7] 执行扫描   →  根据模式执行扫描                   │
│  [5/7] 结果审查   →  分类统计，质量评估                 │
│  [6/7] 自动修正   →  循环修正，重新验证                 │
│  [7/7] 输出报告   →  最终汇总，建议输出                 │
└─────────────────────────────────────────────────────────┘
```

---

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `scan_mode` | string | `combined` | 扫描模式 |
| `target_path` | string | `.` | 检查目标路径 |
| `max_retry` | number | `3` | 自动修正最大重试次数 |
| `multi_project` | boolean | `false` | 是否多项目检查 |
| `init_if_needed` | boolean | `true` | 未初始化时是否自动初始化 |

---

## 输出示例

```json
{
  "success": true,
  "scanMode": "combined",
  "summary": {
    "totalFiles": 5,
    "totalIssues": 12,
    "fixedIssues": 8,
    "remainingIssues": 4
  },
  "issuesByType": {
    "inner_ip_leak": 3,
    "code_style": 6,
    "unused_import": 3
  },
  "quality": {
    "level": "B",
    "fixRate": 0.67,
    "passThreshold": false
  }
}
```

---

## 自动修正能力

| 问题类型 | 修正策略 |
|----------|----------|
| inner_ip_leak | 添加 `@inner_ip_safe` 注释标记 |
| code_style | 自动格式化调整 |
| unused_import | 删除未使用的 import |
| naming_convention | 提示建议，谨慎修正 |

---

## 文件结构

```
preci-code-check/
├── SKILL.md              # 技能主文档（工作流引导）
├── README.md             # 本文件（使用说明）
└── workflows/            # 工作流文档
    ├── 01-env-check.md   # 环境检测
    ├── 02-project-init.md # 项目初始化
    ├── 03-file-filter.md # 文件过滤
    ├── 04-scan.md        # 扫描执行
    ├── 05-auto-fix.md    # 自动修正
    ├── 06-review.md      # 结果审查
    └── 07-report.md      # 输出报告
```

---

## 适用场景

- ✅ 代码提交前检查（pre-commit hook）
- ✅ CI/CD 流水线集成
- ✅ 主动代码质量检查
- ✅ 多项目批量扫描
- ✅ 代码审查辅助

---