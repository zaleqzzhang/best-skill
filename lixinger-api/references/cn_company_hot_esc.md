# API文档/大陆/公司接口/热度数据/高管增减持

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/esc
> API Key: `cn/company/hot/esc`

---

## 高管增减持API

**简要描述:** 获取高管增减持数据。

**说明:**

- 计算股本为流通A股

**请求URL:** `https://open.lixinger.com/api/cn/company/hot/esc`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/esc](https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/esc)

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
| escm_last | Number | 最新高管增减持金额 |
| esc_cap_rc_last | Number | 最新高管增减持股份占流通A股比例 |
| escm_m1 | Number | 过去1个月累计高管增减持金额 |
| escm_m3 | Number | 过去3个月累计高管增减持金额 |
| escm_m6 | Number | 过去6个月累计高管增减持金额 |
| escm_y1 | Number | 过去1年累计高管增减持金额 |
| escm_y2 | Number | 过去2年累计高管增减持金额 |
| escm_y3 | Number | 过去3年累计高管增减持金额 |
| esc_cap_rc_m1 | Number | 过去1个月累计高管增减持占流通A股比例 |
| esc_cap_rc_m3 | Number | 过去3个月累计高管增减持占流通A股比例 |
| esc_cap_rc_m6 | Number | 过去6个月累计高管增减持占流通A股比例 |
| esc_cap_rc_y1 | Number | 过去1年累计高管增减持占流通A股比例 |
| esc_cap_rc_y2 | Number | 过去2年累计高管增减持占流通A股比例 |
| esc_cap_rc_y3 | Number | 过去3年累计高管增减持占流通A股比例 |

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
            "esc_cap_rc_y3": 0,
            "last_data_date": "2022-06-01T00:00:00+08:00",
            "esc_cap_rc_last": 0,
            "escm_last": 0,
            "escm_y3": 0,
            "esc_cap_rc_m1": 0,
            "esc_cap_rc_m3": 0,
            "esc_cap_rc_m6": 0,
            "esc_cap_rc_y1": 0,
            "esc_cap_rc_y2": 0,
            "escm_m1": 0,
            "escm_m3": 0,
            "escm_m6": 0,
            "escm_y1": 0,
            "escm_y2": 0,
            "stockCode": "300750"
        },
        {
            "esc_cap_rc_last": 0,
            "esc_cap_rc_m1": 0,
            "esc_cap_rc_m3": 0,
            "esc_cap_rc_m6": 0,
            "esc_cap_rc_y1": 0,
            "esc_cap_rc_y2": 0,
            "esc_cap_rc_y3": 0,
            "escm_y1": 0,
            "escm_last": 0,
            "escm_m1": 0,
            "escm_m3": 0,
            "escm_m6": 0,
            "escm_y2": 0,
            "escm_y3": 0,
            "last_data_date": "2025-02-11T00:00:00+08:00",
            "stockCode": "600519"
        },
        {
            "esc_cap_rc_y3": 0.0011207698415325847,
            "last_data_date": "2024-09-12T00:00:00+08:00",
            "esc_cap_rc_last": 0.000045009029417797885,
            "esc_cap_rc_y2": 0.0007466997980412666,
            "escm_last": 1060000,
            "escm_y2": 18928011,
            "escm_y3": 30845387,
            "stockCode": "600157"
        }
    ]
}
```
