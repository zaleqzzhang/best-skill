# API文档/宏观/货币供应

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/money-supply
> API Key: `macro/money-supply`

---

## 货币供应API

**简要描述:** 获取货币供应数据，如M1等。

**请求URL:** `https://open.lixinger.com/api/macro/money-supply`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/money-supply](https://www.lixinger.com/api/open-api/html-doc/macro/money-supply)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn`; 香港: `hk`; 美国: `us` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['m.m1.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 大陆支持: M0 : `m0` m(月): t(累积)t_y2y(累积同比); M1 : `m1` m(月): t(累积)t_y2y(累积同比); M2 : `m2` m(月): t(累积)t_y2y(累积同比) 香港支持: M1 : `m1` m(月): t(累积)t_y2y(累积同比); M2 : `m2` m(月): t(累积)t_y2y(累积同比); M3 : `m3` m(月): t(累积)t_y2y(累积同比) 美国支持: M1 : `m1` m(月): t(累积)t_y2y(累积同比); M2 : `m2` m(月): t(累积)t_y2y(累积同比) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.m1.t"
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
            "date": "2026-02-28T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "m1": {
                    "t": 115930000000000
                }
            }
        },
        {
            "date": "2026-01-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "m1": {
                    "t": 117968052000000
                }
            }
        },
        {
            "date": "2025-12-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "m1": {
                    "t": 115514650000000
                }
            }
        }
    ]
}
```
