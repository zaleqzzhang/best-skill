# API文档/宏观/信用证券账户

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/credit-securities-account
> API Key: `macro/credit-securities-account`

---

## 信用证券账户API

**简要描述:** 获取信用证券账户数据，如新增信用证券账户等。

**请求URL:** `https://open.lixinger.com/api/macro/credit-securities-account`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/credit-securities-account](https://www.lixinger.com/api/open-api/html-doc/macro/credit-securities-account)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组。如['ncsa']。 新增信用证券账户 : `ncsa`; 新增个人信用证券账户 : `nisca`; 新增机构信用证券账户 : `nosca`; 新销信用证券账户 : `dcsa`; 新销个人信用证券账户 : `disca`; 新销机构信用证券账户 : `dosca`; 信用证券账户 : `csa`; 个人信用证券账户 : `isca`; 机构信用证券账户 : `osca` |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "ncsa"
    ],
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
            "date": "2023-08-31T00:00:00+08:00",
            "areaCode": "cn",
            "ncsa": 36300
        },
        {
            "date": "2023-07-31T00:00:00+08:00",
            "areaCode": "cn",
            "ncsa": 28600
        },
        {
            "date": "2023-06-30T00:00:00+08:00",
            "areaCode": "cn",
            "ncsa": 38000
        }
    ]
}
```
