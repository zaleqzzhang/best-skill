# API文档/大陆/基金接口/公募基金接口/场内基金收盘价

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/fund/exchange-traded-close-price
> API Key: `cn/fund/exchange-traded-close-price`

---

## 场内基金收盘价API

**简要描述:** 场内基金收盘价数据。

**请求URL:** `https://open.lixinger.com/api/cn/fund/exchange-traded-close-price`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund/exchange-traded-close-price](https://www.lixinger.com/api/open-api/html-doc/cn/fund/exchange-traded-close-price)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考基金信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| date | Date | 数据时间 |
| open | Number | 开盘价 |
| close | Number | 收盘价 |
| low | Number | 最低价 |
| high | Number | 最高价 |

### 示例

```json
{
    "startDate": "2025-03-20",
    "endDate": "2026-03-20",
    "stockCode": "161725",
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
            "open": 0.662,
            "close": 0.657,
            "high": 0.664,
            "low": 0.656
        },
        {
            "date": "2026-03-18T00:00:00+08:00",
            "open": 0.674,
            "close": 0.667,
            "high": 0.675,
            "low": 0.665
        },
        {
            "date": "2026-03-17T00:00:00+08:00",
            "open": 0.674,
            "close": 0.674,
            "high": 0.682,
            "low": 0.67
        }
    ]
}
```
