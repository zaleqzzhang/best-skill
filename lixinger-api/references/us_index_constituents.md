# API文档/美国/指数接口/样本信息

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/us/index/constituents
> API Key: `us/index/constituents`

---

## 样本信息API

**简要描述:** 获取样本信息。

**请求URL:** `https://open.lixinger.com/api/us/index/constituents`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/us/index/constituents](https://www.lixinger.com/api/open-api/html-doc/us/index/constituents)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 指数代码数组。stockCodes长度>=1且<=100，格式如下：[".INX"]。 请参考 指数信息API 获取合法的stockCode。 |
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
        ".INX"
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
            "stockCode": ".INX",
            "constituents": [
                {
                    "stockCode": "ABT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AMD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "APD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SWKS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HWM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AEP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AXP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AFL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AIG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ADI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AMAT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ADM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ADP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AVY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BALL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BAX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BDX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WRB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BMY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BF.B",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CPB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "STZ",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CAT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "JPM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CINF",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CLX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "KO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CAG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TAP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GLW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CMI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TGT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DAL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DOV",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "OMC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ECL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "RVTY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EMR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EFX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EQT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "XOM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FRT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FITB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "USB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MTB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "F",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BEN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GIS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GPC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HAL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HAS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HSY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HPQ",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HRL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HUBB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HUM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HBAN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ITW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "INTC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "IBM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "IFF",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "IP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "IPG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "J",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "K",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "KMB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "KR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LLY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "L",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LOW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MRSH",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MAS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MKC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MCD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SPGI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CVS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ETR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MMM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MSI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BAC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NDSN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ES",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "XEL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WFC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NTRS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NUE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "UDR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PCAR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PKG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PH",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PNR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PEP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PFE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BRO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PPG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PGR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ROL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TRV",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SLB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SHW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AOS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SJM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SNA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "KEY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TFC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LUV",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CVX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SWK",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "STT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SYY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TER",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TXN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TMO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TSN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "UAL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "UNP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "RTX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WMT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EME",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WST",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WDC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WMB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TJX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "JNJ",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LHX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TXT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GWW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CSX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MRK",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SYK",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DHR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CHD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AON",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SCHW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AMGN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "KLAC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NKE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AAPL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LNT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "UHS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AJG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NSC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LRCX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "COO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PNC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "D",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WSM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "RJF",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CAH",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MU",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CTAS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PAYX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "O",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "JBHT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "UNH",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ATO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "VZ",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "T",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "VTR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ROST",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EXPD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "IT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NEE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CFG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BBY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PNW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DOC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WELL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ADSK",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HON",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "JKHY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WEC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PEG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MSFT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MGM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ADBE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "OXY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FISV",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "QCOM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CMS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CDNS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FICO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CCL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FAST",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AMP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "APH",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EOG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PHM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EIX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MCHP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SBUX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "C",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FCX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "IEX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "JCI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TECH",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GEN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MHK",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PTC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CTRA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CSCO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HOLX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HCA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TYL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TRMB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MNST",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AZO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "REGN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "IDXX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AES",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HIG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BIIB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "VRTX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ZBRA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ODFL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "KIM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "INCY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GILD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DHI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ROP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SNPS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "RCL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BSX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MTCH",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EXE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "INTU",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ORLY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "JBL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ALL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CPRT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EQR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NVR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CPT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "COST",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DECK",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "REG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MAA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "IVZ",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AVB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ALB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MLM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TSCO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LH",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ESS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LEN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PPL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ERIE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DVA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "COF",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MCK",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DLTR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DTE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LMT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DRI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WAB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "RMD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "POOL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TTWO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ACGL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HSIC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WAT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NTAP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AEE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PCG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FDS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NRG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "VRSN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AMZN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "IRM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DGX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "STLD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ROK",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SRE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SBAC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "VLO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ISRG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ARE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "RL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BXP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MTD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AME",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "OKE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "YUM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CHRW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PLD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NVDA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ED",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MAR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FFIV",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FDX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PWR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CCI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AMT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CSGP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CMG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CTSH",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MCO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "RSG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SPG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EBAY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NFLX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LKQ",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "URI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BRK.B",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AXON",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LII",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HST",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CNC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BKNG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AKAM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DVN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "UPS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "A",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CHTR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DXCM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TDY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ALGN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ON",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MET",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CRL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EQIX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MDLZ",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CRM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EXC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TROW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TPR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NDAQ",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GRMN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GPN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PFG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CNP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NOC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ZBH",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FIS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PRU",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "STX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CBRE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WTW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "COR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PODD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ELV",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CME",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "COP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NEM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CMCSA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WYNN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CPAY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MOH",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TDG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FTNT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AIZ",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FSLR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MPWR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "RF",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TMUS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MOS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DPZ",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EXR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DLR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LVS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BLDR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TSLA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PLTR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CF",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EXPE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DUK",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "META",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PANW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WDAY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LYV",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LDOS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ORCL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EPAM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BLK",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NOW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CBOE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SMCI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "IBKR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TEL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TRGP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BK",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PSA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "VMC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LULU",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CDW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "V",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ULTA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "KKR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MSCI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AWK",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NXPI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "KDP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "WBD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "VRSK",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ACN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GM",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GNRC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "IQV",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LYB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HII",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "KMI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MPC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "XYZ",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NCLH",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "APTV",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "XYL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PSX",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CRWD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FANG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "UBER",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ABBV",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ETN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ZTS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ABNB",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DDOG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "NWSA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ICE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DELL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ALLE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HLT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PAYC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "ANET",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "KEYS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SYF",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GDDY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MDT",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PYPL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "KHC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HPE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GOOGL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FTV",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TTD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "COIN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "MRNA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "INVH",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "VST",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "IR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BKR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "VICI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "LIN",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "EVRG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DAY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AVGO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CI",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DIS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "AMCR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "APP",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DOW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "FOXA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CTVA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "STE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "OTIS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CARR",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "HOOD",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "VTRS",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "DASH",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TPL",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "APA",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "APO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "CEG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GEHC",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "KVUE",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SOLV",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "VLTO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "TKO",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "GEV",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "BG",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SW",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "PSKY",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "Q",
                    "areaCode": "us",
                    "market": "us"
                },
                {
                    "stockCode": "SOLS",
                    "areaCode": "us",
                    "market": "us"
                }
            ]
        }
    ]
}
```
