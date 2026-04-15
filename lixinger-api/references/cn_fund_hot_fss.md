# API文档/大陆/基金接口/公募基金接口/热度数据/最新持有人结构信息

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/fund/hot/fss
> API Key: `cn/fund/hot/fss`

---

## 最新持有人结构信息API

**简要描述:** 获取最新持有人结构信息数据。

**请求URL:** `https://open.lixinger.com/api/cn/fund/hot/fss`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund/hot/fss](https://www.lixinger.com/api/open-api/html-doc/cn/fund/hot/fss)

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
| f_ins_h_s_r | Number | 机构持有份额比例 |
| f_ind_h_s_r | Number | 个人持有份额占比 |
| f_h_a | Number | 持有人户数 |
| f_ins_h_s_r_c_hy | Number | 机构持有份额占比变化(半年) |
| f_ins_h_s_r_c_1y | Number | 机构持有份额占比变化(一年) |
| f_ind_h_s_r_c_hy | Number | 个人持有份额占比变化(半年) |
| f_ind_h_s_r_c_1y | Number | 个人持有份额占比变化(一年) |

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
            "type": "fss",
            "f_s_s_d": "2024-06-30T00:00:00+08:00",
            "f_ins_h_s_r": 0.0207,
            "f_ins_h_s_r_c_hy": -0.0001999999999999988,
            "f_ins_h_s_r_c_1y": 0.0124,
            "f_ind_h_s_r": 0.9793000000000001,
            "f_ind_h_s_r_c_hy": 0.000200000000000089,
            "f_ind_h_s_r_c_1y": -0.012399999999999967,
            "f_h_a": 4356914,
            "f_h_s_a": 8365,
            "last_data_date": "2025-06-30T00:00:00+08:00",
            "stockCode": "161725"
        },
        {
            "type": "fss",
            "f_s_s_d": "2024-06-30T00:00:00+08:00",
            "f_ins_h_s_r": 0.006999999999999999,
            "f_ins_h_s_r_c_hy": 0.00029999999999999905,
            "f_ins_h_s_r_c_1y": -0.0032000000000000015,
            "f_ind_h_s_r": 0.993,
            "f_ind_h_s_r_c_hy": -0.00029999999999996696,
            "f_ind_h_s_r_c_1y": 0.0031999999999999806,
            "f_h_a": 3032248,
            "f_h_s_a": 6386,
            "last_data_date": "2025-06-30T00:00:00+08:00",
            "stockCode": "005827"
        }
    ]
}
```
