# API文档/香港/公司接口/基础信息

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/company
> API Key: `hk/company`

---

## 股票信息API

**简要描述:** 获取股票详细信息。

**请求URL:** `https://open.lixinger.com/api/hk/company`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/company](https://www.lixinger.com/api/open-api/html-doc/hk/company)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 股票代码数组。 默认值为所有股票代码。格式如下：["00700"]。 请参考 股票信息API 获取合法的stockCode。 |
| fsTableType | No | String | 财报类型，比如，'bank'。 **当前支持:** 非金融: `non_financial`; 银行: `bank`; 证券: `security`; 保险: `insurance`; 房地产投资信托: `reit`; 其他金融: `other_financial` |
| mutualMarkets | No | Array | 互联互通类型，比如：'[ah]'。 **当前支持:** 港股通: `ah` |
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
| ipoDate | Date | 上市时间 |
| delistedDate | Date | 退市时间 |
| sharesPerLot | Number | 每手股数 |
| stockCodeA | String | AH同时上市公司对应的A股代码 |

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
    "total": 2727,
    "data": [
        {
            "areaCode": "hk",
            "market": "h",
            "exchange": "hk",
            "stockCode": "03268",
            "name": "美格智能",
            "fsTableType": "non_financial",
            "ipoDate": "2026-03-10T00:00:00+08:00",
            "sharesPerLot": 100,
            "mutualMarkets": [
                "ah"
            ],
            "mutualMarketFlag": true
        },
        {
            "areaCode": "hk",
            "market": "h",
            "exchange": "hk",
            "stockCode": "02692",
            "name": "兆威机电",
            "fsTableType": "non_financial",
            "ipoDate": "2026-03-09T00:00:00+08:00",
            "sharesPerLot": 100,
            "mutualMarkets": [
                "ah"
            ],
            "mutualMarketFlag": true
        },
        {
            "areaCode": "hk",
            "market": "h",
            "exchange": "hk",
            "stockCode": "02649",
            "name": "优乐赛共享",
            "fsTableType": "non_financial",
            "ipoDate": "2026-03-09T00:00:00+08:00",
            "sharesPerLot": 500,
            "mutualMarketFlag": false
        }
    ]
}
```
