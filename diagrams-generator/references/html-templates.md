# HTML 方案图模板库

为 `diagrams-generator` skill 的 **HTML 方案图** 场景提供 5 种可直接套用的风格模板。

## 通用约定

| 项 | 值 |
|----|---|
| **CDN** | Tailwind CSS v3（`https://cdn.tailwindcss.com`） |
| **字体栈** | `-apple-system, "PingFang SC", "Microsoft YaHei", system-ui, sans-serif`（中英混排无糊字） |
| **画布尺寸** | 默认 1280×800，DPR=2 → 实际 PNG 2560×1600（Retina） |
| **截图模式** | `full_page=True`，背景跟随 HTML |
| **加载等待** | `wait_for_load_state("networkidle")` 必加，否则 Tailwind 没生效就被截图 |
| **目录约定** | `./pic/{name}/{name}.html` + `render.py` + `server.py` + `{name}.png` |

---

## 模板 1：🎨 手绘卡片风（Morandi Hand-drawn）

> **适用**：技术方案讲解、PRD 配图、文章插图。  
> **视觉特征**：米色底 / 莫兰迪暖色卡片 / emoji 步骤 / 圆角虚线 / 软阴影 / tag 标签。

### 配色 Palette

```css
--bg:        #F7F3EC;  /* 米色背景 */
--card-1:    #F5E6D3;  /* 暖米卡片 */
--card-2:    #E8D5B7;  /* 米黄卡片 */
--card-3:    #D6C7A8;  /* 浅棕卡片 */
--accent-1:  #C9826B;  /* 砖红强调 */
--accent-2:  #8FA88E;  /* 鼠尾草绿 */
--accent-3:  #B8956A;  /* 焦糖橙 */
--text:      #3D3528;  /* 深棕文字 */
--muted:     #8B7E6A;  /* 灰棕辅助 */
--border:    #D4C4A8;  /* 卡片边框 */
```

