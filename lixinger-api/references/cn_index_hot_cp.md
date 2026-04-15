# API文档/大陆/指数接口/热度数据/收益率

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/cp
> API Key: `cn/index/hot/cp`

---

## 收益率API

**简要描述:** 获取收益率数据。

**请求URL:** `https://open.lixinger.com/api/cn/index/hot/cp`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/cp](https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/cp)

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
| iscpc | Number | 指定时间涨跌幅 |
| cpc | Number | 涨跌幅 |
| cpc_fys | Number | 今年以来涨跌幅 |
| cpc_w1 | Number | 近一周涨跌幅 |
| cpc_w2 | Number | 近二周涨跌幅 |
| cpc_m1 | Number | 近一月涨跌幅 |
| cpc_m3 | Number | 近三月涨跌幅 |
| cpc_m6 | Number | 近六月涨跌幅 |
| cpc_y1 | Number | 近一年涨跌幅 |
| cp_cac_y2 | Number | 近二年年化涨跌幅 |
| cp_cac_y3 | Number | 近三年年化涨跌幅 |
| cp_cac_y5 | Number | 近五年年化涨跌幅 |
| cp_cac_y10 | Number | 近十年年化涨跌幅 |
| cp_cac_fs | Number | 发布以来年化涨跌幅 |
| cp_cuc_y2 | Number | 近二年累计涨跌幅 |
| cp_cuc_y3 | Number | 近三年累计涨跌幅 |
| cp_cuc_y5 | Number | 近五年累计涨跌幅 |
| cp_cuc_y10 | Number | 近十年累计涨跌幅 |

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
            "cpc": -0.01526289664114966,
            "cpc_fys": -0.03790665527377579,
            "cpc_m1": -0.038927612173941695,
            "cpc_m3": -0.02932757277804776,
            "cpc_m6": 0.00223043983311233,
            "cpc_y1": 0.061620846317383515,
            "cpc_y2": -0.026664651915034088,
            "cpc_y3": -0.05321256293391885,
            "cpc_y5": -0.02090944085669688,
            "cpc_y10": 0.009271148266925655,
            "cpc_fs": 0.046152232130244775,
            "cp_cac_fs": 0.04883133809371998,
            "cp_cac_y10": 0.03136658793070857,
            "cp_cac_y2": 0.09846907568343743,
            "cp_cac_y3": 0.03514980756756381,
            "cp_cac_y5": -0.03649724991107306,
            "cp_cuc_y10": 0.3619749582636169,
            "cp_cuc_y2": 0.20663431023282564,
            "cp_cuc_y3": 0.10942748774057565,
            "cp_cuc_y5": -0.1696431113718031,
            "cpc_w1": -0.018619849506656405,
            "cpc_w2": -0.02416637387274334,
            "stockCode": "000016"
        }
    ]
}
```
