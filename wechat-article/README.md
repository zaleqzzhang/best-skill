# 📱 微信公众号发布工具包 (wechat-toolkit)

> OpenClaw Skill — 支持发布 Markdown 到微信公众号草稿箱、上传图片到永久素材库。
>
> **跨平台支持**: macOS / Linux / Windows（基于 Node.js）

---

## ✨ 功能模块

| 模块 | 功能 | 说明 |
|------|------|------|
| 📱 **发布** | 一键发布到公众号草稿箱 | 基于 wenyan-cli，支持主题配置 |
| 🖼️ **上传图片** | 上传图片到永久素材库 | 返回 media_id 和 url，支持批量 |

---

## 🚀 快速开始

### 环境要求

- **Node.js** ≥ 18
- [OpenClaw](https://github.com/anthropics/openclaw) 运行环境

### 安装

```bash
# 安装发布模块依赖
npm install -g @wenyan-md/cli
```

### 配置凭证

```bash
export WECHAT_APP_ID=your_app_id
export WECHAT_APP_SECRET=your_app_secret
```

> ⚠️ **重要：** 你的 IP 必须添加到微信公众号后台白名单中！

---

## 📖 使用方法

### 📱 发布文章

```bash
# 发布（自动安装 wenyan-cli）
node scripts/publisher/publish.js /path/to/article.md

# 指定主题和代码高亮
node scripts/publisher/publish.js /path/to/article.md lapis solarized-light
```

**Markdown 格式要求：**
```markdown
---
title: 文章标题（必填）
cover: /absolute/path/to/cover.jpg
---

# 正文内容...
```

### 🖼️ 上传图片

```bash
# 上传单张
node scripts/publisher/upload_image.js /path/to/image.jpg

# 批量上传
node scripts/publisher/upload_image.js img1.png img2.jpg img3.png
```

**输出：**
```json
[{ "file": "...", "media_id": "xxx", "url": "https://mmbiz.qpic.cn/..." }]
```

---

## 📁 项目结构

```
wechat-toolkit/
├── SKILL.md                    # OpenClaw Skill 定义
├── README.md                   # 本文件
├── example.md                  # 示例文章
├── references/                 # 参考文档
│   ├── themes.md               #   主题配置说明
│   └── troubleshooting.md      #   故障排查指南
└── scripts/
    └── publisher/
        ├── publish.js          # 发布 Markdown 到草稿箱
        └── upload_image.js     # 上传图片到永久素材库
```

---

## 🔧 故障排查

| 问题 | 解决方法 |
|------|----------|
| IP 不在白名单 | `curl ifconfig.me` → 添加到公众号后台 |
| wenyan 未安装 | `npm install -g @wenyan-md/cli` |
| 环境变量未设置 | `export WECHAT_APP_ID=xxx` |
| 缺少 frontmatter | 添加 `title` 字段 |
| 图片上传失败 | 检查图片格式（jpg/png/gif/bmp/webp）和大小（≤10MB）|

更多排查方法见 [`references/troubleshooting.md`](references/troubleshooting.md)

---

## 📄 License

MIT
