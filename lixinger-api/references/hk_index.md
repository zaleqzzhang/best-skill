# API文档/香港/指数接口/基础信息

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/index
> API Key: `hk/index`

---

## 指数信息API

**简要描述:** 获取指数详细信息。

**请求URL:** `https://open.lixinger.com/api/hk/index`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/index](https://www.lixinger.com/api/open-api/html-doc/hk/index)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 指数代码数组。 默认值为所有指数的股票代码。格式如下：["HSI"]。 请参考 指数信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| name | String | 指数名称 |
| stockCode | String | 指数代码 |
| areaCode | String | 地区代码 |
| market | String | 市场 |
| fsTableType | String | 财务报表类型 非金融 : `non_financial`; 银行 : `bank`; 证券 : `security`; 保险 : `insurance`; 房地产投资信托 : `reit`; 其他金融 : `other_financial`; 混合 : `hybrid` |
| source | String | 指数来源 恒生 : `hsi` |
| currency | String | 货币 |
| series | String | 类型 规模 : `size`; 综合 : `composite`; 行业 : `sector`; 风格 : `style`; 主题 : `thematic`; 策略 : `strategy` |
| launchDate | Date | 发布时间 |
| rebalancingFrequency | String | 调样频率 年度 : `annually`; 半年 : `semi-annually`; 季度 : `quarterly`; 月度 : `monthly`; 不定期 : `irregularly`; 定期 : `aperiodically` |
| caculationMethod | String | 计算方式 派氏加权 : `paasche`; 分级靠档加权 : `grading_weighted`; 股息率加权 : `dividend_grading`; 等权 : `equal`; 自由流通市值加权 : `free_float_cap`; 修正资本化加权 : `modified_cap_weighted`; 流通市值加权 : `negotiable_mc_weighted`; 债券成分券流通金额加权 : `circulation_amount_of_constituent_bonds` |

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
            "areaCode": "hk",
            "market": "h",
            "stockCode": "HSAHP",
            "source": "hsi",
            "fsTableType": "hybrid",
            "name": "恒生沪深港通AH股溢价指数",
            "currency": "HKD",
            "launchDate": "2007-07-09T00:00:00+08:00",
            "series": "strategy"
        },
        {
            "areaCode": "hk",
            "market": "h",
            "stockCode": "HSAIT",
            "source": "hsi",
            "fsTableType": "non_financial",
            "currency": "HKD",
            "name": "恒生人工智能主题指数",
            "series": "sector",
            "launchDate": "2023-09-01T00:00:00+08:00"
        },
        {
            "areaCode": "hk",
            "market": "h",
            "stockCode": "HSBIO",
            "source": "hsi",
            "fsTableType": "non_financial",
            "currency": "HKD",
            "name": "恒生生物科技指数",
            "series": "sector",
            "launchDate": "2019-12-01T00:00:00+08:00"
        }
    ]
}
```
