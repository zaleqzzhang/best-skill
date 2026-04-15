# API文档/香港/公司接口/热度数据/互联互通

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/company/hot/mm_ah
> API Key: `hk/company/hot/mm_ah`

---

## 互联互通API

**简要描述:** 获取互联互通数据。

**说明:**

- 计算股本为总H股

**请求URL:** `https://open.lixinger.com/api/hk/company/hot/mm_ah`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/company/hot/mm_ah](https://www.lixinger.com/api/open-api/html-doc/hk/company/hot/mm_ah)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 股票代码数组。 stockCodes长度>=1且<=100，格式如下：["00700"]。 请参考 股票信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| last_data_date | Date | 数据时间 |
| mm_sh | Number | 港股通持仓 |
| mm_sha | Number | 港股通持仓金额 |
| mm_sh_cap_r | Number | 港股通持仓占H股比例 |
| spc | Number | 涨跌幅 |
| mm_sh_nba_d1 | Number | 港股通过去1个交易日净买入金额 |
| mm_sh_nba_d5 | Number | 港股通过去5个交易日净买入金额 |
| mm_sh_nba_d20 | Number | 港股通过去20个交易日净买入金额 |
| mm_sh_nba_d60 | Number | 港股通过去60个交易日净买入金额 |
| mm_sh_nba_d120 | Number | 港股通过去120个交易日净买入金额 |
| mm_sh_nba_d240 | Number | 港股通过去240个交易日净买入金额 |
| mm_sh_cap_rc_d1 | Number | 港股通过去1个交易日持仓占H股变化比例 |
| mm_sh_cap_rc_d5 | Number | 港股通过去5个交易日持仓占H股变化比例 |
| mm_sh_cap_rc_d20 | Number | 港股通过去20个交易日持仓占H股变化比例 |
| mm_sh_cap_rc_d60 | Number | 港股通过去60个交易日持仓占H股变化比例 |
| mm_sh_cap_rc_d120 | Number | 港股通过去120个交易日持仓占H股变化比例 |
| mm_sh_cap_rc_d240 | Number | 港股通过去240个交易日持仓占H股变化比例 |
| mm_shc_v_r | Number | 港股通过去1个交易日持仓变化占成交量比例 |
| mm_shc_v_r_d5 | Number | 港股通过去5个交易日持仓变化占成交量比例 |
| mm_shc_v_r_d20 | Number | 港股通过去20个交易日持仓变化占成交量比例 |
| mm_shc_v_r_d60 | Number | 港股通过去60个交易日持仓变化占成交量比例 |
| mm_shc_v_r_d120 | Number | 港股通过去120个交易日持仓变化占成交量比例 |
| mm_shc_v_r_d240 | Number | 港股通过去240个交易日持仓变化占成交量比例 |
| mm_sh_nbv_d1 | Number | 港股通过去1个交易日净买入股数 |
| mm_sh_nbv_d5 | Number | 港股通过去5个交易日净买入股数 |
| mm_sh_nbv_d20 | Number | 港股通过去20个交易日净买入股数 |
| mm_sh_nbv_d60 | Number | 港股通过去60个交易日净买入股数 |
| mm_sh_nbv_d120 | Number | 港股通过去120个交易日净买入股数 |
| mm_sh_nbv_d240 | Number | 港股通过去240个交易日净买入股数 |
| mm_sh_nbp_d1 | Number | 港股通过去1个交易日净买入收益 |
| mm_sh_nbp_d5 | Number | 港股通过去5个交易日净买入收益 |
| mm_sh_nbp_d20 | Number | 港股通过去20个交易日净买入收益 |
| mm_sh_nbp_d60 | Number | 港股通过去60个交易日净买入收益 |
| mm_sh_nbp_d120 | Number | 港股通过去120个交易日净买入收益 |
| mm_sh_nbp_d240 | Number | 港股通过去240个交易日净买入收益 |
| mm_sh_nbpr_d1 | Number | 港股通过去1个交易日净买入收益率 |
| mm_sh_nbpr_d5 | Number | 港股通过去5个交易日净买入收益率 |
| mm_sh_nbpr_d20 | Number | 港股通过去20个交易日净买入收益率 |
| mm_sh_nbpr_d60 | Number | 港股通过去60个交易日净买入收益率 |
| mm_sh_nbpr_d120 | Number | 港股通过去120个交易日净买入收益率 |
| mm_sh_nbpr_d240 | Number | 港股通过去240个交易日净买入收益率 |

### 示例

```json
{
    "stockCodes": [
        "00700"
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
            "mm_sh": 1085238279,
            "mm_sha": 596881053450,
            "mm_sh_cap_r": 0.1191737138437467,
            "spc": -0.0152,
            "mm_shc_v_r": -0.04999288680169006,
            "mm_sh_nba_d1": -635456020.3433539,
            "mm_sh_nba_d5": -222217410.54476166,
            "mm_sh_nba_d20": 18171578592.486744,
            "mm_sh_nba_d60": 45140689341.85745,
            "mm_sh_nba_d120": 43770974351.422264,
            "mm_sh_nba_d240": 20469560090.872757,
            "mm_sh_cap_rc_d1": -0.00012557009459147894,
            "mm_sh_cap_rc_d5": -0.000039061178271238006,
            "mm_sh_cap_rc_d20": 0.003821449603147384,
            "mm_sh_cap_rc_d60": 0.009209095904659681,
            "mm_sh_cap_rc_d120": 0.009300832171941595,
            "mm_sh_cap_rc_d240": 0.004836379752315795,
            "mm_sh_nbv_d1": -1143486,
            "mm_sh_nbv_d5": -355705,
            "mm_sh_nbv_d20": 34799481,
            "mm_sh_nbv_d60": 81207072,
            "mm_sh_nbv_d120": 78539429,
            "mm_sh_nbv_d240": 33236108,
            "mm_sh_nbp_d1": 48840509.24467098,
            "mm_sh_nbp_d5": 39893184.212967664,
            "mm_sh_nbp_d20": -318726080.9324729,
            "mm_sh_nbp_d60": -3476977721.915114,
            "mm_sh_nbp_d120": -3476401811.1905665,
            "mm_sh_nbp_d240": -3407886645.650902,
            "mm_sh_nbpr_d1": 0.07685899209559954,
            "mm_sh_nbpr_d5": 0.17952321609351085,
            "mm_sh_nbpr_d20": -0.017539812477505613,
            "mm_sh_nbpr_d60": -0.07702535722446376,
            "mm_sh_nbpr_d120": -0.07942253657137534,
            "mm_sh_nbpr_d240": -0.16648558300822772,
            "last_data_date": "2026-03-17T00:00:00+08:00",
            "mm_shc_v_r_d120": 0.019956408558236372,
            "mm_shc_v_r_d20": 0.08251506078850301,
            "mm_shc_v_r_d240": -0.0029462274575149045,
            "mm_shc_v_r_d5": 0.018875939442240846,
            "mm_shc_v_r_d60": 0.04461180175075257,
            "stockCode": "00700"
        }
    ]
}
```
