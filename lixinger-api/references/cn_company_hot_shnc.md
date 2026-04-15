# API文档/大陆/公司接口/热度数据/股东人数变化

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/shnc
> API Key: `cn/company/hot/shnc`

---

## 股东人数变化API

**简要描述:** 获取股东人数变化数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/hot/shnc`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/shnc](https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/shnc)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 股票代码数组。 stockCodes长度>=1且<=100，格式如下：["300750","600519","600157"]。 请参考 股票信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| shnc_rld | Date | 最新数据时间 |
| shnc_rln | Number | 最新股东人数 |
| shnc_d10 | Number | 10天股东人数变化 |
| shnc_d20 | Number | 20天股东人数变化 |
| shnc_d30 | Number | 30天股东人数变化 |
| shnc_d60 | Number | 60天股东人数变化 |
| shnc_d90 | Number | 90天股东人数变化 |
| shnc_qld | Date | 最新季度数据时间 |
| shnc_qln | Number | 最新季度股东人数 |
| shnc_q1 | Number | 1个季度股东人数变化 |
| shnc_q2 | Number | 2个季度股东人数变化 |
| shnc_q3 | Number | 3个季度股东人数变化 |
| shnc_y1 | Number | 1年股东人数变化 |
| shnc_y2 | Number | 2年股东人数变化 |

### 示例

```json
{
    "stockCodes": [
        "300750",
        "600519",
        "600157"
    ],
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
            "shnc_rld": "2026-02-28T00:00:00+08:00",
            "shnc_rln": 257489,
            "shnc_qld": "2025-12-31T00:00:00+08:00",
            "shnc_qln": 249777,
            "shnc_q1": 0.09804637013460879,
            "shnc_q2": 0.10341125954198473,
            "shnc_q3": 0.10361114670366328,
            "shnc_y1": 0.23318486590038315,
            "shnc_y2": -0.01041890853189854,
            "shnc_d60": 0.03087554098255644,
            "stockCode": "300750"
        },
        {
            "shnc_rld": "2025-09-30T00:00:00+08:00",
            "shnc_rln": 238512,
            "shnc_d90": 0.08091254339294293,
            "shnc_qld": "2025-09-30T00:00:00+08:00",
            "shnc_qln": 238512,
            "shnc_q1": 0.08091254339294293,
            "shnc_q2": 0.2394740944759133,
            "shnc_q3": 0.14727697769055384,
            "shnc_y1": 0.18320088103104443,
            "shnc_y2": 0.5898150308281953,
            "stockCode": "600519"
        },
        {
            "shnc_rld": "2025-09-30T00:00:00+08:00",
            "shnc_rln": 588654,
            "shnc_qld": "2025-09-30T00:00:00+08:00",
            "shnc_qln": 588654,
            "shnc_q1": 0.0482328052880506,
            "shnc_q2": -0.01526978062236735,
            "shnc_q3": -0.13296549855065634,
            "shnc_y1": 0.33687165301756444,
            "shnc_y2": 0.3532026997204649,
            "shnc_d90": 0.0482328052880506,
            "stockCode": "600157"
        }
    ]
}
```
