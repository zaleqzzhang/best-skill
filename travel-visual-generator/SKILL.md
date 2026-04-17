---
name: travel-visual-generator
description: >
  旅游攻略可视化生成 Skill。当用户需要以下任何功能时使用本 Skill：
  1. 将旅游行程信息生成精美 HTML 攻略页面；
  2. 将 HTML 旅游攻略截图为长图 PNG（全页截图）；
  3. 生成手绘水彩风旅游插画（小红书日记风格，每日行程/美食地图/景点插画）；
  4. 同时完成上述所有步骤，制作完整的可分享旅游图文套装。
  触发词：截图长图、生成手绘图、旅游插画、攻略配图、小红书图、每天一张图、手绘攻略、水彩旅游图、旅游攻略、生成攻略、出行计划、行程规划
---

# travel-visual-generator

本 Skill 提供三项核心能力，**标准工作流为依次执行**：

1. **旅游攻略 → HTML 页面**：根据行程信息生成美观的 HTML 攻略页面
2. **HTML → 长图截图**：将 HTML 页面截取为完整长图 PNG
3. **手绘风旅游插画生成**：调用 image_gen 工具，生成小红书日记风格水彩插画

---

## 能力零：生成旅游攻略 HTML 页面

### 何时执行

用户提供旅游目的地、时间、行程要点后，**先生成 HTML 再截图**。没有 HTML 就没有长图。

### HTML 设计规范

生成的 HTML 需满足以下要求：

**视觉风格：**
- 整体色调：`#c0392b`（红色主色）+ 米白背景 `#f5f0eb`
- 字体：系统中文字体（PingFang SC / Helvetica Neue）
- 卡片圆角：`16px`，阴影：`0 2px 12px rgba(0,0,0,0.07)`

**必须包含的模块：**
```
1. Hero 顶部Banner       ← 渐变红色背景，标题+标签行
2. 顶部 sticky 导航栏    ← 各章节锚点快速跳转
3. 行程总览 Grid          ← 每天一张卡片，日期+主题+描述
4. 每日详情（Day Card）   ← 左边框色区分城市，时间线格式
5. 景点/过早/美食分区     ← 带彩色高亮角标的食物卡片
6. 饮品推荐               ← 横向卡片排列
7. 出发前清单（Checklist）← 可打印勾选样式
8. 费用预算表             ← 表格 + 底部总计高亮框
```

**食物卡片高亮规则：**
- `.hl-red`（红色）：出了当地就没有、濒临消失的稀缺美食
- `.hl-orange`（橙色）：老字号经典必吃
- `.hl-green`（绿色）：随处可得、日常款
- 每张卡片右上角有 `.hl-corner` 角标说明推荐等级

**时间线格式（Day Card 内）：**
```html
<ul class="timeline">
  <li>
    <span class="time">09:00</span>
    <div class="content">
      <strong>景点/活动名称</strong>
      <div class="tip">💡 详细说明、地址、价格、注意事项</div>
    </div>
  </li>
</ul>
```

### 关键 CSS 类说明

```css
/* 日卡颜色：不同城市用不同边框色 */
.day-card          { border-left: 5px solid #e74c3c; }  /* 武汉-红 */
.day-card.green    { border-left: 5px solid #27ae60; }  /* 自然/神农架-绿 */
.day-card.blue     { border-left: 5px solid #2980b9; }  /* 郑州-蓝 */
.day-card.purple   { border-left: 5px solid #8e44ad; }  /* 返程-紫 */

/* 食物卡高亮 */
.food-card.hl-red    { background: linear-gradient(135deg,#fff5f5,#fff); border: 2px solid #e74c3c; }
.food-card.hl-orange { background: linear-gradient(135deg,#fff9f0,#fff); border: 2px solid #f39c12; }
.food-card.hl-green  { background: linear-gradient(135deg,#f0fff4,#fff); border: 2px solid #27ae60; }

/* 高亮角标 */
.hl-corner {
  position: absolute; top: -1px; right: -1px;
  background: <对应色>; color: white;
  font-size: 0.7rem; font-weight: 700;
  padding: 3px 10px; border-radius: 0 12px 0 10px;
}
```

### 信息采集清单

生成 HTML 前，需从用户输入或对话历史中提取：

