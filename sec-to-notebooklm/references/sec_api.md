# SEC EDGAR API 参考

## 核心 API 端点

| 用途 | URL |
|------|-----|
| 公司 Ticker 映射 | `https://www.sec.gov/files/company_tickers.json` |
| 公司提交记录 | `https://data.sec.gov/submissions/CIK{cik10位}.json` |
| 报告文档索引 | `https://data.sec.gov/Archives/edgar/data/{cik}/{accession}/{accession}-index.json` |
| 下载文档 | `https://data.sec.gov/Archives/edgar/data/{cik}/{accession}/{filename}` |
| 全文搜索 | `https://efts.sec.gov/LATEST/search-index?q=...&forms=...` |
| 公司模糊搜索 | `https://www.sec.gov/cgi-bin/browse-edgar?company={name}&type=10-K&action=getcompany&output=atom` |

## 访问规则
- User-Agent 必须包含真实邮箱：`"MyApp admin@example.com"`
- 请求间隔 ≥ 0.1 秒（建议 0.5 秒）
- 每秒最多 10 次请求

## 常见报告类型

| 类型 | 说明 | 适用 |
|------|------|------|
| `10-K` | 年度报告 | 美股 |
| `10-Q` | 季度报告 | 美股 |
| `8-K` | 重大事件 | 美股 |
| `20-F` | 外国公司年报 | 中概股 |
| `6-K` | 外国公司中期 | 中概股 |
| `DEF 14A` | 代理说明书 | 美股 |
| `S-1` | IPO 招股书 | 美股 |

## CIK 格式
- CIK 必须补零至 10 位：`str(cik).zfill(10)`
- 文档 URL 中的 CIK 用 `int(cik)`（去掉前导零）
- accession number 格式：`0001234567-24-000001`（含横线）或 `0001234567240000001`（去横线）

## 中概股常用代码

| 公司 | Ticker | 报告类型 |
|------|--------|---------|
| 阿里巴巴 | BABA | 20-F |
| 腾讯 | TCEHY | 20-F |
| 京东 | JD | 20-F |
| 拼多多 | PDD | 20-F |
| 百度 | BIDU | 20-F |
| 网易 | NTES | 20-F |
