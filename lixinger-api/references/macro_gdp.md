# API文档/宏观/GDP

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/gdp
> API Key: `macro/gdp`

---

## Gdp API

**简要描述:** 获取GDP数据，如GDP等。

**请求URL:** `https://open.lixinger.com/api/macro/gdp`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/gdp](https://www.lixinger.com/api/open-api/html-doc/macro/gdp)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn`; 美国: `us` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['q.gdp.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 大陆支持: GDP : `gdp` q(季度): t(累积)t_y2y(累积同比)c(当期)c_c2c(当期环比); 不变价GDP : `gdp_cp` q(季度): t(累积)c(当期); 人均GDP : `per_gdp` q(季度): t(累积)t_y2y(累积同比); 第一产业GDP : `pi_gdp` q(季度): t(累积)t_y2y(累积同比)c(当期)c_c2c(当期环比); 第二产业GDP : `si_gdp` q(季度): t(累积)t_y2y(累积同比)c(当期)c_c2c(当期环比); 第三产业GDP : `ti_gdp` q(季度): t(累积)t_y2y(累积同比)c(当期)c_c2c(当期环比); 第一产业对GDP贡献率 : `pi_gdp_c_r` q(季度): t(累积)c(当期); 第二产业对GDP贡献率 : `si_gdp_c_r` q(季度): t(累积)c(当期); 第三产业对GDP贡献率 : `ti_gdp_c_r` q(季度): t(累积) q(季度): t(累积)c(当期); GNI : `gni` q(季度): t(累积)t_y2y(累积同比) 美国支持: GDP : `gdp` q(季度): t(累积)t_c2c(累积环比)t_y2y(累积同比) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "q.gdp.t"
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
            "q": {
                "gdp": {
                    "t": 140187920000000
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2025-09-30T00:00:00+08:00",
            "q": {
                "gdp": {
                    "t": 101396790000000
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2025-06-30T00:00:00+08:00",
            "q": {
                "gdp": {
                    "t": 65986160000000
                }
            }
        }
    ]
}
```
