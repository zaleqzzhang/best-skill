---
name: skill-publish-guide
summary: "WorkBuddy Skill 发布前检查、脱敏、打包与三件套文案生成"
description: "Use this skill when the user wants to publish, upload, or share a WorkBuddy Skill to a public platform or marketplace. This includes: checking SKILL.md format, sanitizing sensitive data, packaging as ZIP, preparing competition submissions, and generating compelling introduction copy for Skills. Triggers: 发布skill, 上传skill, skill打包, skill脱敏, skill大赛, skill上传, 发布到市场, 上传到平台, skill格式检查, 生成介绍文案, skill介绍, 写skill简介, 发布产物, 三件套, publish skill, upload skill, package skill, skill marketplace, generate skill intro."
read_when:
  - User wants to publish or upload a Skill to marketplace
  - User wants to check SKILL.md format before publishing
  - User wants to sanitize sensitive data in Skill files
  - User wants to package Skill as ZIP for upload
  - User mentions "skill大赛" or "发布skill" or "上传skill"
  - User wants to generate introduction or promotional copy for a Skill
  - User wants to generate release artifacts / 发布产物 / 三件套 for a Skill
---

## ⚡ 默认交付物：发布三件套（DEFAULT DELIVERABLES）

**任何涉及 Skill 发布、上传、打包、分享的请求，默认必须产出以下 3 份产物**，除非用户明确说"只要其中一个"：

| # | 产物 | 文件名规范 | 用途 |
|---|------|-----------|------|
| 1 | **介绍文案** | `{skill-name}-介绍文案.md` | 对外宣发，标题党 + 痛点对比 + 实战数据 |
| 2 | **使用说明** | `{skill-name}-使用说明.md` | 用户上手文档，含安装、场景、故障排查 |
| 3 | **ZIP 安装包** | `{skill-name}.zip`，默认放 `~/Desktop/` | 可导入 WorkBuddy 的标准安装包 |

**输出位置约定**：
- 介绍文案和使用说明：放在 `{当前工作区}/` 根目录
- ZIP 包：放在 `~/Desktop/{skill-name}.zip`
- 若用户指定了其他位置，以用户指定为准

**交付流程（严格按顺序）**：

1. 读取目标 Skill 的 SKILL.md 全文，理解功能、触发词、坑点
2. 执行「发布前检查」（name 合规、summary/description 完整、敏感信息扫描）
3. 如发现 P0/P1 敏感信息 → 先询问用户：完整脱敏 / 改造为通用模板 / 仅内部分享
4. 若缺少 `summary` 字段，**自动补全**后再继续
5. 按本文档「介绍文案模板」生成 `{skill-name}-介绍文案.md`
6. 按本文档「使用说明模板」生成 `{skill-name}-使用说明.md`
7. 用 `zip -r ~/Desktop/{skill-name}.zip {skill-name}/` 打包
8. 调用 `deliver_attachments` 一次性交付 3 个文件
9. 在对话回复中**突出一句话介绍**（标题党版），并总结做了什么 + 风险提示

**如果是内部 Skill（未脱敏）**：
- 3 件套照常产出
- 在介绍文案 + 使用说明的顶部都加上 `⚠️ 仅限内部分享，严禁上传公网` 警告
- SKILL.md 的 frontmatter 下也加入同样警告

# Skill 发布前检查与打包指南

将 WorkBuddy Skill 上传到公开平台（如 Skill 市场、大赛提交）前的完整检查流程。

## 发布前检查清单

### 1. SKILL.md frontmatter 格式校验

必填字段：

| 字段 | 格式要求 | 正确示例 | 常见错误 |
|------|---------|---------|---------|
| `name` | **只允许 `a-z A-Z 0-9 -`** | `excel-to-tapd` | ❌ 中文、引号、冒号、空格、下划线 |
| `summary` | 简短描述，可用中文 | `"从 Excel 批量操作 TAPD"` | — |
| `description` | 触发词+功能描述，可用中文 | `"Triggers: Excel导入..."` | — |

可选字段：
- `read_when`: 触发条件列表（YAML 数组格式）

