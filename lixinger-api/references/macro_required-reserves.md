# API文档/宏观/存款准备金率

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/required-reserves
> API Key: `macro/required-reserves`

---

## 存款准备金率API

**简要描述:** 获取存款准备金率，如大型金融机构存款准备金率等。

**请求URL:** `https://open.lixinger.com/api/macro/required-reserves`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/required-reserves](https://www.lixinger.com/api/open-api/html-doc/macro/required-reserves)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组。如['lfi_drr']。 大型金融机构存款准备金率 : `lfi_drr`; 中小金融机构存款准备金率 : `masfi_drr` |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "lfi_drr"
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
            "date": "2025-05-15T00:00:00+08:00",
            "areaCode": "cn",
            "lfi_drr": 0.09
        },
        {
            "date": "2024-09-27T00:00:00+08:00",
            "areaCode": "cn",
            "lfi_drr": 0.095
        },
        {
            "date": "2024-02-05T00:00:00+08:00",
            "areaCode": "cn",
            "lfi_drr": 0.1
        }
    ]
}
```
