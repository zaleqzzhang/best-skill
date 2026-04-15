# API文档/香港/行业接口/恒生/样本信息

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/industry/constituents/hsi
> API Key: `hk/industry/constituents/hsi`

---

## 样本信息API

**简要描述:** 获取样本信息。

**请求URL:** `https://open.lixinger.com/api/hk/industry/constituents/hsi`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/industry/constituents/hsi](https://www.lixinger.com/api/open-api/html-doc/hk/industry/constituents/hsi)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 行业代码数组。stockCodes长度>=1且<=100，格式如下：["H50","H5010"]。 请参考 行业信息API 获取合法的stockCode。 |
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
        "H50",
        "H5010"
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
            "stockCode": "H50",
            "constituents": [
                {
                    "stockCode": "00005",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00023",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00064",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00080",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00086",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00093",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00111",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00129",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00133",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00139",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00165",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00188",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00204",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00211",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00214",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00218",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00222",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00227",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00234",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00235",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00245",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00279",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00290",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00310",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00329",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00335",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00339",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00356",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00373",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00376",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00388",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00397",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00412",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00428",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00431",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00440",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00510",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00585",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00605",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00612",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00613",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00619",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00622",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00626",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00628",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00629",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00662",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00697",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00717",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00721",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00730",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00736",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00768",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00770",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00804",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00806",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00810",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00818",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00821",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00851",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00863",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00888",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00900",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00905",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00913",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00939",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00945",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00952",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00966",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00993",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00998",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01039",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01051",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01062",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01073",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01140",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01141",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01160",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01216",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01217",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01225",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01226",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01260",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01273",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01282",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01288",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01290",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01299",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01319",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01336",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01339",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01359",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01375",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01398",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01428",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01456",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01461",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01471",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01476",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01508",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01543",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01551",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01572",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01577",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01578",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01601",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01606",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01611",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01658",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01669",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01697",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01709",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01776",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01788",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01828",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01835",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01905",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01911",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01915",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01916",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01942",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01945",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01963",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01973",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01983",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01988",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02003",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02016",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02051",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02139",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02263",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02312",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02318",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02324",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02328",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02356",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02378",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02388",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02483",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02558",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02596",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02598",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02601",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02611",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02621",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02628",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02680",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02799",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02858",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02888",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03328",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03329",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03360",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03618",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03623",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03660",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03678",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03698",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03848",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03866",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03903",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03908",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03938",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03958",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03963",
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
                    "stockCode": "06030",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06058",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06060",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06066",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06069",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06099",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06138",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06178",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06190",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06196",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06199",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06623",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06686",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06806",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06818",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06866",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06881",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06886",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06963",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08019",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08020",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08029",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08030",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08057",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08072",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08087",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08098",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08149",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08163",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08168",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08193",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08210",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08221",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08226",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08239",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08279",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08313",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08333",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08340",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08350",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08365",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08376",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08377",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08383",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08395",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08439",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08452",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08540",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08613",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08621",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "08657",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09668",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09677",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09889",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09923",
                    "areaCode": "hk",
                    "market": "h"
                }
            ]
        },
        {
            "stockCode": "H5010",
            "constituents": [
                {
                    "stockCode": "00005",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00011",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00023",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00440",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00626",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00939",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "00998",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01216",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01288",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01398",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01551",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01578",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01658",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01916",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01963",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01983",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "01988",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02016",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02139",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02356",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02388",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02558",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02596",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "02888",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03328",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03618",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03698",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "03866",
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
                    "stockCode": "06138",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06190",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06196",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06199",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "06818",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09668",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09677",
                    "areaCode": "hk",
                    "market": "h"
                },
                {
                    "stockCode": "09889",
                    "areaCode": "hk",
                    "market": "h"
                }
            ]
        }
    ]
}
```
