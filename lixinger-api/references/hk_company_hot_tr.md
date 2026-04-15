# API文档/香港/公司接口/热度数据/换手率

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/company/hot/tr
> API Key: `hk/company/hot/tr`

---

## 换手率API

**简要描述:** 获取换手率数据。

**请求URL:** `https://open.lixinger.com/api/hk/company/hot/tr`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/company/hot/tr](https://www.lixinger.com/api/open-api/html-doc/hk/company/hot/tr)

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
            "last_data_date": "2026-03-19T00:00:00+08:00",
            "tr_d1": 0.006526515017004126,
            "tr_d5": 0.01592930684994488,
            "tr_d10": 0.0364526303873274,
            "tr_d20": 0.06668940481393704,
            "tr_d60": 0.17482662908157573,
            "tr_d120": 0.2789248304102762,
            "tr_d240": 0.5605876685074678,
            "spc": -0.0681,
            "ta": 30817089730,
            "stockCode": "00700"
        }
    ]
}
```
