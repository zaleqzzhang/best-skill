# API文档/大陆/行业接口/申万/热度数据/互联互通

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mm_ha/sw
> API Key: `cn/industry/hot/mm_ha/sw`

---

## 互联互通API

**简要描述:** 获取互联互通数据。

**请求URL:** `https://open.lixinger.com/api/cn/industry/hot/mm_ha/sw`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mm_ha/sw](https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mm_ha/sw)

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
            "mm_sh_nba_d1": -35055350093.169685,
            "mm_sh_nba_d5": -35055350093.169685,
            "mm_sh_nba_d20": -35055350093.169685,
            "mm_sh_nba_d60": -35055350093.169685,
            "mm_sh_nba_d120": -26713848552.57677,
            "mm_sh_nba_d240": -12725560779.380835,
            "mm_sha": 126612966905,
            "mm_sha_mc_r": 0.015618532971079008,
            "mm_sha_mc_rc_d1": 0.0021543386845829134,
            "mm_sha_mc_rc_d120": 0.002385326435736756,
            "mm_sha_mc_rc_d20": 0.0021298419869506674,
            "mm_sha_mc_rc_d5": 0.002158775829181468,
            "mm_sha_mc_rc_d60": 0.0009934832503658113,
            "mm_sha_mc_rc_d240": -0.0018626657031417457,
            "mm_sh_nba_ys": -28617551567.48706,
            "mm_sh_nba_q1": -9109459991.057096,
            "mm_sh_nba_q2": -44164810084.22678,
            "mm_sh_nba_q3": -35823308543.63387,
            "mm_sh_nba_q4": -37727011558.54416,
            "mm_sha_mc_rc_q1": -0.0013604788668227213,
            "mm_sha_mc_rc_q2": -0.005457375023122114,
            "mm_sha_mc_rc_q3": -0.004463891772756303,
            "mm_sha_mc_rc_q4": -0.00525041830387629,
            "stockCode": "490000"
        }
    ]
}
```
