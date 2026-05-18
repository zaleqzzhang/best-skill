# HTML 模板参考指南（强制规范）

> **本文档为 Stage 10/11 的 HTML 生成强制参考**。智能体生成的 HTML 必须遵循本文档的 CSS 骨架和结构规范，确保每次运行产出视觉风格一致且美观。

## 一、产品侧 UI 原型（Stage 10 · index.html）

### 1.1 强制 CSS 骨架（必须原样复制到 `<style>` 中）

```css
/* ===== 基础重置 ===== */
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'PingFang SC', 'Microsoft YaHei', -apple-system, sans-serif;
  background: #f0f2f5;
  color: #1a1a1a;
}

/* ===== 导航栏（强制蓝底白字） ===== */
.nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #1a73e8;      /* 强制蓝底 */
  color: #fff;               /* 强制白字 */
  padding: 12px 32px;
  display: flex;
  gap: 16px;
  align-items: center;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.nav-brand {
  font-size: 18px;
  font-weight: 700;
  margin-right: 24px;
}
.nav-item {
  padding: 6px 16px;
  border-radius: 20px;       /* 胶囊形 tab */
  cursor: pointer;
  transition: background 0.2s;
}
.nav-item:hover { background: rgba(255,255,255,0.2); }
.nav-item.active {
  background: #fff;
  color: #1a73e8;
  font-weight: 600;
}

/* ===== 视图容器 ===== */
.view {
  display: none;
  padding: 32px;
  max-width: 1400px;         /* 强制 1400px，不可缩小 */
  margin: 0 auto;
}
.view.active { display: block; }

/* ===== 卡片样式 ===== */
.card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.card-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1a73e8;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ===== 徽章标签 ===== */
.badge { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
.badge-blue { background: #e8f0fe; color: #1a73e8; }
.badge-green { background: #e6f4ea; color: #34a853; }
.badge-orange { background: #fef7e0; color: #ea8600; }
.badge-red { background: #fce8e6; color: #ea4335; }

/* ===== 步骤编号圆 ===== */
.step-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px; height: 28px;
  border-radius: 50%;
  background: #1a73e8;
  color: #fff;
  font-size: 14px;
  font-weight: 700;
}

/* ===== 进度条 ===== */
.progress-bar { display: flex; gap: 4px; margin: 16px 0; }
.progress-bar .seg { flex: 1; height: 8px; border-radius: 4px; background: #dadce0; }
.progress-bar .seg.done { background: #34a853; }
.progress-bar .seg.current { background: #fbbc04; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }

/* ===== 布局网格 ===== */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 24px; }

/* ===== 标签/Tag ===== */
.tag { display: inline-block; padding: 4px 12px; border-radius: 16px; font-size: 12px; margin: 4px 4px 4px 0; }

/* ===== 文件列表 ===== */
.file-list { font-size: 13px; line-height: 2; }
.file-list .high { color: #ea4335; font-weight: 600; }
.file-list .mid { color: #fbbc04; }
.file-list .low { color: #5f6368; }

/* ===== 按钮 ===== */
.btn { padding: 10px 24px; border-radius: 8px; border: none; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-primary { background: #1a73e8; color: #fff; }
.btn-primary:hover { background: #1557b0; }
.btn-success { background: #34a853; color: #fff; }

/* ===== 输入组 ===== */
.input-group { margin-bottom: 16px; }
.input-group label { display: block; font-size: 14px; font-weight: 600; margin-bottom: 6px; color: #5f6368; }
.input-group input { width: 100%; padding: 10px 14px; border: 2px solid #dadce0; border-radius: 8px; font-size: 14px; }
.input-group input:focus { border-color: #1a73e8; outline: none; }

/* ===== 检查清单 ===== */
.checklist-item { display: flex; align-items: center; gap: 8px; padding: 8px 0; border-bottom: 1px solid #f0f2f5; font-size: 14px; }
.check-pass { color: #34a853; font-weight: 700; }
.check-warn { color: #fbbc04; font-weight: 700; }
.check-fail { color: #ea4335; font-weight: 700; }

/* ===== 雷达图占位 ===== */
.radar-placeholder {
  width: 300px; height: 300px;
  background: linear-gradient(135deg, #e8f0fe 0%, #e6f4ea 50%, #fef7e0 100%);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; color: #5f6368;
}

/* ===== 归属条 ===== */
.attribution-bar { display: flex; height: 40px; border-radius: 8px; overflow: hidden; margin: 16px 0; }
.attr-existing { background: #5f6368; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 13px; }
.attr-invention { background: #34a853; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 13px; }

/* ===== 差异面板（双栏对比） ===== */
.diff-panel { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.diff-existing { background: #f5f5f5; border-radius: 8px; padding: 16px; border-left: 4px solid #5f6368; }
.diff-invention { background: #fff; border-radius: 8px; padding: 16px; border-left: 4px solid #34a853; }

/* ===== 创新点联动（5列布局：左列 | 箭头 | 中列 | 箭头 | 右列） ===== */
.linkage-grid { display: grid; grid-template-columns: 1fr 60px 1fr 60px 1fr; align-items: start; gap: 0; }
.linkage-col { padding: 16px; }
.linkage-col h4 { font-size: 14px; color: #5f6368; margin-bottom: 12px; text-align: center; }
.linkage-arrow { display: flex; align-items: center; justify-content: center; font-size: 28px; color: #1a73e8; padding-top: 60px; }
.linkage-item { background: #f8f9fa; border-radius: 8px; padding: 12px; margin-bottom: 8px; font-size: 13px; border: 1px solid #dadce0; }
.linkage-item.highlight { border-color: #1a73e8; background: #e8f0fe; }

/* ===== 创新点角标 ===== */
.innovation-badge { position: absolute; top: 8px; right: 8px; background: #1a73e8; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 11px; }

/* ===== 图注标签 ===== */
.fig-label { text-align: center; font-size: 13px; color: #5f6368; margin-top: 8px; font-weight: 600; }

/* ===== 交付物列表 ===== */
.deliverable-item { display: flex; align-items: center; gap: 12px; padding: 12px; background: #f8f9fa; border-radius: 8px; margin-bottom: 8px; }
.deliverable-icon { font-size: 24px; }

/* ===== DOCX 预览 ===== */
.docx-preview { background: #fff; border: 2px solid #dadce0; border-radius: 8px; padding: 20px; font-size: 13px; line-height: 1.8; }
.docx-preview h5 { font-size: 15px; font-weight: 700; color: #1a73e8; margin: 12px 0 6px; }
.docx-preview .toc-item { padding-left: 16px; color: #5f6368; }

/* ===== 对比表格 ===== */
.comparison-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.comparison-table th { background: #f8f9fa; padding: 10px; text-align: left; border-bottom: 2px solid #dadce0; }
.comparison-table td { padding: 10px; border-bottom: 1px solid #f0f2f5; }
```

