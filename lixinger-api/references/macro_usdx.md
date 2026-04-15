# API文档/宏观/美元指数

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/usdx
> API Key: `macro/usdx`

---

## 美元指数API

**简要描述:** 获取美元指数数据

**请求URL:** `https://open.lixinger.com/api/macro/usdx`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/usdx](https://www.lixinger.com/api/open-api/html-doc/macro/usdx)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |

### 示例

```json
{
    "startDate": "2026-03-13",
    "endDate": "2026-03-20",
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
            "date": "2026-03-19T04:00:00.000Z",
            "open": 100.1767,
            "low": 98.9719,
            "high": 100.3042,
            "close": 99.2317
        },
        {
            "date": "2026-03-18T04:00:00.000Z",
            "open": 99.5682,
            "low": 99.4654,
            "high": 100.31,
            "close": 100.1776
        },
        {
            "date": "2026-03-17T04:00:00.000Z",
            "open": 99.7956,
            "low": 99.504,
            "high": 100.1107,
            "close": 99.5642
        }
    ]
}
```
