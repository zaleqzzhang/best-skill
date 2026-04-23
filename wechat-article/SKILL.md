---
name: wechat-toolkit
description: "微信公众号发布工具包 — 支持发布 HTML 到公众号草稿箱、上传图片到永久素材库、自动处理正文内联图片。当用户需要发布文章或上传图片到微信公众号时使用。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📱",
        "requires": { "bins": ["node"] },
        "platforms": ["macos", "linux", "windows"],
        "install":
          [
            {
              "id": "node-brew",
              "kind": "brew",
              "formula": "node",
              "bins": ["node"],
              "label": "Install Node.js (brew)",
            },
          ],
      },
  }
---

# 📱 微信公众号发布工具包 (wechat-toolkit)

三个核心功能：**发布文章到草稿箱** + **上传图片到永久素材库** + **自动处理正文内联图片**。

> ✅ **不依赖 wenyan-cli**，直接调用微信 API，稳定可靠。

---

## 模块一览

| 模块 | 功能 | 触发词示例 |
|------|------|-----------|
| 📱 发布 | 发布 HTML 到公众号草稿箱 | "发布到公众号" / "推送草稿" |
| 🖼️ 上传图片 | 上传图片到微信永久素材库 | "上传图片到公众号" / "获取 media_id" |
| 🔄 内联图片 | 自动上传正文中的本地图片并替换 URL | （随发布流程自动触发） |

---

## 初始化配置（首次使用必读）

当用户首次使用本工具包、或凭证缺失时，**AI 应引导用户完成初始化配置**。

### 触发条件

以下任一情况触发初始化流程：
- 用户主动说"初始化"、"设置"、"配置"
- 脚本报错「环境变量未设置」或「凭证缺失」
- `TOOLS.md` 不存在或内容为空

### 初始化步骤

```
1. 检查项目根目录是否存在 TOOLS.md
   - 存在 → 读取当前内容，确认是否已有有效凭证
   - 不存在 → 创建空文件

2. 引导用户输入以下三项信息：
   a. 微信公众号 AppID     （在公众号后台 → 开发 → 基本配置 中获取）
   b. 微信公众号 AppSecret （同上位置，点击重置可查看）
   c. 默认作者名           （发布文章时自动填入，也可在文章 frontmatter 中单独指定）

3. 将用户输入写入项目根目录的 TOOLS.md，格式如下：

   export WECHAT_APP_ID=用户输入的AppID
   export WECHAT_APP_SECRET=用户输入的Secret
   export WECHAT_AUTHOR=用户输入的作者名

4. 写入后告知用户：「✅ 配置已完成，TOOLS.md 已写入。现在可以开始发布了。」
```

> **注意**：只覆盖 export 开头的行，保留 TOOLS.md 中其他已有内容。

---

## 配置 API 凭证

所有功能都需要微信公众号 API 凭证，确保环境变量已设置（或在 TOOLS.md 中配置）：

```bash
export WECHAT_APP_ID=your_wechat_app_id
export WECHAT_APP_SECRET=your_wechat_app_secret
export WECHAT_AUTHOR=默认作者名          # 可选，发布时自动填入
```

**重要：** IP 必须在微信公众号后台白名单中！

---

# 📱 功能一：发布文章

发布 HTML 文件到微信公众号草稿箱。Markdown 文件需先由 AI 智能排版为 HTML。

## 支持的文件格式

- **`.html`** — 直接发布（由 AI 智能排版生成）

> ⚠️ 不再支持 `.md` 文件直接发布。Markdown 需先由 AI 智能排版为 HTML，见下方「AI 智能排版」。

## AI 智能排版（Markdown → HTML）

当用户想要发布一篇 Markdown 文章时，**AI 应先将其智能排版为适配微信公众号的 HTML**，再调用发布脚本。

> **排版约束文件**：排版时必须严格遵循 `{baseDir}/references/html-constraints.md` 中的技术约束，确保 HTML 可直接粘贴到微信后台且不被过滤。

**核心原则：**

1. **纯 inline style**：微信会剥离 `<style>` 和 `class`，所有样式必须 `style="..."` 内联
2. **手机端优先**：短段落、多留白、字号 15-17px、行高 1.75-2.0
3. **代码高亮**：如文章包含代码块，用 inline style 手动上色
4. **图片处理**：`<img>` 保留本地路径，发布脚本会自动上传替换
5. **纯 HTML 输出**：不输出 Markdown、代码块标记或任何非 HTML 内容
6. **禁止 Emoji**：不使用任何表情符号
7. **列表单行（致命！）**：所有 `<ul>` / `<ol>` 的 `<li>` 必须**压缩到单行书写**，标签间零换行零空白。否则微信会将换行解析为空 `<li>`，产生大量多余空 bullet 点。详见 `{baseDir}/references/html-constraints.md`「结构嵌套规则」章节