### 1.2 强制 HTML 结构骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1440, initial-scale=1">
<title>{发明主题} - 产品原型</title>
<style>
/* 粘贴上述完整 CSS 骨架 */
</style>
</head>
<body>

<!-- 导航栏：蓝底白字 + 胶囊形 tab -->
<div class="nav">
  <span class="nav-brand">🔬 CodePatent {简短品牌名}</span>
  <span class="nav-item active" onclick="showView('overview')">场景总览</span>
  <span class="nav-item" onclick="showView('a1')">场景A-步骤1</span>
  <!-- ... 按图位需求清单的 figure_type 添加 tab ... -->
</div>

<!-- 每个视图对应一个 figure_type -->
<div id="view-overview" class="view active">
  <div class="card">
    <div class="card-title">📋 {标题}</div>
    <!-- 内容使用 .grid-2 / .grid-3 布局 -->
  </div>
  <div class="fig-label">图N：{图注}</div>
</div>

<!-- ... 更多视图 ... -->

<script>
function showView(id) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('view-' + id).classList.add('active');
  event.target.classList.add('active');
}
</script>
</body>
</html>
```

### 1.3 各 figure_type 视图的组件用法速查

| figure_type | 推荐组件 | 布局 |
|------------|---------|------|
| `scenario_overview` | `.card` + `.grid-2`（两个带边框的场景卡片）+ `.progress-bar`（流水线进度） | 双列 |
| `gui_a` / `gui_b` | `.step-num` + `.input-group` / `.file-list` / `.checklist-item` | `.grid-2` 左右分栏 |
| `product_output_preview` | `.docx-preview`（文档预览）+ `.grid-2`（配图缩略） | 双列 |
| `state_transition` | `.card`（带边框对比）+ 决策逻辑流程文字 + `.badge` | 双列 + 中间连接 |
| `innovation_linkage` | `.linkage-grid`（5列布局）+ `.linkage-item` + `.linkage-arrow` | 5列 Grid |
| `comparison` | `.comparison-table`（表格对比）或 `.diff-panel`（双栏差异） | 表格/双栏 |

### 1.4 视觉质量检查清单（生成后自检）

- [ ] 导航栏是否为 `background: #1a73e8; color: #fff`（蓝底白字）
- [ ] `max-width` 是否为 `1400px`
- [ ] 是否使用了 `.card` + `border-radius: 12px` + `box-shadow`
- [ ] 品牌名是否有 emoji 前缀（如 `🔬`）
- [ ] 每个视图底部是否有 `.fig-label` 图注
- [ ] 创新点角标（`.innovation-badge`）是否标注在关键卡片上
- [ ] 联动页是否使用 5 列 `.linkage-grid` 布局（而非 3 列 flat）
- [ ] 归属判定页是否使用 `.attribution-bar`（比例条）
- [ ] 差异化撰写预览页是否使用 `.diff-panel`（双栏对比）

