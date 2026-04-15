# API文档/大陆/公司接口/经营数据

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/operating-data
> API Key: `cn/company/operating-data`

---

## 经营数据API

**简要描述:** 获取经营数据信息。

**请求URL:** `https://open.lixinger.com/api/cn/company/operating-data`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/operating-data](https://www.lixinger.com/api/open-api/html-doc/cn/company/operating-data)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考股票信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| date | Date | 数据时间 |
| declarationDate | Date | 公告日期 |
| startDate | Date | 开始日期 |
| dataList.$.itemName | String | 项目名称 |
| dataList.$.parentItemName | String | 父项名称 |
| dataList.$.unitText | String | 单位 |
| dataList.$.value | Number | 数额 |

### 示例

```json
{
    "startDate": "2025-03-20",
    "endDate": "2026-03-20",
    "stockCode": "600157",
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
            "date": "2025-09-30T00:00:00+08:00",
            "declarationDate": "2025-10-30T00:00:00+08:00",
            "dataList": [
                {
                    "itemName": "煤炭产品主要经营数据"
                },
                {
                    "itemName": "原煤产量",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 1133.1,
                    "unitText": "万吨"
                },
                {
                    "itemName": "洗精煤产量",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 182.52,
                    "unitText": "万吨"
                },
                {
                    "itemName": "原煤销售量",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 1139.05,
                    "unitText": "万吨"
                },
                {
                    "itemName": "洗精煤销售量",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 177.26,
                    "unitText": "万吨"
                },
                {
                    "itemName": "煤炭采选销售收入",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 420939.91,
                    "unitText": "万元"
                },
                {
                    "itemName": "煤炭采选销售成本",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 320852.48,
                    "unitText": "万元"
                },
                {
                    "itemName": "毛利",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 100087.43,
                    "unitText": "万元"
                },
                {
                    "itemName": "电力产品主要经营数据"
                },
                {
                    "itemName": "发电量",
                    "parentItemName": "电力产品主要经营数据",
                    "value": 314.2904,
                    "unitText": "亿千瓦时"
                },
                {
                    "itemName": "上网电量",
                    "parentItemName": "电力产品主要经营数据",
                    "value": 298.1248,
                    "unitText": "亿千瓦时"
                },
                {
                    "itemName": "当期平均上网电价（含税）",
                    "parentItemName": "电力产品主要经营数据"
                },
                {
                    "itemName": "江苏地区",
                    "parentItemName": "当期平均上网电价（含税）",
                    "value": 0.4383,
                    "unitText": "元/千瓦时"
                },
                {
                    "itemName": "河南地区",
                    "parentItemName": "当期平均上网电价（含税）",
                    "value": 0.428,
                    "unitText": "元/千瓦时"
                }
            ],
            "startDate": "2025-01-01T00:00:00+08:00"
        },
        {
            "date": "2025-06-30T00:00:00+08:00",
            "declarationDate": "2025-08-27T00:00:00+08:00",
            "dataList": [
                {
                    "itemName": "煤炭产品主要经营数据"
                },
                {
                    "itemName": "原煤产量",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 691.31,
                    "unitText": "万吨"
                },
                {
                    "itemName": "洗精煤产量",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 115.25,
                    "unitText": "万吨"
                },
                {
                    "itemName": "原煤销售量",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 689.01,
                    "unitText": "万吨"
                },
                {
                    "itemName": "洗精煤销售量",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 108.87,
                    "unitText": "万吨"
                },
                {
                    "itemName": "煤炭采选销售收入",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 253464.28,
                    "unitText": "万元"
                },
                {
                    "itemName": "煤炭采选销售成本",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 194289.16,
                    "unitText": "万元"
                },
                {
                    "itemName": "毛利",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 59175.12,
                    "unitText": "万元"
                },
                {
                    "itemName": "电力产品主要经营数据"
                },
                {
                    "itemName": "发电量",
                    "parentItemName": "电力产品主要经营数据",
                    "value": 178.9358,
                    "unitText": "亿千瓦时"
                },
                {
                    "itemName": "上网电量",
                    "parentItemName": "电力产品主要经营数据",
                    "value": 169.6122,
                    "unitText": "亿千瓦时"
                },
                {
                    "itemName": "当期平均上网电价（含税）",
                    "parentItemName": "电力产品主要经营数据"
                },
                {
                    "itemName": "江苏地区",
                    "parentItemName": "当期平均上网电价（含税）",
                    "value": 0.4471,
                    "unitText": "元/千瓦时"
                },
                {
                    "itemName": "河南地区",
                    "parentItemName": "当期平均上网电价（含税）",
                    "value": 0.4663,
                    "unitText": "元/千瓦时"
                }
            ],
            "startDate": "2025-01-01T00:00:00+08:00"
        },
        {
            "date": "2025-03-31T00:00:00+08:00",
            "declarationDate": "2025-04-29T00:00:00+08:00",
            "dataList": [
                {
                    "itemName": "煤炭产品主要经营数据"
                },
                {
                    "itemName": "原煤产量",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 291.11,
                    "unitText": "万吨"
                },
                {
                    "itemName": "洗精煤产量",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 48.67,
                    "unitText": "万吨"
                },
                {
                    "itemName": "原煤销售量",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 290.45,
                    "unitText": "万吨"
                },
                {
                    "itemName": "洗精煤销售量",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 44.54,
                    "unitText": "万吨"
                },
                {
                    "itemName": "煤炭采选销售收入",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 115884.89,
                    "unitText": "万元"
                },
                {
                    "itemName": "煤炭采选销售成本",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 82619.68,
                    "unitText": "万元"
                },
                {
                    "itemName": "毛利",
                    "parentItemName": "煤炭产品主要经营数据",
                    "value": 33265.21,
                    "unitText": "万元"
                },
                {
                    "itemName": "电力产品主要经营数据"
                },
                {
                    "itemName": "发电量",
                    "parentItemName": "电力产品主要经营数据",
                    "value": 96.3186,
                    "unitText": "亿千瓦时"
                },
                {
                    "itemName": "上网电量",
                    "parentItemName": "电力产品主要经营数据",
                    "value": 91.185,
                    "unitText": "亿千瓦时"
                },
                {
                    "itemName": "当期平均上网电价（含税）",
                    "parentItemName": "电力产品主要经营数据"
                },
                {
                    "itemName": "江苏地区",
                    "parentItemName": "当期平均上网电价（含税）",
                    "value": 0.4623,
                    "unitText": "元/千瓦时"
                },
                {
                    "itemName": "河南地区",
                    "parentItemName": "当期平均上网电价（含税）",
                    "value": 0.4426,
                    "unitText": "元/千瓦时"
                }
            ],
            "startDate": "2025-01-01T00:00:00+08:00"
        }
    ]
}
```
