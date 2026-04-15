# API文档/香港/指数接口/样本信息

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/index/constituents
> API Key: `hk/index/constituents`

---

## 样本信息API

**简要描述:** 获取样本信息。

**请求URL:** `https://open.lixinger.com/api/hk/index/constituents`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/index/constituents](https://www.lixinger.com/api/open-api/html-doc/hk/index/constituents)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 指数代码数组。stockCodes长度>=1且<=100，格式如下：["HSI"]。 请参考 指数信息API 获取合法的stockCode。 |
| date | Yes | String: latest \| YYYY-MM-DD (北京时间) | 信息日期。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 指数代码 |
| constituents.$.stockCode | String | 样本股票代码 |
| constituents.$.areaCode | String | 地区代码 |
| constituents.$.market | String | 市场 |

### 示例

```json
{
    "date": "latest",
    "stockCodes": [
        "HSI"
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
            "stockCode": "HSI",
            "constituents": [
                {
                    "stockCode": "00001",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00002",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00003",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00005",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00006",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00012",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00016",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00027",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00066",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00101",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00175",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00241",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00267",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00285",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00288",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00291",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00300",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00316",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00322",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00386",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00388",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00669",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00688",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00700",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00728",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00762",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00823",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00836",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00857",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00868",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00883",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00939",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00941",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00960",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00968",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00981",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00992",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01024",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01038",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01044",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01088",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01093",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01099",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01109",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01113",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01177",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01209",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01211",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01299",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01378",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01398",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01801",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01810",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01876",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01928",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01929",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01997",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02015",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02020",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02057",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02269",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02313",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02318",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02319",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02331",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02359",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02382",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02388",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02618",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02628",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02688",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02899",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03690",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03692",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03750",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03968",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03988",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03993",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06181",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06618",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06690",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06862",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09618",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09633",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09888",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09901",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09961",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09988",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09992",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09999",
                    "areaCode": "hk",
                    "market": "h"
                }
            ]
        }
    ]
}
```
