# API文档/大陆/公司接口/热度数据/融资融券

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/mtasl
> API Key: `cn/company/hot/mtasl`

---

## 融资融券API

**简要描述:** 获取融资融券数据。

**说明:**

- 计算股本为流通A股

**请求URL:** `https://open.lixinger.com/api/cn/company/hot/mtasl`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/mtasl](https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/mtasl)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 股票代码数组。 stockCodes长度>=1且<=100，格式如下：["300750","600519","600157"]。 请参考 股票信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| last_data_date | Date | 数据时间 |
| spc | Number | 涨跌幅 |
| mtaslb_fb | Number | 融资余额 |
| mtaslb_sb | Number | 融券余额 |
| mtaslb | Number | 融资融券余额 |
| mtaslb_mc_r | Number | 融资融券余额占流通A股市值比例 |
| mtaslb_fbc | Number | 新增融资余额 |
| mtaslb_smc | Number | 新增融券余量 |
| npa_o_f_d1 | Number | 过去1个交易日融资净买入金额 |
| npa_o_f_d5 | Number | 过去5个交易日融资净买入金额 |
| npa_o_f_d20 | Number | 过去20个交易日融资净买入金额 |
| npa_o_f_d60 | Number | 过去60个交易日融资净买入金额 |
| npa_o_f_d120 | Number | 过去120个交易日融资净买入金额 |
| npa_o_f_d240 | Number | 过去240个交易日融资净买入金额 |
| fb_mc_rc_d1 | Number | 过去1个交易日融资余额占流通市值变化比例 |
| fb_mc_rc_d5 | Number | 过去5个交易日融资余额占流通市值变化比例 |
| fb_mc_rc_d20 | Number | 过去20个交易日融资余额占流通市值变化比例 |
| fb_mc_rc_d60 | Number | 过去60个交易日融资余额占流通市值变化比例 |
| fb_mc_rc_d120 | Number | 过去120个交易日融资余额占流通市值变化比例 |
| fb_mc_rc_d240 | Number | 过去240个交易日融资余额占流通市值变化比例 |

### 示例

```json
{
    "stockCodes": [
        "300750",
        "600519",
        "600157"
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
            "spc": -0.0038,
            "mtaslb": 20649244665,
            "mtaslb_mc_r": 0.012112529495903567,
            "mtaslb_fbc": -57590559,
            "mtaslb_fb": 20552054529,
            "mtaslb_smc": 11800,
            "mtaslb_sb": 97190136,
            "fb_mc_rc_d1": -0.00003378173661506541,
            "fb_mc_rc_d5": -0.000006620131922083742,
            "fb_mc_rc_d20": -0.0008491146338510915,
            "fb_mc_rc_d60": -0.0007095426972709686,
            "fb_mc_rc_d120": 0.004932491092931517,
            "sb_mc_rc_d1": -0.000005559072258673159,
            "sb_mc_rc_d5": 5.734560173144818e-7,
            "sb_mc_rc_d20": 0.000018615421136372605,
            "sb_mc_rc_d60": 0.000026871652872358173,
            "sb_mc_rc_d120": 0.000017049081248738734,
            "npa_o_f_d1": -57590559,
            "npa_o_f_d120": 8142840308,
            "npa_o_f_d20": -1327440173,
            "npa_o_f_d5": -14918413,
            "npa_o_f_d60": -1138184417,
            "fb_mc_rc_d240": 0.008660505253887858,
            "npa_o_f_d240": 12911852575,
            "stockCode": "300750"
        },
        {
            "last_data_date": "2026-03-19T00:00:00+08:00",
            "spc": -0.0108,
            "mtaslb": 17165908811.55,
            "mtaslb_mc_r": 0.009435001940921674,
            "mtaslb_fbc": -107103703,
            "mtaslb_fb": 17063241753,
            "mtaslb_smc": -8400,
            "mtaslb_sb": 102667058.55,
            "fb_mc_rc_d1": -0.000058868053930530756,
            "fb_mc_rc_d5": -0.000222941200086483,
            "fb_mc_rc_d20": -0.0001107762636050441,
            "fb_mc_rc_d60": -0.00018659605598484743,
            "fb_mc_rc_d120": 0.0004640638666558012,
            "sb_mc_rc_d1": -0.0000026424237461263856,
            "sb_mc_rc_d5": 0.0000026183934837518345,
            "sb_mc_rc_d20": -0.000017322641000172176,
            "sb_mc_rc_d60": -0.00001261857633391173,
            "sb_mc_rc_d120": -0.0000034641682148831842,
            "npa_o_f_d1": -107103704,
            "npa_o_f_d120": 526641451,
            "npa_o_f_d20": -235331111,
            "npa_o_f_d5": -408263605,
            "npa_o_f_d60": -633341366,
            "fb_mc_rc_d240": 0.0007752508392627393,
            "npa_o_f_d240": 972831538,
            "stockCode": "600519"
        },
        {
            "last_data_date": "2026-03-19T00:00:00+08:00",
            "spc": 0,
            "mtaslb": 1666614069,
            "mtaslb_mc_r": 0.041068785206397174,
            "mtaslb_fbc": -31147564,
            "mtaslb_fb": 1646888025,
            "mtaslb_smc": -803300,
            "mtaslb_sb": 19726044,
            "fb_mc_rc_d1": -0.0007675397918523806,
            "fb_mc_rc_d5": -0.001749114904622378,
            "fb_mc_rc_d20": 0.008866543790079721,
            "fb_mc_rc_d60": 0.005857617525259515,
            "fb_mc_rc_d120": 0.013838777877505136,
            "sb_mc_rc_d1": 0.0000025712992232917,
            "sb_mc_rc_d5": 0.000022791526632948648,
            "sb_mc_rc_d20": -0.00003993414596578447,
            "sb_mc_rc_d60": 0.00003158099981344388,
            "sb_mc_rc_d120": -0.00002518160917353407,
            "npa_o_f_d1": -31147563,
            "npa_o_f_d120": 557390061,
            "npa_o_f_d20": 369916804,
            "npa_o_f_d5": -73693549,
            "npa_o_f_d60": 263458431,
            "fb_mc_rc_d240": 0.005599037902711058,
            "npa_o_f_d240": 317114154,
            "stockCode": "600157"
        }
    ]
}
```
