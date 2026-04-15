# API文档/香港/公司接口/基本面数据/保险

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/company/fundamental/insurance
> API Key: `hk/company/fundamental/insurance`

---

## 基本面数据API

**简要描述:** 获取基本面数据，如PE、PB等。

**请求URL:** `https://open.lixinger.com/api/hk/company/fundamental/insurance`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/company/fundamental/insurance](https://www.lixinger.com/api/open-api/html-doc/hk/company/fundamental/insurance)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 股票代码数组。 stockCodes长度>=1且<=100，格式如下：["01336"]。 请参考 股票信息API 获取合法的stockCode。 需要注意的是，当传入startDate时只能传入一个股票代码。 |
| date | No | String: YYYY-MM-DD (北京时间) | 指定日期。 需要注意的是，startDate和date至少要传一个。 |
| startDate | No | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** 需要注意的是，startDate和date至少要传一个。 |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 需要注意的是，请与startDate一起使用。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| metricsList | Yes | Array | 指标数组。格式如下：['mc', 'pe_ttm', 'pb', 'dyr']。 需要注意的是，当stockCodes长度大于1时最多只能选取48个指标；当stockCodes长度等于1时最多只能获取36 个指标。 **当前支持:** **估值指标:** PEV : `pev`; PE-TTM : `pe_ttm`; PB : `pb`; PS-TTM : `ps_ttm`; 股息率 : `dyr`; PCF-TTM : `pcf_ttm`; 股价 : `sp`; 涨跌幅 : `spc`; 股价振幅 : `spa`; 成交量 : `tv`; 成交金额 : `ta`; 换手率 : `to_r`; 市值 : `mc`; H股市值 : `mc_om`; 港股通持仓股数 : `ah_sh`; 港股通持仓金额 : `ah_shm`; 港股通净买入金额 : `mm_nba`; 每手股数 : `sharesPerLot` **估值统计指标:** 指标格式为[metricsName].[granularity].[statisticsDataType]。 metricsName PE-TTM : `pe_ttm`; PB : `pb`; PS-TTM : `ps_ttm`; PEV : `pev`; 股息率 : `dyr` granularity 上市以来 : `fs`; 20年 : `y20`; 10年 : `y10`; 5年 : `y5`; 3年 : `y3`; 1年 : `y1` statisticsDataType 分位点% : `cvpos`; 20%分位点值 : `q2v`; 50%分位点值 : `q5v`; 80%分位点值 : `q8v`; 最小值 : `minv`; 最大值 : `maxv`; 最大正值 : `maxpv`; 平均值 : `avgv` |

### 示例

```json
{
    "date": "2026-03-10",
    "stockCodes": [
        "01336"
    ],
    "metricsList": [
        "pe_ttm",
        "mc",
        "pe_ttm.y3.cvpos"
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
            "mc": 165024015140,
            "pe_ttm": 4.0347,
            "stockCode": "01336",
            "pe_ttm.y3.cvpos": 0.5266
        }
    ]
}
```
