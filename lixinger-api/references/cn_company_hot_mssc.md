# API文档/大陆/公司接口/热度数据/大股东增减持

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/mssc
> API Key: `cn/company/hot/mssc`

---

## 大股东增减持API

**简要描述:** 获取大股东增减持数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/hot/mssc`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/mssc](https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/mssc)

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
| last_data_date | Date | 数据时间 |
| mssca_last | Number | 最新大股东增减持金额 |
| mssc_cap_rc_last | Number | 最新大股东增减持占流通A股比例 |
| mssca_m1 | Number | 过去1个月累计大股东增减持金额 |
| mssca_m3 | Number | 过去3个月累计大股东增减持金额 |
| mssca_m6 | Number | 过去6个月累计大股东增减持金额 |
| mssca_y1 | Number | 过去1年累计大股东增减持金额 |
| mssca_y2 | Number | 过去2年累计大股东增减持金额 |
| mssca_y3 | Number | 过去3年累计大股东增减持金额 |
| mssc_cap_rc_m1 | Number | 过去1个月累计大股东增减持占流通A股比例 |
| mssc_cap_rc_m3 | Number | 过去3个月累计大股东增减持占流通A股比例 |
| mssc_cap_rc_m6 | Number | 过去6个月累计大股东增减持占流通A股比例 |
| mssc_cap_rc_y1 | Number | 过去1年累计大股东增减持占流通A股比例 |
| mssc_cap_rc_y2 | Number | 过去2年累计大股东增减持占流通A股比例 |
| mssc_cap_rc_y3 | Number | 过去3年累计大股东增减持占流通A股比例 |

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
            "last_data_date": "2025-11-24T00:00:00+08:00",
            "mssca_last": 0,
            "mssc_cap_rc_last": 0,
            "mssca_m6": 0,
            "mssca_y1": 0,
            "mssca_y2": 0,
            "mssca_y3": 0,
            "mssc_cap_rc_m6": 0,
            "mssc_cap_rc_y1": 0,
            "mssc_cap_rc_y2": 0,
            "mssc_cap_rc_y3": 0,
            "stockCode": "300750"
        },
        {
            "last_data_date": "2025-12-26T00:00:00+08:00",
            "mssc_cap_rc_y3": 0.0016540831005870406,
            "msscm_last": 1405917719.001,
            "msscm_y1": 1463197442.001,
            "msscm_y2": 1463197442.001,
            "msscm_y3": 1463197442.001,
            "mssca_y3": 4465110766.056,
            "mssca_last": 2901860325.9839997,
            "mssc_cap_rc_last": 0.0015999246616274427,
            "mssc_cap_rc_m6": 0.0015999246616274427,
            "mssc_cap_rc_y1": 0.0016540831005870406,
            "mssc_cap_rc_y2": 0.0016540831005870406,
            "mssca_m6": 2901860325.9839997,
            "mssca_y1": 3001913324.055,
            "mssca_y2": 3001913324.055,
            "mssc_cap_rc_m3": 0.0015999246616274427,
            "mssca_m3": 2901860325.9839997,
            "stockCode": "600519"
        },
        {
            "last_data_date": "2024-09-12T00:00:00+08:00",
            "mssc_cap_rc_y2": 0,
            "mssc_cap_rc_y3": 0,
            "msscm_last": 5412870,
            "msscm_m6": 36704581,
            "msscm_y1": 36704581,
            "msscm_y2": 36704581,
            "msscm_y3": 36704581,
            "mssca_y2": 31898880,
            "mssca_y3": 68603461,
            "mssca_last": 15171000,
            "stockCode": "600157"
        }
    ]
}
```
