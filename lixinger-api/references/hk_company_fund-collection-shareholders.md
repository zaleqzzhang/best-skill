# API文档/香港/公司接口/股东/内资基金公司持股

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/company/fund-collection-shareholders
> API Key: `hk/company/fund-collection-shareholders`

---

## 内资基金公司持股API

**简要描述:** 获取内资基金公司持股信息。

**请求URL:** `https://open.lixinger.com/api/hk/company/fund-collection-shareholders`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/company/fund-collection-shareholders](https://www.lixinger.com/api/open-api/html-doc/hk/company/fund-collection-shareholders)

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
| marketCap | Number | 市值 |
| name | String | 姓名 |
| holdings | Number | 持仓 |
| fundCollectionCode | String | 基金公司代码 |

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
            "date": "2025-12-31T00:00:00+08:00",
            "marketCap": 202638538,
            "holdings": 374543,
            "name": "国泰基金管理有限公司",
            "fundCollectionCode": "50010000",
            "proportionOfOutstandingSharesA": null
        },
        {
            "date": "2025-12-31T00:00:00+08:00",
            "marketCap": 524538761,
            "holdings": 969521,
            "name": "国泰基金管理有限公司",
            "fundCollectionCode": "50010000",
            "proportionOfOutstandingSharesA": null
        },
        {
            "date": "2025-12-31T00:00:00+08:00",
            "marketCap": 727177299,
            "holdings": 1344064,
            "name": "国泰基金管理有限公司",
            "fundCollectionCode": "50010000",
            "proportionOfOutstandingSharesA": null
        }
    ]
}
```
