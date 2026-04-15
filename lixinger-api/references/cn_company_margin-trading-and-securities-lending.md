# API文档/大陆/公司接口/资金流向/融资融券

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/margin-trading-and-securities-lending
> API Key: `cn/company/margin-trading-and-securities-lending`

---

## 融资融券API

**简要描述:** 获取融资融券数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/margin-trading-and-securities-lending`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/margin-trading-and-securities-lending](https://www.lixinger.com/api/open-api/html-doc/cn/company/margin-trading-and-securities-lending)

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
| financingPurchaseAmount | Number | 融资买入金额 |
| financingRepaymentAmount | Number | 融资偿还金额 |
| financingBalance | Number | 融资余额 |
| securitiesSellVolume | Number | 融券卖出量 |
| securitiesRepaymentVolume | Number | 融券偿还量 |
| securitiesSellAmount | Number | 融券卖出金额 |
| securitiesRepaymentAmount | Number | 融券偿还金额 |
| securitiesBalance | Number | 融券余额 |
| securitiesMargin | Number | 融券余量 |
| financingSecuritiesBalance | Number | 融资融券余额 |

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
            "date": "2026-03-19T00:00:00+08:00",
            "financingPurchaseAmount": 841076743,
            "financingBalance": 20552054529,
            "securitiesSellVolume": 17400,
            "securitiesMargin": 242672,
            "securitiesBalance": 97190136,
            "financingSecuritiesBalance": 20649244665,
            "securitiesSellAmount": 6968700,
            "securitiesRepaymentAmount": 2593725,
            "financingRepaymentAmount": 898667302,
            "financingNetPurchaseAmount": -57590559,
            "securitiesNetSellAmount": 4374975
        },
        {
            "date": "2026-03-18T00:00:00+08:00",
            "financingPurchaseAmount": 638476809,
            "financingBalance": 20609645088,
            "securitiesSellVolume": 8400,
            "securitiesMargin": 230872,
            "securitiesBalance": 92815161,
            "financingSecuritiesBalance": 20702460249,
            "securitiesSellAmount": 3376968,
            "securitiesRepaymentAmount": 7183467,
            "financingRepaymentAmount": 676439173,
            "financingNetPurchaseAmount": -37962364,
            "securitiesNetSellAmount": -3806499
        },
        {
            "date": "2026-03-17T00:00:00+08:00",
            "financingPurchaseAmount": 1024228166,
            "financingBalance": 20647607452,
            "securitiesSellVolume": 20500,
            "securitiesMargin": 238572,
            "securitiesBalance": 96621660,
            "financingSecuritiesBalance": 20744229112,
            "securitiesSellAmount": 8302500,
            "securitiesRepaymentAmount": 2987645,
            "financingRepaymentAmount": 1196883358,
            "financingNetPurchaseAmount": -172655192,
            "securitiesNetSellAmount": 5314855
        }
    ]
}
```
