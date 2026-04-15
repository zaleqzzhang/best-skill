# API文档/宏观/大宗商品/白银

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/silver-price
> API Key: `macro/silver-price`

---

## 白银API

**简要描述:** 获取白银数据，如伦敦银价格等。

**请求URL:** `https://open.lixinger.com/api/macro/silver-price`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/silver-price](https://www.lixinger.com/api/open-api/html-doc/macro/silver-price)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 美国: `us` |
| metricsList | Yes | Array | 指标数组。如['si_eur']。 伦敦银价格 : `si_eur` |

### 示例

```json
{
    "areaCode": "us",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "si_eur"
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
            "date": "2026-03-19T00:00:00-04:00",
            "si_eur": 69.7,
            "areaCode": "us"
        },
        {
            "date": "2026-03-18T00:00:00-04:00",
            "si_eur": 78.6,
            "areaCode": "us"
        },
        {
            "date": "2026-03-17T00:00:00-04:00",
            "si_eur": 80.215,
            "areaCode": "us"
        }
    ]
}
```
