# API文档/大陆/公司接口/热度数据/派息

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/npd
> API Key: `cn/company/hot/npd`

---

## 派息API

**简要描述:** 获取派息数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/hot/npd`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/npd](https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/npd)

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
| tpr_fl | Number | 上市以来总派息率 |
| tnp_fl | Number | 上市以来总净利润 |
| tda_fl | Number | 上市以来总分红 |

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
            "tpr_fl": 0.40790056702109345,
            "tnp_fl": 227258375003,
            "tda_fl": 92698820024.01599,
            "last_data_date": "2025-12-31T00:00:00+08:00",
            "stockCode": "300750"
        },
        {
            "tpr_fl": 0.613809149796455,
            "tnp_fl": 596460419447,
            "tda_fl": 366112862948,
            "last_data_date": "2024-12-31T00:00:00+08:00",
            "stockCode": "600519"
        },
        {
            "tpr_fl": 0.10832451815954766,
            "tnp_fl": 16074726577,
            "tda_fl": 1741287011,
            "last_data_date": "2024-12-31T00:00:00+08:00",
            "stockCode": "600157"
        }
    ]
}
```
