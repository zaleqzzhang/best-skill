---
name: lixinger-api
description: "理杏仁(Lixinger)开放平台金融数据查询 Skill。提供 A股/港股/美股指数/基金/基金经理/基金公司/行业/宏观数据的查询能力(199个接口全覆盖)。This skill should be used when users ask about stock valuation (PE/PB/PS), financial statements (revenue/profit/ROE), stock prices, dividends, index data, fund information, macro economic data, commodity prices, interest rates, exchange rates, HK stocks, US index data, or any financial data analysis using the Lixinger open API. 当用户提及理杏仁、A股数据、港股数据、美股指数、估值分析、财务报表、PE/PB分位点、股息率、指数估值、基金信息、基金经理、基金公司、宏观经济、大宗商品、利率、汇率、国债收益率等金融数据查询需求时，应使用此 Skill。"
---

# 理杏仁(Lixinger) 开放平台 API 数据查询

## 概述

本 Skill 提供理杏仁开放平台 **211 个 API 接口**的完整查询能力。`references/` 目录下每个 `.md` 文件对应一个 API 接口的完整文档，包含参数定义、指标列表、请求示例和返回结果。

## 🚫 严格遵循文档原则 (ABSOLUTE RULE)

**在使用任何 API 接口之前，必须先 read_file 读取对应的 `references/*.md` 参考文档，并严格遵循文档中声明的参数值和约束。**

### 核心原则：文档即边界

**参考文档中明确列出的参数值、枚举选项、指标名称 = 该接口支持的全部能力。文档中未出现的 = 不支持。没有例外。**

### 绝对禁止的行为

1. **禁止猜测任何参数的可选值**: 每个参数的合法取值必须完全来自文档声明。包括但不限于 `areaCode`、`metricsList`、`stockCodes`、`fsTableType`、`granularity`、`source` 等所有枚举型参数
2. **禁止猜测指标名**: `metricsList` 中的指标必须完全来自文档中列出的指标列表，不能自行编造或从其他接口的指标列表中借用
3. **禁止假设接口能力**: 如果文档没有说明支持某个参数值/区域/指标/功能/数据维度，就视为不支持
4. **禁止"试一试"**: 不能以"试试看能不能用"为由传入文档未声明的参数值。即使参数名存在，其合法取值也仅限于文档列举的范围
5. **禁止跨接口推断**: 不能因为 A 接口支持某个参数值，就推断 B 接口也支持。每个接口的能力边界独立由其自身文档定义

### 数据不可用时的回复规范 (MUST follow)

当用户请求的数据在理杏仁 API 中**不被支持**时（包括：接口不存在、参数值不在文档声明范围内、指标不在列表中等任何情况），**必须**明确、诚实地告知用户：

> ⚠️ **理杏仁开放平台暂不支持 [用户请求的数据]。**
>
> 根据接口文档 `[参考文件名]`，`[参数名]` 当前仅支持：[文档中声明的合法取值列表]。
>
> 如需 [用户请求的数据]，建议通过以下渠道获取：
> - [给出 1-2 个替代数据源建议]

**绝对不能**在告知用户不支持之前偷偷尝试请求，也不能用"让我试试"来搪塞。

---

## ⚠️ 核心工作流 (MUST follow)

### Step 0: 检查 Token (MUST do first)

在执行任何 API 请求之前，**必须**确认用户已提供理杏仁 API Token。

**检查方式（按优先级）：**
1. 用户在当前对话中直接提供了 Token
2. 用户的代码/环境变量中已配置 Token（如 `LIXINGER_TOKEN` 环境变量）
3. 项目中已有包含 Token 的配置文件

**如果用户未提供 Token，必须立即提醒：**

> ⚠️ 使用理杏仁开放平台 API 需要提供 API Token。请先前往以下地址获取您的 Token：
>
> 🔗 **https://www.lixinger.com/open/api/token**
>
> 获取后，请将 Token 提供给我，或设置为环境变量 `LIXINGER_TOKEN`：
> ```bash
> export LIXINGER_TOKEN="your-token-here"
> ```
>
> 我将在收到 Token 后继续为您查询数据。

**⚠️ 重要**: 在用户提供有效 Token 之前，**不要**尝试构建或执行任何 API 请求。可以先帮用户分析需求、确定需要查询的接口和参数，但实际请求必须等 Token 就绪后再执行。

### Step 1: 理解用户意图 → 确定数据域

分析用户自然语言查询，识别：
1. **数据域**: A股公司 / A股指数 / A股行业 / A股基金 / 基金经理 / 基金公司 / 港股 / 美股指数 / 宏观数据
2. **数据类型**: 基础信息 / 估值(PE/PB/PS) / 财务报表 / K线价格 / 分红 / 股东 / 热度排名 / 商品价格 / 利率 / 汇率
3. **时间维度**: 单日 / 日期范围 / 最新
4. **实体**: 哪些股票/指数/基金/商品

### Step 2: 精确匹配参考文档

根据用户意图，从下方 **[API 接口索引]** 中找到对应的参考文件名，然后 **read_file 读取 `references/{filename}.md`** 获取完整的参数定义和指标列表。

> **⚠️ 重要**: 每次只读取与当前查询相关的 1-3 个参考文件，不要一次性加载过多文件。

