# API文档/大陆/公司接口/热度数据/换手率

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/tr
> API Key: `cn/company/hot/tr`

---

## 换手率API

**简要描述:** 获取换手率数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/hot/tr`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/tr](https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/tr)

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
| ta | Number | 成交金额 |
| tr_d1 | Number | 过去1个交易日换手率 |
| tr_d5 | Number | 过去5个交易日换手率 |
| tr_d10 | Number | 过去10个交易日换手率 |
| tr_d20 | Number | 过去20个交易日换手率 |
| tr_d60 | Number | 过去60个交易日换手率 |
| tr_d120 | Number | 过去120个交易日换手率 |
| tr_d240 | Number | 过去240个交易日换手率 |

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
            "tr_d1": 0.006880217278739824,
            "tr_d5": 0.038700018191301436,
            "tr_d10": 0.08339525961933233,
            "tr_d20": 0.15032938908361862,
            "tr_d60": 0.43887646108852835,
            "tr_d120": 0.8854072020281178,
            "tr_d240": 1.634617517861922,
            "spc": -0.0038,
            "ta": 11867380765,
            "stockCode": "300750"
        },
        {
            "last_data_date": "2026-03-19T00:00:00+08:00",
            "tr_d1": 0.00242112282451755,
            "tr_d5": 0.01669112604423,
            "tr_d10": 0.02813154826971589,
            "tr_d20": 0.059410819732704415,
            "tr_d60": 0.2234798820955747,
            "tr_d120": 0.3859686944642373,
            "tr_d240": 0.7022066461049584,
            "spc": -0.0108,
            "ta": 4404953481,
            "stockCode": "600519"
        },
        {
            "tr_d1": 0.05318682025747052,
            "tr_d5": 0.320954312892083,
            "tr_d15": 1.1102576586470467,
            "tr_m1": 1.701696410730352,
            "tr_m3": 3.5592374004832616,
            "tr_m6": 4.417871373528347,
            "tr_y1": 5.731797406295671,
            "last_data_date": "2026-03-19T00:00:00+08:00",
            "tr_d10": 0.7774094534745003,
            "tr_d120": 5.743432446478123,
            "tr_d20": 1.5876336534666484,
            "tr_d240": 8.20165961817245,
            "tr_d60": 2.9293737376222793,
            "spc": 0,
            "ta": 2170597916,
            "stockCode": "600157"
        }
    ]
}
```
