---
name: screenshot-to-figma
description: 将任意 UI 截图自动转换为结构清晰、元素可编辑的 Figma 设计稿。调用多模态 AI（GPT-4o/Claude Vision）识别截图中的按钮、文本、输入框、容器等 UI 元素，自动推断位置、尺寸、颜色、字号等样式属性，生成可直接在 Figma 插件中运行的 JS 代码（内嵌所有节点数据，粘贴即运行）。适用场景：(1) 设计师离职/权限丢失导致 Figma 文件无法访问，需从截图重建; (2) 产品经理将竞品截图快速转化为可编辑设计资产; (3) 从线上页面截图提取设计规范; (4) 用户提到"截图转 Figma"、"图片生成设计稿"、"UI 还原"等需求时。
---

# Screenshot to Figma

将 UI 截图通过 AI 视觉识别，生成可在 Figma 中**直接运行**的插件代码，一键还原所有图层。

## 快速开始

```bash
# 安装依赖
pip install requests Pillow openai

# 设置环境变量
export OPENAI_API_KEY="sk-..."

# 运行（传入截图 URL）
python3 scripts/screenshot_to_figma.py "https://example.com/screenshot.png" --name "我的设计稿"

# 运行（传入本地文件）
python3 scripts/screenshot_to_figma.py "$(base64 -w0 /path/to/screenshot.png)" --name "我的设计稿"
```

**输出两个文件：**
- `figma_nodes_YYYYMMDD_HHMMSS.json` — 原始节点数据（备份用）
- `figma_plugin_YYYYMMDD_HHMMSS.js` — **含节点数据的完整插件代码，直接复制粘贴到 Figma 即可运行**

---

## 将设计稿导入 Figma（全程约 2 分钟）

### ✅ 推荐方式：Figma 插件开发模式

> 免费版账号可用，**无需安装任何插件**

1. 打开任意 Figma 文件（新建或已有均可）
2. 点击菜单 `Plugins` → `Development` → `New Plugin...`
3. 在弹出框中选择 **`Run once`** 模式，点击 Next
4. 删除默认代码，将 `figma_plugin_*.js` 的**完整内容**粘贴进去
5. 点击 **`Run`** 按钮，等待几秒后所有图层自动出现在画布上 ✨

导入后视图会自动聚焦到生成的画板，可直接编辑所有图层。

### 备选方式：社区插件「JSON to Figma」

1. 在 Figma 插件市场搜索并安装 **JSON to Figma**（免费）
2. 打开插件，将 `figma_nodes_*.json` 中 `"nodes"` 数组的内容粘贴导入

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `screenshot` | 截图 HTTP URL 或 base64 编码数据 | 必填 |
| `--name` | Figma 画板名称 | `Screenshot to Figma - {时间戳}` |
| `--model` | 视觉识别模型 | `gpt-4o` |
| `--output-dir` | 输出目录 | 当前目录 |
| `--openai-base-url` | OpenAI 兼容 API 地址（支持自定义代理） | `https://api.openai.com` |

## Python API 调用

```python
from scripts.screenshot_to_figma import ScreenshotToFigma

tool = ScreenshotToFigma(
    openai_api_key="sk-...",
    openai_base_url="https://api.openai.com"  # 或自定义代理
)
result = tool.run(
    screenshot_input="https://example.com/ui.png",
    project_name="竞品分析-截图还原",
    model="gpt-4o",
    output_dir="./output"
)
print(result["guide"])  # 打印操作指引
```

## 识别能力

| 元素类型 | 支持 | 识别内容 |
|---------|------|---------|
| 按钮 button | ✅ | 文字、背景色、圆角、边框 |
| 文本 text | ✅ | 字号、颜色、字重、内容 |
| 输入框 input | ✅ | 背景色、边框、占位文字 |
| 容器/卡片 container/card | ✅ | 背景色、圆角、尺寸 |
| 导航栏 navbar | ✅ | 背景色、高度 |
| 图片 image | ✅ | 位置、尺寸（内容需手动替换） |
| 图标 icon | ✅ | 位置、尺寸（形状需手动绘制） |
| 交互状态 hover/active | ⚠️ | 仅识别静态截图中可见状态 |

## 注意事项

- **Figma API 限制**：Figma 免费版 REST API 不支持通过代码直接创建文件；本工具采用"插件代码内嵌数据"方案，用户手动运行一次插件即可完成导入。
- **识别精度**：AI 识别的坐标和颜色为近似值，复杂页面建议导入后手动微调关键图层。
- **图片建议**：使用清晰的全屏截图（分辨率 ≥ 375×667），避免模糊或文字过小。
- **字体**：导入后默认使用 Inter 字体，如需还原原始字体需手动修改。
