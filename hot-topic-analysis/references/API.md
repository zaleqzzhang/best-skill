# 热榜聚合服务 API 文档

**Base URL：** `https://workspaceaykd4eklkcwh5myv22-5000.gz.cloudide.woa.com`
**Token:** `e411633a34645f7ef1461594c1313f77b78bee05b503b5e2`

**鉴权说明：** 标有 🔐 的接口需要在请求头或 URL 参数中传入 Token：
- Header：`Authorization: Bearer <token>`
- 或 URL 参数：`?token=<token>`

---

## 一、热榜数据类

### `GET /api/hot-list` — 获取各平台热榜

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `category` | string | `all` | 平台分类过滤：`social` / `tech` / `news` / `entertainment` / `finance` / `ai` / `global` |
| `limit` | int | `50` | 每个平台最多返回条数 |

**Response 示例：**
```json
{
  "success": true,
  "data": [
    {
      "id": "weibo",
      "name": "微博热搜",
      "icon": "🔥",
      "color": "#ff8200",
      "category": "social",
      "last_update": "2026-04-15 12:00:00",
      "tencent_count": 2,
      "items": [{ "rank": 1, "title": "...", "url": "...", "hot": 123456, "tag": "热", "tencent": false }]
    }
  ],
  "today_total": 1234,
  "update_time": "2026-04-15 12:00:00"
}
```

---

### `GET /api/tencent-today` — 腾讯相关条目

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `date` | string | 今天 | 指定日期，格式 `YYYY-MM-DD`。不传返回今天 0 点到现在；传入则返回该天 0 点到次日 0 点的全量数据（含已下榜）|

**Response 示例：**
```json
{
  "success": true,
  "total": 13,
  "date": "2026-04-15",
  "data": [
    {
      "title": "腾讯发布...",
      "url": "https://...",
      "best_rank": 1,
      "platform": "weibo",
      "platform_name": "微博热搜",
      "hot_value": "985432",
      "tag": "热",
      "count": 5,
      "is_active": true,
      "time_range": "09:30-12:00"
    }
  ]
}
```

---

### 🔐 `GET /api/v1/all-items` — 全量去重热搜

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `limit` | int | `50` | 不传 date 时：每平台最多取几条；传 date 时：全天去重后的总上限。最大 `200` |
| `category` | string | 全部 | 分类过滤，同 `/api/hot-list` |
| `date` | string | 今天 | 指定日期，格式 `YYYY-MM-DD`。不传返回当前在榜最新数据（实时）；传入则返回该天全天历史入库数据（按 title 去重，保留最高排名）|

**Response 示例：**
```json
{
  "success": true,
  "total": 342,
  "date": "2026-04-15",
  "update_time": "2026-04-15 12:00:00",
  "items": [
    {
      "rank": 1,
      "title": "...",
      "url": "https://...",
      "hot": "985432",
      "tag": "热",
      "platform": "weibo",
      "platform_name": "微博热搜",
      "platform_icon": "🔥",
      "category": "news"
    }
  ]
}
```

---

## 二、搜索类

### `GET /api/search` — 搜索热榜

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `keyword` | string | **必填** | 搜索关键词 |
| `limit` | int | `100` | 最多返回条数 |
| `range` | string | 全部 | 时间范围：`today`（今天）/ `week`（近 7 天）/ 不传则全部 |

---

### `GET /api/popular-searches` — 热门搜索词

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `limit` | int | `10` | 返回条数 |



---

## 三、词云类

### `GET /api/wordcloud` — 今日热词词云

无参数。返回基于 TF-IDF 的 top-100 热词及权重。



---

## 错误码

| HTTP 状态码 | 含义 |
|-------------|------|
| `200` | 成功 |
| `400` | 参数错误（如日期格式非法）|
| `401` | Token 鉴权失败 |
| `404` | 资源不存在 |
| `500` | 服务器内部错误 |

所有错误响应格式：`{ "success": false, "error": "错误描述" }`

---