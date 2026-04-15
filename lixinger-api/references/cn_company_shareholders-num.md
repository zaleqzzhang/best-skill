# API文档/大陆/公司接口/股东人数

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/shareholders-num
> API Key: `cn/company/shareholders-num`

---

## 股东人数API

**简要描述:** 获取股东人数数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/shareholders-num`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/shareholders-num](https://www.lixinger.com/api/open-api/html-doc/cn/company/shareholders-num)

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
| total | Number | 股东人数 |
| shareholdersNumberChangeRate | Number | 股东人数变化比例 |
| spc | Number | 股价涨跌幅 |

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
            "num": 257489,
            "total": 257489,
            "shareholdersNumberChangeRate": 0.0309,
            "spc": -0.0688
        },
        {
            "date": "2025-12-31T00:00:00+08:00",
            "num": 249777,
            "total": 249777,
            "shareholdersNumberChangeRate": 0.098,
            "spc": -0.0864
        },
        {
            "date": "2025-09-30T00:00:00+08:00",
            "num": 227474,
            "total": 227474,
            "shareholdersNumberChangeRate": 0.0049,
            "spc": 0.5996
        }
    ]
}
```