> **🚫 关键**: 索引表仅用于定位文件名。**所有参数的合法取值（包括枚举值、指标列表等）必须以读取到的参考文档原文为准**，不能凭索引表中的关键词描述或记忆来推断。

### Step 3: 构建请求参数（含校验）

根据参考文档中的参数表格和指标列表，构建请求 JSON 体。

**⚠️ 参数校验清单（构建请求前逐项检查）：**

1. **枚举参数校验**: 对文档中每个枚举型参数（如 `areaCode`、`fsTableType`、`granularity`、`source` 等），确认用户需求对应的取值是否在文档声明的合法值列表中。如果不在，**停止构建请求**，按「数据不可用时的回复规范」告知用户
2. **指标列表校验**: `metricsList` 中选用的指标是否全部来自文档列出的指标？注意不同枚举参数值下支持的指标可能不同（例如不同 `areaCode` 支持的指标列表不同），不能混用
3. **必选参数校验**: 确认所有文档中标注为必选的参数都已填写
4. **参数值格式校验**: 日期格式、代码格式等是否符合文档要求

**其他关键约束：**

1. **单日查询**: 用 `date` 参数；可传多个 `stockCodes`
2. **日期范围**: 用 `startDate` + `endDate`；`stockCodes` 只能传 **1 个**
3. **指标上限**: 多股票 → 最多 48 个指标；单股票 → 最多 36 个指标；财报 → 最多 128 个指标
4. **日期间隔**: `startDate` 到 `endDate` 不超过 10 年
5. **估值财报**: 需要先确定 `fsTableType`（银行/证券/保险/其他金融/非金融），不确定时先查 `/cn/company` 获取

### Step 4: 执行请求并返回结果

使用以下代码模板：

```python
import requests
import time
import os

headers = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br"
}

def get_token(token=None):
    """Get Lixinger API token from parameter or environment variable.
    
    Priority: explicit parameter > LIXINGER_TOKEN env var
    Raises ValueError if no token is available.
    """
    t = token or os.environ.get("LIXINGER_TOKEN")
    if not t:
        raise ValueError(
            "未提供理杏仁 API Token！\n"
            "请通过以下方式之一提供 Token：\n"
            "1. 直接传入 token 参数\n"
            "2. 设置环境变量: export LIXINGER_TOKEN=\"your-token-here\"\n"
            "Token 获取地址: https://www.lixinger.com/open/api/token"
        )
    return t

def lixinger_request(url, payload, token=None, max_retries=3):
    """Send request to Lixinger API with retry mechanism.
    
    Args:
        url: API endpoint URL
        payload: Request body (token will be injected automatically)
        token: API token (optional, falls back to LIXINGER_TOKEN env var)
        max_retries: Maximum retry attempts for failed requests
    """
    # Ensure token is present in payload
    payload["token"] = get_token(token)
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 429:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue
            response.raise_for_status()
            result = response.json()
            if result.get("code") == 1:
                return result["data"]
            else:
                raise Exception(f"API error: {result.get('message', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
    raise Exception("Max retries exceeded")
```

### Step 5: 格式化呈现

- 大数值转为"亿/万亿"
- 百分比 ×100 并加 % 后缀
- 单实体用列表展示，多实体对比用表格
- 时间序列数据用表格并标注趋势

---

## 全局配置

```
BASE_URL: https://open.lixinger.com/api
HTTP Method: POST (所有接口)
Content-Type: application/json
Auth: request body 中的 token 字段
Date Format: YYYY-MM-DD (北京时间)
Response: JSON { code: 1, message: "success", data: [...] }
```

**Token**: ⚠️ **必须提供**。用户需从 https://www.lixinger.com/open/api/token 获取。可通过环境变量 `LIXINGER_TOKEN` 配置，或在请求时直接传入。

**频率限制**: 每秒 ≤36 次，每分钟 ≤1000 次。超限返回 HTTP 429，需退避重试。

---

## API 接口索引

> 以下索引列出了每个接口的**功能关键词**和对应的**参考文件名**（位于 `references/` 目录下）。
> 用户查询时，根据关键词匹配找到文件名，然后 read_file 读取完整文档。

### 一、A股(CN) 公司接口 — 50 个

#### 基础信息与概况

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 股票列表/基础信息 | 股票列表, 股票信息, 股票代码, fsTableType, 上市日期 | `cn_company.md` |
| 公司概况(地址/实控人) | 公司概况, 实际控制人, 省份, 城市, 历史股名 | `cn_company_profile.md` |
| 股票所属指数 | 股票属于哪个指数, 指数成分 | `cn_company_indices.md` |
| 股票所属行业 | 股票属于哪个行业, 行业分类 | `cn_company_industries.md` |

#### 价格与交易

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| K线/股价/复权 | 股价, K线, 开盘, 收盘, 最高, 最低, 成交量, 换手率, 涨跌幅, 复权, 前复权, 后复权 | `cn_company_candlestick.md` |
| 大宗交易 | 大宗交易, 折溢价率, 成交价, 买方, 卖方 | `cn_company_block-deal.md` |
| 龙虎榜 | 龙虎榜, 异常交易, 涨停, 跌停, 振幅, 连续涨停, 买入金额, 卖出金额, 营业部 | `cn_company_trading-abnormal.md` |

