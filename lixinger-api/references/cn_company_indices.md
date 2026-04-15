# API文档/大陆/公司接口/股票所属指数

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/indices
> API Key: `cn/company/indices`

---

## 股票所属指数信息API

**简要描述:** 获取股票所属指数信息。

**请求URL:** `https://open.lixinger.com/api/cn/company/indices`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/indices](https://www.lixinger.com/api/open-api/html-doc/cn/company/indices)

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
| name | String | 指数名称 |
| areaCode | String | 地区代码 |
| stockCode | String | 指数代码 |
| source | String | 指数来源 中证 : `csi`; 国证 : `cni`; 恒生 : `hsi`; 美指 : `usi`; 理杏仁 : `lxri` |

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
            "stockCode": "1000011",
            "source": "lxri",
            "name": "A股非金融"
        },
        {
            "areaCode": "cn",
            "stockCode": "1000007",
            "source": "lxri",
            "name": "创业板全指"
        },
        {
            "areaCode": "cn",
            "stockCode": "1000003",
            "source": "lxri",
            "name": "深圳A股"
        }
    ]
}
```
