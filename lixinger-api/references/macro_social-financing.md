# API文档/宏观/社会融资

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/social-financing
> API Key: `macro/social-financing`

---

## 社会融资API

**简要描述:** 获取社会融资数据，如社会融资等。

**请求URL:** `https://open.lixinger.com/api/macro/social-financing`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/social-financing](https://www.lixinger.com/api/open-api/html-doc/macro/social-financing)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['m.sf.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 大陆支持: 社会融资 : `sf` m(月): t(累积)t_y2y(累积同比); 人民币贷款 : `sf_rmbl` m(月): t(累积)t_y2y(累积同比); 外币贷款 : `sf_fl` m(月): t(累积)t_y2y(累积同比); 委托贷款 : `sf_el` m(月): t(累积)t_y2y(累积同比); 信托贷款 : `sf_tl` m(月): t(累积)t_y2y(累积同比); 未贴现银行承兑汇票 : `sf_ubc` m(月): t(累积)t_y2y(累积同比); 企业债券 : `sf_nf_cb` m(月): t(累积)t_y2y(累积同比); 政府债券 : `sf_gb` m(月): t(累积)t_y2y(累积同比); 非金融企业境内股票 : `sf_nfef_dsm` m(月): t(累积)t_y2y(累积同比); 存款类金融机构资产支持证券 : `sf_abs_dfi` m(月): t(累积)t_y2y(累积同比); 贷款核销 : `sf_lwo` m(月): t(累积)t_y2y(累积同比) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.sf.t"
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
                "sf": {
                    "t": 451400000000000
                }
            }
        },
        {
            "date": "2026-01-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "sf": {
                    "t": 449110000000000
                }
            }
        },
        {
            "date": "2025-12-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "sf": {
                    "t": 442120000000000
                }
            }
        }
    ]
}
```