**AI 智能排版工作流：**

```
1. 用户提供 Markdown 文章
2. AI 阅读 {baseDir}/references/html-constraints.md 了解排版约束
3. AI 智能排版为微信公众号风格的 HTML（遵循约束文件）
4. 将 HTML 保存为 .html 文件（可加可选 frontmatter）
5. 调用发布脚本: node {baseDir}/scripts/publisher/publish.js article.html
```

## 配图生成

发布前，**主动询问用户是否需要生成配图**：

> 📸 文章准备就绪！需要我帮你生成配图吗？
> - 封面图（cover，建议 900×500）
> - 正文插图（根据段落主题生成）
> - 不需要，直接发布

**如果用户需要配图：**
1. 根据文章标题和内容，生成合适的图片描述 prompt
2. 调用用户提供的**生图 skill** 生成图片
3. 将生成的图片保存到文章目录，使用**绝对路径**引用
4. 封面图设置到 frontmatter 的 `cover` 字段（可选，缺失会自动生成）
5. 正文插图在合适位置插入 `<img src="绝对路径">`

## 发布方式

```bash
# 发布 HTML 文件（由 AI 智能排版生成）
node {baseDir}/scripts/publisher/publish.js /path/to/article.html
```

## 自动化能力

脚本会**自动完成**以下操作，无需手动干预：

| 特性 | 说明 |
|------|------|
| 🖼️ 内联图片上传 | 自动检测正文中的 `<img src="本地路径">` 并上传至微信素材库，URL 自动回填替换 |
| 📸 默认封面 | 无封面图时自动生成 900×500 蓝色封面 |
| 🔑 Token 管理 | 自动获取和管理 Access Token |
| 📝 摘要提取 | 自动从正文前 54 字生成摘要 |

## 故障排查

| 问题 | 解决方法 |
|------|---------|
| IP 不在白名单 | `curl ifconfig.me` → 添加到公众号后台 |
| 环境变量未设置 | `export WECHAT_APP_ID=xxx WECHAT_APP_SECRET=xxx` |
| 缺少标题 | 添加 frontmatter `title` 字段，或 HTML `<title>` 标签 |
| errcode 40007 | 封面图无效 → 检查 cover 路径是否正确，或删除 cover 让其自动生成 |
| errcode 45009 | 发布频率超限 → 等待后重试 |
| errcode 48006 | 正文内容违规 → 检查内容是否符合规范 |

---

# 🖼️ 功能二：上传图片

上传单张或多张图片到微信公众号**永久素材库**，返回 `media_id` 和 `url`。

**支持格式**：jpg / jpeg / png / gif / bmp / webp

## 使用方法

```bash
# 上传单张图片
node {baseDir}/scripts/publisher/upload_image.js /path/to/image.jpg

# 批量上传多张图片
node {baseDir}/scripts/publisher/upload_image.js img1.png img2.jpg img3.png
```

## 输出示例

```json
[
  {
    "file": "/path/to/image.jpg",
    "media_id": "xxx_media_id_xxx",
    "url": "https://mmbiz.qpic.cn/..."
  }
]
```

`media_id` 可用于文章内引用图片；`url` 可直接在文章中使用。

## 注意事项

- 永久素材库上限为 **5000 张**图片
- 单张图片大小不超过 **10MB**
- 上传后图片永久有效，无过期限制

---

## 完整工作流示例

### 标准工作流（Markdown → AI 排版 → 发布）

```
1. 用户提供 Markdown 文章
2. AI 智能排版为微信公众号风格的 HTML（内联样式，适配手机阅读）
3. （可选）AI 生成配图，插入 HTML 中
4. 如需自定义封面/作者，在 HTML 文件顶部添加可选 frontmatter：
   ---
   title: 文章标题 (默认取一级标题作为文章标题，如果没有则自动生成)
   cover: /abs/path/to/cover.jpg
   author: 作者名 （必须）
   digest: 文章摘要 （必须）
   ---
5. node {baseDir}/scripts/publisher/publish.js article.html
   → 图片上传 + 封面处理 → 发布成功
```
