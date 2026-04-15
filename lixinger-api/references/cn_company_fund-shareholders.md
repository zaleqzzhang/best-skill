# API文档/大陆/公司接口/股东/公募基金持股

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/fund-shareholders
> API Key: `cn/company/fund-shareholders`

---

## 公募基金持股API

**简要描述:** 获取公募基金持股信息。

**请求URL:** `https://open.lixinger.com/api/cn/company/fund-shareholders`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/fund-shareholders](https://www.lixinger.com/api/open-api/html-doc/cn/company/fund-shareholders)

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
| date | Date | 数据时间 |
| fundCode | String | 基金代码 |
| name | String | 基金名称 |
| holdings | Number | 持仓 |
| marketCap | Number | 市值 |
| marketCapRank | Number | 当前股票所在基金持仓排名 |
| netValueRatio | Number | 基金持仓占基金规模比例 |
| outstandingSharesA | Number | 流通A股 |
| proportionOfCapitalization | Number | 流通A股占比 |

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
            "date": "2025-12-31T00:00:00+08:00",
            "holdings": 49005734,
            "marketCap": 17997845868,
            "netValueRatio": 0.1792,
            "marketCapRank": 1,
            "declarationDate": "2026-01-22T00:00:00+08:00",
            "fundCode": "159915",
            "name": "易方达创业板ETF",
            "outstandingSharesA": 4256573358,
            "proportionOfOutstandingSharesA": 0.0115
        },
        {
            "date": "2025-12-31T00:00:00+08:00",
            "holdings": 43712032,
            "marketCap": 16053680872,
            "netValueRatio": 0.038,
            "marketCapRank": 1,
            "declarationDate": "2026-01-22T00:00:00+08:00",
            "fundCode": "510300",
            "name": "华泰柏瑞沪深300ETF",
            "outstandingSharesA": 4256573358,
            "proportionOfOutstandingSharesA": 0.0103
        },
        {
            "date": "2025-12-31T00:00:00+08:00",
            "holdings": 31173566,
            "marketCap": 11448803849,
            "netValueRatio": 0.0381,
            "marketCapRank": 1,
            "declarationDate": "2026-01-22T00:00:00+08:00",
            "fundCode": "510310",
            "name": "易方达沪深300ETF",
            "outstandingSharesA": 4256573358,
            "proportionOfOutstandingSharesA": 0.0073
        }
    ]
}
```
