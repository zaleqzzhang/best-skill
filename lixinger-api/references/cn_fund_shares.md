# API文档/大陆/基金接口/公募基金接口/基金份额及规模

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/fund/shares
> API Key: `cn/fund/shares`

---

## 基金份额API

**简要描述:** 获取基金份额及规模数据。

**说明:**

- LOF基金和一些封闭式基金有场内份额和场外份额。

**请求URL:** `https://open.lixinger.com/api/cn/fund/shares`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund/shares](https://www.lixinger.com/api/open-api/html-doc/cn/fund/shares)

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
| date | Date | 数据时间 |
| s | Number | 基金份额 |
| as | Number | 基金规模 |
| et_shares | Number | 场内基金份额 |
| et_as | Number | 场内基金规模 |

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
            "date": "2026-03-19T00:00:00+08:00",
            "et_shares": 3303387622,
            "et_as": 2169995328.8918
        },
        {
            "date": "2026-03-18T00:00:00+08:00",
            "et_shares": 3299081720,
            "et_as": 2199497782.724
        },
        {
            "date": "2026-03-17T00:00:00+08:00",
            "et_shares": 3298758991,
            "et_as": 2225672691.2276998
        }
    ]
}
```
