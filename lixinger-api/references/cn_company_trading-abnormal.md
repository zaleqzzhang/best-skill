# API文档/大陆/公司接口/龙虎榜

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/trading-abnormal
> API Key: `cn/company/trading-abnormal`

---

## 龙虎榜API

**简要描述:** 获取龙虎榜信息。

**请求URL:** `https://open.lixinger.com/api/cn/company/trading-abnormal`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/trading-abnormal](https://www.lixinger.com/api/open-api/html-doc/cn/company/trading-abnormal)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | No | String | 请参考股票信息API获取合法的stockCode。 stockCode仅在请求数据为date range的情况下生效。 |
| date | No | String: YYYY-MM-DD (北京时间) | 信息日期。 用于获取指定日期数据。 |
| startDate | No | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| date | Date | 数据时间 |
| reasonForDisclosure | String | 披露原因 |
| buyList.$.branchName | String | 机构昵称 |
| buyList.$.buyAmount | Number | 买入金额 |
| buyList.$.sellAmount | Number | 卖出金额 |
| institutionBuyCount | Number | 买入机构数 |
| institutionSellCount | Number | 卖出机构数 |
| institutionBuyAmount | Number | 机构买入金额 |
| institutionSellAmount | Number | 机构卖出金额 |
| institutionNetPurchaseAmount | Number | 机构净买入金额 |
| totalPurchaseAmount | Number | 总买入金额 |
| totalSellAmount | Number | 总卖出金额 |
| totalNetPurchaseAmount | Number | 总净买入金额 |
| sellList.$.branchName | String | 机构昵称 |
| sellList.$.buyAmount | Number | 买入金额 |
| sellList.$.sellAmount | Number | 卖出金额 |

### 示例

```json
{
    "date": "2026-03-10",
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
            "date": "2026-03-10T00:00:00+08:00",
            "reasonForDisclosure": "当日换手率达到20%的前5只股票",
            "totalPurchaseAmount": 28264802.589999996,
            "institutionBuyAmount": 0,
            "totalSellAmount": 33456848.450000003,
            "institutionSellAmount": 0,
            "institutionBuyCount": 0,
            "institutionSellCount": 0,
            "totalNetPurchaseAmount": -10898946.170000002,
            "institutionNetPurchaseAmount": 0,
            "stockCode": "920375",
            "buyList": [
                {
                    "branchName": "国信证券股份有限公司深圳互联网分公司",
                    "buyAmount": 22593385.59,
                    "sellAmount": 16886485.28,
                    "isInstitution": false
                },
                {
                    "branchName": "东方财富证券股份有限公司拉萨东环路第二证券营业部",
                    "buyAmount": 9562173.06,
                    "sellAmount": 2024488.17,
                    "isInstitution": false
                },
                {
                    "branchName": "东方财富证券股份有限公司拉萨团结路第二证券营业部",
                    "buyAmount": 6971099.79,
                    "sellAmount": 3465427.6,
                    "isInstitution": false
                },
                {
                    "branchName": "东莞证券股份有限公司揭阳分公司",
                    "buyAmount": 6637282.95,
                    "sellAmount": 0,
                    "isInstitution": false
                },
                {
                    "branchName": "长城证券股份有限公司前海分公司",
                    "buyAmount": 5393085.93,
                    "sellAmount": 515823.68,
                    "isInstitution": false
                }
            ],
            "sellList": [
                {
                    "branchName": "国信证券股份有限公司深圳互联网分公司",
                    "buyAmount": 22593385.59,
                    "sellAmount": 16886485.28,
                    "isInstitution": false
                },
                {
                    "branchName": "国金证券股份有限公司深圳分公司",
                    "buyAmount": 2422043.78,
                    "sellAmount": 14009145.06,
                    "isInstitution": false
                },
                {
                    "branchName": "华福证券有限责任公司深圳分公司",
                    "buyAmount": 0,
                    "sellAmount": 12044368.17,
                    "isInstitution": false
                },
                {
                    "branchName": "东海证券股份有限公司厦门嘉禾路证券营业部",
                    "buyAmount": 41420.95,
                    "sellAmount": 8958080.96,
                    "isInstitution": false
                },
                {
                    "branchName": "华泰证券股份有限公司成都蜀金路证券营业部",
                    "buyAmount": 682812.64,
                    "sellAmount": 7298431.94,
                    "isInstitution": false
                }
            ]
        },
        {
            "date": "2026-03-10T00:00:00+08:00",
            "reasonForDisclosure": "当日换手率达到20%的前5只股票",
            "totalPurchaseAmount": 19315059.65,
            "institutionBuyAmount": 4642899.74,
            "totalSellAmount": 39754557.029999994,
            "institutionSellAmount": 0,
            "institutionBuyCount": 1,
            "institutionSellCount": 0,
            "totalNetPurchaseAmount": -20439497.379999995,
            "institutionNetPurchaseAmount": 4642899.74,
            "stockCode": "920183",
            "buyList": [
                {
                    "branchName": "国信证券股份有限公司深圳红岭中路证券营业部",
                    "buyAmount": 5689504.99,
                    "sellAmount": 75774.85,
                    "isInstitution": false
                },
                {
                    "branchName": "机构专用",
                    "buyAmount": 4717393.82,
                    "sellAmount": 74494.08,
                    "isInstitution": true
                },
                {
                    "branchName": "中信建投证券股份有限公司北京东城分公司",
                    "buyAmount": 4432963.66,
                    "sellAmount": 103587.08,
                    "isInstitution": false
                },
                {
                    "branchName": "国金证券股份有限公司深圳分公司",
                    "buyAmount": 3847848.56,
                    "sellAmount": 1823998.52,
                    "isInstitution": false
                },
                {
                    "branchName": "中国银河证券股份有限公司龙泉华楼街证券营业部",
                    "buyAmount": 3398189.15,
                    "sellAmount": 692986,
                    "isInstitution": false
                }
            ],
            "sellList": [
                {
                    "branchName": "招商证券股份有限公司北京西直门北大街证券营业部",
                    "buyAmount": 0,
                    "sellAmount": 22446884.11,
                    "isInstitution": false
                },
                {
                    "branchName": "中信证券股份有限公司吉林分公司",
                    "buyAmount": 0,
                    "sellAmount": 6384701.87,
                    "isInstitution": false
                },
                {
                    "branchName": "东方财富证券股份有限公司昌都两江大道证券营业部",
                    "buyAmount": 1517751.12,
                    "sellAmount": 5111929.46,
                    "isInstitution": false
                },
                {
                    "branchName": "国投证券股份有限公司北京宏福路证券营业部",
                    "buyAmount": 0,
                    "sellAmount": 4649389.52,
                    "isInstitution": false
                },
                {
                    "branchName": "东方财富证券股份有限公司拉萨东环路第一证券营业部",
                    "buyAmount": 969779.73,
                    "sellAmount": 3649182.92,
                    "isInstitution": false
                }
            ]
        },
        {
            "date": "2026-03-10T00:00:00+08:00",
            "reasonForDisclosure": "当日换手率达到20%的前5只股票",
            "totalPurchaseAmount": 48178702.16000001,
            "institutionBuyAmount": -5968265.949999999,
            "totalSellAmount": 8991478.709999993,
            "institutionSellAmount": 5968265.949999999,
            "institutionBuyCount": 1,
            "institutionSellCount": 1,
            "totalNetPurchaseAmount": 27619711.46000001,
            "institutionNetPurchaseAmount": -5968265.949999999,
            "stockCode": "920088",
            "buyList": [
                {
                    "branchName": "中信证券股份有限公司北京建国门证券营业部",
                    "buyAmount": 36611190.17,
                    "sellAmount": 0,
                    "isInstitution": false
                },
                {
                    "branchName": "国信证券股份有限公司深圳互联网分公司",
                    "buyAmount": 33984997.99,
                    "sellAmount": 13725768.71,
                    "isInstitution": false
                },
                {
                    "branchName": "机构专用",
                    "buyAmount": 23784407.26,
                    "sellAmount": 29752673.21,
                    "isInstitution": true
                },
                {
                    "branchName": "国金证券股份有限公司深圳分公司",
                    "buyAmount": 15050165.06,
                    "sellAmount": 19011121.41,
                    "isInstitution": false
                },
                {
                    "branchName": "东方财富证券股份有限公司拉萨东环路第二证券营业部",
                    "buyAmount": 13369770.84,
                    "sellAmount": 12132265.83,
                    "isInstitution": false
                }
            ],
            "sellList": [
                {
                    "branchName": "机构专用",
                    "buyAmount": 23784407.26,
                    "sellAmount": 29752673.21,
                    "isInstitution": true
                },
                {
                    "branchName": "中信建投证券股份有限公司东莞东莞大道证券营业部",
                    "buyAmount": 0,
                    "sellAmount": 20558990.7,
                    "isInstitution": false
                },
                {
                    "branchName": "国金证券股份有限公司深圳分公司",
                    "buyAmount": 15050165.06,
                    "sellAmount": 19011121.41,
                    "isInstitution": false
                },
                {
                    "branchName": "国信证券股份有限公司深圳互联网分公司",
                    "buyAmount": 33984997.99,
                    "sellAmount": 13725768.71,
                    "isInstitution": false
                },
                {
                    "branchName": "东方财富证券股份有限公司拉萨东环路第二证券营业部",
                    "buyAmount": 13369770.84,
                    "sellAmount": 12132265.83,
                    "isInstitution": false
                }
            ]
        }
    ]
}
```
