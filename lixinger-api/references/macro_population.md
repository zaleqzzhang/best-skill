# API文档/宏观/人口

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/population
> API Key: `macro/population`

---

## 人口API

**简要描述:** 获取人口数据，如总人口等。

**请求URL:** `https://open.lixinger.com/api/macro/population`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/population](https://www.lixinger.com/api/open-api/html-doc/macro/population)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['y.tp.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 大陆支持: 总人口 : `tp` y(年): t(累积); 男性总人口 : `tmp` y(年): t(累积); 女性总人口 : `tfp` y(年): t(累积); 人口增长率 : `pb_r` y(年): t(累积); 人口死亡率 : `pm_r` y(年): t(累积); 人口自然增长率 : `png_r` y(年): t(累积); 0至14岁总人口 : `tp_a_0_14` y(年): t(累积); 15至64岁总人口 : `tp_a_15_64` y(年): t(累积); 65岁以上总人口 : `tp_a_65` y(年): t(累积); 少儿抚养比 : `cr_r` y(年): t(累积); 老年抚养比 : `or_r` y(年): t(累积) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "y.tp.t"
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
            "y": {
                "tp": {
                    "t": 1404890000
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2024-12-31T00:00:00+08:00",
            "y": {
                "tp": {
                    "t": 1408280000
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2023-12-31T00:00:00+08:00",
            "y": {
                "tp": {
                    "t": 1409670000
                }
            }
        }
    ]
}
```
