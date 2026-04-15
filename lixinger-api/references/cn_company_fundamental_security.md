# API文档/大陆/公司接口/基本面数据/证券

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/fundamental/security
> API Key: `cn/company/fundamental/security`

---

## 基本面数据API

**简要描述:** 获取基本面数据，如PE、PB等。

**请求URL:** `https://open.lixinger.com/api/cn/company/fundamental/security`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/fundamental/security](https://www.lixinger.com/api/open-api/html-doc/cn/company/fundamental/security)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 股票代码数组。 stockCodes长度>=1且<=100，格式如下：["600030"]。 请参考 股票信息API 获取合法的stockCode。 需要注意的是，当传入startDate时只能传入一个股票代码。 |
| date | No | String: YYYY-MM-DD (北京时间) | 指定日期。 需要注意的是，startDate和date至少要传一个。 |
| startDate | No | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** 需要注意的是，startDate和date至少要传一个。 |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 需要注意的是，请与startDate一起使用。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| metricsList | Yes | Array | 指标数组。格式如下：['mc', 'pe_ttm', 'pb', 'dyr']。 需要注意的是，当stockCodes长度大于1时最多只能选取48个指标；当stockCodes长度等于1时最多只能获取36 个指标。 **当前支持:** **估值指标:** PE-TTM : `pe_ttm`; PE-TTM(扣非) : `d_pe_ttm`; PB : `pb`; PB(不含商誉) : `pb_wo_gw`; PS-TTM : `ps_ttm`; 股息率 : `dyr`; PCF-TTM : `pcf_ttm`; 股价 : `sp`; 涨跌幅 : `spc`; 股价振幅 : `spa`; 成交量 : `tv`; 成交金额 : `ta`; 换手率 : `to_r`; 总股东人数 : `shn`; 市值 : `mc`; A股市值 : `mc_om`; 流通市值 : `cmc`; 自由流通市值 : `ecmc`; 人均自由流通市值 : `ecmc_psh`; 融资买入金额 : `fpa`; 融资偿还金额 : `fra`; 融资净买入金额 : `fnpa`; 融资余额 : `fb`; 融券卖出金额 : `ssa`; 融券偿还金额 : `sra`; 融券净卖出金额 : `snsa`; 融券余额 : `sb`; 陆股通持仓股数 : `ha_sh`; 陆股通持仓金额 : `ha_shm`; 陆股通净买入金额 : `mm_nba` **估值统计指标:** 指标格式为[metricsName].[granularity].[statisticsDataType]。 metricsName PE-TTM : `pe_ttm`; PE-TTM(扣非) : `d_pe_ttm`; PB : `pb`; PB(不含商誉) : `pb_wo_gw`; PS-TTM : `ps_ttm`; 股息率 : `dyr` granularity 上市以来 : `fs`; 20年 : `y20`; 10年 : `y10`; 5年 : `y5`; 3年 : `y3`; 1年 : `y1` statisticsDataType 分位点% : `cvpos`; 20%分位点值 : `q2v`; 50%分位点值 : `q5v`; 80%分位点值 : `q8v`; 最小值 : `minv`; 最大值 : `maxv`; 最大正值 : `maxpv`; 平均值 : `avgv` |

### 示例

```json
{
    "date": "2026-03-10",
    "stockCodes": [
        "600030"
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
            "mc": 387260888641.77,
            "pe_ttm": 13.7993,
            "stockCode": "600030",
            "pe_ttm.y3.cvpos": 0.0733
        }
    ]
}
```
