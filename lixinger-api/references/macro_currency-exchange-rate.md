# API文档/宏观/汇率

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/currency-exchange-rate
> API Key: `macro/currency-exchange-rate`

---

## 汇率API

**简要描述:** 获取汇率数据。

**请求URL:** `https://open.lixinger.com/api/macro/currency-exchange-rate`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/currency-exchange-rate](https://www.lixinger.com/api/open-api/html-doc/macro/currency-exchange-rate)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| fromCurrency | Yes | String | **当前支持:** 元 : `CNY`; 港币 : `HKD`; 美元 : `USD` |
| toCurrency | Yes | String | **当前支持:** 元 : `CNY` 支持兑换的货币: HKD(港币) USD(美元) EUR(欧元) JPY(日元); 港币 : `HKD` 支持兑换的货币: CNY(元) USD(美元) JPY(日元) EUR(欧元) GBP(英镑) SGD(新加坡元) CAD(加拿大元) MYR(马来西亚林吉特) MOP(澳门元) TWD(台湾元) AUD(澳币) THB(泰铢) BRL(巴西雷亚尔); 美元 : `USD` 支持兑换的货币: ARS(阿根廷比索) AUD(澳币) BRL(巴西雷亚尔) CAD(加拿大元) CHF(瑞士法郎) CLP(智利比索) CNY(元) COP(哥伦比亚比索) DKK(克朗) EUR(欧元) GBP(英镑) HKD(港币) MOP(澳门元) IDR(印尼盾) ILS(以色列谢克尔) INR(印度卢比) JPY(日元) KRW(韩元) MXN(墨西哥比索) MYR(马来西亚林吉特) NOK(挪威克朗) PEN(秘鲁索尔) PHP(菲律宾比索) PLN(波兰兹罗提) RUB(俄国卢布) SEK(瑞典克朗) TRY(土耳其里拉) TWD(台湾元) ZAR(南非兰特) |

### 示例

```json
{
    "startDate": "2026-03-13",
    "endDate": "2026-03-20",
    "fromCurrency": "USD",
    "toCurrency": "CNY",
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
            "fromCurrency": "USD",
            "toCurrency": "CNY",
            "date": "2026-03-17T16:00:00.000Z",
            "open": 6.883733737179045,
            "low": 6.886578059362303,
            "high": 6.872379905161157,
            "close": 6.873324627122138
        },
        {
            "fromCurrency": "USD",
            "toCurrency": "CNY",
            "date": "2026-03-16T16:00:00.000Z",
            "open": 6.885629690835227,
            "low": 6.8913238233064575,
            "high": 6.881838827334664,
            "close": 6.88752668916592
        },
        {
            "fromCurrency": "USD",
            "toCurrency": "CNY",
            "date": "2026-03-15T16:00:00.000Z",
            "open": 6.901787562978812,
            "low": 6.905600441958429,
            "high": 6.895600606812853,
            "close": 6.8965517241379315
        }
    ]
}
```
