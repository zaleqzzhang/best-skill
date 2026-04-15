# API文档/宏观/工业

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/industrialization
> API Key: `macro/industrialization`

---

## 工业API

**简要描述:** 获取工业数据，如工业企业利润总额等。

**请求URL:** `https://open.lixinger.com/api/macro/industrialization`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/industrialization](https://www.lixinger.com/api/open-api/html-doc/macro/industrialization)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['m.adsietp.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 大陆支持: 工业企业利润总额 : `adsietp` m(月): t(累积); 工业企业营业收入 : `ieop` m(月): t(累积); 工业企业存货 : `iei` m(月): t(累积); 工业企业单位数 : `ien` m(月): t(累积); 工业企业平均用工人数 : `ieaw` m(月): t(累积); 工业企业产成品 : `iep` y(年): t(累积) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.adsietp.t"
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
            "areaCode": "cn",
            "date": "2025-12-31T00:00:00+08:00",
            "m": {
                "adsietp": {
                    "t": 7398200000000
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2025-11-30T00:00:00+08:00",
            "m": {
                "adsietp": {
                    "t": 6626860000000.001
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2025-10-31T00:00:00+08:00",
            "m": {
                "adsietp": {
                    "t": 5950290000000
                }
            }
        }
    ]
}
```
