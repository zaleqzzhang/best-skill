# API文档/大陆/基金接口/基金公司接口/热度数据/基金公司资产规模排名

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/fund-company/hot/fc_asr
> API Key: `cn/fund-company/hot/fc_asr`

---

## 基金公司资产规模排名API

**简要描述:** 获取基金公司资产规模排名数据。

**请求URL:** `https://open.lixinger.com/api/cn/fund-company/hot/fc_asr`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund-company/hot/fc_asr](https://www.lixinger.com/api/open-api/html-doc/cn/fund-company/hot/fc_asr)

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
| fc_as_r_d | Date | 最新数据时间 |
| fc_as_rp | Number | 资产规模排名 |
| fc_nb_as_rp | Number | 非债券基金资产规模排名 |
| fc_h_as_rp | Number | 混合型资产规模排名 |
| fc_e_as_rp | Number | 股票型资产规模排名 |
| fc_q_as_rp | Number | QDII型资产规模排名 |
| fc_b_as_rp | Number | 债券型资产规模排名 |
| fc_all_fn | Number | 基金数量 |
| fc_all_mn | Number | 基金经理数量 |
| fc_all_fn_rp | Number | 基金数量排名 |

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
            "type": "fc_asr",
            "fc_as_r_d": "2026-03-17T16:00:00.000Z",
            "fc_rc": 219,
            "fc_as_rp": 0,
            "fc_b_as_rp": 0.0045871559633027525,
            "fc_nb_as_rp": 0,
            "fc_h_as_rp": 0,
            "fc_i_as_rp": 0.0045871559633027525,
            "fc_a_as_rp": 0.0045871559633027525,
            "fc_e_as_rp": 0.0045871559633027525,
            "fc_q_as_rp": 0.0045871559633027525,
            "fc_all_fn_rp": 0.03211009174311927,
            "fc_b_fn_rp": 0.06422018348623854,
            "fc_nb_fn_rp": 0.01834862385321101,
            "fc_h_fn_rp": 0.04128440366972477,
            "fc_i_fn_rp": 0.009174311926605505,
            "fc_a_fn_rp": 0.045871559633027525,
            "fc_e_fn_rp": 0.009174311926605505,
            "fc_q_fn_rp": 0,
            "fc_a_fn": 20,
            "fc_all_fn": 417,
            "fc_all_mn": 104,
            "fc_b_fn": 73,
            "fc_e_fn": 181,
            "fc_h_fn": 134,
            "fc_i_fn": 161,
            "fc_nb_fn": 344,
            "fc_q_fn": 29,
            "stockCode": "50110000"
        },
        {
            "type": "fc_asr",
            "fc_as_r_d": "2026-03-17T16:00:00.000Z",
            "fc_rc": 219,
            "fc_as_rp": 0.0045871559633027525,
            "fc_b_as_rp": 0.04128440366972477,
            "fc_nb_as_rp": 0.0045871559633027525,
            "fc_h_as_rp": 0.03211009174311927,
            "fc_i_as_rp": 0,
            "fc_a_as_rp": 0.03669724770642202,
            "fc_e_as_rp": 0,
            "fc_q_as_rp": 0,
            "fc_all_fn_rp": 0,
            "fc_b_fn_rp": 0.03211009174311927,
            "fc_nb_fn_rp": 0,
            "fc_h_fn_rp": 0.013761467889908258,
            "fc_i_fn_rp": 0,
            "fc_a_fn_rp": 0.03211009174311927,
            "fc_e_fn_rp": 0,
            "fc_q_fn_rp": 0.0045871559633027525,
            "fc_a_fn": 22,
            "fc_all_fn": 493,
            "fc_all_mn": 91,
            "fc_b_fn": 91,
            "fc_e_fn": 220,
            "fc_h_fn": 155,
            "fc_i_fn": 198,
            "fc_nb_fn": 402,
            "fc_q_fn": 27,
            "stockCode": "50030000"
        }
    ]
}
```
