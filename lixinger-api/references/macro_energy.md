# API文档/宏观/能源

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/energy
> API Key: `macro/energy`

---

## 能源API

**简要描述:** 获取能源数据，如电力生产量等。

**请求URL:** `https://open.lixinger.com/api/macro/energy`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/energy](https://www.lixinger.com/api/open-api/html-doc/macro/energy)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['m.ep.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 大陆支持: 电力生产弹性系数 : `ec_elp` m(月): t(累积); 电力消费弹性系数 : `ec_elc` m(月): t(累积); 电力生产量 : `ep` m(月): t(累积); 电力消费量 : `ec` m(月): t(累积); 水力发电量 : `ep_h` m(月): t(累积); 火力发电量 : `ep_t` m(月): t(累积); 核电发电量 : `ep_n` m(月): t(累积); 风力发电量 : `ep_w` m(月): t(累积); 光能发电量 : `ep_s` m(月): t(累积) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.ep.t"
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
                "ep": {
                    "t": 1571790000000
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2025-12-31T00:00:00+08:00",
            "m": {
                "ep": {
                    "t": 9715880000000
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2025-11-30T00:00:00+08:00",
            "m": {
                "ep": {
                    "t": 8856700000000
                }
            }
        }
    ]
}
```
