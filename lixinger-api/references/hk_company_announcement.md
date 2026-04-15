# API文档/香港/公司接口/公告

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/company/announcement
> API Key: `hk/company/announcement`

---

## 公告API

**简要描述:** 获取公告信息。

**请求URL:** `https://open.lixinger.com/api/hk/company/announcement`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/company/announcement](https://www.lixinger.com/api/open-api/html-doc/hk/company/announcement)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考股票信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| date | Date | 公告日期 |
| linkText | String | 链接文本 |
| linkUrl | String | 链接地址 |
| linkType | String | 链接类型 |
| types | Array | 种类 全部 : `all`; 财务报表 : `fs`; 配售 : `spo`; 供股 : `sa`; 回购 : `srp`; 会议及表决 : `m_a_v`; 翌日披露报表—其他 : `ndd_r`; 月报表 : `mr`; IPO : `ipo` |

### 示例

```json
{
    "startDate": "2025-03-20",
    "endDate": "2026-03-20",
    "stockCode": "00700",
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
            "linkUrl": "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0319/2026031900555_c.pdf",
            "date": "2026-03-19T00:00:00+08:00",
            "linkText": "翌日披露報表 - 已發行股份變動",
            "linkType": "PDF",
            "types": [
                "ndd_r"
            ]
        },
        {
            "linkUrl": "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0318/2026031800477_c.pdf",
            "date": "2026-03-18T00:00:00+08:00",
            "linkText": "截至二零二五年十二月三十一日止年度末期股息",
            "linkType": "PDF",
            "types": [
                "all"
            ]
        },
        {
            "linkUrl": "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0318/2026031800389_c.pdf",
            "date": "2026-03-18T00:00:00+08:00",
            "linkText": "截至二零二五年十二月三十一日止年度全年業績公佈",
            "linkType": "PDF",
            "types": [
                "fs",
                "fs_main"
            ]
        }
    ]
}
```
