# API文档/宏观/央行资产负债表

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/central-bank-balance-sheet
> API Key: `macro/central-bank-balance-sheet`

---

## 央行资产负债表API

**简要描述:** 获取央行资产负债表数据，如总资产等。

**请求URL:** `https://open.lixinger.com/api/macro/central-bank-balance-sheet`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/central-bank-balance-sheet](https://www.lixinger.com/api/open-api/html-doc/macro/central-bank-balance-sheet)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn` |
| metricsList | Yes | Array | 指标数组。如['t_a']。 总资产 : `t_a` m(月): t(累积); 国外资产 : `f_a` m(月): t(累积); 对政府债权 : `c_o_g` m(月): t(累积); 对其他存款性公司债权 : `c_o_odc` m(月): t(累积); 对其他金融性公司债权 : `c_o_ofc` m(月): t(累积); 对非金融性公司债权 : `c_o_onfc` m(月): t(累积); 其他资产 : `o_a` m(月): t(累积); 储备货币 : `r_m` m(月): t(累积); 不计入储备货币的金融性公司存款 : `d_o_fc_ef_rm` m(月): t(累积); 发行债券 : `b_i` m(月): t(累积); 国外负债 : `f_l` m(月): t(累积); 政府存款 : `d_o_g` m(月): t(累积); 自有资金 : `o_c` m(月): t(累积); 其他负债 : `o_lia` m(月): t(累积) |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "m.t_a.t"
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
                "t_a": {
                    "t": 49986279000000
                }
            }
        },
        {
            "date": "2026-01-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "t_a": {
                    "t": 49318991000000
                }
            }
        },
        {
            "date": "2025-12-31T00:00:00+08:00",
            "areaCode": "cn",
            "m": {
                "t_a": {
                    "t": 48159134000000
                }
            }
        }
    ]
}
```
