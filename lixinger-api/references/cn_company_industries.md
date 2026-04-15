# API文档/大陆/公司接口/股票所属行业

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/industries
> API Key: `cn/company/industries`

---

## 股票所属行业信息API

**简要描述:** 获取股票所属行业信息。

**请求URL:** `https://open.lixinger.com/api/cn/company/industries`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/industries](https://www.lixinger.com/api/open-api/html-doc/cn/company/industries)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 股票代码 请参考股票信息API获取合法的stockCode。 |
| date | No | String: YYYY-MM-DD (北京时间) | 信息时间。默认值是当前最新时间。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| name | String | 行业名称 |
| areaCode | String | 地区代码 |
| stockCode | String | 行业代码 |
| source | String | 行业来源 申万 : `sw`; 申万2021版 : `sw_2021`; 国证 : `cni` |

### 示例

```json
{
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
            "areaCode": "cn",
            "stockCode": "C030103",
            "source": "cni",
            "name": "电气部件与设备"
        },
        {
            "areaCode": "cn",
            "stockCode": "C0301",
            "source": "cni",
            "name": "工业品"
        },
        {
            "areaCode": "cn",
            "stockCode": "C03",
            "source": "cni",
            "name": "工业"
        }
    ]
}
```
