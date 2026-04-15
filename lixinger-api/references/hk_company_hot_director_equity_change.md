# API文档/香港/公司接口/热度数据/董事权益变动

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/company/hot/director_equity_change
> API Key: `hk/company/hot/director_equity_change`

---

## 董事权益变动API

**简要描述:** 获取董事权益变动数据。

**请求URL:** `https://open.lixinger.com/api/hk/company/hot/director_equity_change`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/company/hot/director_equity_change](https://www.lixinger.com/api/open-api/html-doc/hk/company/hot/director_equity_change)

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
| dec_a_last | Number | 最新董事权益变动金额 |
| dec_cap_rc_last | Number | 最新董事权益变动占H股比例 |
| dec_a_m1 | Number | 过去1个月累计董事权益变动金额 |
| dec_a_m3 | Number | 过去3个月累计董事权益变动金额 |
| dec_a_m6 | Number | 过去6个月累计董事权益变动金额 |
| dec_a_y1 | Number | 过去1年累计董事权益变动金额 |
| dec_a_y2 | Number | 过去2年累计董事权益变动金额 |
| dec_a_y3 | Number | 过去3年累计董事权益变动金额 |
| dec_cap_rc_m1 | Number | 过去1个月累计董事权益变动占H股 |
| dec_cap_rc_m3 | Number | 过去3个月累计董事权益变动占H股 |
| dec_cap_rc_m6 | Number | 过去6个月累计董事权益变动占H股 |
| dec_cap_rc_y1 | Number | 过去1年累计董事权益变动占H股 |
| dec_cap_rc_y2 | Number | 过去2年累计董事权益变动占H股 |
| dec_cap_rc_y3 | Number | 过去3年累计董事权益变动占H股 |

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
            "last_data_date": "2025-10-13T00:00:00+08:00",
            "dec_cap_rc_last": -3.668472869071433e-7,
            "dec_cap_rc_y1": -0.000005479950791365331,
            "dec_cap_rc_y2": -0.000015173795222514373,
            "dec_cap_rc_y3": -0.000018642580061508963,
            "dec_a_last": -2126973.9899999998,
            "dec_a_y1": -25590433.990000002,
            "dec_a_y2": -60368854.3931,
            "dec_a_y3": -70752414.3931,
            "dec_a_m6": -2126973.9899999998,
            "dec_cap_rc_m6": -3.668472869071433e-7,
            "dec_a_m3": 0,
            "dec_cap_rc_m3": 0,
            "dec_a_m1": 0,
            "dec_cap_rc_m1": 0,
            "stockCode": "00700"
        }
    ]
}
```
