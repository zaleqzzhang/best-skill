# API文档/香港/公司接口/公司概况

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/company/profile
> API Key: `hk/company/profile`

---

## 公司概况API

**简要描述:** 获取公司概况数据

**请求URL:** `https://open.lixinger.com/api/hk/company/profile`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/company/profile](https://www.lixinger.com/api/open-api/html-doc/hk/company/profile)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 股票代码数组。 stockCodes长度>=1且<=100，格式如下：["00700"]。 请参考 股票信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| listingDate | Date | 上市日期 |
| chairman | String | 董事长 |
| classAdescription | String | A股 |
| classBdescription | String | B股 |
| capitalStructureClassA | Number | A股股本结构 |
| capitalStructureClassB | Number | B股股本结构 |
| fiscalYearEnd | Date | 财政年度结算日期 |
| summary | String | 公司概况 |
| listingCategory | String | 上市类型 |
| registrar | String | 过户处 |
| website | String | 公司网址 |
| registeredAddress | String | 注册地址 |
| officeAddress | String | 办公地址 |

### 示例

```json
{
    "stockCodes": [
        "00700"
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
            "fiscalYearEnd": "2024-12-31T00:00:00+08:00",
            "listingDate": "2004-06-16T00:00:00+08:00",
            "chairman": "马化腾",
            "officeAddress": "香港/湾仔/皇后大道东1号/太古广场三座29楼",
            "registeredAddress": "开曼群岛",
            "listingCategory": "主要上市",
            "registrar": "香港中央证券登记有限公司",
            "summary": "腾讯控股有限公司是一家主要提供增值服务（VAS）、网络广告服务以及金融科技及企业服务的投资控股公司。该公司主要通过四个分部开展业务。增值服务分部主要从事提供网络游戏、视频号直播服务和视频付费会员服务等社交网络服务。网络广告分部主要从事媒体广告、社交及其他广告业务。金融科技及企业服务主要提供商业支付、金融科技及云服务。其他分部主要从事投资、为第三方制作与发行电影及电视节目、内容授权，商品销售及其他活动。",
            "capitalStructureClassA": null,
            "capitalStructureClassB": null,
            "classAdescription": null,
            "classBdescription": null,
            "website": "http://www.tencent.com",
            "stockCode": "00700"
        }
    ]
}
```
