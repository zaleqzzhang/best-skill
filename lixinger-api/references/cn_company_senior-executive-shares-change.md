# API文档/大陆/公司接口/高管增减持

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/senior-executive-shares-change
> API Key: `cn/company/senior-executive-shares-change`

---

## 高管增减持API

**简要描述:** 获取高管增减持数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/senior-executive-shares-change`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/senior-executive-shares-change](https://www.lixinger.com/api/open-api/html-doc/cn/company/senior-executive-shares-change)

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
| executiveName | String | 高管姓名 |
| duty | String | 职务 |
| relationBetweenES | String | 持股人与高管关系 |
| changeReason | Number | 变动原因 |
| beforeChangeShares | Number | 变动前持股量 |
| changedShares | Number | 变动持股量 |
| afterChangeShares | Number | 变动后持股量 |
| avgPrice | Number | 成交均价 |
| sharesChangeAmount | Number | 增减持金额 |
| changedSharesForCapitalizationProportion | Number | 增减持占总股本比例 |

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
            "stockType": "A股",
            "shareholderName": "郭万花",
            "executiveName": "郭万花",
            "beforeChangeShares": 571700,
            "changedShares": 44060,
            "afterChangeShares": 615760,
            "avgPrice": 6.65,
            "duty": "高级管理人员",
            "changeReason": "二级市场买卖",
            "date": "2026-03-10T00:00:00+08:00",
            "stockCode": "600888",
            "changedSharesForCapitalizationProportion": 0.0007,
            "sharesChangeAmount": 292999
        },
        {
            "stockType": "A股",
            "shareholderName": "杨扬",
            "executiveName": "杨扬",
            "beforeChangeShares": 73758,
            "changedShares": -3000,
            "afterChangeShares": 70758,
            "avgPrice": 5.875,
            "duty": "高级管理人员",
            "changeReason": "二级市场买卖",
            "date": "2026-03-10T00:00:00+08:00",
            "stockCode": "601218",
            "changedSharesForCapitalizationProportion": 0,
            "sharesChangeAmount": 17625
        },
        {
            "stockType": "A股",
            "shareholderName": "朱民法",
            "executiveName": "朱民法",
            "beforeChangeShares": 338000,
            "changedShares": -2000,
            "afterChangeShares": 336000,
            "avgPrice": 8.46,
            "duty": "高级管理人员",
            "changeReason": "二级市场买卖",
            "date": "2026-03-10T00:00:00+08:00",
            "stockCode": "603012",
            "changedSharesForCapitalizationProportion": 0,
            "sharesChangeAmount": 16920
        }
    ]
}
```