#### 估值数据 (fundamental)

> **⚠️ 需按 fsTableType 选择对应文件**

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 非金融公司估值 | PE, PB, PS, PCF, 市盈率, 市净率, 市销率, 市现率, 股息率, 市值, 融资融券, 陆股通, 估值分位点 | `cn_company_fundamental_non_financial.md` |
| 银行估值 | 银行PE, 银行PB, 银行估值 | `cn_company_fundamental_bank.md` |
| 证券估值 | 券商PE, 证券PB, 证券估值 | `cn_company_fundamental_security.md` |
| 保险估值 | 保险PE, 保险PB, 保险估值 | `cn_company_fundamental_insurance.md` |
| 其他金融估值 | 其他金融PE, 其他金融PB | `cn_company_fundamental_other_financial.md` |

#### 财务报表 (fs)

> **⚠️ 需按 fsTableType 选择对应文件，文件中包含数百个具体指标字段**

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 非金融财报 | 营收, 净利润, ROE, 毛利率, 资产负债, 现金流, 营业收入, 归母净利, 资产负债表, 利润表, 非金融 | `cn_company_fs_non_financial.md` |
| 银行财报 | 银行营收, 银行净利润, 不良率, 拨备覆盖率, 净息差, 银行资产 | `cn_company_fs_bank.md` |
| 证券财报 | 券商营收, 证券净利润, 经纪业务, 自营 | `cn_company_fs_security.md` |
| 保险财报 | 保险营收, 保费收入, 赔付, 保险投资 | `cn_company_fs_insurance.md` |
| 其他金融财报 | 其他金融营收, 其他金融净利润 | `cn_company_fs_other_financial.md` |

#### 分红/配股/股本

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 分红记录 | 分红, 每股红利, 红利, 股息, 除权日, 登记日 | `cn_company_dividend.md` |
| 配股 | 配股, 配股价格, 配股比例 | `cn_company_allotment.md` |
| 股本变动 | 股本, 总股本, 流通股, 限售股, 股本变动 | `cn_company_equity-change.md` |
| 股权质押 | 质押, 股权质押, 质押比例 | `cn_company_pledge.md` |

#### 股东相关

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 股东人数变化 | 股东人数, 股东数, 散户 | `cn_company_shareholders-num.md` |
| 前十大股东 | 十大股东, 大股东, 持股比例 | `cn_company_majority-shareholders.md` |
| 前十大流通股东 | 流通股东, 十大流通 | `cn_company_nolimit-shareholders.md` |
| 公募基金持股 | 基金持股, 基金持仓, 公募持股 | `cn_company_fund-shareholders.md` |
| 基金公司持股 | 基金公司持股, 基金公司持仓 | `cn_company_fund-collection-shareholders.md` |
| 高管增减持 | 高管增持, 高管减持, 董事增减持 | `cn_company_senior-executive-shares-change.md` |
| 大股东增减持 | 大股东增持, 大股东减持, 重要股东 | `cn_company_major-shareholders-shares-change.md` |

#### 经营信息

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 营收构成 | 营收构成, 收入结构, 营业收入构成, 产品收入, 地区收入 | `cn_company_operation-revenue-constitution.md` |
| 经营数据 | 经营数据, 运营数据, 业务数据, 产能, 产量, 销量, 用户数 | `cn_company_operating-data.md` |
| 客户 | 客户, 前五大客户, 客户集中度 | `cn_company_customers.md` |
| 供应商 | 供应商, 前五大供应商, 供应商集中度 | `cn_company_suppliers.md` |

#### 公告与监管

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 公告 | 公告, 公司公告, 年报, 季报, 临时公告 | `cn_company_announcement.md` |
| 监管措施 | 监管措施, 处罚, 警示函, 行政处罚 | `cn_company_measures.md` |
| 问询函 | 问询函, 交易所问询, 年报问询 | `cn_company_inquiry.md` |

#### 资金流向

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 陆股通/互联互通(个股) | 陆股通持仓, 沪港通, 深港通, 北向资金个股 | `cn_company_mutual-market.md` |
| 融资融券(个股) | 融资融券, 融资余额, 融券余额, 两融 | `cn_company_margin-trading-and-securities-lending.md` |

#### 公司热度数据 (hot)

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 总市值/流通市值排名 | 市值排名, 总市值排名, 大盘权重 | `cn_company_hot_capita.md` |
| 涨跌幅排名 | 涨跌幅排名, 涨幅榜, 跌幅榜 | `cn_company_hot_shnc.md` |
| 换手率排名 | 换手率排名, 活跃股 | `cn_company_hot_tr.md` |
| 换手率日均排名 | 日均换手率排名 | `cn_company_hot_tr_dri.md` |
| 成交金额排名 | 成交额排名, 成交量排名 | `cn_company_hot_t_a.md` |
| 融资融券排名 | 融资融券排名, 两融排名, 融资余额排名, 融券余额排名 | `cn_company_hot_mtasl.md` |
| 陆股通持仓排名 | 陆股通排名, 北向持仓排名, 北向资金排名 | `cn_company_hot_mm_ha.md` |
| 大股东增减持排名 | 大股东增减持排名, 重要股东增减持排名 | `cn_company_hot_mssc.md` |
| 高管增减持排名 | 高管增减持排名, 董监高增减持排名 | `cn_company_hot_esc.md` |
| 股权质押排名 | 质押比例排名, 质押排名 | `cn_company_hot_ple.md` |
| 股东人数变化排名 | 股东人数变化排名 | `cn_company_hot_npd.md` |
| 分红收益率排名 | 分红收益率排名, 股息排名 | `cn_company_hot_df.md` |
| 杠杆率排名 | 杠杆率排名, 资产负债率排名 | `cn_company_hot_elr.md` |

