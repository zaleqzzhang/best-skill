# API文档/大陆/公司接口/公告

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/announcement
> API Key: `cn/company/announcement`

---

## 公告API

**简要描述:** 获取公告信息。

**请求URL:** `https://open.lixinger.com/api/cn/company/announcement`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/announcement](https://www.lixinger.com/api/open-api/html-doc/cn/company/announcement)

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
| types | Array | 种类 全部 : `all`; 财务报表 : `fs`; 业绩预告 : `fsfc`; 经营数据 : `o_d`; 权益分派 : `eac`; 董事会 : `bm`; 监事会 : `sm`; 股东大会 : `shm`; 股权激励 : `so`; 解禁 : `ntsu`; 债券 : `b`; 可转换债券 : `c_b`; 股权变更 : `eat`; 澄清及风险提示 : `c_rp`; 投资者关系 : `irs`; 问询函 : `i_l`; 配股 : `sa`; 增发 : `spo`; 回购 : `srp`; IPO : `ipo`; 其它 : `other` |

### 示例

```json
{
    "startDate": "2025-03-20",
    "endDate": "2026-03-20",
    "stockCode": "300750",
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
            "linkUrl": "http://static.cninfo.com.cn/finalpage/2026-03-10/1225002708.PDF",
            "date": "2026-03-10T00:00:00+08:00",
            "linkText": "2026年3月9日投资者关系活动记录表",
            "linkType": "PDF",
            "types": [
                "irs"
            ]
        },
        {
            "linkUrl": "https://disc.static.szse.cn/disc/disk03/finalpage/2026-03-10/15ee7faf-ffc6-4f9f-9343-7dbfb1e9bf77.PDF",
            "date": "2026-03-10T00:00:00+08:00",
            "linkText": "宁德时代：《2025年度独立董事述职报告》（林小雄）",
            "linkType": "PDF",
            "types": [
                "fs",
                "fs_b_m"
            ]
        },
        {
            "linkUrl": "https://disc.static.szse.cn/disc/disk03/finalpage/2026-03-10/b99e5038-3393-42fa-acc9-1ffeded79225.PDF",
            "date": "2026-03-10T00:00:00+08:00",
            "linkText": "宁德时代：2025年年度报告摘要",
            "linkType": "PDF",
            "types": [
                "fs",
                "fs_s"
            ]
        }
    ]
}
```