**校验命令**：
```bash
# 检查 name 字段是否合规
head -5 SKILL.md | grep 'name:' | grep -E '^name:\s*[a-zA-Z0-9-]+$' && echo "✅ name 合规" || echo "❌ name 含非法字符"
```

### 2. 隐私脱敏（最重要！）

上传到公开平台前**必须**扫描并替换以下敏感信息：

| 敏感类型 | 替换为 | 匹配特征 |
|---------|--------|---------|
| API 密码/Token/Secret | `YOUR_API_PASSWORD` | password/secret/token 后跟 8+ 位值 |
| UUID 格式凭据 | `YOUR_API_KEY` | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| 纯数字 workspace/project ID | `YOUR_WORKSPACE_ID` | 路径或参数中的 5-12 位纯数字 |
| 长数字 ID（需求/任务） | `EXAMPLE_ID` | 16+ 位连续数字 |
| 内网域名/URL | 通用化 | `*.woa.com` / `*.oa.com` / `*.tencent.com` 等 |
| curl/http 中的 `-u user:pass` | `YOUR_API_USER:YOUR_API_PASSWORD` | Basic Auth 凭据 |
| 真实用户名（RTX） | `user1` / `user2` | 需人工判断，脚本标记可疑项 |

**通用脱敏扫描命令**（直接对 Skill 目录执行，无需手动填写敏感词）：

```bash
#!/bin/bash
# usage: bash scan_sensitive.sh /path/to/skill-dir
DIR="${1:-.}"
echo "🔍 敏感信息扫描: $DIR"
echo "================================"
FOUND=0

# 1. 密码/密钥/Token 赋值（key=value 或 key: value 形式）
echo "--- 密码/密钥/Token ---"
grep -rn -i -E '(password|passwd|secret|token|api_key|apikey|access_key|app_secret)\s*[:=]\s*.{6,}' "$DIR" \
  --include="*.md" --include="*.sh" --include="*.py" --include="*.js" --include="*.json" --include="*.yaml" --include="*.yml" --include="*.toml" \
  && FOUND=1 || echo "  ✅ 未发现"

# 2. UUID 格式（常见于 API Key、Token）
echo "--- UUID 格式 ---"
grep -rn -E '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}' "$DIR" \
  --include="*.md" --include="*.sh" --include="*.py" --include="*.js" --include="*.json" \
  && FOUND=1 || echo "  ✅ 未发现"

# 3. curl -u 基础认证
echo "--- curl Basic Auth ---"
grep -rn -E 'curl\s.*-u\s+\S+:\S+' "$DIR" \
  --include="*.md" --include="*.sh" --include="*.py" \
  && FOUND=1 || echo "  ✅ 未发现"

# 4. 内网域名/URL
echo "--- 内网 URL ---"
grep -rn -E 'https?://[a-zA-Z0-9._-]+\.(woa|oa|tencent)\.(com|cn)[^\s)]*' "$DIR" \
  --include="*.md" --include="*.sh" --include="*.py" --include="*.js" --include="*.json" \
  && FOUND=1 || echo "  ✅ 未发现"

# 5. 长数字 ID（16位以上，常见于 TAPD story_id/task_id）
echo "--- 长数字 ID (>=16位) ---"
grep -rn -E '\b[0-9]{16,}\b' "$DIR" \
  --include="*.md" --include="*.sh" --include="*.py" --include="*.js" \
  && FOUND=1 || echo "  ✅ 未发现"

# 6. 5-12位纯数字（可能是 workspace_id / project_id，需人工确认）
echo "--- 疑似 workspace/project ID (5-12位数字) ---"
grep -rn -E '(workspace|project|space)[-_]?(id)?\s*[:=/"'\'']\s*[0-9]{5,12}' "$DIR" \
  --include="*.md" --include="*.sh" --include="*.py" --include="*.js" --include="*.json" \
  && FOUND=1 || echo "  ✅ 未发现"

echo ""
echo "================================"
[ $FOUND -eq 0 ] && echo "✅ 未发现明显敏感信息" || echo "⚠️ 发现可疑内容，请逐条确认是否需要脱敏"
```