### 二、A股(CN) 指数接口 — 19 个

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 指数列表/信息 | 指数列表, 指数信息, 沪深300, 中证500, 上证50, 创业板指 | `cn_index.md` |
| 指数K线 | 指数K线, 指数点位, 指数涨跌 | `cn_index_candlestick.md` |
| 指数估值 | 指数PE, 指数PB, 指数估值, 指数股息率, PE分位点, PB分位点, 等权/加权 | `cn_index_fundamental.md` |
| 指数成分股 | 指数成分, 成分股列表, 样本股, 指数包含哪些股票 | `cn_index_constituents.md` |
| 成分股权重 | 成分股权重, 权重占比 | `cn_index_constituent-weightings.md` |
| 跟踪基金 | 跟踪基金, ETF跟踪, 指数基金 | `cn_index_tracking-fund.md` |
| 指数财报-非金融 | 指数财报, 指数营收, 指数净利润 | `cn_index_fs_non_financial.md` |
| 指数财报-银行 | 指数银行财报 | `cn_index_fs_bank.md` |
| 指数财报-证券 | 指数证券财报 | `cn_index_fs_security.md` |
| 指数财报-混合 | 指数混合财报 | `cn_index_fs_hybrid.md` |
| 指数陆股通 | 指数陆股通, 指数北向资金 | `cn_index_mutual-market.md` |
| 指数融资融券 | 指数融资融券, 指数两融 | `cn_index_margin-trading-and-securities-lending.md` |
| 指数热度-收盘点位 | 指数收盘, 指数点位排名 | `cn_index_hot_cp.md` |
| 指数热度-换手率 | 指数换手率排名 | `cn_index_hot_tr.md` |
| 指数热度-换手率收盘点位 | 指数日均换手率 | `cn_index_hot_tr_cp.md` |
| 指数热度-指数成分调入调出 | 指数成分调整, 指数调样 | `cn_index_hot_ic.md` |
| 指数热度-陆股通 | 指数陆股通排名 | `cn_index_hot_mm_ha.md` |
| 指数热度-融资融券 | 指数融资融券排名 | `cn_index_hot_mtasl.md` |
| 指数热度-场内基金认购净流入 | 基金净流入, ETF申购, ETF资金流入 | `cn_index_hot_ifet_sni.md` |

### 三、A股(CN) 行业接口 — 35 个

> **行业来源**: `sw`(申万), `sw_2021`(申万2021版), `cni`(国证)

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 行业列表 | 行业列表, 行业分类, 申万行业, 国证行业 | `cn_industry.md` |
| 行业成分股-申万 | 申万行业成分股, 申万行业包含哪些股票 | `cn_industry_constituents_sw.md` |
| 行业成分股-申万2021 | 申万2021行业成分股 | `cn_industry_constituents_sw_2021.md` |
| 行业成分股-国证 | 国证行业成分股 | `cn_industry_constituents_cni.md` |
| 行业估值-申万 | 申万行业PE, 申万行业估值 | `cn_industry_fundamental_sw.md` |
| 行业估值-申万2021 | 申万2021行业估值 | `cn_industry_fundamental_sw_2021.md` |
| 行业估值-国证 | 国证行业PE, 国证行业估值 | `cn_industry_fundamental_cni.md` |
| 行业财报-申万-非金融 | 申万行业财报 | `cn_industry_fs_sw_non_financial.md` |
| 行业财报-申万-银行 | | `cn_industry_fs_sw_bank.md` |
| 行业财报-申万-证券 | | `cn_industry_fs_sw_security.md` |
| 行业财报-申万-保险 | | `cn_industry_fs_sw_insurance.md` |
| 行业财报-申万-混合 | | `cn_industry_fs_sw_hybrid.md` |
| 行业财报-申万2021-非金融 | 申万2021行业财报 | `cn_industry_fs_sw_2021_non_financial.md` |
| 行业财报-申万2021-银行 | | `cn_industry_fs_sw_2021_bank.md` |
| 行业财报-申万2021-证券 | | `cn_industry_fs_sw_2021_security.md` |
| 行业财报-申万2021-保险 | | `cn_industry_fs_sw_2021_insurance.md` |
| 行业财报-申万2021-混合 | | `cn_industry_fs_sw_2021_hybrid.md` |
| 行业财报-国证-非金融 | 国证行业财报 | `cn_industry_fs_cni_non_financial.md` |
| 行业财报-国证-银行 | | `cn_industry_fs_cni_bank.md` |
| 行业财报-国证-证券 | | `cn_industry_fs_cni_security.md` |
| 行业财报-国证-保险 | | `cn_industry_fs_cni_insurance.md` |
| 行业财报-国证-混合 | | `cn_industry_fs_cni_hybrid.md` |
| 行业陆股通-申万 | 申万行业北向资金 | `cn_industry_mutual-market_sw.md` |
| 行业陆股通-申万2021 | | `cn_industry_mutual-market_sw_2021.md` |
| 行业陆股通-国证 | 国证行业北向资金 | `cn_industry_mutual-market_cni.md` |
| 行业融资融券-申万 | 申万行业两融 | `cn_industry_margin-trading-and-securities-lending_sw.md` |
| 行业融资融券-申万2021 | | `cn_industry_margin-trading-and-securities-lending_sw_2021.md` |
| 行业融资融券-国证 | 国证行业两融 | `cn_industry_margin-trading-and-securities-lending_cni.md` |
| 行业热度-陆股通-申万 | 申万行业陆股通排名 | `cn_industry_hot_mm_ha_sw.md` |
| 行业热度-陆股通-申万2021 | | `cn_industry_hot_mm_ha_sw_2021.md` |
| 行业热度-陆股通-国证 | 国证行业陆股通排名 | `cn_industry_hot_mm_ha_cni.md` |
| 行业热度-融资融券-申万 | 申万行业两融排名 | `cn_industry_hot_mtasl_sw.md` |
| 行业热度-融资融券-申万2021 | | `cn_industry_hot_mtasl_sw_2021.md` |
| 行业热度-融资融券-国证 | 国证行业两融排名 | `cn_industry_hot_mtasl_cni.md` |

