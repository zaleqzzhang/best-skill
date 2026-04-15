# 基金持仓API

## 基金持仓API

**简要描述:** 获取基金持仓数据。

**说明:**

- 主基金代码和子基金代码获取相同的数据。

**请求URL:** `https://open.lixinger.com/api/cn/fund/shareholdings`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund/shareholdings](https://www.lixinger.com/api/open-api/html-doc/cn/fund/shareholdings)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考基金信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| date | Date | |
| stockCode | String | 持仓股票代码 |
| stockAreaCode | String | 股票地区代码 |
| holdings | Number | 持股数量 |
| marketCap | Number | 持仓市值 |
| netValueRatio | Number | 持仓占比 |

### 示例

```json
{
    "startDate": "2025-03-20",
    "endDate": "2026-03-20",
    "stockCode": "161725",
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
            "stockCode": "000568",
            "holdings": 53997775,
            "marketCap": 6275621410,
            "netValueRatio": 0.1453,
            "stockAreaCode": "cn"
        },
        {
            "date": "2025-12-31T00:00:00+08:00",
            "stockCode": "000596",
            "holdings": 16754467,
            "marketCap": 2221642324,
            "netValueRatio": 0.0514,
            "stockAreaCode": "cn"
        },
        {
            "date": "2025-12-31T00:00:00+08:00",
            "stockCode": "000858",
            "holdings": 59746139,
            "marketCap": 6329505965,
            "netValueRatio": 0.1465,
            "stockAreaCode": "cn"
        }
    ]
}
```
