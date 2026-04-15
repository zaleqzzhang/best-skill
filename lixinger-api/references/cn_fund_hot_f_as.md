# 最新资产规模信息API

## 最新资产规模信息API

**简要描述:** 获取最新资产规模信息数据。

**请求URL:** `https://open.lixinger.com/api/cn/fund/hot/f_as`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund/hot/f_as](https://www.lixinger.com/api/open-api/html-doc/cn/fund/hot/f_as)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 基金代码数组。 stockCodes长度>=1且<=100，格式如下：["161725","005827"]。 请参考 基金信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| f_tas | Number | 总资产规模 |
| f_tas_d | Date | 总资产规模日期 |
| fet_as | Number | 基金场内规模 |
| fet_as_d | Date | 基金场内规模日期 |

### 示例

```json
{
    "stockCodes": [
        "161725",
        "005827"
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
            "type": "f_as",
            "f_tas": 28496689609.9571,
            "f_tas_d": "2025-12-31T00:00:00+08:00",
            "fet_as": 2169995328.8918,
            "fet_as_d": "2026-03-19T00:00:00+08:00",
            "stockCode": "161725"
        },
        {
            "type": "f_as",
            "f_tas": 31021040662.3722,
            "f_tas_d": "2025-12-31T00:00:00+08:00",
            "stockCode": "005827"
        }
    ]
}
```