---

## 二、技术图表（Stage 11 · tech_charts.html）

### 2.1 强制 CSS 骨架

```css
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'PingFang SC','Microsoft YaHei',-apple-system,sans-serif;background:#f8f9fa;color:#1a1a1a}

/* ===== 图表区域 ===== */
.chart-section{
  padding:32px;
  max-width:1400px;        /* 强制 1400px */
  margin:0 auto;
}
.chart-title{
  font-size:20px;font-weight:700;color:#1a73e8;
  margin-bottom:8px;display:flex;align-items:center;gap:8px;
}
.chart-subtitle{font-size:12px;color:#5f6368;margin-bottom:24px}
.source-tag{
  position:absolute;top:12px;right:12px;
  background:#e8f0fe;color:#1a73e8;
  padding:2px 10px;border-radius:12px;font-size:11px;
}

/* ===== 架构层 ===== */
.arch-layer{
  background:#fff;border-radius:12px;padding:20px;
  margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,0.08);
  position:relative;
}
.arch-layer-title{font-size:14px;font-weight:700;margin-bottom:12px}
.arch-components{display:flex;gap:12px;flex-wrap:wrap}
.arch-comp{
  background:#f8f9fa;border:2px solid #dadce0;border-radius:8px;
  padding:10px 16px;font-size:13px;text-align:center;
  flex:1;min-width:140px;
}
/* 各层配色 */
.layer-1 .arch-comp{border-color:#1a73e8;background:#e8f0fe}
.layer-2 .arch-comp{border-color:#34a853;background:#e6f4ea}
.layer-3 .arch-comp{border-color:#ea8600;background:#fef7e0}
.layer-4 .arch-comp{border-color:#ea4335;background:#fce8e6}

/* ===== 流程图 ===== */
.flow-container{display:flex;flex-direction:column;align-items:center;gap:0;position:relative}
.flow-node{
  background:#fff;border:2px solid #1a73e8;border-radius:10px;
  padding:14px 24px;font-size:14px;text-align:center;
  min-width:280px;position:relative;z-index:2;
}
.flow-node.start{border-radius:24px;background:#1a73e8;color:#fff}
.flow-node.end{border-radius:24px;background:#34a853;color:#fff}
.flow-node.decision{
  background:#fef7e0;border-color:#ea8600;
  clip-path:polygon(50% 0%,100% 50%,50% 100%,0% 50%);
  padding:24px 40px;font-size:13px;
}
.flow-node.process{background:#e8f0fe}
.flow-arrow{font-size:20px;color:#5f6368;padding:4px 0;z-index:1}

/* ===== 时序图 ===== */
.seq-container{
  position:relative;min-height:600px;
  background:#fff;border-radius:12px;padding:24px;
  box-shadow:0 2px 8px rgba(0,0,0,0.08);
}
.seq-actor{
  text-align:center;padding:12px 16px;background:#1a73e8;color:#fff;
  border-radius:8px;font-size:13px;font-weight:600;width:140px;
}
.seq-actors{display:flex;justify-content:space-between;margin-bottom:24px}

/* ===== 数据流 ===== */
.df-container{display:flex;align-items:center;gap:0;flex-wrap:nowrap}
.df-node{
  border-radius:16px;padding:16px 20px;font-size:13px;
  text-align:center;min-width:160px;position:relative;z-index:2;
}
.df-arrow{font-size:24px;padding:0 4px;z-index:1;flex-shrink:0}
.df-label{font-size:11px;color:#5f6368;text-align:center;margin-top:4px}
```

