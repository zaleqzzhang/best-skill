# API文档/大陆/基金接口/基金经理接口/利润率

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/fund-manager/profit-ratio
> API Key: `cn/fund-manager/profit-ratio`

---

## 利润率API

**简要描述:** 获取利润率信息。

**请求URL:** `https://open.lixinger.com/api/cn/fund-manager/profit-ratio`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund-manager/profit-ratio](https://www.lixinger.com/api/open-api/html-doc/cn/fund-manager/profit-ratio)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考基金信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| date | Date | 公告日期 |
| startDate | Date | 计算起始日期 |
| value | Number | 数额 |

### 示例

```json
{
    "startDate": "2025-03-20",
    "endDate": "2026-03-20",
    "stockCode": "8801388323",
    "token": "***********"
}
```

### 返回结果

```json
{
    "code": 1,
    "message": "success",
    "data": []
}
```
