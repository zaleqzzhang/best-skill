# 跨平台舆情分析 Dashboard Skill

> 给 AI Agent 用的"建跨平台舆情分析系统"完整方案，基于 **CFL 生产环境** 沉淀的架构与代码模板。

---

## V1.0.0 功能介绍

**一句话**：通过 4 个内置 fetcher 自动拉取 Discord / Facebook / YouTube / Web Search 的舆情原始数据，由统一 ETL Pipeline 转换成标准化 JSON（4 情感标签 + 平台元信息 + 原始消息），落到 GitHub 仓库作为唯一数据源；前端是纯静态 HTML+JS Dashboard（无后端），加载这些 JSON 即可渲染趋势图、用户排行、频道分布、精选消息等可视化；**每日定时由 GitHub Actions 自动跑 ETL 拉取增量数据**，并支持划词 AI 翻译（任意选中外文自动弹窗）和数据问答（用自然语言查询站内数据）。全流程无需手写后端、无需服务器，部署到任意静态 host 即可内网访问。

## 使用步骤

直接对 AI 说（支持以下任一方式）：

- 「帮我搭一个跨平台舆情 Dashboard，接 Discord 和 YouTube 两个平台，关键词是 `CFL, CrossFire, 穿越火线`」
- 「把 Facebook 也加进来，我要看每条帖子的评论和点赞分布」
- 「跑一下今天的数据，存到 `myorg/sentiment-data` 仓库的 `data/daily/` 目录」
- 「给 Dashboard 加一个划词翻译功能，我接到 DeepSeek」
- 「我想加个数据问答页面，让用户能用自然语言查'昨天负面最多的是哪个频道'」

平台、数据仓库、关键词、ETL 频率、LLM 接入方式（DeepSeek / OpenAI / Ollama / 内部 LLM 网关）全部通过对话传入，无需修改任何文件。

如需扩展内置 4 个平台（Discord / Facebook / YouTube / Web Search）以外的平台，只需提供平台名 + 原始数据格式说明，AI 会自动生成对应的 fetcher 和 ETL 适配代码。

## 内置 4 平台

| 平台 | 数据类型 | 关键字段 |
|---|---|---|
| **Discord** | 频道消息 | 频道、用户、文本、@mention、情感 |
| **Facebook** | 帖子 + 评论 | 帖子标题、评论、点赞、点赞排行 |
| **YouTube** | 视频 + 评论 | 视频元数据、播放量、创作者、搜索词来源 |
| **Web Search** | 搜索结果 | 标题、摘要、URL、来源域名 |

## 输出格式（统一 JSON Schema）

```json
{
  "date": "2026-07-03",
  "platform": "discord",
  "total_messages": 1234,
  "positive": 600, "negative": 80, "feedback": 400, "neutral": 154,
  "channels": { "general": 500, "off-topic": 300 },
  "active_users": 234,
  "keywords": [{ "word": "ranked", "count": 89 }],
  "all_messages": [/* 每条消息原始结构 */],
  "top_messages": [/* 按热度排序的精选 */],
  "_platform_meta": { /* 平台特有扩展：posts / videos / channels / queries */ }
}
```

## 仪表盘页面（默认 4 页）

1. **舆情总览** — 4 KPI 卡片（消息量 / 活跃用户 / 情感分布 / 趋势）+ 7 张图表 + 精选消息
2. **官方社区舆情** — Discord + Facebook 详情，趋势按平台堆叠，频道/帖子分布
3. **外部舆情** — YouTube + Web Search，视频/创作者排行，搜索词聚合
4. **数据问答** — 自然语言查询站内数据（流式 LLM 输出）

附加能力：**划词 AI 翻译** — 选中任何外文文本自动弹出中文翻译浮窗，LLM-agnostic。

## 系统要求

| 依赖 | 说明 |
|---|---|
| Python ≥ 3.10 | ETL Pipeline + fetcher 脚本运行环境 |
| GitHub PAT | `repo` + `workflow` 权限，用于 ETL 推送数据 + 配置 Actions |
| GitHub Actions | 每日定时跑 ETL 增量拉取（默认 UTC 0:00） |
| LLM API Key | 划词翻译 + 数据问答，可选 DeepSeek / OpenAI / Ollama / 内部网关 |
| 静态 host | 部署 Dashboard 前端：Cloudflare Pages / GitHub Pages / 内网 OA Pages |

## 安全提醒

- **GitHub PAT** 只用于 CI/本地 ETL 推送，**不要暴露在前端**
- **LLM API Key** 在前端可见（浏览器 JS），生产环境建议用 Cloudflare Worker / 网关代理避免 key 泄漏
- Dashboard 部署到内网（OA Pages）时启用 `tof` 鉴权，登录后才能访问

## 与参考 skill 的差异

- **Apify 版**：用 Apify 平台做爬虫，托管 actor，依赖第三方
- **本 skill**：自建 fetcher（Python + 各平台官方 API），数据完全自有，不依赖第三方平台账单
- **共同点**：都通过 GitHub 仓库 + Actions 做归档和定时，都输出标准化 JSON + Dashboard
