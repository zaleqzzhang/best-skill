# API文档/大陆/公司接口/热度数据/股权质押

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/ple
> API Key: `cn/company/hot/ple`

---

## 股权质押API

**简要描述:** 获取股权质押数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/hot/ple`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/ple](https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/ple)

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
| ps_sc_r | Number | 股权质押占A股比例 |
| pc | Number | 质押笔数 |
| ps | Number | 质押股数 |
| ps_mc | Number | 质押市值 |
| ps_shbt10sh_r | Number | 质押股数与前十大股东持股之比 |

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
            "ps": 25350000,
            "ps_mc": 10152675000,
            "ps_shbt10sh_r": 0.011775248689519345,
            "ps_sc_r": 0.0058,
            "pc": 7,
            "last_data_date": "2026-03-13T00:00:00+08:00",
            "stockCode": "300750"
        },
        {
            "ps": 736600,
            "ps_mc": 1070184041.9999999,
            "ps_shbt10sh_r": 0.001102863568716865,
            "ps_sc_r": 0.0006,
            "pc": 7,
            "last_data_date": "2026-03-13T00:00:00+08:00",
            "stockCode": "600519"
        },
        {
            "ps": 4176380900.000001,
            "ps_mc": 7768068474.000002,
            "ps_shbt10sh_r": 0.756491220797513,
            "ps_sc_r": 0.1914,
            "pc": 18,
            "last_data_date": "2026-03-13T00:00:00+08:00",
            "stockCode": "600157"
        }
    ]
}
```