| 信息 | 说明 |
|------|------|
| 出发/到达城市 | 含交通车次和时间 |
| 每天行程 | 景点+活动，带时间点 |
| 必吃清单 | 食物名+推荐店+价格+稀缺度 |
| 必喝饮品 | 本地特色饮品 |
| 住宿建议 | 区域+参考价格 |
| 注意事项 | 预约/购票/天气/装备 |
| 费用预算 | 各项分类+总计 |

---

## 能力一：HTML 长图截图

### 使用脚本

```bash
python3 ~/.workbuddy/skills/travel-visual-generator/scripts/screenshot_html.py \
  <html文件路径> \
  [输出PNG路径] \
  [--width 1200]
```

### 依赖说明

- 需要系统已安装 `node` 和 `puppeteer`
- 如果 puppeteer 未安装，先执行：`npm install puppeteer`（在 html 文件所在目录）
- 默认截图宽度 1200px，可通过 `--width` 调整

### 典型用法

```bash
# 基础用法（自动命名输出）
python3 ~/.workbuddy/skills/travel-visual-generator/scripts/screenshot_html.py \
  ./武汉郑州旅游攻略.html

# 指定输出路径和宽度
python3 ~/.workbuddy/skills/travel-visual-generator/scripts/screenshot_html.py \
  ./攻略.html ./攻略长图.png --width 1400
```

---

## 能力二：手绘风旅游插画

### 生成原则

- 风格固定为：**手绘水彩 + 牛皮纸背景 + 中文手写感**（小红书爆款风格）
- 单日行程图尺寸：`1024x1536`（竖版）
- 美食地图尺寸：`1536x1024`（横版）
- quality 始终设为 `high`，style 设为 `natural`

### 使用提示词生成脚本

运行脚本获得优化后的提示词，再传入 image_gen：

```bash
python3 ~/.workbuddy/skills/travel-visual-generator/scripts/gen_travel_image.py \
  --day "Day1" \
  --date "4月29日" \
  --city "武汉" \
  --spots "黄鹤楼,长江轮渡,巴公房子,古德寺" \
  --foods "热干面,鲜鱼糊汤粉,蛋酒,面窝" \
  --theme "古迹+夜游+过早"
```

脚本输出 JSON，其中 `prompt` 字段直接传入 image_gen 工具即可。

### 景点/美食元素库

详见 `references/prompt_guide.md`，包含：
- 武汉/神农架/郑州常用场景描述词
- 武汉特色美食精确描述词
- 配色方案和装饰元素建议

### 标准插画结构（每日行程图）

```
[顶部] 日期徽章 + 城市主题标题
[上半] 当日2-3个核心景点水彩插画
[下半] 当日必吃美食插画（每样带价格标签）
[点缀] 指南针/相机/花朵/纸胶带等装饰
```

---

## 完整套装工作流

当用户要求「出行攻略 + 每天一张图 + HTML长图」时，**严格按以下顺序执行**：

### Step 0 — 生成 HTML 攻略页面（必须先做！）
- 从用户提供的行程信息中提取所有必要数据
- 按上方「设计规范」生成完整 HTML 文件，写入项目目录
- 包含：行程总览、每日时间线、过早/美食/饮品卡片、清单、预算

### Step 1 — 截图长图
- 运行 `screenshot_html.py` 对刚生成的 HTML 文件截图
- 输出 `{城市}旅游攻略_长图.png`

### Step 2 — 逐日生成手绘插画
- 对每一天分别运行 `gen_travel_image.py` 获取提示词
- 调用 image_gen 生成对应插画（每张 `1024x1536`，high quality）

### Step 3 — 生成美食地图
- 单独生成一张横版（`1536x1024`）美食汇总插画
- 包含两城所有必吃美食，分区展示

### Step 4 — 打包交付
- 用 `deliver_attachments` 将所有文件一次性交付
- 顺序：长图 → 美食地图 → Day1 → Day2 → ... → 最后一天

> ⚠️ **没有 HTML 就没有长图**，Step 0 是所有后续步骤的前提，不可跳过。

---

## 注意事项

- HTML 截图依赖 node/puppeteer，在没有安装的环境中会失败；此时改为直接提供 HTML 文件给用户
- image_gen 每次只能生成一张图，多张图需逐个调用
- 提示词中的中文内容要用英文描述（如「黄鹤楼」写成 `Yellow Crane Tower (黄鹤楼)`），以提升生图质量
- 长图截图后用 open_result_view 展示，手绘图用 deliver_attachments 打包交付
