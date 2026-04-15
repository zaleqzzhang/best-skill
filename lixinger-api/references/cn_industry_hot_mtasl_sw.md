# API文档/大陆/行业接口/申万/热度数据/融资融券

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mtasl/sw
> API Key: `cn/industry/hot/mtasl/sw`

---

## 融资融券API

**简要描述:** 获取融资融券数据。

**请求URL:** `https://open.lixinger.com/api/cn/industry/hot/mtasl/sw`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mtasl/sw](https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mtasl/sw)

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
| mtaslb_fb | Number | 融资余额 |
| mtaslb_sb | Number | 融券余额 |
| mtaslb | Number | 融资融券余额 |
| mtaslb_mc_r | Number | 融资融券余额占市值比例 |
| npa_o_f_d1 | Number | 过去1个交易日融资净买入金额 |
| npa_o_f_d5 | Number | 过去5个交易日融资净买入金额 |
| npa_o_f_d20 | Number | 过去20个交易日融资净买入金额 |
| npa_o_f_d60 | Number | 过去60个交易日融资净买入金额 |
| npa_o_f_d120 | Number | 过去120个交易日融资净买入金额 |
| npa_o_f_d240 | Number | 过去240个交易日融资净买入金额 |
| npa_o_f_ys | Number | 今年以来融资净买入金额 |
| fb_mc_rc_d1 | Number | 过去1个交易日融资余额占市值变化比例 |
| fb_mc_rc_d5 | Number | 过去5个交易日融资余额占市值变化比例 |
| fb_mc_rc_d20 | Number | 过去20个交易日融资余额占市值变化比例 |
| fb_mc_rc_d60 | Number | 过去60个交易日融资余额占市值变化比例 |
| fb_mc_rc_d120 | Number | 过去120个交易日融资余额占市值变化比例 |
| fb_mc_rc_d240 | Number | 过去240个交易日融资余额占市值变化比例 |
| fb_mc_rc_ys | Number | 今年以来融资余额占市值变化比例 |

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
            "last_data_date": "2026-03-19T00:00:00+08:00",
            "mtaslb_sb": 356292572.86,
            "mtaslb_fb": 196122348983,
            "mtaslb": 196478641555.86,
            "mtaslb_mc_r": 0.025933384543486815,
            "fb_mc_rc_d1": -0.000017448611504078388,
            "fb_mc_rc_d5": 0.00008514953727647138,
            "fb_mc_rc_d20": 0.0001720486866722948,
            "fb_mc_rc_d60": 0.0012666843034360084,
            "fb_mc_rc_d120": 0.0013712529266768152,
            "sb_mc_rc_d1": 0.000001601838443079755,
            "sb_mc_rc_d5": 0.0000029440281306335394,
            "sb_mc_rc_d20": 0.00000418383645275609,
            "sb_mc_rc_d60": 0.00002454746452416465,
            "sb_mc_rc_d120": 0.00001929452304238898,
            "npa_o_f_d1": -132195607,
            "npa_o_f_d120": 14581498161,
            "npa_o_f_d20": 1597625010,
            "npa_o_f_d5": 789689059,
            "npa_o_f_d60": 11694299840,
            "fb_mc_rc_ys": 0.0016276115332315552,
            "npa_o_f_ys": 13859762879,
            "fb_mc_rc_d240": 0.003170705496469886,
            "npa_o_f_d240": 20611905104,
            "stockCode": "490000"
        }
    ]
}
```
