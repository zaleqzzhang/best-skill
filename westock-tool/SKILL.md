---
name: westock-tool
description: 条件选股/筛选股票工具 - 当用户需要按条件筛选股票时使用（如"找股价大于100的股票"、"PE低于20的股票"、"高股息低估值股票"等）。支持按价格、市盈率、市净率、ROE、涨跌幅、成交量、市值、资金流向等指标筛选，覆盖沪深/港股/美股。注意：本工具只做"选股筛选"，查询个股详情（行情、K线、财务、资金等）请用 westock-data
---

# WeStock Tool

**作用**：将自然语言选股需求转换为结构化查询条件，通过选股引擎批量筛选并返回结果。

> **工具分工说明**：
> - **westock-tool**（本工具）：**筛选/选股** — "找出满足条件的股票列表"
> - **westock-data**：**查询个股详情** — "查某只股票的行情/K线/财务/资金等数据"
> - **westock-portfolio**：**用户自选股查询** — "查看我的自选股列表"（当用户说"我的自选股"、"自选股有哪些"时使用）

**数据源**：腾讯自选股选股数据接口 | **支持市场**：A股（沪深）、港股、美股

---

## 已知限制速查

| 限制项 | 说明 |
|--------|------|
| 市场覆盖 | 沪深A股、港股、美股；**不支持北交所** |
| 市值单位差异 | 沪深 `TotalMV` 单位为**元**，港股/美股为**亿元**，构建条件时注意换算 |
| 港股/美股字段名 | 估值字段名与沪深不同（见常用字段速查），**切勿混用** |
| PE/PB 负值 | 亏损股 PE/PB 为负，筛选时必须排除负值，如 `PE_TTM > 0` |
| 港股特殊字段 | `PsTtm`/`PcfTtm` 仅选股查询支持，快照查询返回 0 |
| 预设函数市场 | 港股必须加 `--market hk`，美股必须加 `--market us` |

---

## 条件选股（filter）

```bash
# 基本用法
westock-tool filter "ClosePrice >= 100"
westock-tool filter "ClosePrice >= 100" --date 2026-03-12
westock-tool filter "ClosePrice >= 100" --date 2026-03-12 --limit 20

# AND 组合条件
westock-tool filter "intersect([PE_TTM > 0, PE_TTM < 20, ROETTM > 15])"

# OR 组合条件
westock-tool filter "union([ChangePCT > 5, Chg5D > 10])"

# 指定排序（按 ROE 降序）
westock-tool filter "intersect([PE_TTM > 0, PE_TTM < 15, ROETTM > 15])" --date 2026-03-12 --limit 20 --orderby ROETTM:desc

# 港股选股（--market hk）
westock-tool filter "intersect([PeTtm > 0, PeTtm < 10, DivTTM > 5])" --market hk

# 美股选股（--market us）
westock-tool filter "intersect([PeTtm > 0, PeTtm < 30, TotalMV > 1000])" --market us

# 按板块筛选（--universe，板块代码通过 westock-data search <关键词> sector 获取）
westock-tool filter "intersect([PE_TTM > 0, PE_TTM < 20])" --date 2026-03-12 --limit 20 --universe 11010001

# 输出原始 JSON
westock-tool filter "ClosePrice >= 100" --raw
```

**参数说明**：

| 参数 | 是否必选 | 说明 |
|------|---------|------|
| 表达式 | ✅ | 选股表达式，详见下方「表达式语法」 |
| `--date` | 可选 | `YYYY-MM-DD`，默认今天 |
| `--limit` | 可选 | 最大返回数量，默认 20 |
| `--orderby` | 可选 | 排序，格式 `字段:asc` 或 `字段:desc`，默认 `desc` |
| `--market` | 可选 | `hk`=港股，`us`=美股，不指定默认沪深 |
| `--universe` | 可选 | 概念板块代码，限定选股范围；通过 `westock-data search <关键词> sector` 获取板块代码 |

---

## 预设选股函数

常见选股场景可直接使用预设函数，无需手写表达式：

**CLI 调用方式**：