### 2.2 强制使用 SVG 连线（禁止 `▼` 文本箭头）

**所有图表的层间连线、步骤间箭头必须使用内联 SVG**，禁止用 `▼` / `→` 等文本字符代替。

#### SVG marker 定义（放在 HTML 开头或每个图表区域开头）

```html
<svg width="0" height="0" style="position:absolute">
  <defs>
    <marker id="ah" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0,10 3.5,0 7" fill="#5f6368"/>
    </marker>
    <marker id="ah-blue" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0,10 3.5,0 7" fill="#1a73e8"/>
    </marker>
    <marker id="ah-green" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0,10 3.5,0 7" fill="#34a853"/>
    </marker>
  </defs>
</svg>
```

#### 架构图层间 SVG 连线示例

```html
<div style="position:relative">
  <!-- 各 .arch-layer -->
  <div class="arch-layer layer-1">...</div>
  <div class="arch-layer layer-2">...</div>
  <!-- SVG 覆盖层绘制层间箭头 -->
  <svg style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:3">
    <line x1="700" y1="95" x2="700" y2="115" stroke="#5f6368" stroke-width="2" marker-end="url(#ah)"/>
    <line x1="700" y1="210" x2="700" y2="230" stroke="#5f6368" stroke-width="2" marker-end="url(#ah)"/>
  </svg>
</div>
```

#### 时序图 SVG 消息线示例

```html
<div style="position:relative;min-height:480px;padding:0 70px">
  <svg style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none">
    <!-- 生命线（垂直虚线） -->
    <line x1="70" y1="0" x2="70" y2="480" stroke="#dadce0" stroke-width="1" stroke-dasharray="5,5"/>
    <line x1="345" y1="0" x2="345" y2="480" stroke="#dadce0" stroke-width="1" stroke-dasharray="5,5"/>
    <!-- 消息线（水平实线 + 箭头） -->
    <line x1="70" y1="30" x2="345" y2="30" stroke="#1a73e8" stroke-width="2" marker-end="url(#ah-blue)"/>
    <text x="180" y="22" fill="#1a73e8" font-size="11">①消息文本</text>
    <!-- 返回消息（虚线） -->
    <line x1="345" y1="70" x2="70" y2="70" stroke="#5f6368" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#ah)"/>
    <text x="180" y="62" fill="#5f6368" font-size="11">②返回消息</text>
  </svg>
</div>
```

### 2.3 各图表 HTML 结构模板

#### 系统架构图

```html
<div id="chart-system-architecture" class="chart-section">
  <div class="chart-title">📐 系统架构图</div>
  <div class="chart-subtitle">支撑场景A/B全流程 | N层架构 · M个核心组件</div>
  <div style="position:relative">
    <div class="arch-layer layer-1">
      <div class="arch-layer-title" style="color:#1a73e8">🎯 {层名}</div>
      <div class="source-tag">支撑4.1产品侧全流程</div>
      <div class="arch-components">
        <div class="arch-comp"><strong>{组件名}</strong><br><span style="font-size:11px;color:#5f6368">{功能描述}</span></div>
      </div>
    </div>
    <!-- 更多层... -->
    <!-- SVG 连线覆盖层 -->
    <svg style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:3">
      <line x1="700" y1="95" x2="700" y2="115" stroke="#5f6368" stroke-width="2" marker-end="url(#ah)"/>
    </svg>
  </div>
</div>
```

#### 技术流程图

