# API文档/大陆/公司接口/热度数据/分红融资

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/df
> API Key: `cn/company/hot/df`

---

## 分红融资API

**简要描述:** 获取分红融资数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/hot/df`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/df](https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/df)

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
| dfr_fs | Number | 上市以来A股总分红融资比 |
| da_fs | Number | 上市以来A股总分红 |
| fa_fs | Number | 上市以来A股总融资 |
| financingFlag | Number | 上市后是否有股权激励外的融资 |

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
            "dfr_fs": 0.8258931457963262,
            "da_fs": 60818902879.858,
            "fa_fs": 73640159371,
            "financingFlag": 1,
            "stockCode": "300750"
        },
        {
            "dfr_fs": 163.12391276363013,
            "da_fs": 366112862948,
            "fa_fs": 2244385000,
            "financingFlag": 0,
            "stockCode": "600519"
        },
        {
            "dfr_fs": 0.07822844747427483,
            "da_fs": 1741287011,
            "fa_fs": 22258999983,
            "financingFlag": 1,
            "stockCode": "600157"
        }
    ]
}
```