**建议扫描范围**：
- `SKILL.md` — 主文件，最常残留真实凭据和 ID
- `examples/` — 示例脚本中容易残留真实数据
- `references/` — 参考文档中的 API 示例
- `scripts/` — 工具脚本中的硬编码凭据
- `assets/` — 附件资源

### 3. 文件结构检查

标准目录结构：
```
skill-name/
├── SKILL.md          ← 必须存在，根目录或一级子目录
├── examples/         ← 示例脚本（可选）
│   ├── example1.sh
│   └── example_result.md
├── references/       ← 参考文档（可选）
├── scripts/          ← 工具脚本（可选）
└── assets/           ← 图片等资源（可选）
```

### 4. 打包上传

```bash
# 打包为 ZIP（从 Skill 目录的上一级执行）
cd ~/.workbuddy/skills/
zip -r ~/Desktop/skill-name.zip skill-name/

# 检查包大小（限制 100MB）
ls -lh ~/Desktop/skill-name.zip

# 检查包内容
unzip -l ~/Desktop/skill-name.zip
```

## 比赛提交额外事项

### 提交表单字段

| 字段 | 说明 |
|------|------|
| **名称** | 展示用标题，可用中文，建议有冲击力 |
| **上传方式** | ZIP 包上传 或 工蜂仓库 |
| **使用说明** | 功能介绍、使用步骤、注意事项、系统要求 |
| **标签** | 从以下选择：需求评审 / 开发 / 质量测试 / 运维 / 数据分析 / 信息检索 / 通用办公 / 项目管理 / 设计 / 生活娱乐 |

### 使用说明建议结构

```
功能介绍（做什么）
  ↓
使用步骤（怎么用）
  ↓
核心技术亮点（凭什么选你）
  ↓
注意事项（有什么限制）
  ↓
系统要求（需要什么环境）
  ↓
实战数据（效果量化）
```

## 一键检查脚本

对任意 Skill 目录执行完整发布前检查：

```bash
#!/bin/bash
# usage: bash check_skill.sh /path/to/skill-dir

SKILL_DIR="${1:-.}"

echo "🔍 Skill 发布前检查: $SKILL_DIR"
echo "================================"

# 1. 检查 SKILL.md 存在
if [ -f "$SKILL_DIR/SKILL.md" ]; then
  echo "✅ SKILL.md 存在"
else
  echo "❌ SKILL.md 不存在！"
  exit 1
fi

# 2. 检查 name 字段
NAME=$(grep '^name:' "$SKILL_DIR/SKILL.md" | head -1 | sed 's/name:\s*//')
if [ -z "$NAME" ]; then
  echo "❌ 缺少 name 字段"
elif echo "$NAME" | grep -qE '^[a-zA-Z0-9-]+$'; then
  echo "✅ name 合规: $NAME"
else
  echo "❌ name 含非法字符: $NAME （只允许 a-z A-Z 0-9 -）"
fi

# 3. 检查 summary 字段
grep -q '^summary:' "$SKILL_DIR/SKILL.md" && echo "✅ summary 存在" || echo "❌ 缺少 summary"

# 4. 检查 description 字段
grep -q '^description:' "$SKILL_DIR/SKILL.md" && echo "✅ description 存在" || echo "❌ 缺少 description"

# 5. 敏感信息扫描（通用模式，无需手动填写）
echo ""
echo "--- 敏感信息扫描 ---"
FOUND=0

# 密码/密钥/Token 赋值
grep -rn -i -E '(password|passwd|secret|token|api_key|apikey|access_key|app_secret)\s*[:=]\s*.{6,}' "$SKILL_DIR" \
  --include="*.md" --include="*.sh" --include="*.py" --include="*.js" --include="*.json" --include="*.yaml" --include="*.yml" && FOUND=1

# UUID 格式
grep -rn -E '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}' "$SKILL_DIR" \
  --include="*.md" --include="*.sh" --include="*.py" --include="*.js" --include="*.json" && FOUND=1

# curl Basic Auth
grep -rn -E 'curl\s.*-u\s+\S+:\S+' "$SKILL_DIR" \
  --include="*.md" --include="*.sh" --include="*.py" && FOUND=1

# 内网 URL
grep -rn -E 'https?://[a-zA-Z0-9._-]+\.(woa|oa|tencent)\.(com|cn)' "$SKILL_DIR" \
  --include="*.md" --include="*.sh" --include="*.py" --include="*.js" --include="*.json" && FOUND=1

# 长数字 ID（>=16位）
grep -rn -E '\b[0-9]{16,}\b' "$SKILL_DIR" \
  --include="*.md" --include="*.sh" --include="*.py" --include="*.js" && FOUND=1

# 疑似 workspace/project ID
grep -rn -E '(workspace|project|space)[-_]?(id)?\s*[:=/"'"'"']\s*[0-9]{5,12}' "$SKILL_DIR" \
  --include="*.md" --include="*.sh" --include="*.py" --include="*.js" --include="*.json" && FOUND=1

[ $FOUND -eq 0 ] && echo "✅ 未发现明显敏感信息" || echo "⚠️ 发现可疑内容，请逐条确认是否需要脱敏"

# 6. 文件大小
echo ""
SIZE=$(du -sh "$SKILL_DIR" | cut -f1)
echo "📦 目录大小: $SIZE"

echo ""
echo "================================"
echo "检查完毕！"
```