### 四、A股(CN) 基金接口 — 24 个

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 基金列表/信息 | 基金列表, 基金代码, 基金名称, 基金类型 | `cn_fund.md` |
| 基金概况 | 基金概况, 投资策略, 业绩基准, 基金公司, 托管人, 运作方式 | `cn_fund_profile.md` |
| 基金经理(基金级) | 基金的经理, 基金管理人 | `cn_fund_manager.md` |
| 基金K线 | 基金K线, 基金涨跌, 基金价格 | `cn_fund_candlestick.md` |
| 基金净值 | 基金净值, 单位净值 | `cn_fund_net-value.md` |
| 基金累积净值 | 累积净值, 累计净值 | `cn_fund_total-net-value.md` |
| 分红再投入净值 | 分红再投入净值, 复权净值 | `cn_fund_net-value-of-dividend-reinvestment.md` |
| 基金费用 | 基金费率, 管理费, 托管费 | `cn_fund_fees.md` |
| 基金回撤 | 基金回撤, 最大回撤 | `cn_fund_drawdown.md` |
| 持仓换手率 | 基金换手率, 持仓换手 | `cn_fund_turnover-rate.md` |
| 场内基金收盘价 | 场内基金, ETF收盘价, LOF收盘价 | `cn_fund_exchange-traded-close-price.md` |
| 基金分红 | 基金分红, 基金分红记录 | `cn_fund_dividend.md` |
| 基金拆分 | 基金拆分 | `cn_fund_split.md` |
| 基金份额及规模 | 基金份额, 基金规模, AUM | `cn_fund_shares.md` |
| 持有人结构 | 持有人结构, 机构持有, 个人持有 | `cn_fund_shareholders-structure.md` |
| 基金持股 | 基金持股, 基金重仓股, 基金买了什么 | `cn_fund_shareholdings.md` |
| 资产组合 | 资产配置, 资产组合, 股票仓位, 债券仓位 | `cn_fund_asset-combination.md` |
| 行业资产组合 | 行业配置, 行业持仓, 基金行业分布 | `cn_fund_asset-industry-combination.md` |
| 基金公告 | 基金公告 | `cn_fund_announcement.md` |
| 基金热度-收益率 | 基金收益率, 基金回报, 基金排名 | `cn_fund_hot_fp.md` |
| 基金热度-收益率排名 | 基金收益排名 | `cn_fund_hot_fpr.md` |
| 基金热度-资产规模 | 基金规模排名, 最大基金 | `cn_fund_hot_f_as.md` |
| 基金热度-持有人结构 | 机构持有排名 | `cn_fund_hot_fss.md` |
| 基金热度-场内份额 | 场内份额排名, ETF规模 | `cn_fund_hot_fet_s.md` |

### 五、基金经理接口 — 6 个

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 基金经理列表 | 基金经理列表, 经理信息, 经理姓名 | `cn_fund-manager.md` |
| 管理的基金 | 基金经理管理哪些基金, 旗下基金 | `cn_fund-manager_management-funds.md` |
| 利润率 | 基金经理利润率, 经理业绩 | `cn_fund-manager_profit-ratio.md` |
| 经理持仓 | 基金经理持仓, 经理重仓 | `cn_fund-manager_shareholdings.md` |
| 经理热度-信息 | 基金经理排名, 经理规模排名 | `cn_fund-manager_hot_fmi.md` |
| 经理热度-收益率 | 基金经理收益排名, 经理业绩排名 | `cn_fund-manager_hot_fmp.md` |

### 六、基金公司接口 — 4 个

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 基金公司列表 | 基金公司列表, 基金公司信息 | `cn_fund-company.md` |
| 旗下基金经理 | 基金公司的基金经理 | `cn_fund-company_fund-manager-list.md` |
| 基金公司热度-规模 | 基金公司规模排名 | `cn_fund-company_hot_fc_as.md` |
| 基金公司热度-规模排名 | 基金公司AUM排名 | `cn_fund-company_hot_fc_asr.md` |

