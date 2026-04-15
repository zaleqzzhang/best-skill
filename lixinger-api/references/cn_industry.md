# API文档/大陆/行业接口/基础信息

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/industry
> API Key: `cn/industry`

---

## 股票信息API

**简要描述:** 获取股票详细信息。

**请求URL:** `https://open.lixinger.com/api/cn/industry`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/industry](https://www.lixinger.com/api/open-api/html-doc/cn/industry)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 行业代码数组。 默认值为所有行业的股票代码。格式如下：["490000"]。 请参考 行业信息API 获取合法的stockCode。 |
| source | Yes | String | 行业来源，例如：{source}。 **当前支持:** 申万: `sw`; 申万2021版: `sw_2021`; 国证: `cni` |
| level | No | String | 行业分类级别，例如：'one'。 **当前支持:** 一级: `one`; 二级: `two`; 三级: `three` |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 行业代码 |
| name | String | 行业名称 |
| launchDate | Date | 发布时间 |
| areaCode | String | 地区代码 |
| market | String | 市场 |
| fsTableType | String | 财务报表类型 非金融 : `non_financial`; 银行 : `bank`; 证券 : `security`; 保险 : `insurance`; 房地产投资信托 : `reit`; 其他金融 : `other_financial`; 混合 : `hybrid` |
| level | String | 行业分类等级 |
| source | String | 行业来源 国证 : `cni`; 申万 : `sw`; 申万2021版 : `sw_2021` |
| currency | String | 货币 |

### 示例

```json
{
    "stockCodes": [
        "490000"
    ],
    "source": "sw",
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
            "stockCode": "490000",
            "name": "非银金融",
            "launchDate": "2014-01-01T00:00:00+08:00",
            "level": "one",
            "areaCode": "cn",
            "market": "a",
            "source": "sw",
            "currency": "CNY",
            "fsTableType": "hybrid"
        }
    ]
}
```
