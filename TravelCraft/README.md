# 行迹 · TravelCraft

> 从一句模糊的出行念头，到一份可以直接转发朋友圈的精美行程；v2.0 起，更可一键上云、扫码分享。

![Version](https://img.shields.io/badge/version-2.2.0-B07B5F) ![CodeBuddy Skill](https://img.shields.io/badge/CodeBuddy-Skill-1565C0) ![License](https://img.shields.io/badge/license-MIT-2E7D32) ![v2.0](https://img.shields.io/badge/v2.0-Cloud%20Deploy-2C4A6E) ![v2.1](https://img.shields.io/badge/v2.1-Complete%20Guide-5B7A5A) ![v2.2](https://img.shields.io/badge/v2.2-Map%20Integration-8E6C88)

---

## 这是什么

**行迹 · TravelCraft** 是一个 CodeBuddy Skill，专为「不想花一整个周末做旅行攻略」的人设计。

你只需要说一句话——

> "五一带爸妈去河南看石窟，三个人自驾"

它会自动完成：**需求澄清 → 小红书调研 → 行程编排 → 预算测算 → 精美网页 / 长图 / PDF 一键输出**。

---

## 它解决什么问题

旅行规划的几个老大难：

| 痛点 | 行迹的方案 |
|------|-----------|
| 想法模糊，不知道去哪 | 模糊输入也能开工，只补问真正缺失的维度 |
| 小红书刷了 100 篇，信息散落一地 | 自动搜索 + 按赞数筛选 + 提取避坑/路线/美食 |
| 行程发给同伴只能甩文字 | 输出微信可直接转发的长图、可打印的 PDF |
| 预算算不清，老人/学生票漏算 | 内置预算模板，自动按人群计算门票 |
| AI 编造的景点介绍不可信 | 调用真实小红书数据，标注博主名+赞数 |
| 行程视觉土到没法分享 | 宋式美学设计，月白底色 / 云雷纹 / 宋体标题 |

---

## 核心能力

### 1. 智能需求澄清
输入可以极度模糊。Skill 会自动识别已知信息，只问真正缺失的维度（谁去 / 几天 / 预算 / 交通 / 节奏偏好），不做无效追问。

### 2. 小红书实地调研
不是拿 AI 编造景点介绍，而是真正搜索小红书，按赞数筛选高质量攻略：
- 提取避坑指南、最佳游览路线、当地美食推荐
- 下载博主实拍照片（拒绝 AI 生成 / 水墨画占位图）
- 标注博主名和赞数作为可信度背书

### 3. 专业行程编排
每天三层结构：**今日看点 → 小红书推荐 → 时间线**
- 按出行人群自动调节节奏（老人 / 小孩 / 年轻人）
- 自驾行程控制每日驾驶 ≤ 4 小时
- 门票自动计算老人半价 / 免票
- 周一闭馆、预约窗口等实际约束自动排避

### 4. 宋式美学输出
三种格式，同一套视觉语言：

| 格式 | 适用场景 |
|------|---------|
| 📱 交互网页（HTML） | 手机浏览器查看，Tab 切换每日行程 |
| 🖼 长图（JPG） | 微信 / 朋友圈 / 家族群直接转发 |
| 📄 PDF | 打印带上飞机，或离线阅读 |

视觉风格：**月白底色 · 云雷纹/回字纹装饰 · 宋体标题 · 赭石/靛蓝/竹青配色**——不是"旅行社传单"，是可以收藏的"旅行手卷"。

### 5. 🆕 云端部署（v2.0 新增）
一键将行程发布到云端，家人同伴扫码即看：

- **双引擎部署**：🇨🇳 EdgeOne Pages（国内飞快）+ 🌏 Vercel（国际稳定），总有一个能打开
- **密码保护**：AES-256 客户端加密，即使有人拿到 HTML 源码也看不到内容
- **旅行书架**：自动维护一个"我的旅行书架"首页，按年份收录所有已发布行程
- **扫码分享**：双二维码嵌入长图底部，微信发给家人一目了然

> 📖 详见下方「云端部署」章节

---

## 使用示例

安装后，直接对 CodeBuddy 说：

> "帮我规划一个五一河南文化自驾行程，三个人，有一位 70 岁老人"

Skill 会自动启动，按 6 个阶段工作：

1. **澄清** — 补问缺失的日期、预算、交通偏好
2. **调研** — 搜索小红书 + 网络，收集景点 / 美食 / 照片
3. **编排** — 生成逐日行程 + 预算表，请你确认
4. **构建** — 输出交互式网页（可实时预览调整）
5. **导出** — 一键生成长图 JPG + 移动端 PDF
6. **🆕 部署**（可选）— 上云 + 加密 + 二维码 + 书架更新

更多触发示例：

- "想去江南古镇走走，4 天 3 晚，两个人"
- "国庆带娃去成都，5 岁小朋友，怕坐车久"
- "西南自驾 7 天，预算 1 万，重点是风景"

---

## 安装

### 方法一：解压安装（推荐）

1. 下载 `TravelCraft.zip`
2. 解压到 CodeBuddy Skills 目录：
   ```bash
   unzip TravelCraft.zip -d ~/.codebuddy/skills/
   ```
3. 重启 CodeBuddy，对话中说"帮我规划旅行"即可触发

### 方法二：手动复制

将整个 `TravelCraft/` 文件夹复制到对应路径：

| 系统 | 路径 |
|------|------|
| macOS | `~/.codebuddy/skills/TravelCraft/` |
| Windows | `%USERPROFILE%\.codebuddy\skills\TravelCraft\` |
| Linux | `~/.codebuddy/skills/TravelCraft/` |

### 验证安装

在 CodeBuddy 中输入：

```
帮我规划一个周末去苏州的行程
```

如果 Skill 正常工作，会先回问你 3-5 个澄清问题（出行人数、预算、交通方式等），即视为安装成功。

---

## 系统要求

| 类型 | 项目 | 说明 |
|------|------|------|
| 必须 | Python 3.8+ | 用于图片处理脚本 |
| 必须 | Pillow + numpy | `pip install pillow numpy` |
| 必须 | Google Chrome | 用于导出长图 / PDF（headless 模式） |
| v2.0 必须 | Python 依赖 | `pip install jinja2 'qrcode[pil]' cryptography` |
| v2.0 云端部署 | Node.js 18+ | 运行 `edgeone` / `vercel` CLI |
| 推荐 | 小红书 Skill | 用于实地调研和照片采集 |
| 推荐 | Noto Serif SC 字体 | 中文宋体标题显示效果更佳 |

---

## 文件结构

```
TravelCraft/
├── SKILL.md                       # AI 工作流核心指令
├── README.md                      # 本文件
├── TravelCraft-使用说明.docx       # Word 版产品介绍 + 安装指南
├── CHANGELOG.md                   # 版本变更日志
├── references/                    # 各阶段参考文档
│   ├── requirement-clarification.md
│   ├── research-methods.md
│   ├── itinerary-composition.md
│   ├── budget-template.md
│   ├── html-template-guide.md
│   ├── design-principles.md
│   └── deployment-guide.md            # 🆕 v2.0 部署指南
├── scripts/                       # 自动化脚本
│   ├── normalize_photos.py
│   ├── make_export_html.py
│   ├── crop_screenshot.py
│   ├── export_itinerary.sh
│   ├── start_preview.sh
│   ├── deploy_to_eop.sh               # 🆕 EdgeOne Pages 部署
│   ├── deploy_to_vercel.sh            # 🆕 Vercel 部署
│   ├── deploy_to_github.sh            # 🆕 v2.3 GitHub Pages 部署
│   ├── deploy_both.sh                 # 🆕 多引擎组合部署
│   ├── geocode_places.py              # 🆕 v2.2 地名→经纬度
│   ├── calibrate_route.py             # 🆕 v2.2 路线校准
│   ├── inject_tmap.py                 # 🆕 v2.2 交互地图注入
│   ├── generate_qrcode.py             # 🆕 二维码生成
│   ├── inject_password.py             # 🆕 AES-256 密码保护
│   ├── embed_qr_in_longimage.py       # 🆕 长图底部嵌入二维码
│   └── update_index.py                # 🆕 旅行书架索引页（支持三引擎 URL）
└── assets/
    ├── template/
    │   ├── example-itinerary.html
    │   └── README.md
    └── index-template/                # 🆕 旅行书架模板
        ├── index.html
        └── trip-card.html
```

---

## ☁️ 云端部署（v2.0 新增）

从 v2.0 起，TravelCraft 支持将生成的行程**一键发布到云端**，家人/同伴扫码即可在手机上查看完整交互版。

### 部署引擎对比

| 引擎 | 国内速度 | 海外速度 | 免费额度 | 推荐场景 |
|------|---------|---------|---------|---------|
| 🇨🇳 **EdgeOne Pages** | ⚡️ 很快 | 🐢 慢 | 足够 | 国内家庭分享 |
| 🌏 **Vercel** | 🐢 中等 | ⚡️ 很快 | 足够 | 海外访问/永久存档 |
| 📡 **双引擎（推荐）** | ⚡️ + ⚡️ | ⚡️ + ⚡️ | 双份免费 | 最稳妥 |

### 密码保护

- **原理**：AES-256-CBC + PBKDF2 客户端加密（使用 `crypto-js`）
- **强度**：足够防住"随手转发给不该看的人"，适用于**家人/朋友级别**的私密
- **体验**：打开页面 → 宋式美学密码框 → 输入密码 → 解锁浏览
- **密码**：每份行程独立设置，4 位以上即可；Skill 不持久化密码

### 旅行书架

- 每次部署后，自动更新一个**专属首页**（如 `my-travelcraft.edgeone.app`）
- 按年份归档所有已发布行程，卡片式展示
- 加密行程显示 🔒 图标，每张卡片两个按钮（🇨🇳 国内版 / 🌏 海外版）
- 纯静态页面，完全符合宋式美学设计

### 首次部署准备

**EdgeOne Pages**（推荐通过集成按钮）：
1. 点击对话框底部 [集成] → [EdgeOne Pages] → [连接]
2. 用腾讯云账号登录（支持微信/QQ/邮箱）
3. 授权完成后即可使用

**Vercel**（通过终端）：
```bash
npx vercel login
# 选 "Continue with GitHub" 最方便
# 浏览器一次性授权，后续无需登录
```

### 使用流程

```
用户："帮我规划五一河南自驾行程"
Skill → Phase 1-5 完成，生成本地文件

Skill："要部署到云端吗？
       1. 🐙 GitHub Pages（国内稳·推荐）
       2. 🌏 Vercel（海外快）
       3. 🇨🇳 EdgeOne Pages（临时）
       4. 📡 组合部署（最稳妥）
       5. 不用了
       
       要加密码保护吗？"

用户："1，密码 hn2026"

Skill → 加密 HTML → push 到 GitHub → 开启 Pages
       → 生成二维码 → 嵌入长图底部 → 更新旅行书架

Skill："✅ 部署完成！
       🐙 访问链接：https://ivorxu.github.io/travelcraft-trips/trips/may2026-henan/
       🔒 密码：hn2026
       📚 你的旅行书架：https://ivorxu.github.io/travelcraft-trips/"
```

详细技术细节见 `references/deployment-guide.md`。

---

## 常见问题

**Q：导出长图时报 "Chrome not found" 怎么办？**
A：确认已安装 Google Chrome；macOS 默认路径为 `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`，如装在其他位置可在 `scripts/export_itinerary.sh` 顶部修改 `CHROME` 变量。

**Q：长图照片有白边？**
A：先用 `python scripts/normalize_photos.py photos/` 把 photos 目录批量裁成 4:3，再重新导出即可。

**Q：小红书调研返回空？**
A：需要先安装并登录「小红书 Skill」。如未安装，TravelCraft 会自动降级为通用网络搜索（图片质量会下降）。

**Q：能不能不调研直接生成？**
A：可以。在对话中明确告诉 Skill「跳过调研，直接用你已有的常识」即可。

### v2.0 云端部署相关

**Q：不想上云，可以只用本地功能吗？**
A：完全可以。Phase 6 永远是**可选**的。Skill 会询问「要部署吗？」，选择「不用了」即可只产出本地文件。

**Q：旅行书架和单份行程的 URL 是一个还是多个？**
A：多个。每份行程是独立的项目（独立 URL），书架是另一个项目（独立 URL，列出所有行程链接）。这样设计便于删除某份行程而不影响其他。

**Q：密码忘了怎么办？**
A：**没有后门可以恢复**——这是客户端加密的好处（真正私密）也是代价。解决办法：
- 重新运行 Phase 6，用新密码生成并部署覆盖
- 或直接删除旧部署（登录 EOP/Vercel 控制台删项目）后重新部署

**Q：Vercel 在国内真的不行吗？**
A：4G/5G 一般能打开但偶有卡顿；部分运营商/校园网可能直接失败。所以**推荐双引擎部署**——家人在国内扫 EOP 码，你出国扫 Vercel 码。

**Q：免费额度会不会用完？**
A：EdgeOne Pages 个人用户每月 10 万请求 + 25GB 流量；Vercel 每月 100GB 流量。一份行程页面约 3-5MB，足够分享给上千人。

---

## 设计哲学

行迹的美学源于**宋代山水手卷**：留白、淡彩、克制的纹样。我们认为，旅行的记录应该和旅行本身一样——值得收藏，而不是用一次就丢的传单。

详细的设计规范请参考 `references/design-principles.md`。

---

## 许可

MIT License — 自由使用、修改、分发。

---

**让每一次出行，都有一份配得上回忆的行程。**
