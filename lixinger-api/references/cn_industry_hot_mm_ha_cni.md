# API文档/大陆/行业接口/国证/热度数据/互联互通

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mm_ha/cni
> API Key: `cn/industry/hot/mm_ha/cni`

---

## 互联互通API

**简要描述:** 获取互联互通数据。

**请求URL:** `https://open.lixinger.com/api/cn/industry/hot/mm_ha/cni`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mm_ha/cni](https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mm_ha/cni)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 行业代码数组。 stockCodes长度>=1且<=100，格式如下：["C07"]。 请参考 行业信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| last_data_date | Date | 数据时间 |
| mm_sha | Number | 陆股通持仓金额 |
| mm_sha_mc_r | Number | 陆股通持仓金额占市值比例 |
| mm_sh_nba_q1 | Number | 陆股通过去1个季度净买入金额 |
| mm_sh_nba_q2 | Number | 陆股通过去2个季度净买入金额 |
| mm_sh_nba_q3 | Number | 陆股通过去3个季度净买入金额 |
| mm_sh_nba_q4 | Number | 陆股通过去4个季度净买入金额 |
| mm_sha_mc_rc_q1 | Number | 陆股通过去1个季度持股金额占市值变化比例 |
| mm_sha_mc_rc_q2 | Number | 陆股通过去2个季度持股金额占市值变化比例 |
| mm_sha_mc_rc_q3 | Number | 陆股通过去3个季度持股金额占市值变化比例 |
| mm_sha_mc_rc_q4 | Number | 陆股通过去4个季度持股金额占市值变化比例 |

### 示例

```json
{
    "stockCodes": [
        "C07"
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
            "last_data_date": "2025-12-31T00:00:00+08:00",
            "mm_sh_nba_d1": -91240953303.5497,
            "mm_sh_nba_d5": -91240953303.5497,
            "mm_sh_nba_d20": -91240953303.5497,
            "mm_sh_nba_d60": -91240953303.5497,
            "mm_sh_nba_d120": -80060447886.57718,
            "mm_sh_nba_d240": -75051510974.98085,
            "mm_sha": 303542752638,
            "mm_sha_mc_r": 0.012768915063650773,
            "mm_sha_mc_rc_d1": 0.0000670579788202251,
            "mm_sha_mc_rc_d120": 0.00032538484726338246,
            "mm_sha_mc_rc_d20": -0.00009078147741434575,
            "mm_sha_mc_rc_d5": 0.00008513862143655695,
            "mm_sha_mc_rc_d60": 0.00023601382618843383,
            "mm_sha_mc_rc_d240": -0.004218169719447872,
            "mm_sh_nba_ys": -77644122949.48085,
            "mm_sh_nba_q1": -14109854821.09236,
            "mm_sh_nba_q2": -105350808124.64206,
            "mm_sh_nba_q3": -94170302707.66953,
            "mm_sh_nba_q4": -91753977770.5732,
            "mm_sha_mc_rc_q1": -0.000916291871931825,
            "mm_sha_mc_rc_q2": -0.005190480976310649,
            "mm_sha_mc_rc_q3": -0.004954467150122216,
            "mm_sha_mc_rc_q4": -0.00497113751396913,
            "stockCode": "C07"
        }
    ]
}
```
