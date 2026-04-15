# API文档/大陆/行业接口/国证/资金流向/互联互通

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/industry/mutual-market/cni
> API Key: `cn/industry/mutual-market/cni`

---

## 互联互通API

**简要描述:** 获取互联互通数据。

**请求URL:** `https://open.lixinger.com/api/cn/industry/mutual-market/cni`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/industry/mutual-market/cni](https://www.lixinger.com/api/open-api/html-doc/cn/industry/mutual-market/cni)

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
| shareholdingsMoney | Number | 持股金额 |
| shareholdingsMoneyToMarketCap | Number | 港资持仓金额占市值比例 |

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
            "date": "2025-12-31T00:00:00+08:00",
            "shareholdingsMoney": 303542752638,
            "shareholdingsMoneyToMarketCap": 0.012768915063650773
        },
        {
            "date": "2025-09-30T00:00:00+08:00",
            "shareholdingsMoney": 304586428302,
            "shareholdingsMoneyToMarketCap": 0.013685206935582598
        },
        {
            "date": "2025-06-30T00:00:00+08:00",
            "shareholdingsMoney": 409942718931,
            "shareholdingsMoneyToMarketCap": 0.017959396039961422
        }
    ]
}
```