### 完整 HTML（可直接渲染）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>方案图</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
  body { font-family: -apple-system, "PingFang SC", "Microsoft YaHei", system-ui, sans-serif; }
  .card-morandi { background: #F5E6D3; border: 1.5px dashed #D4C4A8; border-radius: 14px; }
  .card-soft    { background: #FAF6EE; border: 1px solid #E8DCC4; border-radius: 12px; }
  .step-pill    { background: #F5E6D3; border: 1.5px solid #D4C4A8; border-radius: 999px; }
  .step-pill.active { background: #FFE4B5; border-color: #C9826B; }
  .tag          { background: #FAF6EE; border: 1px solid #D4C4A8; border-radius: 6px; font-size: 11px; }
  .tag.muted    { background: #F0EBE0; color: #A89A82; border-color: #D4C4A8; }
  .arrow-soft   { color: #C9826B; }
</style>
</head>
<body class="bg-[#F7F3EC] text-[#3D3528] p-10">

<div class="max-w-6xl mx-auto space-y-5">

  <!-- 顶部步骤条 -->
  <div class="flex items-center gap-3 flex-wrap">
    <div class="step-pill px-4 py-2.5 text-sm">① 维护 eval-base 模板</div>
    <span class="arrow-soft text-xl">→</span>
    <div class="step-pill px-4 py-2.5 text-sm">② cle env new --template</div>
    <span class="arrow-soft text-xl">→</span>
    <div class="step-pill px-4 py-2.5 text-sm">③ cle env watch · 健康就绪</div>
    <span class="arrow-soft text-xl">→</span>
    <div class="step-pill px-4 py-2.5 text-sm">④ trpc-cli 跑 CoreTest</div>
    <span class="arrow-soft text-xl">→</span>
    <div class="step-pill active px-4 py-2.5 text-sm">⑤ cle env free · 销毁</div>
  </div>

  <!-- 控制面 -->
  <div class="card-morandi p-5">
    <div class="text-base font-semibold mb-1.5">⚙️ 控制面 · 智研环境通</div>
    <div class="text-xs text-[#8B7E6A]">cle CLI · OpenAPI · Python SDK · MCP —— 流水线 / 评测平台后端任选其一即可触发上面 5 步</div>
  </div>

  <!-- 项目卡片 -->
  <div class="card-morandi p-5">
    <div class="text-sm text-[#8B7E6A] mb-3">智研项目 · ime-eval · 一个项目承载全部评测临时环境</div>
    <div class="flex gap-4">
      <!-- 基线模板 -->
      <div class="card-soft p-4 w-56 flex-shrink-0">
        <div class="text-center font-semibold text-sm mb-1">eval-base · 基线模板</div>
        <div class="text-center text-[10px] text-[#8B7E6A] mb-3">长期存在 · 一次部署 · 多次复用</div>
        <div class="grid grid-cols-2 gap-1.5">
          <span class="tag px-2 py-1 text-center">cloudpy_up</span>
          <span class="tag px-2 py-1 text-center">zuci</span>
          <span class="tag px-2 py-1 text-center">ca_123</span>
          <span class="tag px-2 py-1 text-center">ca_45</span>
          <span class="tag px-2 py-1 text-center">locallife</span>
          <span class="tag px-2 py-1 text-center">ct2</span>
          <span class="tag px-2 py-1 text-center">Ksana</span>
          <span class="tag px-2 py-1 text-center">app_scene</span>
        </div>
        <div class="text-center text-[10px] text-[#8B7E6A] mt-3">+ Kernel 词典 / CFS 共享卷</div>
      </div>
      <!-- 克隆箭头 -->
      <div class="flex flex-col justify-center text-[#C9826B] text-xs items-center w-12">
        <div class="text-3xl">→</div>
        <div>克隆</div>
        <div class="text-[10px] text-[#8B7E6A] mt-1">cle env new</div>
      </div>
      <!-- 三个克隆环境 -->
      <div class="flex-1 space-y-3">
        <div class="card-soft p-3">
          <div class="font-medium text-sm mb-0.5">eval-zhangsan-1001 · 评测 master</div>
          <div class="text-[11px] text-[#8B7E6A] mb-2">TTL 2h · 全量 7 服务</div>
          <div class="flex gap-1 flex-wrap">
            <span class="tag px-2 py-0.5">cloudpy</span>
            <span class="tag px-2 py-0.5">zuci</span>
            <span class="tag px-2 py-0.5">ca_123</span>
            <span class="tag px-2 py-0.5">ca_45</span>
            <span class="tag px-2 py-0.5">locallife</span>
            <span class="tag px-2 py-0.5">ct2</span>
            <span class="tag px-2 py-0.5">Ksana</span>
          </div>
        </div>
        <div class="card-soft p-3">
          <div class="font-medium text-sm mb-0.5">eval-lisi-1002 · 评测 v1.233.0-stable</div>
          <div class="text-[11px] text-[#8B7E6A] mb-2">TTL 2h · 子集 (5/7)</div>
          <div class="flex gap-1 flex-wrap">
            <span class="tag px-2 py-0.5">cloudpy</span>
            <span class="tag px-2 py-0.5">zuci</span>
            <span class="tag px-2 py-0.5">ca_123</span>
            <span class="tag muted px-2 py-0.5">未选</span>
            <span class="tag muted px-2 py-0.5">未选</span>
            <span class="tag px-2 py-0.5">ct2</span>
            <span class="tag px-2 py-0.5">Ksana</span>
          </div>
        </div>
        <div class="card-soft p-3">
          <div class="font-medium text-sm mb-0.5">eval-wangwu-1003-featx · 评测 feature/X</div>
          <div class="text-[11px] text-[#8B7E6A] mb-2">TTL 4h · 单服务对照（cloudpy + Ksana）</div>
          <div class="flex gap-1 flex-wrap">
            <span class="tag px-2 py-0.5">cloudpy</span>
            <span class="tag muted px-2 py-0.5">未选</span>
            <span class="tag muted px-2 py-0.5">未选</span>
            <span class="tag muted px-2 py-0.5">未选</span>
            <span class="tag muted px-2 py-0.5">未选</span>
            <span class="tag muted px-2 py-0.5">未选</span>
            <span class="tag px-2 py-0.5">Ksana</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 底部双卡 -->
  <div class="grid grid-cols-2 gap-4">
    <div class="p-4 rounded-xl" style="background:#FFF4D6; border:1.5px solid #E8C97A;">
      <div class="text-sm font-semibold mb-1">🍃 TTL 自实现 · try/finally 调 cle env free</div>
      <div class="text-[11px] text-[#8B7E6A]">+ 兜底 Cron · 每小时扫 eval-* 前缀，age &gt; TTL 强制释放</div>
    </div>
    <div class="p-4 rounded-xl" style="background:#E8F0E5; border:1.5px solid #A8C0A0;">
      <div class="text-sm font-semibold mb-1">✅ 控制台原生支持</div>
      <div class="text-[11px] text-[#8B7E6A]">所有临时环境可在智研控制台直接查看 / 登录 / 杀</div>
    </div>
  </div>

  <!-- 图说 -->
  <div class="text-center text-xs text-[#8B7E6A] mt-3">图 4 · 方案 2：智研环境通模板克隆 —— 一次维护模板，多次克隆销毁</div>

</div>

</body>
</html>
```

---

## 模板 2：🌙 现代深色风（Dark Tech）

> **适用**：系统架构、Hero 配图、技术博客头图。  
> **视觉特征**：深色底 / 网格背景 / 霓虹高亮边 / 等距字体标签。

### 配色覆盖

```css
--bg:        #0B0F19;
--card-1:    #151A2B;
--card-2:    #1F2942;
--accent-1:  #38BDF8;  /* cyan-400 */
--accent-2:  #A78BFA;  /* violet-400 */
--accent-3:  #34D399;  /* emerald-400 */
--text:      #E5E7EB;
--muted:     #94A3B8;
--border:    #334155;
```

### 关键样式覆盖（替换模板 1 的 `<style>`）

```css
body { 
  background: #0B0F19; color: #E5E7EB;
  background-image: 
    linear-gradient(rgba(56,189,248,0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(56,189,248,0.06) 1px, transparent 1px);
  background-size: 32px 32px;
}
.card-morandi { background: #151A2B; border: 1px solid #334155; border-radius: 12px; box-shadow: 0 0 0 1px rgba(56,189,248,0.15) inset; }
.card-soft    { background: #1F2942; border: 1px solid #334155; border-radius: 10px; }
.step-pill    { background: #151A2B; border: 1px solid #334155; color: #E5E7EB; border-radius: 999px; }
.step-pill.active { background: linear-gradient(90deg,#0EA5E9,#A78BFA); border-color: #38BDF8; color: white; box-shadow: 0 0 18px rgba(56,189,248,0.5); }
.tag       { background: #0B0F19; color: #38BDF8; border: 1px solid #334155; font-family: ui-monospace, monospace; }
.tag.muted { background: #1F2942; color: #64748B; border-color: #334155; }
.arrow-soft { color: #38BDF8; }
</style>
<style>body { font-family: ui-sans-serif, "PingFang SC", system-ui, sans-serif; }</style>
```

将 body 的 `bg-[#F7F3EC] text-[#3D3528]` 改为 `bg-[#0B0F19] text-gray-200`。

---

## 模板 3：📐 简约白板风（Whiteboard）

> **适用**：论文/正式文档/英文报告。  
> **视觉特征**：纯白背景 / 0.5pt 细线框 / 单色（蓝或灰）强调 / 无填充色 / 等高布局。

### 配色覆盖

```css
--bg:        #FFFFFF;
--card-1:    #FFFFFF;
--accent-1:  #1F2937;  /* 主色：近黑 */
--accent-2:  #2563EB;  /* 单一蓝色强调 */
--text:      #111827;
--muted:     #6B7280;
--border:    #D1D5DB;
```

### 关键样式覆盖

```css
body { background: #FFFFFF; color: #111827; font-family: "Inter", -apple-system, "PingFang SC", sans-serif; }
.card-morandi { background: #FFFFFF; border: 1px solid #1F2937; border-radius: 4px; box-shadow: none; }
.card-soft    { background: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 4px; }
.step-pill    { background: #FFFFFF; border: 1px solid #1F2937; color: #111827; border-radius: 4px; font-weight: 500; }
.step-pill.active { background: #1F2937; color: white; }
.tag       { background: #F9FAFB; color: #1F2937; border: 1px solid #D1D5DB; font-family: ui-monospace, monospace; border-radius: 2px; }
.tag.muted { color: #9CA3AF; background: #FFFFFF; border-style: dashed; }
.arrow-soft { color: #1F2937; }
```

强调点用 `border-l-4 border-blue-600 pl-3`（左侧蓝色细线）替代填充色。

---

## 模板 4：🌈 渐变科技风（Gradient Hero）

> **适用**：产品发布、官网 Hero、营销材料。  
> **视觉特征**：紫蓝渐变背景 / 毛玻璃卡片 / 大圆角 / 高对比白字。

### 配色覆盖

```css
--bg-grad:   linear-gradient(135deg, #667EEA 0%, #764BA2 50%, #F093FB 100%);
--card-glass: rgba(255,255,255,0.15);
--card-bg:    rgba(255,255,255,0.25);
--accent-1:  #FFFFFF;
--accent-2:  #FFD700;
--text:      #FFFFFF;
--muted:     rgba(255,255,255,0.75);
--border:    rgba(255,255,255,0.3);
```

### 关键样式覆盖

```css
body { 
  background: linear-gradient(135deg,#667EEA 0%,#764BA2 50%,#F093FB 100%);
  color: white; min-height: 100vh;
  font-family: -apple-system, "PingFang SC", system-ui, sans-serif;
}
.card-morandi { 
  background: rgba(255,255,255,0.15); 
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.3); border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}
.card-soft    { background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.25); border-radius: 16px; backdrop-filter: blur(10px); }
.step-pill    { background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.4); color: white; border-radius: 999px; backdrop-filter: blur(10px); }
.step-pill.active { background: white; color: #667EEA; box-shadow: 0 4px 20px rgba(0,0,0,0.2); }
.tag       { background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3); border-radius: 8px; }
.tag.muted { color: rgba(255,255,255,0.5); border-style: dashed; }
.arrow-soft { color: rgba(255,255,255,0.85); }
```

注意：渐变背景需手动给所有 `text-[#3D3528]`/`text-[#8B7E6A]` 改成 `text-white`/`text-white/75`。

---

## 模板 5：📰 杂志风（Editorial Infographic）

> **适用**：公众号配图、数据洞察、PPT 内页。  
> **视觉特征**：超大数字标题 / 衬线主标题 / 强对比色块 / 重点引用线。

### 配色覆盖

```css
--bg:        #FFF8F0;
--card-1:    #FFFFFF;
--accent-1:  #C8102E;  /* 杂志红 */
--accent-2:  #003F5C;  /* 深海军蓝 */
--accent-3:  #FFA600;  /* 强调橙 */
--text:      #1A1A1A;
--muted:     #6B6B6B;
--border:    #1A1A1A;
```

### 关键样式覆盖

```css
body { background: #FFF8F0; color: #1A1A1A; font-family: "Inter", -apple-system, "PingFang SC", sans-serif; }
h1, .headline { font-family: "Georgia", "Songti SC", serif; font-weight: 800; letter-spacing: -0.02em; }
.bignum   { font-size: 96px; font-weight: 900; color: #C8102E; line-height: 1; font-family: "Georgia", serif; }
.card-morandi { background: #FFFFFF; border: 2px solid #1A1A1A; border-radius: 0; box-shadow: 6px 6px 0 #1A1A1A; }
.card-soft    { background: #FFFFFF; border: 1px solid #1A1A1A; border-radius: 0; }
.step-pill    { background: #FFFFFF; border: 2px solid #1A1A1A; color: #1A1A1A; border-radius: 0; font-weight: 700; }
.step-pill.active { background: #C8102E; color: white; border-color: #1A1A1A; }
.tag       { background: #1A1A1A; color: #FFF8F0; border: none; font-weight: 600; border-radius: 0; }
.tag.muted { background: #FFF8F0; color: #1A1A1A; border: 1px solid #1A1A1A; }
.arrow-soft { color: #C8102E; font-weight: 900; }
.quote    { border-left: 4px solid #C8102E; padding-left: 16px; font-style: italic; }
```

杂志风的关键是 **大数字 + 强对比方块 + Brutalist 阴影**（`box-shadow: 6px 6px 0 黑`）。

---

## 风格选择决策树

```
用户描述里有...
├─ "技术方案" / "PRD" / "架构方案" / "手绘"          → 1. 手绘卡片风（默认）
├─ "系统架构" / "技术博客" / "Hero" / "酷炫"         → 2. 现代深色风
├─ "论文" / "正式" / "学术" / "英文"                 → 3. 简约白板风
├─ "产品发布" / "营销" / "官网" / "渐变"             → 4. 渐变科技风
└─ "公众号" / "数据洞察" / "杂志" / "强调"           → 5. 杂志风
```

如果用户没明确说，**默认走模板 1**（用户最初的视觉锚点）。

---

## 进阶：自定义风格

用户可在确认阶段说："改成 xxx 配色 / 把卡片改成圆角 16 / 字体换衬线"。
按要求改 `<style>` 块对应变量即可，**不要重写整个 HTML**。

---

## 排错速查

| 现象 | 原因 | 解决 |
|------|------|------|
| PNG 截图样式错乱、像素堆叠 | Tailwind CDN 没加载完 | 加 `await page.wait_for_load_state("networkidle")` |
| 中文字符变小方块 | Linux 容器无中文字体 | 加 `apt-get install fonts-noto-cjk` 或本地 macOS/Windows 跑 |
| 截图发虚 | 没设 device_scale_factor | `device_scale_factor=2` |
| Playwright 启动报错 chromium not found | 只装了 pip 包没下浏览器 | `playwright install chromium` |
| 端口 8765 被占 | 已有进程占用 | server.py 的 `find_free_port` 会自动 +1，最多到 8800 |
| HTML 内容超出可视区，截图被裁 | `viewport` 高度不够 | 用 `full_page=True`（已默认） |

---

## 快速开始（Skill 内部参考流程）

1. 在 Phase 1 用户选了 **方案 A + 风格 N**
2. 复制模板 1 的完整 HTML 作为 base
3. 根据风格 N 替换 `<style>` 块中的样式变量
4. 替换内容（步骤文字、卡片标题、tag 名字）
5. 写入 `./pic/{name}/{name}.html`
6. 写入 render.py / server.py（见 SKILL.md Phase 2 的通用模板）
7. 执行 `python render.py` → PNG
8. 后台 `python server.py` + 调 `preview_url`
9. 报告产物路径
