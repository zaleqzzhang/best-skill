# 行迹 · TravelCraft — 版本变更日志

遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/) 和 [Keep a Changelog](https://keepachangelog.com/zh-CN/) 规范。

---

## [2.3.0] — 2026-04-21

### 🐙 GitHub Pages 部署引擎

v2.0 的 EdgeOne Pages 预览域名在国内 3 小时过期、Vercel 在国内 5G 下访问不稳定——为此新增 GitHub Pages 作为第三条部署路径，**国内访问稳定 + 免备案 + 完全免费**。

#### 新增功能
- **deploy_to_github.sh**：一键 clone/commit/push 到 GitHub 仓库 + 自动开启 GitHub Pages
- **多引擎并存**：EdgeOne Pages / Vercel / GitHub Pages 三选一或组合部署
- **书架卡片按钮优化**：优先显示 `🚀 打开`（GitHub Pages），备用 `🌏 备用`（Vercel），按可用性自动切换
- **update_index.py** 新增 `--url-github` 参数，统一管理三种 URL

#### 部署引擎对比

| 引擎 | 国内访问 | 海外访问 | 免备案 | 成本 | 公开/私密 |
|------|---------|---------|-------|------|---------|
| GitHub Pages | ⚡️ 快 | ⚡️ 快 | ✅ | 免费 | 公开（建议加 AES 密码）|
| EdgeOne Pages | 需备案域名 | 需备案域名 | ❌ | 免费 | 默认预览域名 3h 过期 |
| Vercel | 🐢 不稳 | ⚡️ 快 | ✅ | 免费 | 可加访问保护 |

#### 准备工作
首次使用 GitHub Pages 部署需要：
1. 创建一个 GitHub 公开仓库（如 `travelcraft-trips`）
2. 生成 Personal Access Token (scope: `repo`)：https://github.com/settings/tokens/new
3. `export GH_TOKEN=ghp_xxx`

详见 `references/deployment-guide.md` 的 GitHub 章节。

#### 变更
- SKILL.md 升级到 v2.3.0
- 索引页模板按钮文案更新
- 书架 trips.json schema 新增 `urls.github` 字段

#### 兼容性
- ✅ 完全向后兼容 v2.2
- ✅ 老的 urls.eop / urls.vercel 仍然支持
- ✅ 如果 `urls.github` 存在，书架会优先显示它

---

## [2.2.0] — 2026-04-20

### 🗺 地图集成版

#### 新增功能
- **Phase 3.5 路线校准**：调用腾讯位置服务 WebService API，对 Phase 3 的行程估算时长做真实路线核验，偏差 > 20% 自动提示用户调整
- **Phase 4.5 交互地图嵌入**：在行程 HTML 顶部注入 Javascript API GL 地图，显示完整路线、分段配色、景点标注
- **一键导航按钮**：点击任意景点或每日段落 → 唤起腾讯地图 APP 进行导航（未装 APP 时自动落地 H5）
- **每日路线卡片**：实测 km + 实测小时 + 与估算偏差 + 导航按钮
- **工作流扩展为 7 阶段**：在 Phase 3（编排）后、Phase 4（构建）前新增 Phase 3.5

#### 新增文件
- `scripts/geocode_places.py` — 批量地理编码（地名 → 经纬度）
- `scripts/calibrate_route.py` — 驾车路线校准（含 polyline 差分解码）
- `scripts/inject_tmap.py` — 地图嵌入工具 + 宋式美学 UI 模板
- `references/map-integration-guide.md` — Phase 3.5/4.5 技术指南

#### 变更
- SKILL.md frontmatter `version: 2.2.0`
- SKILL.md 工作流由 6 阶段扩展为 7 阶段（Phase 3.5 为可选）
- SKILL.md 新增 Step 4.5 地图注入说明
- README + 使用说明.docx 同步说明新增能力

#### 新增依赖
- **运行时**：仅使用 Python 标准库（urllib），无新增 pip 依赖
- **外部服务**：腾讯位置服务 Key（免费，10k 次/日/产品）
- **关键配置**：Key 创建后必须在「配额管理」手动分配额度（常见陷阱）

#### 兼容性
- ✅ 完全向后兼容 v2.1
- ✅ Phase 3.5/4.5 均为可选，不配置 Key 时跳过
- ✅ 纯城内行程（无跨城驾车）会自动跳过 Phase 3.5

---

## [2.1.0] — 2026-04-20

### 📖 文档增强版

#### 变更
- **完整重构 Word 文档**：从「8 章产品介绍」升级为「18 章 + 3 附录」的产品说明 + 使用手册一体化指南
- 新增 **Part II 使用手册** 章节（9-18 章）：
  - 第 9 章：5 分钟快速上手
  - 第 10 章：需求澄清话术库（20+ 句模板）
  - 第 11 章：调研阶段的控制
  - 第 12 章：行程修改指令手册
  - 第 13 章：本地交付物使用指南
  - 第 14 章：云端部署完整流程（深度扩展）
  - 第 15 章：**10 个实战场景脚本**（完整对话 Demo）
  - 第 16 章：故障自查手册（7 类常见问题 + 排查表）
  - 第 17 章：进阶技巧（自定义视觉、批量生成、脚本化调用）
  - 第 18 章：版本升级与迁移
- 新增 **3 个附录**：
  - 附录 A：触发词索引（按字母排序）
  - 附录 B：指令速查（按场景分类）
  - 附录 C：快捷参考卡（1 页 A4 可打印）

#### 新增对话 Demo
第 15 章包含 10 个完整实战场景脚本：
1. 家庭出游（含 70 岁老人）
2. 情侣蜜月（预算敏感）
3. 亲子短途（5 岁小朋友）
4. 毕业旅行（学生票 + 青旅）
5. 商务 + 顺游组合
6. 自驾长途（7 天以上）
7. 美食主题深度游
8. 小众目的地（未被攻略覆盖）
9. 跨季改期（原计划取消 → 换季节重排）
10. 带宠物出行

#### SKILL.md
- `version` 字段升级为 `2.1.0`
- description 同步更新，说明 v2.1 文档增强

#### 兼容性
- ✅ 完全向后兼容 v2.0 所有功能
- ✅ 仅文档增强，运行时行为与 v2.0 完全一致
- ✅ 无新增依赖

---

## [2.0.0] — 2026-04-20

### 🎉 重大新增 —— 云端分享时代

#### 新功能
- **Phase 6 云端部署工作流**：Phase 5 完成后可选上云，一键发布交互网页
- **双引擎部署**：
  - 🇨🇳 EdgeOne Pages（国内访问飞快，通过 CodeBuddy 集成按钮登录）
  - 🌏 Vercel（国际稳定、永久免费）
  - 📡 双引擎模式（推荐，互为备份）
- **客户端密码保护**：AES-256-CBC + PBKDF2-SHA256 加密，密码不经服务器
- **旅行书架索引页**：自动维护"我的旅行书架"首页，按年份归档所有已发布行程
- **双二维码嵌入**：长图底部自动附加 🇨🇳 + 🌏 双二维码分享区（宋式美学）
- **本地元数据管理**：`data/trips.json` 记录所有已部署行程

#### 新增文件
- `references/deployment-guide.md` — Phase 6 技术参考文档
- `scripts/deploy_to_eop.sh` — EdgeOne Pages 一键部署
- `scripts/deploy_to_vercel.sh` — Vercel 一键部署
- `scripts/deploy_both.sh` — 双引擎部署包装
- `scripts/generate_qrcode.py` — 单/双二维码生成（宋式配色）
- `scripts/inject_password.py` — AES 密码保护注入
- `scripts/embed_qr_in_longimage.py` — 长图底部追加分享区
- `scripts/update_index.py` — 旅行书架索引页渲染
- `assets/index-template/index.html` — 旅行书架 Jinja2 模板
- `assets/index-template/trip-card.html` — 单份行程卡片模板
- `CHANGELOG.md` — 本文件

#### 变更
- `SKILL.md` frontmatter 新增 `version: 2.0.0` 字段
- `SKILL.md` 工作流由 5 阶段扩展为 6 阶段（第 6 阶段可选）
- `README.md` 新增「云端部署」章节和 5 条 FAQ
- Word 使用说明扩展为 8 章（新增第 8 章「云端部署」）

#### 新增依赖
- `jinja2` — 索引页模板渲染
- `qrcode[pil]` — 二维码生成
- `cryptography` — AES 加密
- Node.js 18+（运行时，部署 CLI 通过 npx 拉取）

#### 兼容性
- ✅ 完全向后兼容 v1.0 工作流
- ✅ 不部署时行为与 v1.0 完全一致
- ⚠️ Phase 6 首次使用需要一次性授权（EdgeOne Pages 通过集成按钮 / Vercel 通过 `npx vercel login`）

---

## [1.0.0] — 2026-04-17

### 🎉 首个正式版

#### 核心能力
- 5 阶段工作流：需求澄清 → 小红书调研 → 行程编排 → HTML 构建 → 导出
- 三种输出格式：交互式 HTML + 长图 JPG + 移动端 PDF
- 宋式美学设计规范（月白底 / 赭石主色 / 云雷纹装饰）
- 按出行人群自动调节节奏（老人 / 小孩 / 年轻人）
- 门票自动计算老人/学生折扣
- 自驾每日驾驶时间 ≤ 4 小时约束

#### 交付物
- `SKILL.md` — AI 工作流核心指令
- `README.md` — Markdown 产品介绍
- `TravelCraft-使用说明.docx` — 7 章节 Word 产品文档
- 6 份参考文档（`references/`）
- 5 个自动化脚本（`scripts/`）
- 参考实现模板（`assets/template/`）

---

## 版本号规则

- **主版本号（X.0.0）**：不兼容的重大变更 / 新增一个完整工作流阶段
- **次版本号（x.Y.0）**：向后兼容的功能新增
- **修订号（x.y.Z）**：向后兼容的问题修复 / 文档更新

## 未来规划（Roadmap）

### v2.1（计划中）
- 自动删除 90 天未访问的云端行程（隐私清理）
- 支持导入 v1.0 生成的历史行程到书架
- 多语言密码门户（英文版）

### v2.2（构想）
- "行程评论"功能：同伴扫码后可留言（需轻量 serverless 函数）
- 集成高德/百度地图 SDK，行程内直接导航
- 支持 PWA 离线缓存，坐飞机也能查

### v3.0（愿景）
- 协作编辑：多人共同规划同一份行程
- 预算实时同步：支付宝账单自动归入对应日期
- AI 摄影师：基于行程自动规划拍摄机位和光线时间

---

## 反馈与贡献

- 问题反馈：对 CodeBuddy 说「行迹 skill 有个问题...」
- 功能建议：欢迎提出你希望 v2.1 / v3.0 支持的能力
- 二次开发：修改 `references/design-principles.md` 和 `assets/template/` 即可自定义视觉风格
