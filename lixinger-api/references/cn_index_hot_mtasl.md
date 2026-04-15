# API文档/大陆/指数接口/热度数据/融资融券

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/mtasl
> API Key: `cn/index/hot/mtasl`

---

## 融资融券API

**简要描述:** 获取融资融券数据。

**请求URL:** `https://open.lixinger.com/api/cn/index/hot/mtasl`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/mtasl](https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/mtasl)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 指数代码数组。 stockCodes长度>=1且<=100，格式如下：["000016"]。 请参考 指数信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| last_data_date | Date | 数据时间 |
| cpc | Number | 涨跌幅 |
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
        "000016"
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
            "spc": 0.022797252251715402,
            "mtaslb_sb": 926011812.54,
            "mtaslb_fb": 286922961045,
            "mtaslb": 287848972857.54,
            "mtaslb_mc_r": 0.010120674920583318,
            "fb_mc_rc_d1": -0.000024506310794917948,
            "fb_mc_rc_d5": -0.00006154931589251054,
            "fb_mc_rc_d20": -0.00008445537342320446,
            "fb_mc_rc_d60": 0.0008258051859459082,
            "fb_mc_rc_d120": 0.0014598152071685281,
            "sb_mc_rc_d1": 6.749531073929412e-7,
            "sb_mc_rc_d5": -0.0000012658752194814802,
            "sb_mc_rc_d20": -0.0000039618947448132055,
            "sb_mc_rc_d60": 0.000003632621058576301,
            "sb_mc_rc_d120": 0.000008329781386924407,
            "cpc": -0.015262896641149654,
            "npa_o_f_d1": -697000579,
            "npa_o_f_d120": 33498444893,
            "npa_o_f_d20": -2441426681,
            "npa_o_f_d5": -1751534415,
            "npa_o_f_d60": 24424163292,
            "fb_mc_rc_ys": 0.0009256022120375699,
            "npa_o_f_ys": 27219502217,
            "fb_mc_rc_d240": 0.003195176358764539,
            "npa_o_f_d240": 86018094480,
            "stockCode": "000016"
        }
    ]
}
```
