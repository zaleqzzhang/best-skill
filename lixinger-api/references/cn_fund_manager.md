# API文档/大陆/基金接口/公募基金接口/基金经理

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/fund/manager
> API Key: `cn/fund/manager`

---

## 基金经理API

**简要描述:** 获取该基金历史上所有的基金经理任职信息。

**说明:**

- 主基金代码和子基金代码获取相同的数据。

**请求URL:** `https://open.lixinger.com/api/cn/fund/manager`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund/manager](https://www.lixinger.com/api/open-api/html-doc/cn/fund/manager)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 基金代码数组。 stockCodes长度>=1且<=100，格式如下：["161725","005827"]。 请参考 基金信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 基金代码 |
| managers | Array | 基金经理数组。 子字段: 基金经理姓名 : `name` : (String); 基金经理代码 : `managerCode` : (String); 任职日期 : `appointmentDate` : (Date); 离任日期 : `departureDate` : (Date) |

### 示例

```json
{
    "stockCodes": [
        "161725",
        "005827"
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
            "stockCode": "005827",
            "managers": [
                {
                    "name": "张坤",
                    "appointmentDate": "2018-09-05T00:00:00+08:00",
                    "managerCode": "8801372475"
                }
            ]
        },
        {
            "stockCode": "161725",
            "managers": [
                {
                    "name": "王立立",
                    "appointmentDate": "2015-05-27T00:00:00+08:00",
                    "departureDate": "2016-05-19T00:00:00+08:00",
                    "managerCode": "8801381441"
                },
                {
                    "name": "王平",
                    "appointmentDate": "2015-05-27T00:00:00+08:00",
                    "departureDate": "2016-12-03T00:00:00+08:00",
                    "managerCode": "db20069308"
                },
                {
                    "name": "陈剑波",
                    "appointmentDate": "2016-04-19T00:00:00+08:00",
                    "departureDate": "2017-09-05T00:00:00+08:00",
                    "managerCode": "8801404091"
                },
                {
                    "name": "侯昊",
                    "appointmentDate": "2017-08-22T00:00:00+08:00",
                    "managerCode": "db20376719"
                }
            ]
        }
    ]
}
```
