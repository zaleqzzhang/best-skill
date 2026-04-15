# API文档/大陆/公司接口/营收构成

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/operation-revenue-constitution
> API Key: `cn/company/operation-revenue-constitution`

---

## 营收构成API

**简要描述:** 获取营收构成数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/operation-revenue-constitution`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/operation-revenue-constitution](https://www.lixinger.com/api/open-api/html-doc/cn/company/operation-revenue-constitution)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考股票信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| date | Date | 数据时间 |
| declarationDate | Date | 公告日期 |
| dataList.$.classifyType | String | 分类方式 |
| dataList.$.itemName | String | 分类名称 |
| dataList.$.parentItemName | Number | 上级项目序号 |
| dataList.$.revenue | Number | 收入 |
| dataList.$.revenuePercentage | Number | 收入比例 |
| dataList.$.costs | Number | 成本 |
| dataList.$.costPercentage | Number | 成本比例 |
| dataList.$.grossProfitMargin | Number | 毛利率 |

### 示例

```json
{
    "startDate": "2025-03-20",
    "endDate": "2026-03-20",
    "stockCode": "300750",
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
            "date": "2025-12-30T16:00:00.000Z",
            "declarationDate": "2026-03-09T16:00:00.000Z",
            "dataList": [
                {
                    "classifyType": "industries",
                    "itemName": "合计",
                    "revenue": 423701834000,
                    "revenuePercentage": 100,
                    "costs": 312383297000,
                    "costPercentage": 100,
                    "grossProfitMargin": 0.2627
                },
                {
                    "classifyType": "industries",
                    "itemName": "电气机械及器材制造业",
                    "revenue": 417723738000,
                    "revenuePercentage": 98.58907950820907,
                    "costs": 307077698000,
                    "costPercentage": 98.3016,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.2649
                },
                {
                    "classifyType": "industries",
                    "itemName": "采选冶炼行业",
                    "revenue": 5978096000,
                    "revenuePercentage": 1.4109204917909324,
                    "costs": 5305599000,
                    "costPercentage": 1.6984,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.1125
                },
                {
                    "classifyType": "products",
                    "itemName": "合计",
                    "revenue": 406785221000,
                    "revenuePercentage": 96.00742511773032,
                    "costs": 308033498000,
                    "costPercentage": 98.6075,
                    "grossProfitMargin": 0.2428
                },
                {
                    "classifyType": "products",
                    "itemName": "动力电池系统",
                    "revenue": 316506369000,
                    "revenuePercentage": 74.70025938098725,
                    "costs": 241064397000,
                    "costPercentage": 77.1694,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.2384
                },
                {
                    "classifyType": "products",
                    "itemName": "储能电池系统",
                    "revenue": 62439820000,
                    "revenuePercentage": 14.7367358339072,
                    "costs": 45763689000,
                    "costPercentage": 14.6499,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.2671
                },
                {
                    "classifyType": "products",
                    "itemName": "电池材料及回收",
                    "revenue": 21860936000,
                    "revenuePercentage": 5.159509411044938,
                    "costs": 15899813000,
                    "costPercentage": 5.0898,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.2727
                },
                {
                    "classifyType": "products",
                    "itemName": "电池矿产资源",
                    "revenue": 5978096000,
                    "revenuePercentage": 1.4109204917909324,
                    "costs": 5305599000,
                    "costPercentage": 1.6984,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.1125
                },
                {
                    "classifyType": "region",
                    "itemName": "合计",
                    "revenue": 423701834000,
                    "revenuePercentage": 100,
                    "costs": 312383297000,
                    "costPercentage": 100,
                    "grossProfitMargin": 0.2627
                },
                {
                    "classifyType": "region",
                    "itemName": "境内",
                    "revenue": 294060576000,
                    "revenuePercentage": 69.40271492900831,
                    "costs": 223497885000,
                    "costPercentage": 71.546,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.24
                },
                {
                    "classifyType": "region",
                    "itemName": "境外",
                    "revenue": 129641258000,
                    "revenuePercentage": 30.597285070991692,
                    "costs": 88885412000,
                    "costPercentage": 28.454,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.3144
                }
            ]
        },
        {
            "date": "2025-06-29T16:00:00.000Z",
            "declarationDate": "2025-07-30T16:00:00.000Z",
            "dataList": [
                {
                    "classifyType": "industries",
                    "itemName": "合计",
                    "revenue": 178886253000,
                    "revenuePercentage": 100,
                    "costs": 134123603000,
                    "costPercentage": 100,
                    "grossProfitMargin": 0.2502
                },
                {
                    "classifyType": "industries",
                    "itemName": "电气机械及器材制造业",
                    "revenue": 175525013000,
                    "revenuePercentage": 98.1210182763457,
                    "costs": 131067097000,
                    "costPercentage": 97.7211,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.2533
                },
                {
                    "classifyType": "industries",
                    "itemName": "采选冶炼行业",
                    "revenue": 3361240000,
                    "revenuePercentage": 1.8789817236543045,
                    "costs": 3056506000,
                    "costPercentage": 2.2789,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.0907
                },
                {
                    "classifyType": "products",
                    "itemName": "合计",
                    "revenue": 171221175000,
                    "revenuePercentage": 95.71511065190683,
                    "costs": 132098945000,
                    "costPercentage": 98.4905,
                    "grossProfitMargin": 0.2285
                },
                {
                    "classifyType": "products",
                    "itemName": "动力电池系统",
                    "revenue": 131572512000,
                    "revenuePercentage": 73.55093518561205,
                    "costs": 102085255000,
                    "costPercentage": 76.1128,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.2241
                },
                {
                    "classifyType": "products",
                    "itemName": "储能电池系统",
                    "revenue": 28400044000,
                    "revenuePercentage": 15.87603492371211,
                    "costs": 21153269000,
                    "costPercentage": 15.7715,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.2552
                },
                {
                    "classifyType": "products",
                    "itemName": "电池材料及回收",
                    "revenue": 7887379000,
                    "revenuePercentage": 4.409158818928361,
                    "costs": 5803915000,
                    "costPercentage": 4.3273,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.2642
                },
                {
                    "classifyType": "products",
                    "itemName": "电池矿产资源",
                    "revenue": 3361240000,
                    "revenuePercentage": 1.8789817236543045,
                    "costs": 3056506000,
                    "costPercentage": 2.2789,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.0907
                },
                {
                    "classifyType": "region",
                    "itemName": "合计",
                    "revenue": 178886253000,
                    "revenuePercentage": 100,
                    "costs": 134123603000,
                    "costPercentage": 100,
                    "grossProfitMargin": 0.2502
                },
                {
                    "classifyType": "region",
                    "itemName": "境内",
                    "revenue": 117677899000,
                    "revenuePercentage": 65.78364576734693,
                    "costs": 90680806000,
                    "costPercentage": 67.6099,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.2294
                },
                {
                    "classifyType": "region",
                    "itemName": "境外",
                    "revenue": 61208354000,
                    "revenuePercentage": 34.21635423265308,
                    "costs": 43442797000,
                    "costPercentage": 32.3901,
                    "parentItemName": "合计",
                    "grossProfitMargin": 0.2902
                }
            ]
        }
    ]
}
```
