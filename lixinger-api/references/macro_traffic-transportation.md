# API文档/宏观/交通运输

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/traffic-transportation
> API Key: `macro/traffic-transportation`

---

## 交通运输API

**简要描述:** 获取交通运输数据，如铁路货运量等。

**请求URL:** `https://open.lixinger.com/api/macro/traffic-transportation`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/traffic-transportation](https://www.lixinger.com/api/open-api/html-doc/macro/traffic-transportation)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['m.rfv.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 大陆支持: 铁路货运量 : `rfv` m(月): t(累积)t_y2y(累积同比)c(当期)c_c2c(当期环比) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.rfv.t"
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
                "rfv": {
                    "t": 5277480724.299999
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2025-11-30T00:00:00+08:00",
            "m": {
                "rfv": {
                    "t": 4830149196
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2025-10-31T00:00:00+08:00",
            "m": {
                "rfv": {
                    "t": 4369892507
                }
            }
        }
    ]
}
```
