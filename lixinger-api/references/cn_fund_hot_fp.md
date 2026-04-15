# 分红再投入收益率API

## 分红再投入收益率API

**简要描述:** 获取分红再投入收益率数据。

**请求URL:** `https://open.lixinger.com/api/cn/fund/hot/fp`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund/hot/fp](https://www.lixinger.com/api/open-api/html-doc/cn/fund/hot/fp)

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
| f_p_r | Number | 指定时间段投资收益率 |
| f_p_r_fys | Number | 今年以来分红再投入收益率 |
| f_p_r_m1 | Number | 分红再投入收益率(1个月) |
| f_p_r_m3 | Number | 分红再投入收益率(3个月) |
| f_p_r_m6 | Number | 分红再投入收益率(6个月) |
| f_p_r_y1 | Number | 分红再投入收益率(1年) |
| f_p_r_y2 | Number | 分红再投入收益率(2年) |
| f_p_r_y3 | Number | 分红再投入收益率(3年) |
| f_p_r_y5 | Number | 分红再投入收益率(5年) |
| f_p_r_y10 | Number | 分红再投入收益率(10年) |
| f_cagr_p_r_fs | Number | 成立以来分红再投入年化收益率 |

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
            "f_p_r_fys": -0.07465840259191425,
            "f_p_r_m1": -0.06650561318743775,
            "f_p_r_m3": -0.10565010211027925,
            "f_p_r_m6": -0.18458291956305894,
            "f_p_r_y1": -0.23740422567912745,
            "f_p_r_y3": -0.43960075072513327,
            "f_p_r_y5": -0.4197440112345956,
            "f_p_r_y10": 2.3607446947767357,
            "f_cagr_p_r_fs": 0.09466334455900727,
            "stockCode": "161725"
        },
        {
            "f_p_r_fys": -0.01433711002523752,
            "f_p_r_m1": -0.03794549266247382,
            "f_p_r_m3": -0.0372895578748621,
            "f_p_r_m6": -0.10484736174778075,
            "f_p_r_y1": -0.07531106745252125,
            "f_p_r_y3": -0.12818807884113004,
            "f_p_r_y5": -0.35638148667601655,
            "f_cagr_p_r_fs": 0.08391394914605788,
            "stockCode": "005827"
        }
    ]
}
```
