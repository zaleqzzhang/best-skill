# API文档/宏观/全社会固定资产投资

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/investment-in-fixed-assets
> API Key: `macro/investment-in-fixed-assets`

---

## 全社会固定资产投资API

**简要描述:** 获取全社会固定资产投资数据，如固定资产投资(不含农户)等。

**请求URL:** `https://open.lixinger.com/api/macro/investment-in-fixed-assets`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/investment-in-fixed-assets](https://www.lixinger.com/api/open-api/html-doc/macro/investment-in-fixed-assets)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['m.fai_ef.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 大陆支持: 固定资产投资(不含农户) : `fai_ef` m(月): t(累积); 固定资产投资额累计增长(不含农户) : `cg_o_fai_ef` m(月): t(累积) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.fai_ef.t"
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
            "areaCode": "cn",
            "date": "2025-12-31T00:00:00+08:00",
            "m": {
                "fai_ef": {
                    "t": 48518600000000
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2024-12-31T00:00:00+08:00",
            "m": {
                "fai_ef": {
                    "t": 51437396060000
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2023-12-31T00:00:00+08:00",
            "m": {
                "fai_ef": {
                    "t": 49839396210000
                }
            }
        }
    ]
}
```
