# 按行业分类的股票投资组合API

## 按行业分类的股票投资组合API

**简要描述:** 获取按行业分类的股票投资组合的数据。

**说明:**

- 主基金代码和子基金代码获取相同的数据。

**请求URL:** `https://open.lixinger.com/api/cn/fund/asset-industry-combination`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund/asset-industry-combination](https://www.lixinger.com/api/open-api/html-doc/cn/fund/asset-industry-combination)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考基金信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| date | Date | 财报日期 |
| aic_cn | Array | 按行业分类的股票投资组合 子字段: 行业名称 : `name` : (String); 公允价值 : `value` : (Number); 比例 : `proportion` : (Number) |

### 示例

```json
{
    "startDate": "2025-03-20",
    "endDate": "2026-03-20",
    "stockCode": "005827",
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
            "date": "2025-12-31T00:00:00+08:00",
            "aic_cn": [
                {
                    "name": "采矿业",
                    "value": 103284,
                    "proportion": 0.000007
                },
                {
                    "name": "制造业",
                    "value": 13540022277,
                    "proportion": 0.903143
                },
                {
                    "name": "批发和零售业",
                    "value": 26694,
                    "proportion": 0.000002
                },
                {
                    "name": "信息传输、软件和信息技术服务业",
                    "value": 32995,
                    "proportion": 0.000002
                },
                {
                    "name": "租赁和商务服务业",
                    "value": 1451890000,
                    "proportion": 0.096844
                },
                {
                    "name": "科学研究和技术服务业",
                    "value": 35847,
                    "proportion": 0.000002
                }
            ],
            "declarationDate": "2026-01-22T00:00:00+08:00"
        },
        {
            "date": "2025-09-30T00:00:00+08:00",
            "aic_cn": [
                {
                    "name": "制造业",
                    "value": 15354172213,
                    "proportion": 0.884809
                },
                {
                    "name": "批发和零售业",
                    "value": 21698,
                    "proportion": 0.000001
                },
                {
                    "name": "租赁和商务服务业",
                    "value": 1998880000,
                    "proportion": 0.115189
                },
                {
                    "name": "科学研究和技术服务业",
                    "value": 18256,
                    "proportion": 0.000001
                }
            ],
            "declarationDate": "2025-10-28T00:00:00+08:00"
        },
        {
            "date": "2025-06-30T00:00:00+08:00",
            "aic_cn": [
                {
                    "name": "制造业",
                    "value": 13450927359,
                    "proportion": 0.777094
                },
                {
                    "name": "批发和零售业",
                    "value": 2244,
                    "proportion": 0
                },
                {
                    "name": "交通运输、仓储和邮政业",
                    "value": 2047923608,
                    "proportion": 0.118314
                },
                {
                    "name": "租赁和商务服务业",
                    "value": 1810400000,
                    "proportion": 0.104591
                },
                {
                    "name": "科学研究和技术服务业",
                    "value": 2922,
                    "proportion": 0
                }
            ],
            "declarationDate": "2025-08-30T00:00:00+08:00"
        }
    ]
}
```