## 常见踩坑

| 错误信息 | 原因 | 解法 |
|---------|------|------|
| `缺少必填字段 name` | frontmatter 没写 name | 添加 `name: my-skill` |
| `name 包含非法字符` | 用了中文/引号/冒号/空格 | 改为 `a-zA-Z0-9-` |
| `invalid zip file` | SKILL.md 不在根目录或一级子目录 | 调整目录结构 |
| 上传后触发词不生效 | description 中触发词覆盖不够 | 补充更多触发表述 |

---

## 一键生成介绍文案

当用户要求生成 Skill 介绍时，按以下流程执行：

### Step 1：信息采集

先阅读目标 Skill 的 SKILL.md 全文，提取以下关键信息：

| 采集项 | 来源 | 用途 |
|--------|------|------|
| 核心功能 | SKILL.md 正文 | 一句话介绍 + 能力全景 |
| 解决的痛点 | 用户描述 / SKILL.md 背景段 | 痛点场景表 |
| 技术亮点 | SKILL.md 中的特殊实现 | 技术亮点章节 |
| 实战数据 | 用户提供 / SKILL.md 中的案例 | 量化对比表 |
| 适用人群 | 推断 | 适用人群列表 |
| 已有经验/踩坑 | SKILL.md 中的注意事项 | 差异化优势 |

如果信息不足，主动追问用户补充实战案例和量化数据。

### Step 2：按模板生成文案

严格按以下结构输出，每个章节都必须包含：

---

#### 📄 介绍文案输出模板