### 七、港股(HK) 公司接口 — 23 个

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 港股公司列表 | 港股列表, 港股代码, 港股信息, 腾讯, 美团, 阿里 | `hk_company.md` |
| 港股公司概况 | 港股公司概况 | `hk_company_profile.md` |
| 港股K线 | 港股K线, 港股股价 | `hk_company_candlestick.md` |
| 港股估值-非金融 | 港股PE, 港股PB, 港股估值, 港股市值 | `hk_company_fundamental_non_financial.md` |
| 港股估值-银行 | 港股银行估值 | `hk_company_fundamental_bank.md` |
| 港股估值-证券 | 港股券商估值 | `hk_company_fundamental_security.md` |
| 港股估值-保险 | 港股保险估值 | `hk_company_fundamental_insurance.md` |
| 港股估值-其他金融 | 港股其他金融估值 | `hk_company_fundamental_other_financial.md` |
| 港股财报-非金融 | 港股财报, 港股营收, 港股净利润 | `hk_company_fs_non_financial.md` |
| 港股财报-银行 | 港股银行财报 | `hk_company_fs_bank.md` |
| 港股财报-证券 | 港股券商财报 | `hk_company_fs_security.md` |
| 港股所属指数 | 港股属于哪个指数 | `hk_company_indices.md` |
| 港股所属行业 | 港股属于哪个行业 | `hk_company_industries.md` |
| 港股分红 | 港股分红, 港股股息 | `hk_company_dividend.md` |
| 港股配股 | 港股配股 | `hk_company_allotment.md` |
| 港股拆分 | 港股拆合股 | `hk_company_split.md` |
| 港股股东权益变动 | 港股股东变动, 港股增持减持 | `hk_company_shareholders-equity-change.md` |
| 港股公司回购 | 港股回购 | `hk_company_repurchase.md` |
| 基金公司持股(港股) | 基金持港股 | `hk_company_fund-collection-shareholders.md` |
| 港股公告 | 港股公告 | `hk_company_announcement.md` |
| 港股热度-董事权益变动 | 港股董事增减持 | `hk_company_hot_director_equity_change.md` |
| 港股热度-换手率 | 港股换手率排名 | `hk_company_hot_tr.md` |
| 港股热度-港股通 | 港股通排名, 南向资金 | `hk_company_hot_mm_ah.md` |

### 八、港股(HK) 指数接口 — 6 个

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 港股指数列表 | 恒生指数列表, 港股指数 | `hk_index.md` |
| 港股指数K线 | 恒指K线, 港股指数K线 | `hk_index_candlestick.md` |
| 港股指数估值 | 恒指PE, 恒指PB, 港股指数估值 | `hk_index_fundamental.md` |
| 港股指数成分 | 恒指成分股, 港股指数成分 | `hk_index_constituents.md` |
| 港股指数财报 | 恒指财报 | `hk_index_fs_hybrid.md` |
| 港股指数热度-港股通 | 恒指港股通排名 | `hk_index_hot_mm_ah.md` |

### 九、港股(HK) 行业接口 — 1 个

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 恒生行业成分 | 恒生行业分类, 港股行业成分 | `hk_industry_constituents_hsi.md` |

### 十、美股(US) 指数接口 — 8 个

| 功能 | 关键词 | 参考文件 |
|------|--------|----------|
| 美股指数列表 | 标普500, 纳斯达克, 道琼斯, 美股指数 | `us_index.md` |
| 美股指数K线 | 美股指数K线, 标普K线, 纳指K线 | `us_index_candlestick.md` |
| 美股指数估值 | 标普PE, 纳指PB, 美股指数估值 | `us_index_fundamental.md` |
| 美股指数成分 | 标普成分股, 纳指成分 | `us_index_constituents.md` |
| 美股指数财报 | 标普财报, 美股指数财报 | `us_index_fs_non_financial.md` |
| 美股指数热度-收盘点位 | 美股指数排名, 收盘点位 | `us_index_hot_cp.md` |
| 美股指数热度-ETF净流入 | 美股ETF资金流入 | `us_index_hot_ifet_sni.md` |
| 美股指数跟踪基金 | 美股跟踪基金, 标普ETF | `us_index_tracking-fund.md` |

### 十一、宏观(Macro) 数据接口 — 36 个

> **⚠️ 宏观接口的参数支持范围各不相同，下表已标注每个接口的 `areaCode` 支持区域。请求前务必确认用户需求在文档声明的支持范围内，不在范围内的必须明确告知用户"不支持"，不能猜测或尝试。**

#### 市场数据

| 功能 | 关键词 | areaCode 支持 | 参考文件 |
|------|--------|---------------|----------|
| 投资者数据 | 投资者, 开户数, 新增投资者, 散户数量 | 🇨🇳 仅`cn` | `macro_investor.md` |
| 信用证券账户 | 信用账户, 信用证券 | 🇨🇳 仅`cn` | `macro_credit-securities-account.md` |
| 印花税 | 印花税, 股票印花税, 证券交易印花税 | 🇨🇳 仅`cn` | `macro_stamp-duty.md` |

#### 价格与通胀

