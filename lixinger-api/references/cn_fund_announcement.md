# 公告API

## 公告API

**简要描述:** 获取公告信息。

**请求URL:** `https://open.lixinger.com/api/cn/fund/announcement`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund/announcement](https://www.lixinger.com/api/open-api/html-doc/cn/fund/announcement)

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
| lang | String | 语言 |
| linkText | String | 链接文本 |
| linkUrl | String | 链接地址 |
| linkType | String | 链接类型 |
| types | Array | 种类 全部 : `all`; 财务报表 : `fs`; 招募设立 : `s_u`; 分红 : `dividend`; 拆分折算 : `split`; 其它 : `other` |

### 示例

```json
{
    "startDate": "2025-03-20",
    "endDate": "2026-03-20",
    "stockCode": "161725",
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
            "linkUrl": "http://eid.csrc.gov.cn/fund/disclose/instance_show_pdf_id.do?instanceid=1431521",
            "date": "2026-01-30T00:00:00+08:00",
            "linkText": "招商中证白酒指数证券投资基金（LOF）溢价风险提示公告",
            "linkType": "PDF",
            "lang": "cmn_hans_cn",
            "types": [
                "other"
            ]
        },
        {
            "linkUrl": "http://eid.csrc.gov.cn/fund/disclose/instance_show_pdf_id.do?instanceid=1416653",
            "date": "2026-01-21T00:00:00+08:00",
            "linkText": "招商中证白酒指数证券投资基金2025年第4季度报告",
            "linkType": "PDF",
            "lang": "cmn_hans_cn",
            "types": [
                "fs",
                "fs_full"
            ]
        },
        {
            "linkUrl": "http://eid.csrc.gov.cn/fund/disclose/instance_show_pdf_id.do?instanceid=1369803",
            "date": "2025-10-27T00:00:00+08:00",
            "linkText": "招商中证白酒指数证券投资基金2025年第3季度报告",
            "linkType": "PDF",
            "lang": "cmn_hans_cn",
            "types": [
                "fs",
                "fs_full"
            ]
        }
    ]
}
```
