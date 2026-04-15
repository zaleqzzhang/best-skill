# API文档/宏观/对外贸易

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/foreign-trade
> API Key: `macro/foreign-trade`

---

## 对外贸易API

**简要描述:** 获取对外贸易数据，如进出口总额(人民币)等。

**请求URL:** `https://open.lixinger.com/api/macro/foreign-trade`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/foreign-trade](https://www.lixinger.com/api/open-api/html-doc/macro/foreign-trade)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['m.tiae_rmb.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 大陆支持: 进出口总额(人民币) : `tiae_rmb` m(月): t(累积); 进口差额(人民币) : `iaeb_rmb` m(月): t(累积); 出口总额(人民币) : `te_rmb` m(月): t(累积); 进口总额(人民币) : `ti_rmb` m(月): t(累积); 进出口总额(美元) : `tiae_usd` m(月): t(累积)t_y2y(累积同比)c(当期)c_c2c(当期环比); 进口差额(美元) : `iaeb_usd` m(月): t(累积)c(当期); 出口总额(美元) : `te_usd` m(月): t(累积)t_y2y(累积同比)c(当期)c_c2c(当期环比); 进口总额(美元) : `ti_usd` m(月): t(累积)t_y2y(累积同比)c(当期)c_c2c(当期环比) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.tiae_rmb.t"
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
                "tiae_rmb": {
                    "t": 45468500000000
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2024-12-31T00:00:00+08:00",
            "m": {
                "tiae_rmb": {
                    "t": 43823391740000
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2023-12-31T00:00:00+08:00",
            "m": {
                "tiae_rmb": {
                    "t": 41751010000000
                }
            }
        }
    ]
}
```
