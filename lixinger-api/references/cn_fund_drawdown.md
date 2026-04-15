# API文档/大陆/基金接口/公募基金接口/回撤

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/fund/drawdown
> API Key: `cn/fund/drawdown`

---

## 基金回撤API

**简要描述:** 获取基金回撤数据。

**请求URL:** `https://open.lixinger.com/api/cn/fund/drawdown`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund/drawdown](https://www.lixinger.com/api/open-api/html-doc/cn/fund/drawdown)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考基金信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 |
| granularity | Yes | String | 回撤周期，例如：“y”。 **当前支持:** 月: `m`; 季度: `q`; 半年: `hy`; 1年: `y1`; 3年: `y3`; 5年: `y5`; 10年: `y10`; 上市以来: `fs` |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| date | Date | 数据时间 |
| value | Number | 回撤 |

### 示例

```json
{
    "startDate": "2023-03-20",
    "endDate": "2026-03-20",
    "granularity": "y1",
    "stockCode": "161725",
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
            "date": "2026-03-19T00:00:00+08:00",
            "value": -0.2374
        },
        {
            "date": "2026-03-18T00:00:00+08:00",
            "value": -0.2338
        },
        {
            "date": "2026-03-17T00:00:00+08:00",
            "value": -0.2304
        }
    ]
}
```
