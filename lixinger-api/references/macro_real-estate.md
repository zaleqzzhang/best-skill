# API文档/宏观/房地产

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/real-estate
> API Key: `macro/real-estate`

---

## 房地产API

**简要描述:** 获取房地产数据，如房地产投资额等。

**请求URL:** `https://open.lixinger.com/api/macro/real-estate`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/real-estate](https://www.lixinger.com/api/open-api/html-doc/macro/real-estate)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['m.rei.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 大陆支持: 房地产投资额 : `rei` m(月): t(累积)t_y2y(累积同比); 房地产施工面积 : `re_ca` m(月): t(累积)t_y2y(累积同比); 房地产新开工施工面积 : `nsca_i_re` m(月): t(累积)t_y2y(累积同比); 房地产竣工面积 : `ca_o_re` m(月): t(累积)t_y2y(累积同比); 购置土地面积 : `l_pa` m(月): t(累积)t_y2y(累积同比); 土地成交价款 : `l_tr` m(月): t(累积)t_y2y(累积同比); 商品房销售面积 : `sa_o_ch` m(月): t(累积)t_y2y(累积同比); 商品房销售额 : `st_o_ch` m(月): t(累积)t_y2y(累积同比); 商品住宅房销售面积 : `sa_o_crb` m(月): t(累积)t_y2y(累积同比); 商品住宅房销售额 : `st_o_crb` m(月): t(累积)t_y2y(累积同比) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.rei.t"
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
                "rei": {
                    "t": 8278814000000
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2025-11-30T00:00:00+08:00",
            "m": {
                "rei": {
                    "t": 7859089999999.999
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2025-10-31T00:00:00+08:00",
            "m": {
                "rei": {
                    "t": 7356270000000
                }
            }
        }
    ]
}
```
