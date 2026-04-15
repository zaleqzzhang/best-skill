# API文档/香港/指数接口/热度数据/互联互通

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/index/hot/mm_ah
> API Key: `hk/index/hot/mm_ah`

---

## 互联互通API

**简要描述:** 获取互联互通数据。

**请求URL:** `https://open.lixinger.com/api/hk/index/hot/mm_ah`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/index/hot/mm_ah](https://www.lixinger.com/api/open-api/html-doc/hk/index/hot/mm_ah)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 指数代码数组。 stockCodes长度>=1且<=100，格式如下：["HSI"]。 请参考 指数信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| last_data_date | Date | 数据时间 |
| cpc | Number | 涨跌幅 |
| mm_sha | Number | 港股通持仓金额 |
| mm_sha_mc_r | Number | 港股通持仓金额占市值比例 |
| mm_sh_nba_d1 | Number | 港股通过去1个交易日净买入金额 |
| mm_sh_nba_d5 | Number | 港股通过去5个交易日净买入金额 |
| mm_sh_nba_d20 | Number | 港股通过去20个交易日净买入金额 |
| mm_sh_nba_d60 | Number | 港股通过去60个交易日净买入金额 |
| mm_sh_nba_d120 | Number | 港股通过去120个交易日净买入金额 |
| mm_sh_nba_d240 | Number | 港股通过去240个交易日净买入金额 |
| mm_sh_nba_ys | Number | 港股通今年以来净买入金额 |
| mm_sha_mc_rc_d1 | Number | 港股通过去1个交易日持股金额占市值变化比例 |
| mm_sha_mc_rc_d5 | Number | 港股通过去5个交易日持股金额占市值变化比例 |
| mm_sha_mc_rc_d20 | Number | 港股通过去20个交易日持股金额占市值变化比例 |
| mm_sha_mc_rc_d60 | Number | 港股通过去60个交易日持股金额占市值变化比例 |
| mm_sha_mc_rc_d120 | Number | 港股通过去120个交易日持股金额占市值变化比例 |
| mm_sha_mc_rc_d240 | Number | 港股通过去240个交易日持股金额占市值变化比例 |
| mm_sha_mc_rc_ys | Number | 港股通今年以來持股金额占市值变化比例 |

### 示例

```json
{
    "stockCodes": [
        "HSI"
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
            "last_data_date": "2026-01-13T00:00:00+08:00",
            "spc": -0.015201790494398565,
            "mm_sha": 4134261936936,
            "mm_sha_mc_r": 0.09362080659745317,
            "mm_sh_nba_d1": 1282014918.1119783,
            "mm_sh_nba_d5": 7492482662.237818,
            "mm_sh_nba_d20": 78733862834.68509,
            "mm_sh_nba_d60": 215699073292.34625,
            "mm_sh_nba_d120": 366326640320.4986,
            "mm_sh_nba_d240": 806952952425.7264,
            "mm_sha_mc_rc_d1": -0.00003321192598187972,
            "mm_sha_mc_rc_d5": -0.000059270710015837946,
            "mm_sha_mc_rc_d20": 0.0010126984684258183,
            "mm_sha_mc_rc_d60": 0.004335384339413689,
            "mm_sha_mc_rc_d120": 0.008300566029887393,
            "mm_sha_mc_rc_d240": 0.02119083107418636,
            "cpc": 0.009019305123780148,
            "mm_sh_nba_ys": 760093260374.2798,
            "mm_sha_mc_rc_ys": 0.01825131511935829,
            "stockCode": "HSI"
        }
    ]
}
```
