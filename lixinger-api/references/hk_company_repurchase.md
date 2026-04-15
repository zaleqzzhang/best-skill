# API文档/香港/公司接口/回购

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/company/repurchase
> API Key: `hk/company/repurchase`

---

## 回购API

**简要描述:** 获取回购数据。

**说明:**

- 计算股本为总H股

**请求URL:** `https://open.lixinger.com/api/hk/company/repurchase`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/company/repurchase](https://www.lixinger.com/api/open-api/html-doc/hk/company/repurchase)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考股票信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| methodOfRepurchase | String | 回购方式 |
| highestPrice | Number | 最高价 |
| lowestPrice | Number | 最低价 |
| avgPrice | Number | 成交均价 |
| num | Number | 回购股数 |
| totalPaid | Number | 总金额 |
| numPurchasedInYearSinceResolution | Number | 本年内至今（自决议案通过以来）在交易所购回的股数 |
| ratioPurchasedSinceResolution | Number | 自决议通过以来回购股数占通过决议时股本百分比 |

### 示例

```json
{
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
            "date": "2026-01-15T00:00:00+08:00",
            "num": 1017000,
            "highestPrice": 632,
            "lowestPrice": 619,
            "totalPaid": 635630186.7,
            "methodOfPurchase": "exchange",
            "numPurchasedInYearSinceResolution": 112206000,
            "ratioPurchasedSinceResolution": 0.01221,
            "avgPrice": 625.0051000000001,
            "stockCode": "00700"
        },
        {
            "date": "2026-01-14T00:00:00+08:00",
            "num": 1006000,
            "highestPrice": 638,
            "lowestPrice": 626,
            "totalPaid": 635964629.6,
            "methodOfPurchase": "exchange",
            "numPurchasedInYearSinceResolution": 111189000,
            "ratioPurchasedSinceResolution": 0.0121,
            "avgPrice": 632.1716,
            "stockCode": "00700"
        },
        {
            "date": "2026-01-13T00:00:00+08:00",
            "num": 1012000,
            "highestPrice": 638,
            "lowestPrice": 623,
            "totalPaid": 635956789.6,
            "methodOfPurchase": "exchange",
            "numPurchasedInYearSinceResolution": 110183000,
            "ratioPurchasedSinceResolution": 0.01199,
            "avgPrice": 628.4158,
            "stockCode": "00700"
        }
    ]
}
```
