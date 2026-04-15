# API文档/大陆/公司接口/股本变动

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/equity-change
> API Key: `cn/company/equity-change`

---

## 股本变动API

**简要描述:** 获取股本变动数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/equity-change`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/equity-change](https://www.lixinger.com/api/open-api/html-doc/cn/company/equity-change)

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
| date | Date | 变动日期 |
| declarationDate | Date | 公告日期 |
| changeReason | String | 变动原因 |
| capitalization | Number | 总股本 |
| outstandingSharesA | Number | 流通A股 |
| limitedSharesA | Number | 限售A股 |
| outstandingSharesH | Number | 流通H股 |
| capitalizationChangeRatio | Number | 总股本变动比例 |
| outstandingSharesAChangeRatio | Number | 流通A股变动比例 |
| limitedSharesAChangeRatio | Number | 限售A股变动比例 |
| outstandingSharesHChangeRatio | Number | 流通H股变动比例 |

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
            "date": "2026-02-28T00:00:00+08:00",
            "declarationDate": "2026-03-05T00:00:00+08:00",
            "changeReason": "期权行权",
            "capitalization": 4563868956,
            "outstandingSharesA": 4256638826,
            "outstandingSharesH": 155915300,
            "changeReasonTypes": [
                "equityOption"
            ],
            "capitalizationChangeRatio": 0,
            "outstandingSharesAChangeRatio": 0,
            "outstandingSharesHChangeRatio": 0,
            "limitedSharesAChangeRatio": 0
        },
        {
            "date": "2026-02-09T00:00:00+08:00",
            "declarationDate": "2026-02-09T00:00:00+08:00",
            "changeReason": "期权行权",
            "capitalization": 4563858928,
            "outstandingSharesA": 4256628798,
            "outstandingSharesH": 155915300,
            "changeReasonTypes": [
                "equityOption"
            ],
            "capitalizationChangeRatio": 0,
            "outstandingSharesAChangeRatio": 0,
            "outstandingSharesHChangeRatio": 0,
            "limitedSharesAChangeRatio": 0
        },
        {
            "date": "2026-01-31T00:00:00+08:00",
            "declarationDate": "2026-02-05T00:00:00+08:00",
            "changeReason": "增发新股上市,股权激励,期权行权",
            "capitalization": 4563849720,
            "outstandingSharesA": 4256619590,
            "outstandingSharesH": 155915300,
            "changeReasonTypes": [
                "SPO",
                "equityIncentive",
                "equityOption"
            ],
            "capitalizationChangeRatio": 0,
            "outstandingSharesAChangeRatio": 0,
            "outstandingSharesHChangeRatio": 0,
            "limitedSharesAChangeRatio": 0
        }
    ]
}
```
