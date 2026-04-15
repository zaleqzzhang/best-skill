# API文档/大陆/公司接口/热度数据/龙虎榜

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/t_a
> API Key: `cn/company/hot/t_a`

---

## 龙虎榜API

**简要描述:** 获取龙虎榜数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/hot/t_a`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/t_a](https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/t_a)

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
| tatnpa_last | Number | 最新龙虎榜总净买入金额 |
| tainpa_last | Number | 最新龙虎榜机构净买入金额 |
| tatnpa_m1 | Number | 过去1个月龙虎榜总净买入金额 |
| tatnpa_m3 | Number | 过去3个月龙虎榜总净买入金额 |
| tatnpa_m6 | Number | 过去6个月龙虎榜总净买入金额 |
| tatnpa_y1 | Number | 过去1年龙虎榜总净买入金额 |
| tainpa_m1 | Number | 过去1个月龙虎榜机构净买入金额 |
| tainpa_m3 | Number | 过去3个月龙虎榜机构净买入金额 |
| tainpa_m6 | Number | 过去6个月龙虎榜机构净买入金额 |
| tainpa_y1 | Number | 过去1年龙虎榜机构净买入金额 |

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
            "last_data_date": "2025-09-18T00:00:00+08:00",
            "tatnpa_d1": 0,
            "tatnpa_m1": 286047600,
            "tatnpa_m3": 286047600,
            "tatnpa_m6": 286047600,
            "tatnpa_y1": 286047600,
            "tainpa_last": 0,
            "tatnpa_last": 286047600,
            "stockCode": "600157"
        }
    ]
}
```
