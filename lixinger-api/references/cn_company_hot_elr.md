# API文档/大陆/公司接口/热度数据/限售解禁

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/elr
> API Key: `cn/company/hot/elr`

---

## 限售解禁API

**简要描述:** 获取限售解禁数据。

**请求URL:** `https://open.lixinger.com/api/cn/company/hot/elr`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/elr](https://www.lixinger.com/api/open-api/html-doc/cn/company/hot/elr)

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
| last_data_date | Date | 最近一期预计解除限售时间 |
| srl_last | Number | 最近预计解除限售股数 |
| srl_cap_r_last | Number | 最近预计解除限售股数占总股本比例 |
| elr_s_y1 | Number | 未来一年预计解除限售股数 |
| elr_s_cap_r_y1 | Number | 未来一年预计解除限售股数占总股本比例 |
| elr_mc_y1 | Number | 未来一年预计解除限售市值 |

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
            "elr_s_y1": 45632363,
            "elr_s_cap_r_y1": 0.009998613772643125,
            "elr_mc_y1": 18275761381.5,
            "last_data_date": "2026-05-24T00:00:00+08:00",
            "srl_cap_r_last": 0.009998613772643125,
            "srl_last": 45632363,
            "stockCode": "300750"
        },
        {
            "elr_s_y1": 0,
            "elr_s_cap_r_y1": 0,
            "elr_mc_y1": 0,
            "stockCode": "600519"
        },
        {
            "elr_s_y1": 0,
            "elr_s_cap_r_y1": 0,
            "elr_mc_y1": 0,
            "stockCode": "600157"
        }
    ]
}
```