```markdown
# [Skill 名称]

## 一句话介绍

**[动词开头，直击痛点，量化效果，制造反差]**

> 🔥 **标题党 4 要素**（缺一不可）：
> 1. **量化数字**：具体到秒/分钟/百分比/人数（越具体越打动人）
> 2. **反差对比**：原本 X 时间 → 现在 Y 时间，形成数量级落差
> 3. **情绪词**：「破表单」「老板催」「下午崩溃」「告别熬夜」等踩痛点词汇
> 4. **画面动词**：「砸进」「哐当」「喂给」「一键炸穿」比「生成」「处理」强 10 倍
>
> 写法公式：`[动词] + [对象] + [量化反差] + [情绪共鸣词]`
>
> 好的一句话示例（**标题党风格**）：
> - "一句话让 AI 把 TAPD 需求哐当一声砸进 iWiki——140+ PM 自动对号入座，3 分钟搞定你下午要填 40 分钟的破表单"
> - "49 条需求 3 分钟导入 TAPD——从 Excel 到看板，一句话搞定过去半天的重复劳动"
> - "一句话让 AI 帮你写完专利初稿——从灵感到 20 页技术交底书，2 小时替代 2 周"
> - "把散落在 10 个群里的日报自动聚合成周报——每周五省出 40 分钟"
>
> 差的一句话示例（**必须避免**）：
> - ❌ "一个帮助处理 TAPD 操作的工具" （太抽象，没有量化）
> - ❌ "Excel 数据导入 Skill" （没有价值感，读了也不想用）
> - ❌ "帮助产品经理提升效率的工具" （谁不是"提升效率"？）

---

## 痛点场景

> 用表格对比"没有 Skill 前"和"有 Skill 后"的体验差异，制造强烈反差。
> 每行一个具体场景，不要写抽象描述。

| 😫 痛点场景 | ⏱️ 手工耗时 | 🚀 用 Skill 后 |
|------------|------------|----------------|
| [具体场景1] | [X 小时/分钟] | [Y 分钟/秒] |
| [具体场景2] | [X 小时/分钟] | [Y 分钟/秒] |
| [具体场景3] | [X 小时/分钟] | [Y 分钟/秒] |

**核心价值：[一句话总结这个 Skill 的根本价值]**

---

## 能力全景

> 用 ASCII 框图或列表展示 Skill 的模块组成，让读者一眼看清能力边界。

---

## 核心能力详解

> 每个能力单独一节，结构为：一句话说明 + 亮点标注。
> 亮点用加粗标注，突出"别人做不到但我能做到"的点。

### 1. [能力名称] — [一句话卖点]

[2-3 行功能说明]

**亮点**：[这个能力最独特/最有价值的地方]

### 2. [能力名称] — [一句话卖点]

...

---

## 实战案例

> 必须有至少 1 个真实案例。结构：背景 → 操作 → 结果。
> 操作部分用代码块展示用户实际输入和 AI 响应，让读者直观感受使用体验。

### 案例：[项目/场景名]

**背景**：[X 条数据/Y 个团队，需要做什么]

**操作**：
\```
用户：[用户实际说的那句话]
AI：（[AI 执行的步骤链]）
\```

**结果**：[量化结果 + 耗时]

---

## 技术亮点

> 挑 2-3 个最硬核的技术点，用简洁的图示或伪代码说明原理。
> 重点突出"行业难题 → 我的方案"的叙事。

---

## 适用人群

> 用角色 + 场景的方式列出，让不同读者快速对号入座。

- **[角色1]**：[具体使用场景]
- **[角色2]**：[具体使用场景]
- **[角色3]**：[具体使用场景]

---

## 差异化优势

> 用对比表，维度不超过 6 行，每行一个决策点。

| 维度 | 传统方式 | 本 Skill |
|------|---------|---------|
| [维度1] | [痛点] | [优势] |
| [维度2] | [痛点] | [优势] |

---

*[一句收尾金句，呼应一句话介绍，制造记忆点]*
```

### Step 3：文案质量自检

生成文案后，逐项检查：

| 检查项 | 标准 | 不通过则 |
|--------|------|---------|
| 一句话介绍 | 包含量化数据 + 动词开头 + 反差对比 | 重写，必须有数字 |
| 痛点表格 | ≥3 行，每行有具体耗时对比 | 补充场景 |
| 实战案例 | ≥1 个，有真实数据支撑 | 向用户追问案例 |
| 技术亮点 | 突出"别人做不到"的点 | 重新提炼差异化 |
| 差异化表格 | ≤6 行，每行一个决策维度 | 精简合并 |
| 收尾金句 | 有记忆点，呼应开头 | 重写 |

### 文案写作原则

1. **数字优先**：能量化就量化。"3 分钟" 比 "很快" 有说服力 100 倍。
2. **反差制造**：痛点越痛，价值越明显。"大半天 → 3 分钟" 比 "有所提升" 更打动人。
3. **角色代入**：开头用"作为 XX，你一定遇到过…"拉近距离。
4. **先说结果**：每段先说用了之后怎样，再说怎么做到的。读者关心结果远多于原理。
5. **避免废话**：不要"本 Skill 是一个…"这种开头。直接说"从 X 到 Y，一步搞定。"
6. **视觉友好**：多用表格、代码块、emoji 分隔符，避免大段纯文字。

---

## 📘 使用说明模板（User Manual）