| 功能 | 关键词 | areaCode 支持 | 参考文件 |
|------|--------|---------------|----------|
| 价格指数(CPI/PPI) | CPI, PPI, 消费者价格指数, 生产者价格指数, 通胀, 物价 | 🇨🇳🇺🇸 `cn`+`us` | `macro_price-index.md` |

#### 货币金融

| 功能 | 关键词 | areaCode 支持 | 参考文件 |
|------|--------|---------------|----------|
| 利率 | 利率, LPR, Shibor, HIBOR, 同业拆借, 贷款利率, 存款利率 | 🇨🇳🇭🇰🇺🇸 `cn`+`hk`+`us` | `macro_interest-rates.md` |
| 国债收益率 | 国债, 国债收益率, 10年期国债, 中美利差 | 🇨🇳🇺🇸 `cn`+`us` | `macro_national-debt.md` |
| 货币供应 | M0, M1, M2, 货币供应, 货币发行 | 🇨🇳🇭🇰🇺🇸 `cn`+`hk`+`us` | `macro_money-supply.md` |
| 社会融资 | 社融, 社会融资, 社融规模 | 🇨🇳 仅`cn` | `macro_social-financing.md` |
| 人民币贷款 | 贷款, 人民币贷款, 信贷 | 🇨🇳 仅`cn` | `macro_rmb-loans.md` |
| 人民币存款 | 存款, 人民币存款, 储蓄 | 🇨🇳 仅`cn` | `macro_rmb-deposits.md` |
| 央行资产负债表 | 央行, 央行资产, 外汇占款 | 🇨🇳 仅`cn` | `macro_central-bank-balance-sheet.md` |
| 存款准备金率 | 存准率, 准备金率, 降准 | 🇨🇳 仅`cn` | `macro_required-reserves.md` |
| 杠杆率 | 杠杆率, 宏观杠杆, 居民杠杆, 企业杠杆 | 🇨🇳 仅`cn` | `macro_leverage-ratio.md` |
| 债券发行 | 债券发行, 国内债券 | 🇨🇳 仅`cn` | `macro_domestic-debt-securities.md` |

#### 经济指标

| 功能 | 关键词 | areaCode 支持 | 参考文件 |
|------|--------|---------------|----------|
| GDP | GDP, 国内生产总值, 经济增长 | 🇨🇳🇺🇸 `cn`+`us` | `macro_gdp.md` |
| 人口 | 人口, 出生率, 死亡率, 人口增长 | 🇨🇳 仅`cn` | `macro_population.md` |
| 失业率 | 失业率, 美国失业率 | 🇺🇸 **仅`us`（不支持中国）** | `macro_unemployment-rate.md` |
| 外贸 | 进出口, 外贸, 贸易顺差, 出口额, 进口额 | 🇨🇳 仅`cn` | `macro_foreign-trade.md` |
| 国际收支 | BOP, 国际收支, 经常账户 | 🇨🇳 仅`cn` | `macro_bop.md` |
| 外汇资产 | 外汇储备, 外汇资产, 外汇占款 | 🇨🇳 仅`cn` | `macro_foreign-assets.md` |
| 固定资产投资 | 固定资产投资, FAI, 基建投资 | 🇨🇳 仅`cn` | `macro_investment-in-fixed-assets.md` |
| 国内贸易(零售) | 社零, 社会消费品零售, 零售额 | 🇨🇳 仅`cn` | `macro_domestic-trade.md` |
| 交通运输 | 交通, 运输, 货运量, 客运量 | 🇨🇳 仅`cn` | `macro_traffic-transportation.md` |
| 房地产 | 房地产, 房价, 商品房销售, 房地产投资 | 🇨🇳 仅`cn` | `macro_real-estate.md` |
| 石油 | 石油, 成品油, 汽油, 柴油 | 🇺🇸 仅`us` | `macro_petroleum.md` |
| 能源 | 能源, 发电量, 用电量, 煤炭产量 | 🇨🇳 仅`cn` | `macro_energy.md` |
| 工业化 | 工业, 工业增加值, 规模以上工业 | 🇨🇳 仅`cn` | `macro_industrialization.md` |

#### 大宗商品

| 功能 | 关键词 | areaCode 支持 | 参考文件 |
|------|--------|---------------|----------|
| 原油 | 原油, WTI, 布伦特, 油价 | 🇺🇸 仅`us` | `macro_crude-oil.md` |
| 天然气 | 天然气, 天然气价格 | 🇺🇸 仅`us` | `macro_natural-gas.md` |
| 黄金 | 黄金, 金价, 上海金, 伦敦金 | 🇨🇳🇺🇸 `cn`+`us` | `macro_gold-price.md` |
| 白银 | 白银, 银价 | 🇺🇸 仅`us` | `macro_silver-price.md` |
| 铂金 | 铂金, 铂金价格 | 🇺🇸 仅`us` | `macro_platinum-price.md` |
| 有色金属 | 铜, 锌, 铅, 铝, 镍, 锡, 铜价, 有色金属 | 🇺🇸 仅`us` | `macro_non-ferrous-metals.md` |

#### 汇率指数

