# API文档/大陆/公司接口/分红送配/分红

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/dividend
> API Key: `cn/company/dividend`

---

## 分红API

**简要描述:** 获取分红信息。

**请求URL:** `https://open.lixinger.com/api/cn/company/dividend`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/dividend](https://www.lixinger.com/api/open-api/html-doc/cn/company/dividend)

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
| date | Date | 公告日期 |
| content | String | 内容 |
| bonusSharesFromProfit | Number | 送股(股) |
| bonusSharesFromCapitalReserve | Number | 转增(股) |
| dividend | Number | 分红 |
| currency | String | 货币 |
| dividendAmount | Number | 分红金额 |
| annualNetProfit | Number | 年度净利润 |
| annualNetProfitDividendRatio | Number | 年度净利润分红比例 |
| registerDate | Date | 股权登记日 |
| exDate | Date | 除权除息日 |
| paymentDate | Date | 分红到账日 |
| fsEndDate | Date | 财报时间 |

### 示例

```json
{
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
            "date": "2026-03-10T00:00:00+08:00",
            "fsEndDate": "2025-12-31T00:00:00+08:00",
            "currency": "CNY",
            "bonusSharesFromProfit": 0,
            "bonusSharesFromCapitalReserve": 0,
            "dividend": 2.178
        },
        {
            "date": "2026-03-10T00:00:00+08:00",
            "fsEndDate": "2025-12-31T00:00:00+08:00",
            "currency": "CNY",
            "bonusSharesFromProfit": 0,
            "bonusSharesFromCapitalReserve": 0,
            "dividend": 4.779
        },
        {
            "date": "2025-07-31T00:00:00+08:00",
            "fsEndDate": "2025-06-30T00:00:00+08:00",
            "currency": "CNY",
            "registerDate": "2025-08-19T00:00:00+08:00",
            "exDate": "2025-08-20T00:00:00+08:00",
            "paymentDate": "2025-08-20T00:00:00+08:00",
            "bonusSharesFromProfit": 0,
            "bonusSharesFromCapitalReserve": 0,
            "dividend": 1.007,
            "dividendAmount": 4411427859
        }
    ]
}
```
