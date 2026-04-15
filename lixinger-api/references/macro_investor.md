# API文档/宏观/投资者

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/investor
> API Key: `macro/investor`

---

## 投资者API

**简要描述:** 获取投资者数据，如自然人等。

**请求URL:** `https://open.lixinger.com/api/macro/investor`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/investor](https://www.lixinger.com/api/open-api/html-doc/macro/investor)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| granularity | Yes | String | 数据统计维度 **当前支持:** 月度数据: m。 `该数据只有在2015年3月后有数据。`; 周数据: w。 `该数据只在2020年4月之间有数据。` |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组。如['ni']。 新增自然人 : `nni`; 新增非自然人 : `n_non_ni`; 自然人 : `ni`; A股自然人 : `nia`; B股自然人 : `nib`; 非自然人 : `non_ni`; A股非自然人 : `non_nia`; B股非自然人 : `non_nib` |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "granularity": "m",
    "metricsList": [
        "ni"
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
            "date": "2026-02-28T00:00:00+08:00",
            "areaCode": "cn",
            "ni": 405282872
        },
        {
            "date": "2026-01-31T00:00:00+08:00",
            "areaCode": "cn",
            "ni": 402766437
        },
        {
            "date": "2025-12-31T00:00:00+08:00",
            "areaCode": "cn",
            "ni": 397860649
        }
    ]
}
```
