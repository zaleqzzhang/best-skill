# API文档/宏观/石油

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/petroleum
> API Key: `macro/petroleum`

---

## 石油API

**简要描述:** 获取石油数据，如世界石油和其他液体库存等。

**请求URL:** `https://open.lixinger.com/api/macro/petroleum`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/petroleum](https://www.lixinger.com/api/open-api/html-doc/macro/petroleum)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 美国: `us` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['y.w_petaol_sto.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 美国支持: 世界石油和其他液体库存 : `w_petaol_sto` y(年): t(累积); 世界石油和其他液体产量 : `w_petaol_pro` y(年): t(累积) m(月): c(当期); 世界石油和其他液体消耗 : `w_petaol_con` y(年): t(累积) |

### 示例

```json
{
    "areaCode": "us",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "y.w_petaol_sto.t"
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
            "date": "2016-12-31T00:00:00-05:00",
            "areaCode": "us",
            "y": {
                "w_petaol_sto": {
                    "t": 4597943740.3
                }
            }
        }
    ]
}
```
