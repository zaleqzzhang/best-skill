# API文档/大陆/行业接口/国证/热度数据/融资融券

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mtasl/cni
> API Key: `cn/industry/hot/mtasl/cni`

---

## 融资融券API

**简要描述:** 获取融资融券数据。

**请求URL:** `https://open.lixinger.com/api/cn/industry/hot/mtasl/cni`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mtasl/cni](https://www.lixinger.com/api/open-api/html-doc/cn/industry/hot/mtasl/cni)

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
            "last_data_date": "2026-03-19T00:00:00+08:00",
            "mtaslb_sb": 603190594.2,
            "mtaslb_fb": 273316429536,
            "mtaslb": 273919620130.2,
            "mtaslb_mc_r": 0.01215600053796096,
            "fb_mc_rc_d1": -0.000011052318737080405,
            "fb_mc_rc_d5": -0.000025103717069549565,
            "fb_mc_rc_d20": -0.0000028360403129946006,
            "fb_mc_rc_d60": 0.0005670566316029824,
            "fb_mc_rc_d120": 0.0007402989751419339,
            "sb_mc_rc_d1": 9.334782053707629e-7,
            "sb_mc_rc_d5": -4.1123952788790006e-7,
            "sb_mc_rc_d20": -0.0000029943868749168857,
            "sb_mc_rc_d60": 0.000006784583048965865,
            "sb_mc_rc_d120": 0.000008232307749173073,
            "npa_o_f_d1": -249049585,
            "npa_o_f_d120": 20008952720,
            "npa_o_f_d20": 171567526,
            "npa_o_f_d5": -420091408,
            "npa_o_f_d60": 14391317366,
            "fb_mc_rc_ys": 0.0007388045155442005,
            "npa_o_f_ys": 17710205862,
            "fb_mc_rc_d240": 0.002083135755300472,
            "npa_o_f_d240": 40160661961,
            "stockCode": "C07"
        }
    ]
}
```
