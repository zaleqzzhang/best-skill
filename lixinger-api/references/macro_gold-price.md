# API文档/宏观/大宗商品/黄金

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/gold-price
> API Key: `macro/gold-price`

---

## 黄金API

**简要描述:** 获取黄金数据，如上海金价格等。

**请求URL:** `https://open.lixinger.com/api/macro/gold-price`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/gold-price](https://www.lixinger.com/api/open-api/html-doc/macro/gold-price)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn`; 美国: `us` |
| metricsList | Yes | Array | 指标数组。如['sge_pm_cny']。 大陆支持: 上海金价格 : `sge_pm_cny` 美国支持: 伦敦金价格 : `lbma_pm_usd` |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "sge_pm_cny"
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
            "date": "2026-03-19T00:00:00+08:00",
            "sge_pm_cny": 1061.35,
            "areaCode": "cn"
        },
        {
            "date": "2026-03-18T00:00:00+08:00",
            "sge_pm_cny": 1112.41,
            "areaCode": "cn"
        },
        {
            "date": "2026-03-17T00:00:00+08:00",
            "sge_pm_cny": 1114.86,
            "areaCode": "cn"
        }
    ]
}
```
