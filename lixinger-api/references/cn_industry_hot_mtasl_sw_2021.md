# API文档/大陆/行业接口/申万2021版/热度数据/融资融券

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mtasl/sw_2021
> API Key: `cn/industry/hot/mtasl/sw_2021`

---

## 融资融券API

**简要描述:** 获取融资融券数据。

**请求URL:** `https://open.lixinger.com/api/cn/industry/hot/mtasl/sw_2021`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mtasl/sw_2021](https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mtasl/sw_2021)

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
            "mtaslb_sb": 358326468.86,
            "mtaslb_fb": 197602788627,
            "mtaslb": 197961115095.86,
            "mtaslb_mc_r": 0.026044354825162604,
            "fb_mc_rc_d1": -0.000019713865477707892,
            "fb_mc_rc_d5": 0.00008684899462403726,
            "fb_mc_rc_d20": 0.00018478646443001803,
            "fb_mc_rc_d60": 0.0013223663036888128,
            "fb_mc_rc_d120": 0.0013956998969413285,
            "sb_mc_rc_d1": 0.0000015483607573408718,
            "sb_mc_rc_d5": 0.000002986210727401379,
            "sb_mc_rc_d20": 0.000004285566272369595,
            "sb_mc_rc_d60": 0.000024660331411740625,
            "sb_mc_rc_d120": 0.00001941797926016951,
            "npa_o_f_d1": -149843559,
            "npa_o_f_d120": 14828853542,
            "npa_o_f_d20": 1697275236,
            "npa_o_f_d5": 805204545,
            "npa_o_f_d60": 12177076121,
            "fb_mc_rc_ys": 0.0016402910783650893,
            "npa_o_f_ys": 14000339284,
            "fb_mc_rc_d240": 0.0032383577588212848,
            "npa_o_f_d240": 21214463239,
            "stockCode": "490000"
        }
    ]
}
```
