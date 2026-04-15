# API文档/宏观/国债

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/national-debt
> API Key: `macro/national-debt`

---

## 国债API

**简要描述:** 获取国债数据，如十年期收益率等。

**请求URL:** `https://open.lixinger.com/api/macro/national-debt`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/national-debt](https://www.lixinger.com/api/open-api/html-doc/macro/national-debt)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn`; 美国: `us` |
| metricsList | Yes | Array | 指标数组。如['tcm_y10']。 大陆支持: 三月期收益率 : `tcm_m3`; 六月期收益率 : `tcm_m6`; 一年期收益率 : `tcm_y1`; 二年期收益率 : `tcm_y2`; 三年期收益率 : `tcm_y3`; 五年期收益率 : `tcm_y5`; 七年期收益率 : `tcm_y7`; 十年期收益率 : `tcm_y10`; 二十年期收益率 : `tcm_y20`; 三十年期收益率 : `tcm_y30` 美国支持: 三月期收益率 : `tcm_m3`; 六月期收益率 : `tcm_m6`; 一年期收益率 : `tcm_y1`; 二年期收益率 : `tcm_y2`; 三年期收益率 : `tcm_y3`; 五年期收益率 : `tcm_y5`; 七年期收益率 : `tcm_y7`; 十年期收益率 : `tcm_y10`; 二十年期收益率 : `tcm_y20`; 三十年期收益率 : `tcm_y30` |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "tcm_y10"
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
            "date": "2026-03-19T00:00:00+08:00",
            "areaCode": "cn",
            "tcm_y10": 0.018252
        },
        {
            "date": "2026-03-18T00:00:00+08:00",
            "areaCode": "cn",
            "tcm_y10": 0.018175
        },
        {
            "date": "2026-03-17T00:00:00+08:00",
            "areaCode": "cn",
            "tcm_y10": 0.018314
        }
    ]
}
```
