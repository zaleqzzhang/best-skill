# API文档/大陆/基金接口/基金经理接口/管理的基金

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/fund-manager/management-funds
> API Key: `cn/fund-manager/management-funds`

---

## 管理的基金信息API

**简要描述:** 获取管理的基金详细信息。

**请求URL:** `https://open.lixinger.com/api/cn/fund-manager/management-funds`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund-manager/management-funds](https://www.lixinger.com/api/open-api/html-doc/cn/fund-manager/management-funds)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 基金经理代码数组。 stockCodes长度>=1且<=100，格式如下：["8801388323","8801372475"]。 请参考 基金信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| funds | Array | 基金数组。 子字段: 基金名称 : `name` : (String); 基金代码 : `code` : (String); 任职日期 : `appointmentDate` : (Date); 离任日期 : `departureDate` : (Date) |

### 示例

```json
{
    "stockCodes": [
        "8801388323",
        "8801372475"
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
            "stockCode": "8801372475",
            "funds": [
                {
                    "code": "118001",
                    "name": "易方达亚洲精选股票（QDII）",
                    "appointmentDate": "2014-04-08T00:00:00+08:00"
                },
                {
                    "code": "110011",
                    "name": "易方达优质精选混合（QDII）",
                    "appointmentDate": "2012-09-28T00:00:00+08:00"
                },
                {
                    "code": "009342",
                    "name": "易方达优质企业三年持有混合",
                    "appointmentDate": "2020-06-17T00:00:00+08:00"
                },
                {
                    "code": "005827",
                    "name": "易方达蓝筹精选混合",
                    "appointmentDate": "2018-09-05T00:00:00+08:00"
                },
                {
                    "code": "001373",
                    "name": "易方达新丝路混合",
                    "appointmentDate": "2015-11-07T00:00:00+08:00",
                    "departureDate": "2021-02-11T00:00:00+08:00"
                }
            ]
        },
        {
            "stockCode": "8801388323",
            "funds": [
                {
                    "code": "960000",
                    "name": "汇丰晋信大盘股票H",
                    "appointmentDate": "2015-12-28T00:00:00+08:00",
                    "departureDate": "2018-04-28T00:00:00+08:00"
                },
                {
                    "code": "540006",
                    "name": "汇丰晋信大盘股票A",
                    "appointmentDate": "2014-09-16T00:00:00+08:00",
                    "departureDate": "2018-04-28T00:00:00+08:00"
                },
                {
                    "code": "017650",
                    "name": "中庚港股通价值股票",
                    "appointmentDate": "2023-01-11T00:00:00+08:00",
                    "departureDate": "2024-07-19T00:00:00+08:00"
                },
                {
                    "code": "011174",
                    "name": "中庚价值品质一年持有期混合",
                    "appointmentDate": "2021-01-19T00:00:00+08:00",
                    "departureDate": "2024-07-19T00:00:00+08:00"
                },
                {
                    "code": "007497",
                    "name": "中庚价值灵动灵活配置混合",
                    "appointmentDate": "2019-07-16T00:00:00+08:00",
                    "departureDate": "2024-07-19T00:00:00+08:00"
                },
                {
                    "code": "007130",
                    "name": "中庚小盘价值股票",
                    "appointmentDate": "2019-04-03T00:00:00+08:00",
                    "departureDate": "2024-07-19T00:00:00+08:00"
                },
                {
                    "code": "006551",
                    "name": "中庚价值领航混合",
                    "appointmentDate": "2018-12-19T00:00:00+08:00",
                    "departureDate": "2024-07-19T00:00:00+08:00"
                },
                {
                    "code": "000850",
                    "name": "汇丰晋信双核策略混合C",
                    "appointmentDate": "2014-11-26T00:00:00+08:00",
                    "departureDate": "2018-04-28T00:00:00+08:00"
                },
                {
                    "code": "000849",
                    "name": "汇丰晋信双核策略混合A",
                    "appointmentDate": "2014-11-26T00:00:00+08:00",
                    "departureDate": "2018-04-28T00:00:00+08:00"
                }
            ]
        }
    ]
}
```
