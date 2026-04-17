# 🌌 Google Gemini Design 星芒前端设计师

> **Elite Frontend Design Skill** — 为你的前端界面注入 Awwwards 级别的视觉灵魂，灵感源自 Google Gemini 的深邃美学。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Style Prompts](https://img.shields.io/badge/Style_Prompts-186%2B-blueviolet)]()
[![Categories](https://img.shields.io/badge/Categories-11-ff6b6b)]()
[![Brand References](https://img.shields.io/badge/Brand_References-66-00c853)]()

---

## ✨ 这是什么？

**Google Gemini Design** 是一个专业的前端设计 Skill，内置 **186+ 风格提示词库**，覆盖 **11 大设计分类**（含 **66 个世界顶级品牌设计系统参考**）。它能够根据你的需求，自动组合风格配方，生成具有极高审美、极强未来感的完整可运行前端代码。

**核心理念**：没有廉价感，只有深邃、流动、发光的高级质感。

### 🏢 v1.1 新增：世界级品牌设计系统

`references/` 目录包含 **66 个世界顶级品牌**的完整 `DESIGN.md` 设计规范文件，涵盖 Apple、Stripe、Tesla、Linear、Nike、Spotify 等行业标杆。选择 K 类风格时，Agent 会自动读取对应品牌的 Design Tokens（色板、字体、间距、阴影等），作为代码生成的核心参考基准。

---

## 🎯 适用场景

| 场景 | 示例 |
|------|------|
| 🏠 **Landing Page** | AI 产品官网、SaaS 首页、创意机构门户 |
| 📊 **Dashboard** | 数据可视化面板、管理后台、监控仪表盘 |
| 🎨 **UI 组件** | Hero Section、定价卡片、导航栏、表单 |
| 💼 **作品集** | 个人 Portfolio、设计师展示页 |
| 🤖 **AI 界面** | 聊天对话 UI、AI 助手面板、知识图谱 |
| 📱 **移动端页面** | 响应式着陆页、App 推广页 |
| 🏢 **品牌官网** | 基于真实品牌设计系统的高保真还原 |

---

## 🚀 快速开始

### 安装 Skill

将 `SKILL.md` 文件及 `references/` 目录一并放入你的 Skill 目录即可使用。

### 基本用法

向 AI 助手发送设计请求，Google Gemini Design 会自动激活：

```
帮我设计一个 AI 产品的 Landing Page
```

如果你没有指定具体风格，Google Gemini Design 会展示 **风格菜单** 供你选择，绝不盲猜。

### 品牌风格用法（NEW）

直接指定世界级品牌设计系统作为基准：

```
用 Stripe 的设计风格做一个支付页面
K49 Stripe + B01 毛玻璃 + E02 丝滑滚动
帮我做一个 Apple 风格的产品展示页
```

---

## 📁 项目结构

```
Google-Gemini-Design-Md/
├── SKILL.md                 # Skill 核心定义文件
├── README.md                # 项目说明文档
├── metadata.json            # Skill 元数据
└── references/              # 66 个品牌设计系统参考文件
    ├── 01-AI-Platforms/     # AI 平台（13 个）
    ├── 02-Developer-Tools/  # 开发者工具（13 个）
    ├── 03-Design-Build/     # 设计与建站（4 个）
    ├── 04-SaaS-Productivity/# SaaS 与效率工具（10 个）
    ├── 05-E-Commerce-Retail/# 电商与零售（4 个）
    ├── 06-Finance-Crypto/   # 金融与加密（6 个）
    ├── 07-Entertainment-Media/ # 娱乐与媒体（4 个）
    ├── 08-Automotive-Luxury/# 汽车与奢华（6 个）
    └── 09-Tech-Giants/      # 科技巨头（6 个）
```

---

## 💬 唤起 Skill 的提示词

以下是能够触发 Google Gemini Design 的各类提示词示例：

### 🇨🇳 中文唤起词

```
帮我设计一个网页
做个好看的 Landing Page
前端美化一下这个页面
UI 设计一个定价页
给我写个好看的页面
帮我做一个深色风格的仪表盘
设计一个毛玻璃风格的登录页
做个赛博朋克风的作品集网站
用 Linear 的设计风格做一个项目管理面板
```

### 🇺🇸 英文唤起词

```
Design a web page for my AI product
Create a landing page with Gemini style
Build a dashboard with glassmorphism effect
Make a dark UI with neon glow
Design a hero section with aurora effect
Create a pricing page with mesh gradient
Build a futuristic design for my portfolio
Make a Stripe-style payment page
```

### 🎨 风格关键词唤起

```
Gemini style / 深空流光 / frosted glass / glassmorphism
dark UI / neon glow / futuristic design / aurora effect
mesh gradient / 幻彩渐变 / 毛玻璃 / 极光效果
赛博霓虹 / Art Deco / Neobrutalism / Y2K
K49 Stripe / K61 Apple / K17 Linear / K42 Nike
```

---

## 📖 提示词案例大全

### 案例 1：AI 产品 Landing Page（推荐新手入门）

**提示词：**
```
帮我设计一个 AI 写作助手的官网首页，要有科技感和未来感
```

**Google Gemini Design 行为**：展示风格菜单 → 用户选择 `A + C`（Gemini Core + 发光渐变）→ 输出完整设计方案 + 代码

---

### 案例 2：指定风格 — 毛玻璃 Dashboard

**提示词：**
```
用毛玻璃风格设计一个数据分析仪表盘，配色用深海蓝，需要有动态数字效果
```

**Google Gemini Design 行为**：识别风格 `B`（Glassmorphism）+ 配色 `I05`（Deep Ocean）+ 动效 `E11`（滚轮式数字计数）→ 直接输出设计方案

---

### 案例 3：组合风格配方

**提示词：**
```
设计一个个人作品集页面，风格选 A + G + I04，要有 RGB Glitch 效果和霓虹东京配色
```

**Google Gemini Design 行为**：
- 从 CAT-A 提取：`A01 深空黑曜石基底`、`A02 流体渐变光带`
- 从 CAT-G 提取：`G08 故障艺术 RGB 色散`、`G02 无限视差跑马灯`
- 配色：`I04 Neon Tokyo 霓虹东京`
- 输出完整可运行代码

---

### 案例 4：AI 聊天界面

**提示词：**
```
帮我做一个类似 Gemini 的 AI 对话界面，要有流式输出效果、思考动画、毛玻璃代码块
```

**Google Gemini Design 行为**：
- 自动选择 CAT-F（AI Interface）：`F01 思考脉冲三点`、`F03 流式输出文字显影`、`F04 毛玻璃代码块`
- 叠加 CAT-B：`B01 多层毛玻璃`、`B09 半透明发光按钮`
- 输出完整聊天 UI 代码

---

### 案例 5：品牌设计系统参考（NEW）

**提示词：**
```
用 Stripe 的设计风格做一个 SaaS 定价页，加上毛玻璃效果
```

**Google Gemini Design 行为**：
- 读取 `references/06-Finance-Crypto/Stripe-DESIGN.md`，提取完整 Design Tokens
- 品牌基因：`K49 Stripe`（sohne-var 字体、蓝紫 `#533afd`、蓝调阴影）
- 叠加：`B01 多层毛玻璃` + `E05 弹性悬停缩放`
- 输出严格遵循 Stripe 设计系统的完整代码

---

### 案例 6：品牌基因 + 美学技法混搭（NEW）

**提示词：**
```
K61 Apple + B01 多层毛玻璃 + E02 物理滚动，做一个产品展示页
```

**Google Gemini Design 行为**：
- 读取 `references/09-Tech-Giants/Apple-DESIGN.md`，提取 Apple 设计系统
- 融合 Apple SF Pro 字体系统 + 毛玻璃空间分层 + 高阻尼丝滑滚动
- 输出 Apple 级品牌质感的完整代码

---

### 案例 7：经典设计风格

**提示词：**
```
用 Art Deco 风格做一个高端珠宝品牌的展示页，配色用金色装饰方案
```

**Google Gemini Design 行为**：
- 风格：`H04 Art Deco 金色几何`
- 配色：`I09 Gold Deco 金色装饰`
- 叠加：`D09 黄金比例行高` + `D01 极致克制宏观留白`
- 输出完整奢华感页面代码

---

### 案例 8：Bento 布局信息面板

**提示词：**
```
做一个 Apple 发布会风格的 Bento Grid 产品特性展示区，暗色背景
```

**Google Gemini Design 行为**：
- 布局：`H03 Bento 格子信息仪表` + `J02 不均等 Masonry 瀑布流`
- 视觉：`A01 深空黑曜石基底` + `B01 多层毛玻璃`
- 动效：`E05 弹性悬停缩放` + `D07 字母级错位入场动画`

---

### 案例 9：复古像素游戏风

**提示词：**
```
做一个独立游戏工作室的官网，要复古像素风 + CRT 显示器效果
```

**Google Gemini Design 行为**：
- 风格：`H06 复古像素点阵风` + `H07 Retro-Futuristic CRT`
- 配色：`I06 Amber Terminal 琥珀终端`
- 布局：`J08 浮动命令面板 HUD`

---

### 案例 10：极简阅读类页面

**提示词：**
```
设计一个极简风格的个人博客首页，强调排版美感和阅读体验
```

**Google Gemini Design 行为**：
- 风格：`H05 极简瑞士国际主义` + `D01 极致克制宏观留白`
- 排版：`D02 clamp() 流体字号` + `D09 黄金比例行高`
- 布局：`J10 极简单栏阅读布局`

---

## 🎨 11 大风格分类速查

| 代号 | 分类名 | 关键词 | 数量 |
|------|--------|--------|------|
| **A** | Gemini Core | 深空流光、AI 原生美学 | 12 |
| **B** | Glassmorphism Pro | 毛玻璃、空间分层 | 14 |
| **C** | Neon Luminance | 霓虹发光、流体渐变 | 14 |
| **D** | Editorial Type | 流体排版、极致留白 | 12 |
| **E** | Micro-Motion | 呼吸微交互、弹性动效 | 12 |
| **F** | AI Interface | AI 对话态、数据可视 | 10 |
| **G** | Awwwards Experimental | 获奖级、实验性 | 14 |
| **H** | Classic Aesthetic | 经典视觉运动风格 | 12 |
| **I** | Color Palette | 配色方案预设 | 10 |
| **J** | Layout & Structure | 布局与结构专项 | 10 |
| **K** | Brand References | 66 个世界级品牌设计系统 | 66 |

---

## 🏢 品牌参考分类速查（CAT-K）

| 子类 | 品牌分类 | 代表品牌 | 数量 |
|------|----------|----------|------|
| K-1 | AI 平台 | Claude, xAI, Runway, Cursor | 13 |
| K-2 | 开发者工具 | Vercel, Linear, Supabase, Sentry | 13 |
| K-3 | 设计与建站 | Figma, Framer, Webflow | 4 |
| K-4 | SaaS 与效率 | Notion, Raycast, Superhuman | 10 |
| K-5 | 电商与零售 | Nike, Airbnb, Shopify | 4 |
| K-6 | 金融与加密 | Stripe, Coinbase, Revolut | 6 |
| K-7 | 娱乐与媒体 | Spotify, WIRED, PlayStation | 4 |
| K-8 | 汽车与奢华 | Tesla, Ferrari, BMW | 6 |
| K-9 | 科技巨头 | Apple, NVIDIA, SpaceX | 6 |

---

## 🧪 风格组合配方示例

> Google Gemini Design 的精髓在于**跨分类组合**，以下是一些经典配方：

### 🔮 「深空幻境」配方
```
A01 + A02 + B01 + C01 + E02
```
深空黑底 → Gemini 流体渐变 → 多层毛玻璃 → 文字幻彩流光 → 高阻尼平滑滚动

### 🌊 「深海实验室」配方
```
A07 + B04 + C08 + F09 + I05
```
深蓝宝石底 → 动态色后模糊 → 幽灵荧光交织 → 底部悬浮命令岛 → Deep Ocean 配色

### 🏙️ 「霓虹东京」配方
```
C06 + G08 + H02 + I04 + J06
```
克制赛博霓虹 → RGB 色散故障 → Y2K 美学 → 霓虹东京配色 → 斜切分割线布局

### 💎 「Stripe 金融奢华」配方（NEW）
```
K49 + B01 + E05 + D09
```
Stripe 品牌基因 → 多层毛玻璃 → 弹性悬停 → 黄金比例行高

### 🍎 「Apple 极致克制」配方（NEW）
```
K61 + D01 + E02 + J10
```
Apple 设计系统 → 宏观留白 → 丝滑物理滚动 → 极简单栏布局

### 🍃 「自然呼吸」配方
```
D01 + D09 + H12 + I08 + J10
```
极致留白 → 黄金比例行高 → 自然简约 → 森林协议配色 → 极简单栏布局

### 👾 「终端黑客」配方
```
C06 + D12 + F05 + H07 + I06
```
克制霓虹发光 → 终端排版 → 全息扫描线 → CRT 复古 → 琥珀终端配色

---

## 🤖 多智能体协同评审 (Multi-Agent Collaboration)

Google Gemini Design 的核心竞争力在于其**四 Agent 交叉评审机制**——在生成最终界面前，内部调用四个虚拟角色进行协作与交叉验收：

| Agent | 角色 | 职责 |
|-------|------|------|
| 🕵️ **Agent 1** | 品牌与行业策略师 | 分析用户所属行业（Web3、医疗、SaaS、时尚等），提炼行业专有视觉 DNA |
| 🎨 **Agent 2** | 视觉魔法师 | 从 186+ 风格库中提取配方，生成机器可读的 `DESIGN.md` 设计系统 |
| 👨‍💻 **Agent 3** | 架构工程师 | 严格遵循 `DESIGN.md` 规范，将美学意图转化为高质量 HTML/CSS/JS 代码 |
| 🧑‍⚖️ **Agent 4** | 首席评审官 | 对照 `DESIGN.md` 与绝对禁止清单进行严格交叉验收，确保 Awwwards 级品质 |

> 这种多 Agent 机制确保了每次输出在**行业适配度、品牌一致性、代码质量和视觉审美**四个维度都经过严格检验。

---

## ⚙️ 工作流说明

```
用户输入需求
    │
    ├─ 是否指定了风格？
    │   ├─ ✅ 是 → 进入 Agent 协同流程
    │   └─ ❌ 否 → 展示风格菜单，等待用户选择
    │
    ▼ Agent 协同流程
    │
    ├─ 🕵️ Agent 1：行业分析 & 视觉 DNA 提取
    │
    ├─ 🎨 Agent 2：从 186+ 风格词库中挑选 5-8 个提示词
    │   ├─ K 类品牌风格？→ 自动读取 references/ 中对应 DESIGN.md
    │   └─ 非 K 类？→ 使用内置风格提示词组合
    │   └─ 输出 DESIGN.md 设计系统（Design Tokens）
    │
    ├─ 👨‍💻 Agent 3：严格遵循 DESIGN.md 生成完整前端代码
    │
    └─ 🧑‍⚖️ Agent 4：交叉评审 & 验收
        │
        └─ 输出四段式设计方案
            ├── 🌌 Vision（视觉解构与行业映射）
            ├── 📄 DESIGN.md（核心视觉字典）
            ├── 💻 The Source（完整可运行代码）
            └── 🧑‍⚖️ Critic's Audit（评审官结案陈词）
```

---

## 🚫 设计红线

Google Gemini Design **绝不会**输出以下内容：

| ❌ 禁止项 | 原因 |
|-----------|------|
| Inter / Roboto / Arial 字体 | 无聊通用，毫无设计感 |
| 紫色渐变 + 白色背景 | 廉价 AI 模板感 |
| 均匀三栏卡片布局 | 千篇一律的模板 |
| 无动效的静态页面 | 缺乏生命力 |
| 高饱和平涂色块 | 卡通化廉价感 |
| `border: 1px solid #333` | 无设计感的灰色边框 |
| 处理 API Keys | 只写 UI Mock，不处理真实后端逻辑 |

---

## ✅ 代码质量保证

每次输出前，Google Gemini Design 会自查：

- [x] **字体**：使用 Google Fonts 特色展示字体（Syne、Orbitron、Space Mono 等）或品牌指定字体
- [x] **配色**：主色/辅色/强调色层级清晰，或严格遵循品牌 Design Tokens
- [x] **布局**：有意外感，非对称或网格突破
- [x] **动效**：至少 2 种微交互 + 1 种入场动画
- [x] **深度**：渐变/阴影/发光/纹理形成空间感
- [x] **响应式**：移动端 + 桌面端全覆盖
- [x] **完整性**：所有代码可直接在浏览器运行
- [x] **无障碍**：语义化 HTML + ARIA 标签
- [x] **品牌一致性**：K 类风格严格遵循品牌 DESIGN.md 规范

---

## 📄 License

MIT License — 自由使用、修改和分发。