```html
<div id="chart-technical-flowchart" class="chart-section" style="background:#fff;border-radius:12px;margin:32px auto;box-shadow:0 2px 8px rgba(0,0,0,0.08)">
  <div class="chart-title">🔄 核心算法流程图</div>
  <div class="chart-subtitle">支撑场景A步骤1-3全流程 | N个处理步骤 + M个判断分支</div>
  <div style="position:relative;padding:24px">
    <!-- 流程节点（Flexbox 纵向排列） -->
    <div class="flow-container">
      <div class="flow-node start" style="margin-bottom:48px">{开始节点文本}</div>
      <div class="flow-node process" style="margin-bottom:48px"><strong>S1</strong> {步骤名}<br><span style="font-size:12px;color:#5f6368">{描述}</span></div>
      <!-- 判断节点 -->
      <div class="flow-node" style="border-color:#ea8600;background:#fef7e0;margin-bottom:48px">{判断条件}</div>
      <div style="display:flex;gap:80px;align-items:center;margin-bottom:8px">
        <div style="text-align:center"><span style="font-size:12px;color:#ea4335;font-weight:700">否</span></div>
        <div style="text-align:center"><span style="font-size:12px;color:#34a853;font-weight:700">是</span></div>
      </div>
      <div class="flow-node end">{结束节点文本}</div>
    </div>
    <!-- SVG 连线覆盖层：绘制步骤间箭头（禁止使用 ↓ 文本箭头） -->
    <svg style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:3">
      <!-- 开始 → S1（向下箭头） -->
      <line x1="50%" y1="80" x2="50%" y2="110" stroke="#5f6368" stroke-width="2" marker-end="url(#ah)"/>
      <!-- S1 → 判断节点（向下箭头） -->
      <line x1="50%" y1="175" x2="50%" y2="205" stroke="#5f6368" stroke-width="2" marker-end="url(#ah)"/>
      <!-- 判断节点 → 结束（向下箭头，"是"分支） -->
      <line x1="55%" y1="270" x2="55%" y2="320" stroke="#34a853" stroke-width="2" marker-end="url(#ah-green)"/>
      <!-- 判断节点 → 左侧回退（"否"分支示例） -->
      <polyline points="45%,255 30%,255 30%,155" fill="none" stroke="#ea4335" stroke-width="2" marker-end="url(#ah)"/>
    </svg>
  </div>
</div>
```

> **⚠️ 关键变更**：流程图步骤间箭头**必须使用 SVG `<line>` + `marker-end`**绘制，**严禁使用 `<div class="flow-arrow">↓</div>` 文本箭头**。节点间留出 48px 间距（`margin-bottom:48px`），SVG 覆盖层在间距区域绘制箭头连线。判断分支用 `<polyline>` 绘制折线箭头，Yes/No 分支用不同颜色 marker（绿色 `#ah-green` / 红色 `#ah`）区分。

#### 模块时序图

```html
<div id="chart-module-sequence" class="chart-section" style="background:#fff;border-radius:12px;margin:32px auto;box-shadow:0 2px 8px rgba(0,0,0,0.08)">
  <div class="chart-title">⏱ 模块间时序图</div>
  <div class="chart-subtitle">支撑4.1全流程 | N个参与者 · M次调用</div>
  <div style="padding:24px">
    <div class="seq-actors">
      <div class="seq-actor">👤 {角色1}</div>
      <div class="seq-actor" style="background:#34a853">📋 {角色2}</div>
      <!-- 更多角色 -->
    </div>
    <div style="position:relative;min-height:480px;padding:0 70px">
      <svg style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none">
        <!-- 生命线 -->
        <line x1="70" y1="0" x2="70" y2="480" stroke="#dadce0" stroke-width="1" stroke-dasharray="5,5"/>
        <!-- 消息箭头 -->
        <line x1="70" y1="30" x2="345" y2="30" stroke="#1a73e8" stroke-width="2" marker-end="url(#ah-blue)"/>
        <text x="180" y="22" fill="#1a73e8" font-size="11">①{消息}</text>
      </svg>
    </div>
  </div>
</div>
```

#### 数据流图

```html
<div id="chart-data-flow" class="chart-section" style="background:#fff;border-radius:12px;margin:32px auto;box-shadow:0 2px 8px rgba(0,0,0,0.08)">
  <div class="chart-title">📊 数据流向图</div>
  <div class="chart-subtitle">支撑4.2.4数据流描述 | N次主要格式转化</div>
  <div style="padding:24px">
    <div class="df-container" style="justify-content:center">
      <div class="df-node" style="background:#e8f0fe;border:2px solid #1a73e8">
        <div style="font-size:24px;margin-bottom:4px">📁</div>
        <strong>{节点名}</strong>
        <div class="df-label">{说明}</div>
      </div>
      <div class="df-arrow" style="color:#1a73e8">→<div style="font-size:10px;color:#5f6368">转化1<br>{处理}</div></div>
      <!-- 更多节点 -->
    </div>
  </div>
</div>
```

