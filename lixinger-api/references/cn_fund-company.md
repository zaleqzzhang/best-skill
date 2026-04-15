# API文档/大陆/基金接口/基金公司接口/基础信息

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/fund-company
> API Key: `cn/fund-company`

---

## 基金公司信息API

**简要描述:** 获取基金公司详细信息。

**请求URL:** `https://open.lixinger.com/api/cn/fund-company`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund-company](https://www.lixinger.com/api/open-api/html-doc/cn/fund-company)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 基金公司代码数组。 请参考 基金信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| name | String | 基金公司名称 |
| stockCode | String | 基金公司代码 |
| inceptionDate | Date | 成立日期 |
| fundsNum | Number | 基金数量 |
| assetScale | Number | 总资产规模 |
| fundCollectionType | String | 基金公司类型 基金公司 : `fund_company`; 证券公司 : `securities_company`; 证券公司资产管理子公司 : `securities_company_amsc`; 保险资产管理公司 : `insurance_am_company` |

### 示例

```json
{
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
            "fundCollectionType": "securities_company_amsc",
            "stockCode": "13700000",
            "name": "华安证券资产管理有限公司",
            "inceptionDate": ""
        },
        {
            "fundCollectionType": "securities_company_amsc",
            "stockCode": "13810000",
            "name": "国联证券资产管理有限公司",
            "inceptionDate": ""
        },
        {
            "fundCollectionType": "securities_company_amsc",
            "stockCode": "13840000",
            "name": "长城证券资产管理有限公司",
            "inceptionDate": ""
        }
    ]
}
```
