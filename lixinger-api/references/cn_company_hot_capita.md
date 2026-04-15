# API文档/大陆/公司接口/热度数据/人均指标

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/capita
> API Key: `cn/company/hot/capita`

---

## 人均指标API

**简要描述:** 获取人均指标数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/hot/capita`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/capita](https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/capita)

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
| last_data_date | Date | 数据时间 |
| stn | Number | 员工人数 |
| stn_mc_pc | Number | 人均市值 |
| stn_toi_pc | Number | 人均营业总收入 |
| stn_np_pc | Number | 人均净利润 |
| stn_ncffoa_pc | Number | 人均经营活动产生的现金流量净额 |
| stn_rade_pc | Number | 人均研发费用 |
| stn_s_pc | Number | 人均薪酬 |

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
            "cptofe_pc": 105448,
            "stn": 185839,
            "stn_mc_pc": 9835554,
            "stn_ncffoa_pc": 838318,
            "stn_np_pc": 483195.6316,
            "stn_s_pc": 234385.4739,
            "stn_toi_pc": 2666241.9115,
            "last_data_date": "2025-12-31T00:00:00+08:00",
            "stockCode": "300750"
        },
        {
            "cptofe_pc": 244570,
            "stn": 34750,
            "stn_mc_pc": 52356427,
            "stn_ncffoa_pc": 2717442,
            "stn_np_pc": 2625484.2775,
            "stn_s_pc": 463615.7992,
            "stn_toi_pc": 5117970.6683,
            "stn_rade_pc": 2896,
            "last_data_date": "2024-12-31T00:00:00+08:00",
            "stockCode": "600519"
        },
        {
            "cptofe_pc": 128505,
            "stn": 13337,
            "stn_mc_pc": 3042741,
            "stn_ncffoa_pc": 571231,
            "stn_np_pc": 178142.304,
            "stn_s_pc": 257027.6115,
            "stn_toi_pc": 2488178.5433,
            "last_data_date": "2024-12-31T00:00:00+08:00",
            "stockCode": "600157"
        }
    ]
}
```
