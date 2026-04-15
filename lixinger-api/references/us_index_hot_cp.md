# API文档/美国/指数接口/热度数据/收盘点位

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/us/index/hot/cp
> API Key: `us/index/hot/cp`

---

## 收盘点位API

**简要描述:** 获取收盘点位数据。

**请求URL:** `https://open.lixinger.com/api/us/index/hot/cp`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/us/index/hot/cp](https://www.lixinger.com/api/open-api/html-doc/us/index/hot/cp)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 指数代码数组。 stockCodes长度>=1且<=100，格式如下：[".INX"]。 请参考 指数信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| last_data_date | Date | 数据时间 |
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

### 示例

```json
{
    "stockCodes": [
        ".INX"
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
            "cpc": -0.0027488037194136616,
            "cpc_fys": -0.03491490760353522,
            "cpc_m1": -0.039937163127369724,
            "cpc_m3": -0.02483778023132932,
            "cpc_m6": -0.008683504492554395,
            "cpc_y1": 0.16407972103628188,
            "cpc_y3": 0.1026398852364856,
            "cpc_y5": 0.14262901527278138,
            "cpc_y10": 0.10746747393053901,
            "cpc_fs": 0.08252831450947729,
            "last_data_date": "2026-03-19T00:00:00-04:00",
            "cp_cac_fs": 0.08369353651832379,
            "cp_cac_y10": 0.12412857722925907,
            "cp_cac_y3": 0.1899695167866673,
            "cp_cac_y5": 0.11042688235809184,
            "cp_cuc_y10": 1.7466343143393863,
            "cp_cuc_y2": 0.4328998142060885,
            "cp_cuc_y3": 0.312463182697972,
            "cp_cuc_y5": 0.9479916592360778,
            "cp_cac_y2": 0.12949153739544372,
            "cpc_w1": -0.009910649789737769,
            "cpc_w2": -0.03828662930344273,
            "stockCode": ".INX"
        }
    ]
}
```
