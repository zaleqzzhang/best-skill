# API文档/大陆/公司接口/公司概况

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/profile
> API Key: `cn/company/profile`

---

## 公司概况API

**简要描述:** 获取公司概况数据

**请求URL:** `https://open.lixinger.com/api/cn/company/profile`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/profile](https://www.lixinger.com/api/open-api/html-doc/cn/company/profile)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 股票代码数组。 stockCodes长度>=1且<=100，格式如下：["300750","600519","600157"]。 请参考 股票信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| companyName | String | 公司名称 |
| historyStockNames | Array | 历史名称 新名称 : `newName`; 老名称 : `oldName` |
| province | String | 省份 |
| city | String | 城市 |
| actualControllerTypes | Array | 实际控制人类型 自然人 : `natural_person`; 集体 : `collective`; 外企 : `foreign_company`; 国有 : `state_owned` |
| actualControllerName | String | 实际控制人 |

### 示例

```json
{
    "stockCodes": [
        "300750",
        "600519",
        "600157"
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
            "city": "宁德市",
            "province": "福建",
            "companyName": "宁德时代新能源科技股份有限公司",
            "historyStockNames": [],
            "stockCode": "300750",
            "actualControllerTypes": [
                "natural_person"
            ],
            "actualControllerName": "曾毓群"
        },
        {
            "city": "晋中市",
            "province": "山西",
            "companyName": "永泰能源集团股份有限公司",
            "historyStockNames": [
                {
                    "date": "2021-04-29T00:00:00+08:00",
                    "newName": "永泰能源",
                    "oldName": "ST永泰"
                },
                {
                    "date": "2021-01-18T00:00:00+08:00",
                    "newName": "ST永泰",
                    "oldName": "*ST永泰"
                },
                {
                    "date": "2020-09-26T00:00:00+08:00",
                    "newName": "*ST永泰",
                    "oldName": "永泰能源"
                },
                {
                    "date": "2010-10-26T00:00:00+08:00",
                    "newName": "永泰能源",
                    "oldName": "鲁润股份"
                }
            ],
            "stockCode": "600157",
            "actualControllerTypes": [
                "natural_person"
            ],
            "actualControllerName": "王广西"
        },
        {
            "city": "遵义市",
            "province": "贵州",
            "companyName": "贵州茅台酒股份有限公司",
            "historyStockNames": [],
            "stockCode": "600519",
            "actualControllerTypes": [
                "state_owned"
            ],
            "actualControllerName": "贵州省国有资产监督管理委员会"
        }
    ]
}
```