发布三件套的第二份产物——用户上手文档。和介绍文案互补：介绍文案负责"骗人入坑"，使用说明负责"真能用起来"。

### 使用说明输出模板

```markdown
# [Skill 名称] — 使用说明

## 📦 包含内容

- `{skill-name}.zip` — Skill 安装包
- `SKILL.md` — Skill 主文件（说明核心资源）

## 🚀 快速开始（3 步）

### Step 1：安装 Skill

**方式 A — ZIP 导入（推荐）**：WorkBuddy → 设置 → Skills → 导入 → 选择 ZIP

**方式 B — 手动放置**：把文件夹放到 `~/.workbuddy/skills/{skill-name}/`

### Step 2：配置依赖（MCP / 账号权限等）

[列出必要的 MCP、API、账号权限前置条件]

### Step 3：开始使用

[列出 3-5 个触发词 / 典型指令]

---

## 🎯 典型使用场景

> 至少 3 个场景，每个场景结构：用户原话（代码块）+ AI 自动动作（列表）+ 输出示例

### 场景 1：[最简场景]
### 场景 2：[进阶场景]
### 场景 3：[批量/组合场景]

---

## 📋 关键配置（如有内置常量）

用表格列出 Skill 内置的配置项及说明。

---

## ⚠️ 注意事项

### 使用前必看

1. 权限要求
2. 数据格式要求
3. 仅限内部/可公开的说明

### 踩坑提醒

把 SKILL.md 里沉淀的「坑点总结」搬过来，按「错误现象 → 原因 → 解法」格式。

---

## 🔧 故障排查

| 错误信息 | 原因 | 解法 |
|---------|------|------|
| [错误1] | [原因] | [解法] |

---

## 📬 反馈与维护

说明如何反馈 bug、如何维护内置数据（如映射表过期）。

---

## 📖 版本信息

- **Skill 名称**：xxx
- **当前版本**：YYYY-MM 版
- **适用平台**：WorkBuddy Code / WorkBuddy Mini Program
- **标签**：[从 10 个比赛标签中选 1-2 个]
```

### 使用说明质量自检

| 检查项 | 标准 |
|--------|------|
| 快速开始 | 必须 3 步以内，每步有明确产物 |
| 典型场景 | ≥3 个，覆盖最简/进阶/批量 |
| 每个场景都有用户原话代码块 | 让读者直接复制即可用 |
| 故障排查 | ≥3 条常见错误 |
| 踩坑提醒 | 从 SKILL.md 经验章节自动搬运 |

---

## 🎁 完整发布流程（三件套）

当用户说"帮我发布 Skill"、"生成发布产物"、"打包 Skill"、"三件套"等触发词时，**严格按以下步骤执行**：

```
1. 读取 ~/.workbuddy/skills/{skill-name}/SKILL.md 全文
      ↓
2. 基本字段检查（name 合规、summary 存在、description 存在）
   → 缺 summary 自动补全
      ↓
3. 敏感信息扫描（执行本文档的扫描命令）
   → 发现敏感信息时 AskUserQuestion:
     - 完整脱敏
     - 改造为通用模板
     - 仅内部分享（加警告）
      ↓
4. 生成 {workspace}/{skill-name}-介绍文案.md
   → 应用「标题党 4 要素」
   → 必包含：一句话介绍、痛点表、能力全景、核心能力、实战案例、技术亮点、差异化表、收尾金句
      ↓
5. 生成 {workspace}/{skill-name}-使用说明.md
   → 应用使用说明模板
   → 必包含：3 步安装、3+ 场景、故障排查、版本信息
      ↓
6. 打包 ZIP：cd ~/.workbuddy/skills/ && zip -r ~/Desktop/{skill-name}.zip {skill-name}/
      ↓
7. deliver_attachments 一次交付 3 个文件（顺序：介绍文案 > 使用说明 > ZIP）
      ↓
8. open_result_view 主推介绍文案
      ↓
9. 对话回复：突出一句话介绍 + 做了什么 + 风险提示（如果是内部 Skill）
```

**不得擅自省略任何一件产物**，除非用户明确说"只要 XX"。
