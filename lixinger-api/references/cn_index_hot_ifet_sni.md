# API文档/大陆/指数接口/热度数据/场内基金认购净流入

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/ifet_sni
> API Key: `cn/index/hot/ifet_sni`

---

## 场内基金认购净流入API

**简要描述:** 获取场内基金认购净流入数据。

**请求URL:** `https://open.lixinger.com/api/cn/index/hot/ifet_sni`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/ifet_sni](https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/ifet_sni)

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
| ifet_as | Number | 场内基金资产规模 |
| ifet_sni_ytd | Number | 过去1天场内基金认购净流入 |
| ifet_sni_w1 | Number | 过去1周场内基金认购净流入 |
| ifet_sni_w2 | Number | 过去2周场内基金认购净流入 |
| ifet_ssni_m1 | Number | 过去1个月场内基金认购净流入 |
| ifet_sni_m3 | Number | 过去3个月场内基金认购净流入 |
| ifet_sni_m6 | Number | 过去6个月场内基金认购净流入 |
| ifet_sni_y1 | Number | 过去1年场内基金认购净流入 |
| ifet_sni_y2 | Number | 过去2年场内基金认购净流入 |
| ifet_sni_fys | Number | 今年以来场内基金认购净流入 |

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
            "ifet_sni_w1": 1999720966.5900002,
            "ifet_sni_w2": 2153986323.53,
            "ifet_ssni_m1": -2192559964.2,
            "ifet_sni_m3": -108768691821.65999,
            "ifet_sni_m6": -110475408631.20998,
            "ifet_sni_y1": -99475482420.93,
            "ifet_sni_y2": -80280448534.04758,
            "ifet_sni_fys": -106476470099.45,
            "ifet_as": 76161669568.53001,
            "ifet_sni_ytd": -114064569.51000002,
            "spc": 0.022797252251715402,
            "last_data_date": "2026-03-19T00:00:00+08:00",
            "cpc": -0.015262896641149654,
            "stockCode": "000016"
        }
    ]
}
```
