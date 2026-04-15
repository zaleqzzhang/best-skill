# Figma API 使用说明与限制

## Figma REST API 限制

### 当前 API 不支持的操作
- **直接在草稿空间创建文件**：Figma REST API (`POST /v1/files`) 仅对组织版/专业版账号生效，且需要 team_id
- **批量创建图层节点**：Figma REST API 不提供直接写入图层的端点，仅支持读取
- **实时添加节点**：无法通过 REST API 直接向已有文件添加 Frame 和图层

### 支持的 API 操作（仅读取/查询）
- `GET /v1/files/:file_key` — 获取文件结构
- `GET /v1/files/:file_key/nodes` — 获取节点信息
- `GET /v1/teams/:team_id/projects` — 获取团队项目列表
- `GET /v1/me` — 获取当前用户信息

## 实际可行的导入方案

### 方案一：Figma 插件（推荐）
通过 Figma 插件 API (`figma.*`) 在插件运行时直接操作画布：
- `figma.createFrame()` — 创建画板
- `figma.createRectangle()` — 创建矩形
- `figma.createText()` — 创建文字
- 支持完整的节点属性设置

**工作流**：
1. 运行脚本生成 `figma_nodes.json`
2. 在 Figma 中创建插件（Plugins > Development > New Plugin）
3. 将 `_plugin.js` 内容粘贴到插件编辑器中（注入 JSON_DATA）
4. 运行插件，自动创建所有图层

### 方案二：现有导入插件
推荐使用以下 Figma 社区插件：
- **"JSON to Figma"** (插件 ID: 789839703) — 支持标准 JSON 格式导入
- **"Figma to JSON"** — 双向转换工具

### 方案三：Figma REST API（受限）
仅对拥有 Team 管理员权限的组织版账号可用：
```
POST https://api.figma.com/v1/files
Headers: X-Figma-Token: {token}
Body: {"name": "文件名", "team_id": "xxx"}
```

## 获取 Figma Personal Access Token
1. 登录 figma.com
2. 进入 Settings > Account > Personal access tokens
3. 点击 "Generate new token"
4. 复制 token（形如 `figd_xxxxxxxxxxxx`）

## 节点 JSON 格式规范（本工具输出格式）

```json
{
  "meta": {
    "project_name": "My Design",
    "canvas_width": 390,
    "canvas_height": 844,
    "node_count": 12,
    "created_at": "2024-01-01T12:00:00"
  },
  "nodes": [
    {
      "id": "node_0",
      "type": "RECTANGLE",
      "name": "button_1_登录",
      "x": 39.0,
      "y": 168.8,
      "width": 312.0,
      "height": 42.4,
      "opacity": 1.0,
      "cornerRadius": 8,
      "fills": [{"type": "SOLID", "color": {"r": 0.09, "g": 0.46, "b": 1.0, "a": 1.0}}],
      "strokes": []
    },
    {
      "id": "node_1",
      "type": "TEXT",
      "name": "text_2_登录",
      "x": 175.5,
      "y": 180.0,
      "width": 39.0,
      "height": 22.0,
      "opacity": 1.0,
      "cornerRadius": 0,
      "characters": "登录",
      "fontSize": 16,
      "fontWeight": 500,
      "fills": [{"type": "SOLID", "color": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0}}],
      "strokes": []
    }
  ]
}
```
