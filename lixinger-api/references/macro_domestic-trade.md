# API文档/宏观/社会消费品零售

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/domestic-trade
> API Key: `macro/domestic-trade`

---

## 社会消费品零售API

**简要描述:** 获取社会消费品零售数据，如社会消费品零售总额等。

**请求URL:** `https://open.lixinger.com/api/macro/domestic-trade`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/domestic-trade](https://www.lixinger.com/api/open-api/html-doc/macro/domestic-trade)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['m.src.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 大陆支持: 社会消费品零售总额 : `src` m(月): t(累积)t_y2y(累积同比); 城镇社会消费品零售总额 : `src_u` m(月): t(累积)t_y2y(累积同比); 乡村社会消费品零售总额 : `src_c` m(月): t(累积)t_y2y(累积同比); 网上零售总额 : `sr_o` m(月): t(累积)t_y2y(累积同比) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.src.t"
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
            "date": "2026-02-28T00:00:00+08:00",
            "m": {
                "src": {
                    "t": 8607889999999.999
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2025-12-31T00:00:00+08:00",
            "m": {
                "src": {
                    "t": 50120240000000
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2025-11-30T00:00:00+08:00",
            "m": {
                "src": {
                    "t": 45606660000000
                }
            }
        }
    ]
}
```
