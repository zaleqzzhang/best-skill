# API文档/大陆/行业接口/国证/资金流向/融资融券

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/industry/margin-trading-and-securities-lending/cni
> API Key: `cn/industry/margin-trading-and-securities-lending/cni`

---

## 融资融券API

**简要描述:** 获取融资融券数据。

**请求URL:** `https://open.lixinger.com/api/cn/industry/margin-trading-and-securities-lending/cni`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/industry/margin-trading-and-securities-lending/cni](https://www.lixinger.com/api/open-api/html-doc/cn/industry/margin-trading-and-securities-lending/cni)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考行业信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| date | Date | 数据时间 |
| financingBalance | Number | 融资余额 |
| securitiesBalance | Number | 融券余额 |
| financingBalanceToMarketCap | Number | 融资余额占流通市值比例 |
| securitiesBalanceToMarketCap | Number | 融券余额占流通市值比例 |

### 示例

```json
{
    "startDate": "2025-03-20",
    "endDate": "2026-03-20",
    "stockCode": "C07",
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
            "date": "2026-03-20T00:00:00+08:00",
            "financingBalanceToMarketCap": null,
            "securitiesBalanceToMarketCap": null
        },
        {
            "date": "2026-03-19T00:00:00+08:00",
            "financingBalance": 273316429536,
            "securitiesBalance": 603190594.2,
            "financingBalanceToMarketCap": 0.012129232155381782,
            "securitiesBalanceToMarketCap": 0.0000267683825791776
        },
        {
            "date": "2026-03-18T00:00:00+08:00",
            "financingBalance": 273565479126,
            "securitiesBalance": 597018192.4300001,
            "financingBalanceToMarketCap": 0.012132818060336713,
            "securitiesBalanceToMarketCap": 0.000026478169433534538
        }
    ]
}
```
