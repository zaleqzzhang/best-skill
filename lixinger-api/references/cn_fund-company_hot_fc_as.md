# API文档/大陆/基金接口/基金公司接口/热度数据/基金公司资产规模

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/fund-company/hot/fc_as
> API Key: `cn/fund-company/hot/fc_as`

---

## 基金公司资产规模API

**简要描述:** 获取基金公司资产规模数据。

**请求URL:** `https://open.lixinger.com/api/cn/fund-company/hot/fc_as`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund-company/hot/fc_as](https://www.lixinger.com/api/open-api/html-doc/cn/fund-company/hot/fc_as)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 基金公司代码数组。 stockCodes长度>=1且<=100，格式如下：["50110000","50030000"]。 请参考 基金信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| fc_as_d | Date | 最新数据时间 |
| fc_as | Number | 总资产规模 |
| fc_nb_as | Number | 非债券基金资产规模 |
| fc_h_as | Number | 混合型资产规模 |
| fc_e_as | Number | 股票型资产规模 |
| fc_q_as | Number | QDII型资产规模 |
| fc_b_as | Number | 债券型资产规模 |

### 示例

```json
{
    "stockCodes": [
        "50110000",
        "50030000"
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
            "type": "fc_as",
            "fc_all_mn": 94,
            "fc_as": 1475643716702.1235,
            "fc_b_as": 406192220189.959,
            "fc_nb_as": 1069451496512.1637,
            "fc_h_as": 251442310206.4365,
            "fc_i_as": 617717454342.7557,
            "fc_a_as": 47479572566.3017,
            "fc_e_as": 665197026909.0574,
            "fc_q_as": 152812159396.66998,
            "fc_all_fn": 383,
            "fc_b_fn": 72,
            "fc_nb_fn": 311,
            "fc_h_fn": 125,
            "fc_i_fn": 139,
            "fc_a_fn": 19,
            "fc_e_fn": 158,
            "fc_q_fn": 28,
            "fc_as_d": "2026-03-17T16:00:00.000Z",
            "stockCode": "50110000"
        },
        {
            "type": "fc_as",
            "fc_all_mn": 91,
            "fc_as": 1237975178858.3005,
            "fc_b_as": 280700976186.749,
            "fc_nb_as": 957274202671.5511,
            "fc_h_as": 129796725405.52016,
            "fc_i_as": 645389733071.6042,
            "fc_a_as": 24366009176.830105,
            "fc_e_as": 669755742248.4344,
            "fc_q_as": 157721735017.59558,
            "fc_all_fn": 477,
            "fc_b_fn": 88,
            "fc_nb_fn": 389,
            "fc_h_fn": 153,
            "fc_i_fn": 188,
            "fc_a_fn": 22,
            "fc_e_fn": 210,
            "fc_q_fn": 26,
            "fc_as_d": "2026-03-17T16:00:00.000Z",
            "stockCode": "50030000"
        }
    ]
}
```
