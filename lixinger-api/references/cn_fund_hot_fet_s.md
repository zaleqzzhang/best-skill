# API文档/大陆/基金接口/公募基金接口/热度数据/最新场内份额信息

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/fund/hot/fet_s
> API Key: `cn/fund/hot/fet_s`

---

## 最新场内份额信息API

**简要描述:** 获取最新场内份额信息数据。

**请求URL:** `https://open.lixinger.com/api/cn/fund/hot/fet_s`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund/hot/fet_s](https://www.lixinger.com/api/open-api/html-doc/cn/fund/hot/fet_s)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 基金代码数组。 stockCodes长度>=1且<=100，格式如下：["161725","005827"]。 请参考 基金信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| last_data_date | Date | 数据时间 |
| fet_s_d_nv | Number | 净值 |
| fet_s_d_nv_cr | Number | 净值涨跌幅 |
| fet_s | Number | 基金场内份额 |
| fet_s_d_as | Number | 基金场内规模 |
| fet_s_ni_1d | Number | 过去1个交易日场内基金资金净流入 |
| fet_s_ni_5d | Number | 过去5个交易日场内基金资金净流入 |
| fet_s_ni_20d | Number | 过去20个交易日场内基金资金净流入 |
| fet_s_ni_60d | Number | 过去60个交易日场内基金资金净流入 |
| fet_s_ni_120d | Number | 过去120个交易日场内基金资金净流入 |
| fet_s_ni_240d | Number | 过去240个交易日场内基金资金净流入 |
| fet_s_rc_1d | Number | 过去1个交易日场内基金份额变化 |
| fet_s_rc_5d | Number | 过去5个交易日场内基金份额变化 |
| fet_s_rc_20d | Number | 过去20个交易日场内基金份额变化 |
| fet_s_rc_60d | Number | 过去60个交易日场内基金份额变化 |
| fet_s_rc_120d | Number | 过去120个交易日场内基金份额变化 |
| fet_s_rc_240d | Number | 过去240个交易日场内基金份额变化 |

### 示例

```json
{
    "stockCodes": [
        "161725",
        "005827"
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
            "type": "fet_s",
            "f_ets": 1193228027,
            "f_ets_d": "2022-02-10T00:00:00+08:00",
            "f_ets_rc_120d": 0.7342469529537468,
            "f_ets_rc_1d": -0.0033058337738748377,
            "f_ets_rc_20d": 0.1938365863937508,
            "f_ets_rc_5d": 0.0021024374516934374,
            "f_ets_rc_60d": 0.15476643609939458,
            "fet_s": 3303387622,
            "fet_s_d": "2025-03-10T00:00:00+08:00",
            "fet_s_rc_120d": 0.39882194461796466,
            "fet_s_rc_1d": 0.0013051819765167866,
            "fet_s_rc_20d": 0.058641576214804446,
            "fet_s_rc_5d": 0.007777878143415288,
            "fet_s_rc_60d": 0.22337127025536224,
            "fet_s_ni_120d": 673232000.2382998,
            "fet_s_ni_1d": 2828547.0238,
            "fet_s_ni_20d": 120445491.2878,
            "fet_s_ni_5d": 17018702.3691,
            "fet_s_ni_60d": 416234726.36509997,
            "fet_s_d_as": 2169995328.8918,
            "fet_s_d_nv": 0.6569,
            "fet_s_d_nv_cr": -0.014699265036748121,
            "last_data_date": 1773849600000,
            "fet_s_ni_240d": 1303803321.0762005,
            "fet_s_rc_240d": 1.1437327540494144,
            "stockCode": "161725"
        }
    ]
}
```
