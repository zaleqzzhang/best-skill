# API文档/大陆/公司接口/大宗交易

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/block-deal
> API Key: `cn/company/block-deal`

---

## 大宗交易API

**简要描述:** 获取大宗交易数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/block-deal`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/block-deal](https://www.lixinger.com/api/open-api/html-doc/cn/company/block-deal)

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
| stockCode | String | 股票代码 |
| tradingPrice | Number | 成交价 |
| tradingAmount | Number | 成交金额 |
| tradingVolume | Number | 成交量 |
| buyBranch | String | 买入营业部 |
| sellBranch | String | 卖出营业部 |
| discountRate | Number | 折价率 |

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
            "buyBranch": "东北证券股份有限公司烟台分公司",
            "sellBranch": "国金证券股份有限公司深圳分公司",
            "tradingPrice": 124.49,
            "tradingVolume": 10000,
            "tradingAmount": 0,
            "stockCode": "920493",
            "discountRate": 0.2857716580608147
        },
        {
            "date": "2026-03-10T00:00:00+08:00",
            "buyBranch": "东北证券股份有限公司烟台分公司",
            "sellBranch": "国金证券股份有限公司深圳分公司",
            "tradingPrice": 28.24,
            "tradingVolume": 105530,
            "tradingAmount": 0,
            "stockCode": "920640",
            "discountRate": 0.31655372700871254
        },
        {
            "date": "2026-03-10T00:00:00+08:00",
            "buyBranch": "中国国际金融股份有限公司北京建国门外大街证券营业部",
            "sellBranch": "国泰海通证券股份有限公司深圳福华三路证券营业部",
            "tradingPrice": 3.03,
            "tradingVolume": 500000,
            "tradingAmount": 1515000,
            "stockCode": "600010",
            "discountRate": 0
        }
    ]
}
```
