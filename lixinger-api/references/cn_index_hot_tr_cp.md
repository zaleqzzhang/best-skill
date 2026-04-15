# API文档/大陆/指数接口/热度数据/全收益率

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/tr_cp
> API Key: `cn/index/hot/tr_cp`

---

## 全收益率API

**简要描述:** 获取全收益率数据。

**请求URL:** `https://open.lixinger.com/api/cn/index/hot/tr_cp`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/tr_cp](https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/tr_cp)

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
| start_date | Date | 数据起始时间 |
| istrcpc | Number | 指定时间全收益涨跌幅 |
| tr_cpc_fys | Number | 今年以来全收益涨跌幅 |
| tr_cpc_w1 | Number | 近一个周全收益年化涨跌幅 |
| tr_cpc_w2 | Number | 近二个周全收益年化涨跌幅 |
| tr_cpc_m1 | Number | 近一个月全收益年化涨跌幅 |
| tr_cpc_m3 | Number | 近三个月全收益年化涨跌幅 |
| tr_cpc_m6 | Number | 近六个月全收益年化涨跌幅 |
| tr_cpc_y1 | Number | 近一年全收益年化涨跌幅 |
| tr_cp_cac_y2 | Number | 近二年全收益率年化涨跌幅 |
| tr_cp_cac_y3 | Number | 近三年全收益率年化涨跌幅 |
| tr_cp_cac_y5 | Number | 近五年全收益年化涨跌幅 |
| tr_cp_cac_y10 | Number | 近十年全收益年化涨跌幅 |
| tr_cp_cac_fs | Number | 有数据以来全收益年化涨跌幅 |
| tr_cp_cuc_y2 | Number | 近二年全收益累计涨跌幅 |
| tr_cp_cuc_y3 | Number | 近三年全收益累计涨跌幅 |
| tr_cp_cuc_y5 | Number | 近五年全收益累计涨跌幅 |
| tr_cp_cuc_y10 | Number | 近十年全收益累计涨跌幅 |

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
            "tr_cpc_fys": -0.03492988795268159,
            "tr_cpc_m1": -0.03892474780659372,
            "tr_cpc_m3": -0.02588089655672232,
            "tr_cpc_m6": 0.012449028202189405,
            "tr_cpc_y1": 0.09857673964474811,
            "tr_cpc_y2": 0.009337935219049243,
            "tr_cpc_y3": -0.020069658941374247,
            "tr_cpc_y5": 0.008890694533815635,
            "tr_cpc_y10": 0.038166859615306636,
            "tr_cpc_fs": 0.07295380420365594,
            "start_date": "2012-08-31T00:00:00+08:00",
            "tr_cp_cac_fs": 0.07808443326605397,
            "tr_cp_cac_y10": 0.062232524655255306,
            "tr_cp_cac_y2": 0.13912672601916998,
            "tr_cp_cac_y3": 0.07261020980598776,
            "tr_cp_cac_y5": -0.005531188125677877,
            "tr_cp_cuc_y10": 0.8292425451776761,
            "tr_cp_cuc_y2": 0.2976096979311533,
            "tr_cp_cuc_y3": 0.2345451611702063,
            "tr_cp_cuc_y5": -0.02735168774679586,
            "tr_cpc_w1": -0.018618538025428455,
            "tr_cpc_w2": -0.024164447749655094,
            "stockCode": "000016"
        }
    ]
}
```
