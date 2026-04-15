# API文档/大陆/行业接口/申万2021版/基本面数据

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/industry/fundamental/sw_2021
> API Key: `cn/industry/fundamental/sw_2021`

---

## 基本面数据API

**简要描述:** 获取基本面数据，如PE、PB等。

**说明:**

- 指标计算请参考行业估值计算

**请求URL:** `https://open.lixinger.com/api/cn/industry/fundamental/sw_2021`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/industry/fundamental/sw_2021](https://www.lixinger.com/api/open-api/html-doc/cn/industry/fundamental/sw_2021)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 行业代码数组。 stockCodes长度>=1且<=100，格式如下：["490000"]。 请参考 行业信息API 获取合法的stockCode。 需要注意的是，当传入startDate时只能传入一个股票代码。 |
| date | No | String: YYYY-MM-DD (北京时间) | 指定日期。 需要注意的是，startDate和date至少要传一个。 |
| startDate | No | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** 需要注意的是，startDate和date至少要传一个。 |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 需要注意的是，请与startDate一起使用。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| metricsList | Yes | Array | 指标列表。例如：['mc', 'pe_ttm.ew', 'pe_ttm.y10.ew.cvpos’]。 **需要注意的是** ，共有三种形式的指标格式： **[metricsName].[granularity].[metricsType].[statisticsDataType]** : 支持指标有 `pe_ttm, pb, ps_ttm, dyr(股息率)` **[metricsName].[metricsType]** : 支持指标有 `dyr(股息率), pe_ttm, pb, ps_ttm` **[metricsName]** : 被剩余的指标支持，如 `, mc(市值)` `, tv(成交量)` `, ta(成交金额)` **当前支持:** metricsName PE-TTM : `pe_ttm`; PB : `pb`; PS-TTM : `ps_ttm`; 股息率 : `dyr`; 成交金额 : `ta`; 换手率 : `to_r`; 市值 : `mc`; A股市值 : `mc_om`; 流通市值 : `cmc`; 自由流通市值 : `ecmc`; 融资买入金额 : `fpa`; 融资偿还金额 : `fra`; 融资净买入金额 : `fnpa`; 融资余额 : `fb`; 融券卖出金额 : `ssa`; 融券偿还金额 : `sra`; 融券净卖出金额 : `snsa`; 融券余额 : `sb`; 陆股通持仓金额 : `ha_shm`; 陆股通净买入金额 : `mm_nba`; 发布时间 : `launchDate` granularity 上市以来 : `fs`; 20年 : `y20`; 10年 : `y10`; 5年 : `y5`; 3年 : `y3`; 1年 : `y1` metricsType 市值加权 : `mcw`; 等权 : `ew`; 正数等权 : `ewpvo`; 平均值 : `avg`; 中位数 : `median` statisticsDataType 当前值 : `cv`; 分位点% : `cvpos`; 最小值 : `minv`; 最大值 : `maxv`; 最大正值 : `maxpv`; 50%分位点值 : `q5v`; 80%分位点值 : `q8v`; 20%分位点值 : `q2v`; 平均值 : `avgv` |

### 示例

```json
{
    "date": "2026-03-10",
    "stockCodes": [
        "490000"
    ],
    "metricsList": [
        "pe_ttm.y10.mcw.cvpos",
        "pe_ttm.mcw",
        "mc"
    ],
    "token": "***********"
}
```

### 返回结果

```json
{
    "code": 1,
    "message": "success",
    "data": [
        {
            "date": "2026-03-10T00:00:00+08:00",
            "pe_ttm.y10.mcw.cvpos": 0.004534212695795548,
            "pe_ttm.mcw": 10.934917833071196,
            "mc": 7696880092328.66,
            "stockCode": "490000"
        }
    ]
}
```
