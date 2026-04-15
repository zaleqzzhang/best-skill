# API文档/宏观/价格指数

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/price-index
> API Key: `macro/price-index`

---

## 价格指数API

**简要描述:** 获取价格指数数据，如居民消费价格指数(CPI)等。

**请求URL:** `https://open.lixinger.com/api/macro/price-index`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/price-index](https://www.lixinger.com/api/open-api/html-doc/macro/price-index)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn`; 美国: `us` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['m.cpi.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 大陆支持: 居民消费价格指数(CPI) : `cpi` m(月): t(累积); 核心居民消费价格指数(CCPI) : `ccpi` m(月): t(累积); 城市居民消费价格指数 : `ucpi` m(月): t(累积); 农村居民消费价格指数 : `rcpi` m(月): t(累积); 居民消费水平 : `hci` m(月): t(累积)t_y2y(累积同比); 农村居民消费水平 : `rrci` m(月): t(累积)t_y2y(累积同比); 城镇居民消费水平 : `urci` m(月): t(累积)t_y2y(累积同比); 工业品出厂价格指数(PPI) : `ppi` m(月): t(累积); 工业生产者购进价格指数(PPPI) : `pppi` m(月): t(累积); 制造业采购经理指数 : `mi_pmi` m(月): t(累积); 非制造业采购经理指数 : `n_mi_pmi` m(月): t(累积); 综合采购经理指数 : `c_pmi` m(月): t(累积) 美国支持: 美国-所有城市消费者的消费物价指数：美国城市平均所有项目（季调） : `cpiaucsl` m(月): t(累积)t_y2y(累积同比)t_c2c(累积环比); 生产者价格指数按商品分类：最终需求 : `ppifis` m(月): t(累积)t_y2y(累积同比); 制造业采购经理指数 : `mi_pmi` m(月): t(累积) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.cpi.t"
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
            "date": "2026-02-28T00:00:00+08:00",
            "m": {
                "cpi": {
                    "t": 0.008
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2026-01-31T00:00:00+08:00",
            "m": {
                "cpi": {
                    "t": 0.002
                }
            }
        },
        {
            "areaCode": "cn",
            "date": "2025-12-31T00:00:00+08:00",
            "m": {
                "cpi": {
                    "t": 0.008
                }
            }
        }
    ]
}
```
