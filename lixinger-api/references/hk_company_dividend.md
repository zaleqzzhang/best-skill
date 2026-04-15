# API文档/香港/公司接口/分红送配/分红

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/company/dividend
> API Key: `hk/company/dividend`

---

## 分红API

**简要描述:** 获取分红信息。

**请求URL:** `https://open.lixinger.com/api/hk/company/dividend`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/company/dividend](https://www.lixinger.com/api/open-api/html-doc/hk/company/dividend)

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
| dividendAmount | Number | 分红金额（港币） |
| annualNetProfit | Number | 年度净利润（港币） |
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
            "date": "2026-03-18T00:00:00+08:00",
            "fsEndDate": "2025-12-31T00:00:00+08:00",
            "content": "末期息HKD 5.30",
            "currency": "HKD",
            "exDate": "2026-05-15T00:00:00+08:00",
            "paymentDate": "2026-06-01T00:00:00+08:00",
            "dividend": 5.3,
            "dividendAmount": 48263687462.5,
            "annualNetProfit": 250170451300,
            "annualNetProfitDividendRatio": 0.1929
        },
        {
            "date": "2025-11-13T00:00:00+08:00",
            "fsEndDate": "2025-12-31T00:00:00+08:00",
            "content": "无股息截至期末2025/09/30",
            "dividend": 0
        },
        {
            "date": "2025-08-13T00:00:00+08:00",
            "fsEndDate": "2025-12-31T00:00:00+08:00",
            "content": "无股息截至期末2025/06/30",
            "dividend": 0
        }
    ]
}
```
