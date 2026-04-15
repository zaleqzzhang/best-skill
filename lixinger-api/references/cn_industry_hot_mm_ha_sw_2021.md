# API文档/大陆/行业接口/申万2021版/热度数据/互联互通

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mm_ha/sw_2021
> API Key: `cn/industry/hot/mm_ha/sw_2021`

---

## 互联互通API

**简要描述:** 获取互联互通数据。

**请求URL:** `https://open.lixinger.com/api/cn/industry/hot/mm_ha/sw_2021`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mm_ha/sw_2021](https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mm_ha/sw_2021)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 行业代码数组。 stockCodes长度>=1且<=100，格式如下：["490000"]。 请参考 行业信息API 获取合法的stockCode。 |

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
        "490000"
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
            "mm_sh_nba_d1": -35012210206.33032,
            "mm_sh_nba_d5": -35012210206.33032,
            "mm_sh_nba_d20": -35012210206.33032,
            "mm_sh_nba_d60": -35012210206.33032,
            "mm_sh_nba_d120": -26612683751.220757,
            "mm_sh_nba_d240": -12664233119.014938,
            "mm_sha": 126938802928,
            "mm_sha_mc_r": 0.015606838048527699,
            "mm_sha_mc_rc_d1": 0.0021601429848808855,
            "mm_sha_mc_rc_d120": 0.002354704210495287,
            "mm_sha_mc_rc_d20": 0.0021376901168692897,
            "mm_sha_mc_rc_d5": 0.0021654971916669624,
            "mm_sha_mc_rc_d60": 0.000974885466531062,
            "mm_sha_mc_rc_d240": -0.0018569194464212145,
            "mm_sh_nba_ys": -28635123019.99491,
            "mm_sh_nba_q1": -9038749718.544529,
            "mm_sh_nba_q2": -44050959924.87485,
            "mm_sh_nba_q3": -35651433469.76528,
            "mm_sh_nba_q4": -37673872738.53944,
            "mm_sha_mc_rc_q1": -0.0013489147055201888,
            "mm_sha_mc_rc_q2": -0.005412174155838728,
            "mm_sha_mc_rc_q3": -0.004437288689307666,
            "mm_sha_mc_rc_q4": -0.005241844289460186,
            "stockCode": "490000"
        }
    ]
}
```