```bash
# 使用预设函数（--preset）
westock-tool filter --preset MACDGoldenCross --date 2026-03-24 --limit 30
westock-tool filter --preset LowPE --date 2026-03-12 --limit 20
westock-tool filter --preset HighDividend --date 2026-03-12 --limit 20 --market hk

# 省略日期或数量（使用默认值）
westock-tool filter --preset BullishMA                        # 今天，默认20条
westock-tool filter --preset BullishMA --date 2026-03-28      # 指定日期，默认20条
westock-tool filter --preset BullishMA --date 2026-03-28 --limit 3 # 指定日期和数量

# 查看所有可用预设函数名称列表
westock-tool filter --list-presets
```

> `--list-presets` 返回纯文本函数名列表（每行一个函数名），不含参数说明。

**参数说明**：

| 参数 | 是否必选 | 说明 |
|------|---------|------|
| `--preset` | 可选 | 预设函数名（见下表） |
| `--date` | 可选 | `YYYY-MM-DD`，默认今天 |
| `--limit` | 可选 | 最大返回数量，默认 20 |
| `--market` | 可选 | `hk`=港股，`us`=美股 |
| `--universe` | 可选 | 概念板块代码 |

> 所有参数均为命名参数，顺序不限。

> ⚠️ **预设函数的参数均为内置默认值，不支持通过 CLI 传入自定义参数。** 如需自定义条件，请使用 `filter` 表达式语法手写条件。

#### 估值分析类

| 函数名 | 说明 | 内置默认值 |
|--------|------|------|
| `LowPE` | 低PE筛选 | `maxPE`=20 |
| `LowPB` | 破净股筛选(PB<1) | `maxPB`=1 |
| `HighDividend` | 高股息筛选 | `minDividend`=3% |
| `ValuationPercentile` | 估值百分位低位 | `maxPercentile`=30 |
| `PEG` | PEG策略(PEG<1) | `maxPEG`=1, `minGrowth`=20% |

#### 技术指标类

| 函数名 | 说明 | 内置默认值 |
|--------|------|------|
| `BullishMA` | 均线多头排列 | - |
| `MACDGoldenCross` | MACD金叉 | - |
| `KDJOversold` | KDJ超卖 | `maxJ`=20 |
| `RSIOversold` | RSI超卖 | `maxRSI`=30 |
| `BollingerBreakout` | 布林带突破上轨 | - |
| `NineTurnGreen9` | 神奇九转绿9信号 | - |

#### 财务分析类

| 函数名 | 说明 | 内置默认值 |
|--------|------|------|
| `HighROE` | 高ROE筛选 | `minROE`=15% |
| `HighGrowth` | 高成长筛选 | `minRevenueGrowth`=20%, `minProfitGrowth`=30% |
| `LowDebt` | 低负债筛选 | `maxDebtRatio`=50% |
| `PositiveCashFlow` | 正现金流筛选 | - |

#### 资金流向类

| 函数名 | 说明 | 内置默认值 |
|--------|------|------|
| `MainInflow` | 主力资金流入 | `minInflow`=1亿 |
| `SustainedInflow` | 主力持续流入(5/10/20日) | - |
| `HighShortRatio` | 高卖空比例 | `minShortRatio`=10% |

#### 机构评级类（港股/美股）

| 函数名 | 说明 | 内置默认值 |
|--------|------|------|
| `HighRating` | 高机构评级 | `minBuyRating`=5 |
| `TargetPriceUpside` | 目标价上行空间 | `minUpside`=20% |

#### 组合策略类

| 函数名 | 说明 | 内置默认值 |
|--------|------|------|
| `HighDividendLowValuation` | 高股息+低估值 | `minDividend`, `maxPE`, `maxPB` |
| `WhiteHorseGrowth` | 白马成长(高ROE+稳定增长) | - |
| `Turnaround` | 困境反转 | `minTurnaround`=50% |
| `SmallCapValue` | 小盘价值(20-100亿市值) | - |
| `TechFundamentalCombo` | 技术面+基本面组合 | - |

---

## 表达式语法

| 语法 | 说明 | 示例 |
|------|------|------|
| `字段 比较符 值` | 单条件 | `ClosePrice >= 100` |
| `intersect([条件1, 条件2])` | AND 组合 | `intersect([ClosePrice >= 100, PE_TTM < 20])` |
| `union([条件1, 条件2])` | OR 组合 | `union([ChangePCT > 5, Chg5D > 10])` |

---

## 使用规范

