# API文档/宏观/杠杆率

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/leverage-ratio
> API Key: `macro/leverage-ratio`

---

## 杠杆率API

**简要描述:** 获取杠杆率数据

**请求URL:** `https://open.lixinger.com/api/macro/leverage-ratio`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/leverage-ratio](https://www.lixinger.com/api/open-api/html-doc/macro/leverage-ratio)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组。如['lr_h']。 居民杠杆率 : `lr_h`; 非金融企业部门杠杆率 : `lr_nfc`; 政府杠杆率 : `lr_gg`; 实体经济部门杠杆率 : `lr_nfs`; 中央政府杠杆率 : `lr_cg`; 地方政府杠杆率 : `lr_lg`; 金融部门资产方杠杆率 : `lr_fsas`; 金融部门负债方杠杆率 : `lr_fsls` |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "lr_h"
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
            "date": "2024-12-31T00:00:00+08:00",
            "areaCode": "cn",
            "lr_h": 0.614
        },
        {
            "date": "2024-09-30T00:00:00+08:00",
            "areaCode": "cn",
            "lr_h": 0.616
        },
        {
            "date": "2024-06-30T00:00:00+08:00",
            "areaCode": "cn",
            "lr_h": 0.618
        }
    ]
}
```
