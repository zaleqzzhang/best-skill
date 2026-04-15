# API文档/宏观/人民币存贷款/人民币贷款

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/rmb-loans
> API Key: `macro/rmb-loans`

---

## 人民币贷款

**简要描述:** 获取人民币贷款数据，如人民币贷款等。

**请求URL:** `https://open.lixinger.com/api/macro/rmb-loans`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/rmb-loans](https://www.lixinger.com/api/open-api/html-doc/macro/rmb-loans)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组。如['rmb_l']。 人民币贷款 : `rmb_l` m(月): t(累积); 境内贷款 : `rmb_d_l` m(月): t(累积); 海外贷款 : `rmb_o_l` m(月): t(累积); 住户贷款 : `rmb_h_l` m(月): t(累积); 住户短期贷款 : `rmb_h_s_l` m(月): t(累积); 住户中长期贷款 : `rmb_h_ml_l` m(月): t(累积); 企（事）业单位贷款 : `rmb_nfeg_l` m(月): t(累积); 企（事）业单位短期贷款 : `rmb_nfeg_s_l` m(月): t(累积); 企（事）业单位中长期贷款 : `rmb_nfeg_ml_l` m(月): t(累积); 企（事）业单位票据融资 : `rmb_nfeg_p_f` m(月): t(累积); 企（事）业单位融资租赁 : `rmb_nfeg_f_l` m(月): t(累积); 企（事）业单位各项垫款 : `rmb_nfeg_ta_l` m(月): t(累积); 非银行业金融机构贷款 : `rmb_nbfo_l` m(月): t(累积) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.rmb_l.t"
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
                "rmb_l": {
                    "t": 277518127000000
                }
            }
        },
        {
            "date": "2026-01-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "rmb_l": {
                    "t": 276618081000000
                }
            }
        },
        {
            "date": "2025-12-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "rmb_l": {
                    "t": 271912662000000
                }
            }
        }
    ]
}
```
