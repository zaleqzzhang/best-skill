# API文档/大陆/指数接口/K线数据

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/index/candlestick
> API Key: `cn/index/candlestick`

---

## K线数据API

**简要描述:** 获取K线数据。

**说明:**

- 中证指数全收益率2016年以前没有数据。

**请求URL:** `https://open.lixinger.com/api/cn/index/candlestick`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/index/candlestick](https://www.lixinger.com/api/open-api/html-doc/cn/index/candlestick)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考指数信息API获取合法的stockCode。 stockCode仅在请求数据为date range的情况下生效。 |
| type | Yes | String | 收盘点位类型，例如，“normal”。 **当前支持:** 正常点位 : `normal` 全收益率点位 : `total_return` |
| date | No | String: YYYY-MM-DD (北京时间) | 信息日期。 用于获取指定日期数据。 |
| startDate | No | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| date | Date | 数据时间 |
| open | Number | 开盘价 |
| close | Number | 收盘价 |
| high | Number | 最高价 |
| low | Number | 最低价 |
| volume | Number | 成交量 |
| amount | Number | 金额 |
| change | Number | 涨跌幅 |

### 示例

```json
{
    "type": "normal",
    "startDate": "2025-03-20",
    "endDate": "2026-03-20",
    "stockCode": "000016",
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
            "volume": 6707944100,
            "open": 2933.58,
            "high": 2942.46,
            "low": 2908.44,
            "close": 2916.23,
            "change": -0.015300000000000001,
            "amount": 136419483407
        },
        {
            "date": "2026-03-18T00:00:00+08:00",
            "volume": 5441380000,
            "open": 2965.86,
            "high": 2970.19,
            "low": 2939.75,
            "close": 2961.43,
            "change": -0.0007,
            "amount": 113722000000
        },
        {
            "date": "2026-03-17T00:00:00+08:00",
            "volume": 6260500000,
            "open": 2957.01,
            "high": 2995.23,
            "low": 2956.16,
            "close": 2963.58,
            "change": 0.0032,
            "amount": 132384000000
        }
    ]
}
```
