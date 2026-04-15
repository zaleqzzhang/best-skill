# API文档/大陆/行业接口/国证/样本信息

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/industry/constituents/cni
> API Key: `cn/industry/constituents/cni`

---

## 样本信息API

**简要描述:** 获取样本信息。

**请求URL:** `https://open.lixinger.com/api/cn/industry/constituents/cni`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/industry/constituents/cni](https://www.lixinger.com/api/open-api/html-doc/cn/industry/constituents/cni)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 行业代码数组。stockCodes长度>=1且<=100，格式如下：["C07"]。 请参考 行业信息API 获取合法的stockCode。 |
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
        "C07"
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
            "stockCode": "C07",
            "constituents": [
                {
                    "stockCode": "000001",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "001227",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "001236",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "000166",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002142",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002423",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002500",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002647",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002670",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002673",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002736",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002797",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002807",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002839",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002926",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002936",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002939",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002945",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002948",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002958",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002961",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "002966",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "300059",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "300773",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "000415",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "000532",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "000563",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "000567",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600000",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600015",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600016",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600030",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600036",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600053",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600061",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600095",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600109",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600120",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600155",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600318",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600369",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600390",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600621",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600643",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600816",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600830",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600901",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600906",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600908",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600909",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600918",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600919",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600926",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600927",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600928",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600958",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "600999",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601009",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601059",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601066",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601077",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601099",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601108",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601128",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601136",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601162",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601166",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601169",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601187",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601198",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601211",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601229",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601236",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601288",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601318",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601319",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601328",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601336",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601375",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601377",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601398",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601456",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601528",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601555",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601577",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601601",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601628",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601658",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601665",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601688",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601696",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601788",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601818",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601825",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601838",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601860",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601878",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601881",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601901",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601916",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601939",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601963",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601988",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601990",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601995",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601997",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "601998",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "603093",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "603123",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "603323",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "000617",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "000686",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "000712",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "000728",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "000750",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "000776",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "000783",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "000958",
                    "areaCode": "cn",
                    "market": "a"
                },
                {
                    "stockCode": "000987",
                    "areaCode": "cn",
                    "market": "a"
                }
            ]
        }
    ]
}
```
