# API文档/宏观/国内各类债券

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/domestic-debt-securities
> API Key: `macro/domestic-debt-securities`

---

## 国内各类债券API

**简要描述:** 获取国内各类债券数据，如政府债券发行金额等。

**请求URL:** `https://open.lixinger.com/api/macro/domestic-debt-securities`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/domestic-debt-securities](https://www.lixinger.com/api/open-api/html-doc/macro/domestic-debt-securities)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['m.gs_i.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 大陆支持: 政府债券发行金额 : `gs_i` m(月): c(当期); 金融债券发行金额 : `fb_i` m(月): c(当期); 公司信用类债券发行金额 : `cdb_i` m(月): c(当期); 国际机构债券发行金额 : `iib_i` m(月): c(当期); 政府债券累积余额 : `gs_o` m(月): t(累积); 金融债券累积余额 : `fb_o` m(月): t(累积); 公司信用类债券累积余额 : `cdb_o` m(月): t(累积); 国际机构债券累积余额 : `iib_o` m(月): t(累积) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.gs_i.t"
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
            "date": "2025-12-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "gs_i": {
                    "t": 26296400000000
                }
            }
        },
        {
            "date": "2024-12-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "gs_i": {
                    "t": 22245900000000
                }
            }
        },
        {
            "date": "2023-12-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "gs_i": {
                    "t": 20421000000000
                }
            }
        }
    ]
}
```
