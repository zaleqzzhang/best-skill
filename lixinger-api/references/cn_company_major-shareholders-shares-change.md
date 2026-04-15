# API文档/大陆/公司接口/大股东增减持

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/major-shareholders-shares-change
> API Key: `cn/company/major-shareholders-shares-change`

---

## 大股东增减持API

**简要描述:** 获取大股东增减持数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/major-shareholders-shares-change`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/major-shareholders-shares-change](https://www.lixinger.com/api/open-api/html-doc/cn/company/major-shareholders-shares-change)

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
| shareholderName | String | 股东名称 |
| changeQuantity | Number | 变动持股量 |
| sharesChangeRatio | Number | 变动数量占总股本比例 |
| priceFloor | Number | 增(减)持价格下限 |
| priceCeiling | Number | 增(减)持价格上限 |
| avgPrice | Number | 增减持平均价格【如果没有价格上下限，我们会根据数据时间所在交易日的成交均价做计算】 |
| quantityHeldAfterChange | Number | 变动后持股数量 |
| sharesHeldAfterChange | Number | 变动后占比 |
| sharesChangeAmount | Number | 增减持金额 |

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
            "shareholderName": "苏州明玖管理咨询中心(有限合伙)",
            "date": "2026-03-10T00:00:00+08:00",
            "changeQuantity": -161051,
            "sharesChangeRatio": 0.00121,
            "sharesHeldAfterChange": 0.03539,
            "quantityHeldAfterChange": 4725875,
            "priceFloor": 15.41,
            "priceCeiling": 19.43,
            "stockCode": "920663",
            "sharesChangeAmount": 2805508.42,
            "avgPrice": 17.42
        },
        {
            "shareholderName": "一汽股权投资(天津)有限公司",
            "date": "2026-03-10T00:00:00+08:00",
            "changeQuantity": -916200,
            "sharesChangeRatio": 0.00647,
            "sharesHeldAfterChange": 0.1885,
            "quantityHeldAfterChange": 26674431,
            "stockCode": "600148",
            "sharesChangeAmount": 18028880.7575,
            "avgPrice": 19.677887751015504
        },
        {
            "shareholderName": "陕国投·恒力石化第五期员工持股集合资金信托计划",
            "date": "2026-03-10T00:00:00+08:00",
            "changeQuantity": -2032300,
            "sharesChangeRatio": 0.00029,
            "sharesHeldAfterChange": 0.0004,
            "quantityHeldAfterChange": 2509700,
            "stockCode": "600346",
            "sharesChangeAmount": 45751109.9186,
            "avgPrice": 22.511986379268528
        }
    ]
}
```
