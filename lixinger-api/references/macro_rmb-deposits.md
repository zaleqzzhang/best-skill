# API文档/宏观/人民币存贷款/人民币存款

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/rmb-deposits
> API Key: `macro/rmb-deposits`

---

## 人民币存款

**简要描述:** 获取人民币贷款数据，如人民币存款等。

**请求URL:** `https://open.lixinger.com/api/macro/rmb-deposits`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/rmb-deposits](https://www.lixinger.com/api/open-api/html-doc/macro/rmb-deposits)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组。如['rmb_d']。 人民币存款 : `rmb_d` m(月): t(累积); 境内存款 : `rmb_d_d` m(月): t(累积); 境外存款 : `rmb_o_d` m(月): t(累积); 住户存款 : `rmb_h_d` m(月): t(累积); 非金融企业存款 : `rmb_nfe_d` m(月): t(累积); 机关团体存款 : `rmb_gdo_d` m(月): t(累积); 财政性存款 : `rmb_f_d` m(月): t(累积); 非银行业金融机构存款 : `rmb_nbfi_d` m(月): t(累积); 住户活期存款 : `rmb_h_d_d` m(月): t(累积); 住户定期及其他存款 : `rmb_h_to_d` m(月): t(累积); 非金融企业活期存款 : `rmb_nfe_d_d` m(月): t(累积); 非金融企业定期及其他存款 : `rmb_nfe_to_d` m(月): t(累积) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.rmb_d.t"
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
            "date": "2026-02-28T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "rmb_d": {
                    "t": 337936982000000
                }
            }
        },
        {
            "date": "2026-01-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "rmb_d": {
                    "t": 336769602000000
                }
            }
        },
        {
            "date": "2025-12-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "rmb_d": {
                    "t": 328642875000000
                }
            }
        }
    ]
}
```
