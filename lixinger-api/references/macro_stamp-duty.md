# API文档/宏观/印花税

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/stamp-duty
> API Key: `macro/stamp-duty`

---

## 印花税API

**简要描述:** 获取印花税数据，如沪市A股印花税等。

**请求URL:** `https://open.lixinger.com/api/macro/stamp-duty`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/stamp-duty](https://www.lixinger.com/api/open-api/html-doc/macro/stamp-duty)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组。如['sdsha']。 沪市A股印花税 : `sdsha`; 沪市B股印花税 : `sdshb`; 深市A股印花税 : `sdsza`; 深市B股印花税 : `sdszb` |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "sdsha"
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
            "sdsha": 7476995500
        },
        {
            "date": "2023-07-31T00:00:00+08:00",
            "areaCode": "cn",
            "sdsha": 7398616900
        },
        {
            "date": "2023-06-30T00:00:00+08:00",
            "areaCode": "cn",
            "sdsha": 7842439300
        }
    ]
}
```
