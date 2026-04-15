# API文档/美国/指数接口/跟踪基金

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/us/index/tracking-fund
> API Key: `us/index/tracking-fund`

---

## 指数跟踪基金信息API

**简要描述:** 获取指数跟踪基金数据。

**请求URL:** `https://open.lixinger.com/api/us/index/tracking-fund`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/us/index/tracking-fund](https://www.lixinger.com/api/open-api/html-doc/us/index/tracking-fund)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 股票代码 请参考指数信息API获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| name | String | 基金名称 |
| stockCode | String | 基金代码 |
| shortName | String | 简称 |
| areaCode | String | 地区代码 |
| market | String | 市场 |
| exchange | String | 交易所 |

### 示例

```json
{
    "stockCode": ".INX",
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
            "stockCode": "006075",
            "name": "博时标普500交易型开放式指数证券投资基金联接基金",
            "areaCode": "cn",
            "market": "a",
            "shortName": "博时标普500ETF联接C",
            "exchange": "jj"
        },
        {
            "stockCode": "007722",
            "name": "天弘标普500发起式证券投资基金（QDII-FOF）",
            "areaCode": "cn",
            "market": "a",
            "shortName": "天弘标普500发起（QDII-FOF）C",
            "exchange": "jj"
        },
        {
            "exchange": "sh",
            "stockCode": "513500",
            "areaCode": "cn",
            "name": "博时标普500交易型开放式指数证券投资基金",
            "market": "a",
            "shortName": "博时标普500ETF"
        }
    ]
}
```
