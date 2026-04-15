# API文档/宏观/失业率

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/unemployment-rate
> API Key: `macro/unemployment-rate`

---

## 失业率API

**简要描述:** 获取失业率数据，如美国失业率等。

**请求URL:** `https://open.lixinger.com/api/macro/unemployment-rate`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/unemployment-rate](https://www.lixinger.com/api/open-api/html-doc/macro/unemployment-rate)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 美国: `us` |
| metricsList | Yes | Array | 指标数组。如['u_r']。 美国失业率 : `u_r` m(月): t(累积) |

### 示例

```json
{
    "areaCode": "us",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.u_r.t"
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
            "date": "2026-02-01T00:00:00-05:00",
            "areaCode": "us",
            "m": {
                "u_r": {
                    "t": 0.044
                }
            }
        },
        {
            "date": "2026-01-01T00:00:00-05:00",
            "areaCode": "us",
            "m": {
                "u_r": {
                    "t": 0.043
                }
            }
        },
        {
            "date": "2025-12-01T00:00:00-05:00",
            "areaCode": "us",
            "m": {
                "u_r": {
                    "t": 0.044
                }
            }
        }
    ]
}
```
