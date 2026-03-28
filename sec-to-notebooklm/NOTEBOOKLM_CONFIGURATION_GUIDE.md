# NotebookLM 笔记本配置规范

## ⚠️ 重要提醒

配置 NotebookLM 笔记本的 custom prompt 时，**必须使用完整的提示词文件内容**，不能使用简化的名称或描述。

---

## ✅ 正确的配置方法

### 方法一：使用脚本（推荐）

```bash
# 使用 sec-to-notebooklm skill（自动配置完整提示词）
python3 scripts/batch_sec_to_notebooklm.py TICKER

# 或使用上传脚本
python3 scripts/notebooklm_uploader_v2.py \
  --manifest ./sec_reports/TICKER/manifest.json \
  --notebook "TICKER SEC Reports"
```

### 方法二：手动配置

```bash
# ✅ 正确：使用完整的提示词文件内容
notebooklm configure \
  --notebook {notebook_id} \
  --persona "$(cat assets/sec_analyst_prompt.txt)" \
  --response-length longer

# ❌ 错误：使用简化的名称
notebooklm configure \
  --notebook {notebook_id} \
  --persona "SEC 分析师" \
  --response-length longer
```

---

## 📋 配置后验证

配置完成后，应该看到类似输出：

```
Chat configured: persona: "name: 财报深度分析师
description: 基于《手把手教你读财报》方法论，同时识别美股与...", response length: longer
```

如果看到简化的 persona（如 `"SEC 分析师"`），说明配置错误，需要重新配置。

---

## 🎯 避免错误的最佳实践

### 1. 优先使用脚本
- ✅ 使用 skill 提供的脚本（自动配置完整提示词）
- ❌ 避免手动配置（容易出错）

### 2. 查看文档
- 手动配置前，先查看 SKILL.md 或此文档
- 确认正确的配置命令

### 3. 验证配置结果
- 配置后检查输出，确认 persona 包含完整内容
- 如果怀疑配置错误，重新运行配置命令

### 4. 记录到工作日志
- 记录配置方法（手动/脚本）
- 记录笔记本 ID 和配置时间

---

## 📊 提示词文件信息

| Skill | 提示词文件 | 大小 |
|-------|-----------|------|
| sec-to-notebooklm | `assets/sec_analyst_prompt.txt` | 18591 字节 |
| cninfo-to-notebooklm | `assets/financial_analyst_prompt.txt` | ~18000 字节 |

---

## 🔍 问题案例

### 案例 1：辉瑞（PFE）笔记本配置错误

**问题**：手动配置时使用了简化的 persona 名称
```bash
# ❌ 错误命令
notebooklm configure --notebook 71066ed1-b46d-4102-bd06-33902d224264 \
  --persona "SEC 分析师" --response-length longer
```

**修复**：使用完整的提示词文件
```bash
# ✅ 正确命令
notebooklm configure --notebook 71066ed1-b46d-4102-bd06-33902d224264 \
  --persona "$(cat assets/sec_analyst_prompt.txt)" --response-length longer
```

**教训**：手动配置时必须查看文档，使用完整的提示词文件内容。

---

## 📝 更新日志

- 2026-03-28: 创建文档，记录辉瑞笔记本配置错误案例