- ✅ 使用 `westock-tool` CLI 命令执行选股查询，命令输出 Markdown 表格，AI 直接从表格读取数据
- ✅ 查询结果应转为表格或可读格式展示，禁止直接输出原始 JSON
- ❌ 不创建临时脚本文件，不将数据分析逻辑写成独立脚本
- ⚠️ **港股必须指定 `--market hk`，美股必须指定 `--market us`**
- ⚠️ 筛选 PE/PB 时排除负值（亏损股），如 `intersect([PE_TTM > 0, PE_TTM < 20])`
- ⚠️ 沪深和港股/美股的估值字段名不同，切勿混用
- ⚠️ **市值单位**：沪深 `TotalMV` 单位为"元"，港股/美股为"亿元"，构建条件时注意换算

---

## 股票代码格式

| 市场 | 格式 | 示例 |
|------|------|------|
| 沪市/科创板 | sh + 6位数字 | `sh600519`、`sh688981` |
| 深市 | sz + 6位数字 | `sz000001` |
| 北交所 | bj + 6位数字 | `bj430047` |
| 港股 | hk + 5位数字 | `hk00700` |
| 美股 | us + 代码 | `usAAPL` |

---

## 常用字段速查

> ⚠️ 沪深 `TotalMV` 单位为"元"，港股/美股为"亿元"

| 类别 | 沪深(HS) | 港股(HK) | 美股(US) |
|------|----------|----------|----------|
| 市盈率TTM | PE_TTM | PeTtm | PeTtm |
| 市净率 | PB | PbLF | PbLF |
| 股息率TTM | DividendRatioTTM | DivTTM | DivTTM |
| 市销率TTM | PS_TTM | PsTtm ⚠️ | - |
| 市现率TTM | PCF_TTM | PcfTtm ⚠️ | - |
| 收盘价 | ClosePrice | ClosePrice | ClosePrice |
| 涨跌幅 | ChangePCT | ChangePCT | ChangePCT |
| 总市值 | TotalMV (元) | TotalMV (亿元) | TotalMV (亿元) |
| 换手率 | TurnoverRate | TurnoverRate | TurnoverRate |
| ROE(TTM) | ROETTM | RoeWeighted | ROE |
| 主力净流入 | MainNetFlow | MainNetFlow | - |

> ⚠️ 港股 PsTtm/PcfTtm 仅选股查询支持，快照查询返回 0

**完整字段速查表（含行情、财务、技术指标等全部字段）参见 [references/fields-guide.md](./references/fields-guide.md)**

**详细返回格式、分析模板参见 [references/ai_usage_guide.md](./references/ai_usage_guide.md)**

---

## 常见场景速查

```
价格筛选：filter "intersect([ClosePrice >= 50, ClosePrice <= 200])"
低估值蓝筹：filter "intersect([PE_TTM > 0, PE_TTM < 15, ROETTM > 15])" --orderby ROETTM:desc
技术面选股：filter "intersect([MA_5 > MA_10, MA_10 > MA_20, MA_20 > MA_60])"
主力流入：filter "MainNetFlow > 100000000" --orderby MainNetFlow:desc
港股高股息：filter "intersect([PeTtm > 0, PeTtm < 10, DivTTM > 5])" --market hk
按板块筛选：westock-data search 半导体 sector → 获取板块代码 → filter ... --universe <代码>
联动分析：filter "intersect([PE_TTM > 0, PE_TTM < 15, ROETTM > 15])" --date 2026-03-31 --limit 5 --orderby ROETTM:desc
         → 取结果中的股票代码（如 sh600519,sh000858）
         → westock-data quote sh600519,sh000858    # 查实时行情
         → westock-data finance sh600519,sh000858 lrb 4  # 查近4期利润表对比
```

---

## 附录：环境安装

**环境要求**：Node.js >= v18（脚本为单文件打包，无需 npm install）

> 本文件（SKILL.md）所在目录即为技能根目录，脚本路径为 `scripts/index.js`。

**运行方式**：
```bash
node <SKILL.md所在目录>/scripts/index.js filter "ClosePrice >= 100"
```

如未安装 Node.js，根据系统自动安装：

```bash
# 检测
node --version 2>/dev/null || echo "未安装"

# macOS / Linux：通过 nvm 安装（无需 sudo）
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash \
  && export NVM_DIR="$HOME/.nvm" && \. "$NVM_DIR/nvm.sh" \
  && nvm install --lts && nvm use --lts
```

```powershell
# Windows PowerShell
if (-not (Get-Command node -EA SilentlyContinue)) { winget install OpenJS.NodeJS.LTS }
```
