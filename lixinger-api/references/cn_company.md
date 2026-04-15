# API文档/大陆/公司接口/基础信息

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company
> API Key: `cn/company`

---

## 股票信息API

**简要描述:** 获取股票详细信息。

**请求URL:** `https://open.lixinger.com/api/cn/company`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company](https://www.lixinger.com/api/open-api/html-doc/cn/company)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 股票代码数组。 默认值为所有股票代码。格式如下：["300750","600519","600157"]。 请参考 股票信息API 获取合法的stockCode。 |
| fsTableType | No | String | 财报类型，比如，'bank'。 **当前支持:** 非金融: `non_financial`; 银行: `bank`; 保险: `insurance`; 证券: `security`; 其他金融: `other_financial` |
| mutualMarkets | No | Array | 互联互通类型，比如：'[ha]'。 **当前支持:** 陆股通: `ha` |
| includeDelisted | No | Boolean | 是否包含退市股。 默认值是false。 |
| pageIndex | Yes | Number | 页面索引。 默认值是0。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| total | Number | 公司总数 |
| name | String | 公司名称 |
| stockCode | String | 股票代码 |
| areaCode | String | 地区代码 |
| market | String | 市场 |
| exchange | String | 交易所 |
| fsTableType | String | 财报类型 |
| mutualMarkets | String | 互联互通 |
| mutualMarketFlag | Boolean | 是否是互联互通标的 |
| marginTradingAndSecuritiesLendingFlag | Boolean | 是否是融资融券标的 |
| ipoDate | Date | 上市时间 |
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
    "total": 5595,
    "data": [
        {
            "name": "新恒泰",
            "market": "a",
            "exchange": "bj",
            "areaCode": "cn",
            "stockCode": "920028",
            "fsTableType": "non_financial",
            "ipoDate": "2026-03-20T00:00:00+08:00",
            "mutualMarketFlag": false
        },
        {
            "name": "族兴新材",
            "market": "a",
            "exchange": "bj",
            "areaCode": "cn",
            "stockCode": "920078",
            "fsTableType": "non_financial",
            "ipoDate": "2026-03-18T00:00:00+08:00",
            "mutualMarketFlag": false
        },
        {
            "name": "觅睿科技",
            "market": "a",
            "exchange": "bj",
            "areaCode": "cn",
            "stockCode": "920036",
            "fsTableType": "non_financial",
            "ipoDate": "2026-03-09T00:00:00+08:00",
            "mutualMarketFlag": false
        }
    ]
}
```
