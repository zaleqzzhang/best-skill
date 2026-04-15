# API文档/大陆/公司接口/资金流向/互联互通

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/mutual-market
> API Key: `cn/company/mutual-market`

---

## 互联互通API

**简要描述:** 获取互联互通数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/mutual-market`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/mutual-market](https://www.lixinger.com/api/open-api/html-doc/cn/company/mutual-market)

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
| shareholdings | Number | 持股数量 |

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
            "shareholdings": 692541784
        },
        {
            "date": "2025-09-30T00:00:00+08:00",
            "shareholdings": 660844057
        },
        {
            "date": "2025-06-30T00:00:00+08:00",
            "shareholdings": 606921205
        }
    ]
}
```
