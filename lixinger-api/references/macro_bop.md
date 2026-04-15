# API文档/宏观/国际收支平衡

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/bop
> API Key: `macro/bop`

---

## 国际收支平衡API

**简要描述:** 获取国际收支平衡数据，如资本账户差额等。

**请求URL:** `https://open.lixinger.com/api/macro/bop`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/bop](https://www.lixinger.com/api/open-api/html-doc/macro/bop)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。 如['m.bop_ca.t'] 指标参数示例: 指标名 : `metricsName` granularity(时间粒度):expressionCalculateType(数据统计方式): 大陆支持: 经常账户差额 : `bop_cura` q(季度): c(当期)t(累积); 货物于服务差额 : `bop_gas` q(季度): c(当期)t(累积); 货物差额 : `bop_g` q(季度): c(当期)t(累积); 服务差额 : `bop_s` q(季度): c(当期)t(累积); 初次收入差额 : `bop_firi` q(季度): c(当期)t(累积); 二次收入差额 : `bop_seci` q(季度): c(当期)t(累积); 资本与金融账户差额 : `bop_cafa` q(季度): c(当期)t(累积); 资本账户差额 : `bop_ca` q(季度): c(当期)t(累积); 金融账户差额 : `bop_fa` q(季度): c(当期)t(累积); 非储备性质金融账户差额 : `bop_nsfa` q(季度): c(当期)t(累积); 直接投资差额 : `bop_di` q(季度): c(当期)t(累积); 证券投资差额 : `bop_si` q(季度): c(当期)t(累积); 金融衍生工具差额 : `bop_nsfa_fd` q(季度): c(当期)t(累积); 其他投资差额 : `bop_nsfa_oi` q(季度): c(当期)t(累积); 储备资产差额 : `bop_ra` q(季度): c(当期)t(累积); 净误差与遗漏差额 : `bop_eao` q(季度): c(当期)t(累积) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.bop_ca.t"
    ],
    "token": "***********"
}
```

### 返回结果

```json
{
    "code": 1,
    "message": "success",
    "data": []
}
```
