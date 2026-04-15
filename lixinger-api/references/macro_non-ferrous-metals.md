# API文档/宏观/大宗商品/有色金属

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/non-ferrous-metals
> API Key: `macro/non-ferrous-metals`

---

## 有色金属API

**简要描述:** 获取有色金属数据，如伦敦铜价格等。

**请求URL:** `https://open.lixinger.com/api/macro/non-ferrous-metals`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/non-ferrous-metals](https://www.lixinger.com/api/open-api/html-doc/macro/non-ferrous-metals)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 美国: `us` |
| metricsList | Yes | Array | 指标数组。如['l_cu_p']。 伦敦铜价格 : `l_cu_p`; 伦敦锌价格 : `l_zn_p`; 伦敦铅价格 : `l_pb_p`; 伦敦铝价格 : `l_al_p`; 伦敦镍价格 : `l_ni_p`; 伦敦锡价格 : `l_sn_p` |

### 示例

```json
{
    "areaCode": "us",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "l_cu_p"
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
            "date": "2026-03-18T00:00:00-04:00",
            "areaCode": "us",
            "l_cu_p": 12503
        },
        {
            "date": "2026-03-17T00:00:00-04:00",
            "areaCode": "us",
            "l_cu_p": 12677
        },
        {
            "date": "2026-03-16T00:00:00-04:00",
            "areaCode": "us",
            "l_cu_p": 12759.5
        }
    ]
}
```
