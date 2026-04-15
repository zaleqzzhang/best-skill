# API文档/美国/指数接口/K线数据

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/us/index/candlestick
> API Key: `us/index/candlestick`

---

## K线数据API

**简要描述:** 获取K线数据。

**说明:**

- 中证指数全收益率2016年以前没有数据。

**请求URL:** `https://open.lixinger.com/api/us/index/candlestick`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/us/index/candlestick](https://www.lixinger.com/api/open-api/html-doc/us/index/candlestick)

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
    "stockCode": ".INX",
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
            "open": 6583.12,
            "close": 6606.49,
            "high": 6636.74,
            "low": 6557.82,
            "volume": 3244958242
        },
        {
            "date": "2026-03-18T00:00:00-04:00",
            "open": 6697.16,
            "close": 6624.7,
            "high": 6705.18,
            "low": 6621.66,
            "volume": 3009753418
        },
        {
            "date": "2026-03-17T00:00:00-04:00",
            "open": 6722.35,
            "close": 6716.09,
            "high": 6754.3,
            "low": 6710.8,
            "volume": 2900989570
        }
    ]
}
```
