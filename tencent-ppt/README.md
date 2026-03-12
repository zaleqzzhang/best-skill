# tencent-ppt

**tencent-ppt** 是一个演示文稿生成技能，可以将用户的内容需求直接生成为基于 HTML 的幻灯片，严格遵循腾讯官方 PPT 模板设计规范（TencentSans 字体、品牌配色、1920×1080 固定画布）。

**功能：**
- 生成完整幻灯片项目：封面、目录、章节页、内容页、结尾页
- 支持 15+ 种内容布局：文字、图片、视频、图表、卡片、时间线、对比、引用等
- 内置幻灯片播放器：键盘翻页、全屏、缩略图画廊
- 支持嵌入本地图片/视频（绝对路径）和远程 URL
- 支持 PDF 导出

**使用方法：**
1. 下载并解压，打开 CodeBuddy → 右上角设置 → Skills → 导入/Import Skill → 选择 `tencent-ppt` 文件夹
2. 对话中说"帮我做一份腾讯风PPT"、"生成腾讯风演示文稿"、"创建腾讯风幻灯片"等即可触发

**预览方式：**
- CodeBuddy 默认会帮你打开
- 或者在 Finder/文件资源管理器中双击 `slides-output/index.html` 在浏览器中打开

**注意事项：**
- 零外部依赖：生成的幻灯片为纯 HTML/CSS/JS，无需安装任何包
- 每页幻灯片独立可用：单独打开任意 `.html` 文件即可查看该页
- `file://` 下键盘快捷键需先点击 iframe 外部区域获取焦点

**生成文件结构：**
```
slides-output/
├── index.html              # 幻灯片播放器
├── slide-01-cover.html     # 封面
├── slide-02-toc.html       # 目录
├── slide-03-section.html   # 章节分隔页
├── slide-04-content.html   # 内容页
├── ...
├── slide-XX-ending.html    # 结尾页
└── assets/
    ├── fonts/              # TencentSans 字体文件
    └── media/              # 腾讯 Logo 及装饰图案
```

**更新日志：**
- 2025-03-05：初始发布
- 2026-03-05：新增 PDF 导出
