# API文档/宏观/大宗商品/天然气

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/natural-gas
> API Key: `macro/natural-gas`

---

## 天然气API

**简要描述:** 获取天然气数据，如亨利港天然气现货价格等。

**请求URL:** `https://open.lixinger.com/api/macro/natural-gas`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/natural-gas](https://www.lixinger.com/api/open-api/html-doc/macro/natural-gas)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 美国: `us` |
| metricsList | Yes | Array | 指标数组。如['hh_ng_sp']。 亨利港天然气现货价格 : `hh_ng_sp` |

### 示例

```json
{
    "areaCode": "us",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "hh_ng_sp"
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
            "date": "2026-03-16T00:00:00-04:00",
            "areaCode": "us",
            "hh_ng_sp": 3.03
        },
        {
            "date": "2026-03-13T00:00:00-04:00",
            "areaCode": "us",
            "hh_ng_sp": 3.2
        },
        {
            "date": "2026-03-12T00:00:00-04:00",
            "areaCode": "us",
            "hh_ng_sp": 3.27
        }
    ]
}
```
