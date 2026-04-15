# API文档/大陆/基金接口/公募基金接口/基础信息

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/fund
> API Key: `cn/fund`

---

## 基金信息API

**简要描述:** 获取基金详细信息。

**说明:**

- 场内基金的exchange是 sz 或 sh。

**请求URL:** `https://open.lixinger.com/api/cn/fund`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund](https://www.lixinger.com/api/open-api/html-doc/cn/fund)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 基金代码数组。 默认值为所有基金的基金代码。格式如下：["161725","005827"]。 请参考 基金信息API 获取合法的stockCode。 |
| pageIndex | Yes | Number | 页面索引。 默认值是0。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| total | Number | 基金总数 |
| name | String | 基金名称 |
| stockCode | String | 基金代码 |
| fundFirstLevel | String | 基金一级类型，目前只有商品基金有这个类型。 互认基金 : `mutual_recognition` |
| fundSecondLevel | String | 基金类型 股票型 : `company`; 混合型 : `hybrid`; 债券型 : `bond`; QDII : `QDII`; REIT : `reit`; FOF : `fof`; 商品基金 : `commodity` |
| shortName | String | 简称 |
| areaCode | String | 地区代码 |
| market | String | 市场 |
| exchange | String | 交易所 |
| inceptionDate | Date | 合同生效日 |
| delistedDate | Date | 退市时间 |

### 示例

```json
{
    "pageIndex": 0,
    "token": "***********"
}
```

### 返回结果

```json
{
    "code": 1,
    "message": "success",
    "total": 28753,
    "data": [
        {
            "stockCode": "560210",
            "fundSecondLevel": "company",
            "areaCode": "cn",
            "market": "a",
            "exchange": "jj",
            "shortName": "景顺长城农牧渔ETF",
            "name": "景顺长城中证全指农牧渔交易型开放式指数证券投资基金",
            "inceptionDate": "2026-03-13T00:00:00+08:00"
        },
        {
            "stockCode": "026732",
            "fundSecondLevel": "hybrid",
            "areaCode": "cn",
            "market": "a",
            "exchange": "jj",
            "shortName": "广发成长甄选混合",
            "name": "广发成长甄选混合型证券投资基金",
            "inceptionDate": "2026-03-13T00:00:00+08:00"
        },
        {
            "stockCode": "026396",
            "fundSecondLevel": "hybrid",
            "areaCode": "cn",
            "market": "a",
            "exchange": "jj",
            "shortName": "鹏扬科技先锋混合",
            "name": "鹏扬科技先锋混合型证券投资基金",
            "inceptionDate": "2026-03-13T00:00:00+08:00"
        }
    ]
}
```
