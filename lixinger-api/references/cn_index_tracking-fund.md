# API文档/大陆/指数接口/跟踪基金

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/index/tracking-fund
> API Key: `cn/index/tracking-fund`

---

## 指数跟踪基金信息API

**简要描述:** 获取指数跟踪基金数据。

**请求URL:** `https://open.lixinger.com/api/cn/index/tracking-fund`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/index/tracking-fund](https://www.lixinger.com/api/open-api/html-doc/cn/index/tracking-fund)

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
    "stockCode": "000016",
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
            "stockCode": "005737",
            "areaCode": "cn",
            "exchange": "jj",
            "market": "a",
            "name": "博时上证50交易型开放式指数证券投资基金联接基金",
            "shortName": "博时上证50ETF联接C"
        },
        {
            "stockCode": "005733",
            "areaCode": "cn",
            "exchange": "jj",
            "market": "a",
            "name": "华夏上证50交易型开放式指数证券投资基金联接基金",
            "shortName": "华夏上证50ETF联接C"
        },
        {
            "stockCode": "510800",
            "areaCode": "cn",
            "exchange": "sh",
            "market": "a",
            "name": "建信上证50交易型开放式指数证券投资基金",
            "shortName": "建信上证50ETF"
        }
    ]
}
```