---

## 三、Playwright 截图脚本模板

### 3.1 产品侧截图脚本（`playwright_screenshot.js`）

```javascript
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    deviceScaleFactor: 2,          // 强制 2x 高清
    viewport: { width: 1440, height: 900 }  // 强制 1440 宽
  });

  // 使用无中文路径的副本（避免 file:// URL 编码问题）
  const htmlPath = process.env.HTML_PATH || path.resolve('patent_run/stage-08/code/index.html');
  await page.goto('file://' + htmlPath);

  // 图位需求清单（由智能体根据 invention_content.md 的占位符动态生成）
  const figures = [
    { viewId: 'overview', file: 'step_01_fig_scenario_overview.png' },
    { viewId: 'a1',       file: 'step_02_fig_gui_a_step1.png' },
    // ... 按清单逐一添加
  ];

  const screenshotDir = process.env.SCREENSHOT_DIR || path.resolve('patent_run/stage-08/screenshots');
  const { mkdirSync } = require('fs');
  mkdirSync(screenshotDir, { recursive: true });

  for (const fig of figures) {
    // 切换视图：触发导航 tab 的点击
    await page.evaluate((vid) => {
      document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      const target = document.getElementById('view-' + vid);
      if (target) target.classList.add('active');
    }, fig.viewId);
    await page.waitForTimeout(300);

    // 截取当前活跃视图
    const viewEl = await page.$('.view.active');
    if (viewEl) {
      await viewEl.screenshot({ path: path.join(screenshotDir, fig.file) });
    } else {
      // fallback: 全页截图
      await page.screenshot({ path: path.join(screenshotDir, fig.file), fullPage: false });
    }
  }

  await browser.close();
})();
```

### 3.2 技术图表截图脚本（`playwright_charts.js`）

> **强制要求**：技术图表必须使用**元素级截图**（`element.screenshot()`），不是全页截图。

```javascript
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    deviceScaleFactor: 2,
    viewport: { width: 1440, height: 900 }
  });

  const htmlPath = process.env.HTML_PATH || path.resolve('charts/tech_charts.html');
  await page.goto('file://' + htmlPath);

  const charts = [
    { id: '#chart-system-architecture', file: 'system_architecture.png' },
    { id: '#chart-technical-flowchart', file: 'technical_flowchart.png' },
    { id: '#chart-module-sequence',     file: 'module_sequence.png' },
    { id: '#chart-data-flow',           file: 'data_flow_diagram.png' }
  ];

  const chartsDir = process.env.CHARTS_DIR || path.resolve('charts');

  for (const chart of charts) {
    const element = await page.$(chart.id);
    if (element) {
      await element.screenshot({ path: path.join(chartsDir, chart.file) });
    }
  }

  await browser.close();
})();
```

---

## 四、禁止行为清单

| 编号 | 禁止行为 | 正确做法 |
|------|---------|---------|
| N1 | 导航栏白底灰字（`background:#fff`） | 必须 `background:#1a73e8; color:#fff` |
| N2 | `max-width: 1200px` 或更小 | 必须 `max-width: 1400px` |
| N3 | 用 `▼` / `→` / `↓` 文本代替连线（包括流程图中的 `<div class="flow-arrow">↓</div>`） | 必须用 SVG `<line>` + `marker-end`，流程图节点间留 48px 间距由 SVG 覆盖层绘制箭头 |
| N4 | 联动页用 3 列 flat 布局 | 必须用 5 列 `.linkage-grid`（含箭头列） |
| N5 | 时序图用绝对定位 `<div>` 标签 | 必须用 SVG `<line>` 生命线 + 消息箭头 |
| N6 | 技术图表全页截图 | 必须用 `element.screenshot()` 元素级截图 |
| N7 | 品牌名过于简短（如 "PatentSkill"） | 使用完整描述性品牌名（如 "🔬 CodePatent {系统名}"） |
| N8 | 缺少 `.fig-label` 图注 | 每个视图底部必须有图注 |
| N9 | 架构图用垂直文字标签（`writing-mode:vertical-rl`） | 使用水平标题（`.arch-layer-title`） |
