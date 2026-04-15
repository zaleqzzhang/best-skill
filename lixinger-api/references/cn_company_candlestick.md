# API文档/大陆/公司接口/K线数据

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/candlestick
> API Key: `cn/company/candlestick`

---

## K线数据API

**简要描述:** 获取K线数据。

**说明:**

- 复权计算仅对所选时间段的价格进行复权
- 成交量不进行复权计算

**请求URL:** `https://open.lixinger.com/api/cn/company/candlestick`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/candlestick](https://www.lixinger.com/api/open-api/html-doc/cn/company/candlestick)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考股票信息API获取合法的stockCode。 stockCode仅在请求数据为date range的情况下生效。 |
| type | No | String | 除复权类型， 例如， “lxr_fc_rights”。 **当前支持:** 不复权 : `ex_rights` 理杏仁前复权 : `lxr_fc_rights` 前复权 : `fc_rights` 后复权 : `bc_rights` |
| date | No | String: YYYY-MM-DD (北京时间) | 信息日期。 用于获取指定日期数据。 |
| startDate | No | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 |
| adjustForwardDate | No | String: YYYY-MM-DD (北京时间) | 前复权指定起始时间点。 需要注意的是，请与endDate一起使用且大于或等于endDate。 获取复权类型数据时要传入，不传时默认值是endDate。 |
| adjustBackwardDate | No | String: YYYY-MM-DD (北京时间) | 后复权指定起始时间点。 需要注意的是，请与startDate一起使用且小于或等于startDate。 获取复权类型数据时要传入，不传时默认值是startDate。 |
| limit | No | Number | 返回最近数据的数量。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 不同复权类型数据字段均相同 |
| --- | --- | --- |
| date | Date | 数据时间 |
| stockCode | String | 股票代码 |
| open | Number | 开盘价 |
| close | Number | 收盘价 |
| high | Number | 最高价 |
| low | Number | 最低价 |
| volume | Number | 成交量 |
| amount | Number | 金额 |
| change | Number | 涨跌幅 |
| to_r | Number | 换手率 |
| complexFactor | Number | 复权因子 |

### 示例

```json
{
    "type": "lxr_fc_rights",
    "startDate": "2025-03-20",
    "endDate": "2026-03-20",
    "stockCode": "300750",
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
            "open": 401.94,
            "close": 400.5,
            "high": 414,
            "low": 400,
            "volume": 29286600,
            "amount": 11867380765,
            "change": -0.0038,
            "stockCode": "300750",
            "to_r": 0.00688
        },
        {
            "date": "2026-03-18T00:00:00+08:00",
            "open": 405.36,
            "close": 402.02,
            "high": 406,
            "low": 396.77,
            "volume": 26530000,
            "amount": 10653633584,
            "change": -0.0074,
            "stockCode": "300750",
            "to_r": 0.006233
        },
        {
            "date": "2026-03-17T00:00:00+08:00",
            "open": 415.78,
            "close": 405,
            "high": 420,
            "low": 404.56,
            "volume": 35980700,
            "amount": 14787230790,
            "change": -0.0083,
            "stockCode": "300750",
            "to_r": 0.008453
        }
    ]
}
```
