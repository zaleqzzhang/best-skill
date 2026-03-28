---
name: sec-to-notebooklm
description: 从 SEC EDGAR 下载美股研报（10-K 年报、10-Q 季报、8-K 公告、20-F 中概股年报等），并自动上传到 Google NotebookLM 笔记本，支持一键完成全流程。触发场景：(1) 用户要从 SEC/EDGAR 下载美股公司的报告/研报/披露文件，(2) 用户要将美股财报上传到 NotebookLM，(3) 用户提到 10-K、10-Q、8-K、20-F 等 SEC 文件类型，(4) 用户要自动化处理 SEC EDGAR 数据并导入 AI 笔记本。
---

# SEC → NotebookLM 工作流

## 快速开始

### 一键全流程
```bash
# 下载 AAPL 最近3份年报 + 自动上传到 NotebookLM
python3 scripts/sec_to_notebooklm.py AAPL

# 指定笔记本名称
python3 scripts/sec_to_notebooklm.py TSLA --form 10-Q --count 5 --notebook "Tesla Research"

# 中概股年报（20-F）
python3 scripts/sec_to_notebooklm.py BABA --form 20-F --count 2

# 首次使用（需 Google 登录）：加 --no-headless 显示浏览器
python3 scripts/sec_to_notebooklm.py AAPL --no-headless

# 只下载不上传
python3 scripts/sec_to_notebooklm.py NVDA --download-only
```

### 分步执行
```bash
# 步骤1：仅下载
python3 scripts/sec_downloader.py AAPL --form 10-K --count 3 --output ./sec_reports

# 步骤2：仅上传（从已下载的清单）
python3 scripts/notebooklm_uploader.py --manifest ./sec_reports/AAPL/manifest.json --notebook "AAPL Research"
```

## 报告类型

| 参数 | 说明 |
|------|------|
| `10-K` | 年度报告（默认） |
| `10-Q` | 季度报告 |
| `8-K` | 重大事件公告 |
| `20-F` | 外国公司年报（中概股用此） |
| `6-K` | 外国公司中期报告 |
| `DEF 14A` | 代理说明书 |
| `S-1` | IPO 招股书 |

## 工作流程

1. **搜索公司**：通过 `company_tickers.json` 精确匹配 Ticker → 获取 CIK
2. **获取报告列表**：调用 `submissions/CIK{}.json` 获取最近 N 份报告
3. **下载文件**：下载主文档（.htm/.txt/.pdf），保存到 `./sec_reports/{TICKER}/`，生成 `manifest.json`
4. **转换格式**：将 HTML 转换为 PDF（WeasyPrint），优化文件大小
5. **配置笔记本**：设置 custom prompt（SEC 财报分析师）
6. **上传 NotebookLM**：使用 NotebookLM CLI 上传 PDF 文件

## Custom Prompt 配置

### 默认配置

每次创建笔记本时，会自动配置 **SEC 财报深度分析师** prompt，包含：

- ✅ SEC 财报文件类型解读（10-K、10-Q、8-K、DEF 14A）
- ✅ 财务报表分析框架（资产负债表、利润表、现金流量表）
- ✅ AI 业务价值分析（收入贡献、投资回报、商业化评估）
- ✅ 估值分析框架（PE、DCF、安全边际计算）
- ✅ 风险因素识别（从 10-K Item 1A 提取）
- ✅ MD&A 深度解读（管理层讨论与分析）
- ✅ 竞争格局分析（同行业对比、护城河评估）
- ✅ 完整分析报告模板

Prompt 文件位置：`assets/sec_analyst_prompt.txt`

### 自定义 Prompt

```bash
# 使用自定义 prompt
python3 scripts/upload_sec_to_notebooklm.py \
  --manifest ./sec_reports/MSFT/manifest.json \
  --prompt ./my_custom_prompt.txt

# 跳过配置（不设置 custom prompt）
python3 scripts/upload_sec_to_notebooklm.py \
  --manifest ./sec_reports/MSFT/manifest.json \
  --no-configure
```

### 配置现有笔记本

> ⚠️ **重要提醒**：配置 custom prompt 时，必须使用完整的提示词文件内容，不能使用简化的名称！

如果笔记本已存在，可以单独配置 custom prompt：

```bash
# ✅ 正确方法：使用完整的提示词文件内容
notebooklm configure \
  --notebook 0dcf32ad-7dd5-4106-b320-f7ee3a2ce949 \
  --persona "$(cat assets/sec_analyst_prompt.txt)" \
  --response-length longer

# ❌ 错误方法：使用简化的名称
# notebooklm configure --notebook {id} --persona "SEC 分析师"
```

> 📖 **详细说明**：参见 [NOTEBOOKLM_CONFIGURATION_GUIDE.md](./NOTEBOOKLM_CONFIGURATION_GUIDE.md)

## NotebookLM 登录说明

- **首次使用**：必须加 `--no-headless` 参数，浏览器会弹出 Google 登录页，完成登录后 Cookie 自动保存到 `~/.sec-to-notebooklm/cookies.json`
- **后续使用**：Cookie 有效期内无需重新登录，可使用无头模式
- **运行在 AnyDev 云端开发机**：由于无法显示桌面，建议先在**个人电脑**上完成 Google 登录并导出 cookies，或使用下方"手动模式"

## 云端无桌面环境（AnyDev）说明

AnyDev 开发机无法显示浏览器界面，上传步骤有两种方案：

**方案 A（推荐）：下载后手动上传**
1. 先运行下载：`python3 scripts/sec_downloader.py AAPL --download-only`
2. 将 `./sec_reports/AAPL/` 目录打包下载到本地
3. 在个人电脑上手动上传到 NotebookLM，或使用个人电脑 Agent 执行上传

**方案 B：通过个人电脑 Agent**
在本地 Knot 个人电脑 Agent 中使用此 Skill，可正常显示浏览器完成登录和上传。

## 依赖安装

```bash
pip install requests playwright
python3 -m playwright install chromium --with-deps
```

## API 参考

SEC EDGAR API 详情见 `references/sec_api.md`
