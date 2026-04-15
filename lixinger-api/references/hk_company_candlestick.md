# API文档/香港/公司接口/K线数据

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/company/candlestick
> API Key: `hk/company/candlestick`

---

## K线数据API

**简要描述:** 获取K线数据。

**说明:**

- 复权计算仅对所选时间段的价格进行复权
- 成交量不进行复权计算

**请求URL:** `https://open.lixinger.com/api/hk/company/candlestick`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/company/candlestick](https://www.lixinger.com/api/open-api/html-doc/hk/company/candlestick)

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

### 示例

```json
{
    "type": "lxr_fc_rights",
    "startDate": "2025-03-20",
    "endDate": "2026-03-20",
    "stockCode": "00700",
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
            "open": 528,
            "close": 513,
            "high": 529.5,
            "low": 512,
            "volume": 59432770,
            "amount": 30817089730,
            "change": -0.0681,
            "stockCode": "00700",
            "to_r": 0.006527
        },
        {
            "date": "2026-03-18T00:00:00+08:00",
            "open": 546.5,
            "close": 550.5,
            "high": 552,
            "low": 542.5,
            "volume": 21350876,
            "amount": 11686255183,
            "change": 0.0009,
            "stockCode": "00700",
            "to_r": 0.002345
        },
        {
            "date": "2026-03-17T00:00:00+08:00",
            "open": 563,
            "close": 550,
            "high": 566,
            "low": 549,
            "volume": 22872974,
            "amount": 12710928714,
            "change": -0.0152,
            "stockCode": "00700",
            "to_r": 0.002512
        }
    ]
}
```