| 功能 | 关键词 | areaCode 支持 | 参考文件 |
|------|--------|---------------|----------|
| 美元指数 | 美元指数, DXY, USDX | 无areaCode参数 | `macro_usdx.md` |
| 人民币指数 | 人民币指数, CFETS, 人民币汇率指数 | 无areaCode参数 | `macro_rmbidx.md` |
| 汇率 | 汇率, USD/CNY, 美元兑人民币, 外汇, 货币兑换 | 无areaCode，用fromCurrency/toCurrency | `macro_currency-exchange-rate.md` |

---

## 常用代码速查

### 常用股票代码

| 公司 | 代码 | fsTableType |
|------|------|-------------|
| 贵州茅台 | 600519 | non_financial |
| 宁德时代 | 300750 | non_financial |
| 比亚迪 | 002594 | non_financial |
| 招商银行 | 600036 | bank |
| 工商银行 | 601398 | bank |
| 中国平安 | 601318 | insurance |
| 中信证券 | 600030 | security |

### 常用指数代码

| 指数 | 代码 |
|------|------|
| 上证50 | 000016 |
| 沪深300 | 000300 |
| 中证500 | 000905 |
| 中证1000 | 000852 |
| 创业板指 | 399006 |

### fsTableType 判断

| 公司类型 | fsTableType | 示例 |
|----------|-------------|------|
| 银行 | `bank` | 工商银行、招商银行、建设银行 |
| 证券 | `security` | 中信证券、华泰证券 |
| 保险 | `insurance` | 中国平安、中国人寿 |
| 其他金融 | `other_financial` | 信托、期货、多元金融 |
| **其他所有公司** | `non_financial` | 茅台、宁德时代、比亚迪 |

> 不确定时，先查 `cn_company.md` 对应的 `/cn/company` 接口获取 fsTableType。

---

## 多接口编排示例

**"分析茅台投资价值"：**
1. 读取 `references/cn_company_fundamental_non_financial.md` → 查 PE/PB/DY/分位点/市值
2. 读取 `references/cn_company_fs_non_financial.md` → 查营收/净利润/ROE/毛利率
3. 读取 `references/cn_company_dividend.md` → 查分红历史
4. 综合分析呈现

**"对比沪深300和中证500估值"：**
1. 读取 `references/cn_index_fundamental.md` → 查两个指数的 PE/PB 分位点
2. 对比呈现

**"查询铜价"：**
1. 读取 `references/macro_non-ferrous-metals.md` → 获取指标和参数
2. 请求 `/macro/non-ferrous-metals` → `metricsList=["l_cu_p"]`

**"中美10年期国债收益率对比"：**
1. 读取 `references/macro_national-debt.md` → 获取参数
2. 分别查 `areaCode="cn"` 和 `"us"` 的 `tcm_y10`

**"基金经理张坤的业绩"：**
1. 读取 `references/cn_fund-manager.md` → 查经理信息
2. 读取 `references/cn_fund-manager_management-funds.md` → 查管理基金
3. 读取 `references/cn_fund-manager_hot_fmp.md` → 查收益率排名

---

## 错误处理

| 错误 | 原因 | 处理 |
|------|------|------|
| Token 缺失 | 用户未提供 API Token | 提示用户前往 https://www.lixinger.com/open/api/token 获取 Token |
| **参数值不在文档声明范围** | **用户请求的参数值在该接口文档中未被列为合法取值** | **明确告知用户该接口不支持该参数值，列出文档声明的合法取值范围，并按需建议替代方案。绝对不能尝试传入未声明的值** |
| **指标不存在** | **用户请求的指标在该接口/参数组合下不存在** | **告知用户该接口不提供此指标，列出可用指标供选择** |
| HTTP 429 | 请求频率超限 | 等待 ≥1s 后重试，降低频率 |
| 网络超时 | 网络问题 | 指数退避重试 (1s→2s→4s)，最多 3 次 |
| `code != 1` | API 业务错误 | 展示错误信息给用户 |
| `data` 为空 | 非交易日/代码错误 | 建议尝试相邻交易日 |
| 不确定代码 | 股票代码未知 | 先查 `/cn/company` 验证 |
| 不确定 fsTableType | 公司类型未知 | 先查 `/cn/company` 获取 fsTableType |

---

## 宏观接口 areaCode 速查表

> 快速判断宏观接口的区域支持情况。**此表仅作速查参考，构建请求前仍必须 read_file 读取参考文档确认完整的参数约束。**

| areaCode 支持 | 接口列表 |
|--------------|---------|
| 🇨🇳 仅`cn` (21个) | investor, credit-securities-account, stamp-duty, social-financing, rmb-loans, rmb-deposits, central-bank-balance-sheet, required-reserves, leverage-ratio, domestic-debt-securities, population, foreign-trade, bop, foreign-assets, investment-in-fixed-assets, domestic-trade, traffic-transportation, real-estate, energy, industrialization |
| 🇺🇸 仅`us` (7个) | **unemployment-rate**, crude-oil, natural-gas, non-ferrous-metals, petroleum, platinum-price, silver-price |
| 🇨🇳🇺🇸 `cn`+`us` (4个) | gdp, gold-price, national-debt, price-index |
| 🇨🇳🇭🇰🇺🇸 `cn`+`hk`+`us` (2个) | interest-rates, money-supply |
| 无areaCode参数 (3个) | usdx, rmbidx, currency-exchange-rate |
