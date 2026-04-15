# API文档/大陆/公司接口/热度数据/分红再投入收益率

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/tr_dri
> API Key: `cn/company/hot/tr_dri`

---

## 分红再投入收益率API

**简要描述:** 获取分红再投入收益率数据。

**说明:**

- 理杏仁采用分红再投入策略计算投资收益率

**请求URL:** `https://open.lixinger.com/api/cn/company/hot/tr_dri`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/tr_dri](https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/tr_dri)

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
| p_r | Number | 指定时间段投资收益率 |
| cagr_p_r_fys | Number | 今年以来投资收益率 |
| cagr_p_r_d7 | Number | 近7日投资收益率 |
| cagr_p_r_d14 | Number | 近14日投资收益率 |
| cagr_p_r_d30 | Number | 近30日投资收益率 |
| cagr_p_r_d60 | Number | 近60日投资收益率 |
| cagr_p_r_d90 | Number | 近90日投资收益率 |
| cagr_p_r_y1 | Number | 近一年投资收益率 |
| cagr_p_r_y3 | Number | 近三年年化投资收益率 |
| cagr_p_r_y5 | Number | 近五年年化投资收益率 |
| cagr_p_r_y10 | Number | 近十年年化投资收益率 |
| cagr_p_r_y20 | Number | 近二十年年化投资收益率 |
| cagr_p_r_fs | Number | 上市至今年化投资收益率 |
| p_r_fs | Number | 上市以来总投资收益率 |
| period_date | Date | 投资收益率计算起始日期 |

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
            "cagr_p_r_fs": 0.3562158280525505,
            "cagr_p_r_fys": 0.09050808691390322,
            "cagr_p_r_y1": 0.5445581015578311,
            "cagr_p_r_y3": 0.2662884464709223,
            "p_r_fs": 9.675643129927284,
            "cagr_p_r_d30": 0.09623911972409327,
            "cagr_p_r_d60": 0.13675068119891032,
            "cagr_p_r_d90": 0.0708556149732622,
            "cagr_p_r_y5": 0.19336424263935048,
            "last_data_date": "2026-03-19T00:00:00+08:00",
            "period_date": "2018-06-11T00:00:00+08:00",
            "cagr_p_r_d14": 0.14346895074946486,
            "cagr_p_r_d7": 0.012642225031605614,
            "stockCode": "300750"
        },
        {
            "cagr_p_r_fs": 0.263312435889534,
            "cagr_p_r_fys": 0.05496013592994342,
            "cagr_p_r_y1": -0.0790226973318342,
            "cagr_p_r_y3": -0.027173667453979644,
            "cagr_p_r_y5": -0.03791063659223792,
            "p_r_fs": 310.2119069389031,
            "cagr_p_r_d30": -0.02183397293476108,
            "cagr_p_r_d60": 0.051280752532560925,
            "cagr_p_r_d90": 0.030404255319148366,
            "last_data_date": "2026-03-19T00:00:00+08:00",
            "period_date": "2001-08-27T00:00:00+08:00",
            "cagr_p_r_y10": 0.22974193516977093,
            "cagr_p_r_y20": 0.25051161525099874,
            "cagr_p_r_d14": 0.03847638380603824,
            "cagr_p_r_d7": 0.043728448275861975,
            "stockCode": "600519"
        },
        {
            "cagr_p_r_fs": 0.03748714789865493,
            "cagr_p_r_fys": 0.1847133757961794,
            "cagr_p_r_y1": 0.2400000000000022,
            "cagr_p_r_y3": 0.06607405027654756,
            "cagr_p_r_y5": 0.054732771563050564,
            "p_r_fs": 1.786884082927077,
            "cagr_p_r_d30": 0.1411042944785279,
            "cagr_p_r_d60": 0.14814814814814903,
            "cagr_p_r_d90": 0.16250000000000098,
            "last_data_date": "2026-03-19T00:00:00+08:00",
            "period_date": "1998-05-13T00:00:00+08:00",
            "cagr_p_r_y10": -0.07104662295723763,
            "cagr_p_r_y20": 0.08265499298831402,
            "cagr_p_r_d14": 0.016393442622950838,
            "cagr_p_r_d7": -0.08374384236453192,
            "stockCode": "600157"
        }
    ]
}
```
