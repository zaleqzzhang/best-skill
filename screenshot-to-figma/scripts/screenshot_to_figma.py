#!/usr/bin/env python3
"""
Screenshot to Figma - 将 UI 截图转换为结构化 Figma 设计稿
依赖：pip install requests Pillow openai
"""

import os
import sys
import json
import base64
import time
import textwrap
import requests
from io import BytesIO
from PIL import Image
from typing import Dict, List, Any, Optional


class ScreenshotToFigma:
    def __init__(self, openai_api_key: str, figma_token: str = "", openai_base_url: str = "https://api.openai.com"):
        self.openai_api_key = openai_api_key
        self.figma_token = figma_token
        self.openai_base_url = openai_base_url.rstrip("/")
        self.headers_openai = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        }

    # ------------------------------------------------------------------ #
    #  1. 获取图片
    # ------------------------------------------------------------------ #
    def download_image(self, url: str) -> bytes:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.content

    # ------------------------------------------------------------------ #
    #  2. 视觉识别
    # ------------------------------------------------------------------ #
    def analyze_with_vision(self, image_data: bytes, model: str = "gpt-4o") -> List[Dict]:
        """调用多模态模型识别截图中的所有 UI 元素"""
        base64_image = base64.b64encode(image_data).decode("utf-8")

        prompt = textwrap.dedent("""
        你是一个专业的 UI 分析专家。请仔细识别这张截图中的所有界面元素，包括：
        按钮、输入框、文本标签、图标、图片、卡片/容器、导航栏、分割线、列表项、弹窗、标签页等所有可见元素。

        对每个元素，输出一个 JSON 对象，严格包含以下字段：
        - "type": 元素类型，只能是以下值之一:
          "button" | "text" | "input" | "image" | "container" | "icon" | "navbar" | "card" | "divider" | "tab"
        - "bounding_box": [x1, y1, x2, y2]，归一化相对坐标（0.0 ~ 1.0），左上角(0,0) 右下角(1,1)
        - "text_content": 元素内文字（字符串），无文字则为 null
        - "layer_name": 给这个图层起一个语义化名称（中文或英文均可，如"主标题"、"登录按钮"、"用户头像"）
        - "style": 样式对象，包含：
            - "font_size": 字号(px)，数字或 null
            - "color": 文字颜色十六进制，如 "#333333"，或 null
            - "background_color": 背景色十六进制，或 null
            - "border_radius": 圆角(px)，数字或 null
            - "opacity": 透明度 0.0~1.0，不确定则为 1.0
            - "font_weight": "regular" | "medium" | "bold" 或 null
            - "border_color": 边框颜色十六进制，或 null
            - "border_width": 边框宽度(px)，数字或 null

        注意：
        1. 请尽量识别所有可见元素，不要遗漏
        2. 坐标要尽量精确，体现实际位置和大小比例
        3. 颜色要尽量精确识别
        4. 只输出合法的 JSON 数组，不要包含任何解释文字、markdown 标记或代码块

        示例：
        [{"type":"button","bounding_box":[0.1,0.8,0.9,0.9],"text_content":"立即登录","layer_name":"登录按钮","style":{"font_size":16,"color":"#FFFFFF","background_color":"#1677FF","border_radius":8,"opacity":1.0,"font_weight":"medium","border_color":null,"border_width":null}}]
        """).strip()

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 4096,
            "temperature": 0.1
        }

        resp = requests.post(
            f"{self.openai_base_url}/v1/chat/completions",
            headers=self.headers_openai,
            json=payload,
            timeout=180
        )
        resp.raise_for_status()
        result = resp.json()
        content = result["choices"][0]["message"]["content"].strip()

        # 清理 markdown 代码块
        if content.startswith("```"):
            lines = content.split("\n")
            start = 1
            end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
            content = "\n".join(lines[start:end])
        content = content.strip()

        elements = json.loads(content)
        print(f"✅ 识别到 {len(elements)} 个 UI 元素")
        return elements

    # ------------------------------------------------------------------ #
    #  3. 坐标映射 + 节点构建
    # ------------------------------------------------------------------ #
    def hex_to_rgb(self, hex_color: str) -> Dict:
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join(c * 2 for c in hex_color)
        return {
            "r": int(hex_color[0:2], 16) / 255.0,
            "g": int(hex_color[2:4], 16) / 255.0,
            "b": int(hex_color[4:6], 16) / 255.0,
            "a": 1.0
        }

    def build_figma_nodes(self, elements: List[Dict], img_width: int, img_height: int) -> List[Dict]:
        nodes = []
        for i, elem in enumerate(elements):
            bb = elem.get("bounding_box", [0, 0, 1, 1])
            if len(bb) != 4:
                continue
            x1, y1, x2, y2 = [float(v) for v in bb]
            x = round(x1 * img_width, 2)
            y = round(y1 * img_height, 2)
            w = round(max((x2 - x1) * img_width, 2), 2)
            h = round(max((y2 - y1) * img_height, 2), 2)

            style = elem.get("style") or {}
            text_content = elem.get("text_content")
            elem_type = (elem.get("type") or "container").lower()
            layer_name = elem.get("layer_name") or f"{elem_type}_{i + 1}"

            # 决定 Figma 节点类型
            is_text_node = (elem_type == "text") or (
                text_content and elem_type not in ("button", "input", "container", "card", "navbar", "image", "icon")
            )
            figma_type = "TEXT" if is_text_node else "RECTANGLE"

            node: Dict[str, Any] = {
                "id": f"node_{i}",
                "type": figma_type,
                "name": layer_name,
                "x": x,
                "y": y,
                "width": w,
                "height": h,
                "opacity": float(style.get("opacity") or 1.0),
                "cornerRadius": float(style.get("border_radius") or 0),
                "fills": [],
                "strokes": [],
            }

            # 背景色
            bg = style.get("background_color")
            if bg:
                try:
                    node["fills"] = [{"type": "SOLID", "color": self.hex_to_rgb(bg)}]
                except Exception:
                    pass

            # 边框
            bc = style.get("border_color")
            bw = style.get("border_width")
            if bc and bw:
                try:
                    node["strokes"] = [{"type": "SOLID", "color": self.hex_to_rgb(bc)}]
                    node["strokeWeight"] = float(bw)
                except Exception:
                    pass

            # 文字节点额外属性
            if figma_type == "TEXT":
                node["characters"] = text_content or ""
                node["fontSize"] = float(style.get("font_size") or 14)
                fw = style.get("font_weight") or "regular"
                node["fontWeight"] = {"bold": 700, "medium": 500, "regular": 400}.get(fw, 400)
                txt_color = style.get("color")
                if txt_color:
                    try:
                        node["fills"] = [{"type": "SOLID", "color": self.hex_to_rgb(txt_color)}]
                    except Exception:
                        node["fills"] = [{"type": "SOLID", "color": {"r": 0.2, "g": 0.2, "b": 0.2, "a": 1.0}}]
                else:
                    node["fills"] = [{"type": "SOLID", "color": {"r": 0.2, "g": 0.2, "b": 0.2, "a": 1.0}}]
            else:
                # 矩形没有文字 fill 覆盖时给默认透明
                if not node["fills"]:
                    node["fills"] = []

            nodes.append(node)
        return nodes

    # ------------------------------------------------------------------ #
    #  4. 生成 Figma 插件代码（内嵌 JSON，可直接运行）
    # ------------------------------------------------------------------ #
    def generate_plugin_code(self, export_data: Dict) -> str:
        json_str = json.dumps(export_data, ensure_ascii=False, separators=(",", ":"))
        # 转义反引号，防止模板字符串中断
        json_str = json_str.replace("`", "\\`")

        return f"""// ================================================
// Figma Plugin - Screenshot to Figma
// 使用方式（二选一）：
//   方式 A：Figma 菜单 → Plugins → Development → New Plugin
//            → "Run once" 模式 → 粘贴此代码 → Run
//   方式 B：打开已有 Figma 文件 → F12 开发者工具控制台
//            → 粘贴此代码 → 回车（需开启 Figma 桌面版开发者工具）
// ================================================

(async function importScreenshotToFigma() {{
  const DATA = {json_str};
  const {{ meta, nodes }} = DATA;
  const {{ canvas_width, canvas_height, project_name }} = meta;

  // ---- 加载字体 ----
  try {{
    await figma.loadFontAsync({{ family: "Inter", style: "Regular" }});
    await figma.loadFontAsync({{ family: "Inter", style: "Medium" }});
    await figma.loadFontAsync({{ family: "Inter", style: "Bold" }});
  }} catch(e) {{
    // 字体加载失败时使用系统字体
    try {{ await figma.loadFontAsync({{ family: "Roboto", style: "Regular" }}); }} catch(_) {{}}
  }}

  // ---- 创建画板 Frame ----
  const frame = figma.createFrame();
  frame.name = project_name || "Screenshot Import";
  frame.resize(canvas_width, canvas_height);
  frame.x = figma.viewport.center.x - canvas_width / 2;
  frame.y = figma.viewport.center.y - canvas_height / 2;
  frame.fills = [{{ type: "SOLID", color: {{ r:1, g:1, b:1 }} }}];

  let successCount = 0;
  let errorCount = 0;

  // ---- 遍历节点创建图层 ----
  for (const node of nodes) {{
    try {{
      let figmaNode;

      if (node.type === "TEXT" && node.characters) {{
        figmaNode = figma.createText();
        figmaNode.characters = node.characters;
        figmaNode.fontSize = node.fontSize || 14;
        const w = node.fontWeight || 400;
        const style = w >= 700 ? "Bold" : w >= 500 ? "Medium" : "Regular";
        try {{
          figmaNode.fontName = {{ family: "Inter", style }};
        }} catch(e) {{
          // 字体设置失败，保持默认
        }}
      }} else {{
        figmaNode = figma.createRectangle();
        if (typeof node.cornerRadius === "number") {{
          figmaNode.cornerRadius = node.cornerRadius;
        }}
        if (node.strokes && node.strokes.length > 0 && node.strokeWeight) {{
          const sc = node.strokes[0].color;
          figmaNode.strokes = [{{
            type: "SOLID",
            color: {{ r: sc.r, g: sc.g, b: sc.b }},
            opacity: sc.a || 1
          }}];
          figmaNode.strokeWeight = node.strokeWeight;
        }}
      }}

      figmaNode.name = node.name || "element";
      figmaNode.x = node.x;
      figmaNode.y = node.y;
      figmaNode.resize(Math.max(node.width, 1), Math.max(node.height, 1));
      figmaNode.opacity = typeof node.opacity === "number" ? node.opacity : 1;

      if (node.fills && node.fills.length > 0) {{
        const fill = node.fills[0];
        if (fill.type === "SOLID" && fill.color) {{
          const c = fill.color;
          figmaNode.fills = [{{
            type: "SOLID",
            color: {{ r: c.r || 0, g: c.g || 0, b: c.b || 0 }},
            opacity: c.a != null ? c.a : 1
          }}];
        }}
      }} else if (node.type !== "TEXT") {{
        figmaNode.fills = [];
      }}

      frame.appendChild(figmaNode);
      successCount++;
    }} catch (err) {{
      console.error("节点创建失败:", node.name, err.message);
      errorCount++;
    }}
  }}

  // ---- 完成 ----
  figma.currentPage.appendChild(frame);
  figma.viewport.scrollAndZoomIntoView([frame]);
  figma.notify(`✅ 导入完成！成功 ${{successCount}} 个图层${{errorCount > 0 ? "，失败 " + errorCount + " 个" : ""}}`, {{ timeout: 4000 }});
  figma.closePlugin();
}})();
"""

    # ------------------------------------------------------------------ #
    #  5. 主流程
    # ------------------------------------------------------------------ #
    def run(
        self,
        screenshot_input: str,
        project_name: Optional[str] = None,
        model: str = "gpt-4o",
        output_dir: str = ".",
    ) -> Dict:

        # Step 1: 获取图片
        if screenshot_input.startswith("http://") or screenshot_input.startswith("https://"):
            print(f"📥 正在下载图片: {screenshot_input}")
            img_data = self.download_image(screenshot_input)
        else:
            print("📥 解码 base64 图片数据...")
            img_data = base64.b64decode(screenshot_input)

        img = Image.open(BytesIO(img_data))
        width, height = img.size
        print(f"📐 图片尺寸: {width} x {height}")

        # Step 2: 视觉识别
        print(f"🔍 正在调用 {model} 分析截图中的 UI 元素...")
        elements = self.analyze_with_vision(img_data, model=model)

        # Step 3: 构建节点
        nodes = self.build_figma_nodes(elements, width, height)

        if not project_name:
            project_name = f"Screenshot to Figma - {time.strftime('%Y%m%d_%H%M%S')}"

        export_data = {
            "meta": {
                "project_name": project_name,
                "canvas_width": width,
                "canvas_height": height,
                "node_count": len(nodes),
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%S")
            },
            "nodes": nodes
        }

        # Step 4: 保存文件
        os.makedirs(output_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join(output_dir, f"figma_nodes_{timestamp}.json")
        plugin_path = os.path.join(output_dir, f"figma_plugin_{timestamp}.js")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        print(f"💾 节点 JSON 已保存: {json_path}")

        plugin_code = self.generate_plugin_code(export_data)
        with open(plugin_path, "w", encoding="utf-8") as f:
            f.write(plugin_code)
        print(f"📦 Figma 插件代码已保存: {plugin_path}")

        # Step 5: 生成操作指引
        guide = self._generate_guide(project_name, plugin_path, len(nodes))
        print("\n" + guide)

        return {
            "status": "success",
            "json_path": json_path,
            "plugin_path": plugin_path,
            "node_count": len(nodes),
            "canvas_size": f"{width}x{height}",
            "project_name": project_name,
            "guide": guide,
        }

    def _generate_guide(self, project_name: str, plugin_path: str, node_count: int) -> str:
        return f"""
╔══════════════════════════════════════════════════════════════╗
║         🎨  Screenshot to Figma 导入指引                      ║
╚══════════════════════════════════════════════════════════════╝

识别结果：共 {node_count} 个 UI 图层，画板名称「{project_name}」

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 推荐方式：Figma 插件开发模式（约 1 分钟完成）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

第 1 步：打开任意 Figma 文件（新建或已有均可）
第 2 步：点击菜单栏 「Plugins」→「Development」→「New Plugin...」
第 3 步：在弹出框中选择 「Run once」（不需要保存插件），点击 Next
第 4 步：在代码编辑框中，删除默认代码，把下面文件的内容完整粘贴进去：
          📄 {plugin_path}
第 5 步：点击 「Run」按钮，等待几秒钟，所有图层自动创建 ✨

导入完成后，Figma 视图会自动聚焦到生成的画板，你就可以编辑啦！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
备选方式：使用社区插件「JSON to Figma」
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Figma 搜索并安装插件「Figma to JSON / JSON to Figma」（插件市场免费）
2. 打开插件，选择导入，粘贴 figma_nodes_*.json 中 "nodes" 数组的内容
（注意：不同插件对 JSON 格式要求略有差异，推荐使用上方方式一）
"""


# ------------------------------------------------------------------ #
#  命令行入口
# ------------------------------------------------------------------ #
def main():
    import argparse
    parser = argparse.ArgumentParser(description="将 UI 截图转换为 Figma 可导入的设计稿")
    parser.add_argument("screenshot", help="截图的 HTTP URL 或 base64 编码数据")
    parser.add_argument("--name", default=None, help="Figma 画板/项目名称")
    parser.add_argument("--model", default="gpt-4o", help="视觉识别模型（默认: gpt-4o）")
    parser.add_argument("--output-dir", default=".", help="输出目录（默认: 当前目录）")
    parser.add_argument("--openai-base-url", default="https://api.openai.com", help="OpenAI API 基础 URL")
    args = parser.parse_args()

    openai_key = os.getenv("OPENAI_API_KEY")
    figma_token = os.getenv("FIGMA_ACCESS_TOKEN", "")

    if not openai_key:
        print("❌ 错误：请设置 OPENAI_API_KEY 环境变量")
        sys.exit(1)

    tool = ScreenshotToFigma(
        openai_api_key=openai_key,
        figma_token=figma_token,
        openai_base_url=args.openai_base_url
    )
    result = tool.run(
        screenshot_input=args.screenshot,
        project_name=args.name,
        model=args.model,
        output_dir=args.output_dir
    )
    print("\n📋 执行结果：")
    print(json.dumps({k: v for k, v in result.items() if k != "guide"}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
