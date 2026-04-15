# API文档/宏观/国外资产

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/foreign-assets
> API Key: `macro/foreign-assets`

---

## 国外资产

**简要描述:** 获取国外资产数据，如外汇等。

**请求URL:** `https://open.lixinger.com/api/macro/foreign-assets`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/foreign-assets](https://www.lixinger.com/api/open-api/html-doc/macro/foreign-assets)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组。如['f_e']。 外汇 : `f_e` m(月): t(累积); 货币黄金 : `m_g` m(月): t(累积); 其他国外资产 : `o_f_a` m(月): t(累积) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.f_e.t"
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
            "m": {
                "f_e": {
                    "t": 21376392000000
                }
            }
        },
        {
            "date": "2026-01-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "f_e": {
                    "t": 21292261000000
                }
            }
        },
        {
            "date": "2025-12-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "f_e": {
                    "t": 21239123000000
                }
            }
        }
    ]
}
```
