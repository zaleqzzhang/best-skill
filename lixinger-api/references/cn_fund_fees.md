# API文档/大陆/基金接口/公募基金接口/费用

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/fund/fees
> API Key: `cn/fund/fees`

---

## 费用API

**简要描述:** 获取费用API

**请求URL:** `https://open.lixinger.com/api/cn/fund/fees`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund/fees](https://www.lixinger.com/api/open-api/html-doc/cn/fund/fees)

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
| date | Date | 公告日期 |
| m_f_r | Number | 管理报酬费用率 |
| m_f | Number | 管理报酬 |
| c_f_r | Number | 托管费用率 |
| c_f | Number | 托管费用 |

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
            "date": "2025-06-30T00:00:00+08:00",
            "m_f": 207705586,
            "m_f_r": 0.01,
            "c_f": 41541117,
            "c_f_r": 0.002,
            "declarationDate": "2025-08-28T00:00:00+08:00"
        },
        {
            "date": "2025-05-26T00:00:00+08:00",
            "declarationDate": "2025-05-26T00:00:00+08:00",
            "m_f_r": 0.01,
            "c_f_r": 0.002
        },
        {
            "date": "2025-03-21T00:00:00+08:00",
            "declarationDate": "2025-03-21T00:00:00+08:00",
            "m_f_r": 0.01,
            "c_f_r": 0.002
        }
    ]
}
```
