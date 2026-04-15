# API文档/大陆/指数接口/热度数据/样本

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/ic
> API Key: `cn/index/hot/ic`

---

## 样本API

**简要描述:** 获取样本数据。

**请求URL:** `https://open.lixinger.com/api/cn/index/hot/ic`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/ic](https://www.lixinger.com/api/open-api/html-doc/cn/index/hot/ic)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 指数代码数组。 stockCodes长度>=1且<=100，格式如下：["000016"]。 请参考 指数信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| ic_t10_ws | Number | 前十大权重 |
| ic_num | Number | 样本数 |

### 示例

```json
{
    "stockCodes": [
        "000016"
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
            "ic_t10_ws": 0.46829099999999996,
            "ic_num": 50,
            "stockCode": "000016"
        }
    ]
}
```
