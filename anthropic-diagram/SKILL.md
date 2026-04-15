---
name: anthropic-diagram
description: Generate architecture diagrams, flowcharts, and system diagrams in Anthropic's signature visual style — warm gray backgrounds, soft pastel color blocks, dashed group containers, and clean arrow connections. Produces pure SVG output. Can also analyze source code (project structure, class hierarchies, API routes, data flows) and automatically generate corresponding diagrams. Use this skill when the user asks to create architecture diagrams, visualize code structure, or generate any technical visual in a clean, modern, Anthropic-inspired aesthetic.
---

# Anthropic-Style Diagram Generator

Generate beautiful, clean technical diagrams in Anthropic's signature visual style. Output pure SVG or HTML that can be viewed offline, embedded anywhere, or exported to PNG.

> **⚠️ Font Licensing Notice — MANDATORY user-facing warning:**
>
> This skill uses **Anthropic Sans** (Styrene A, by Commercial Type) and optionally **TencentSans** (by Monotype for Tencent). Both are **proprietary commercial fonts**.
>
> **The agent MUST do ALL of the following:**
>
> 1. **Before generating the FIRST diagram in a session**, proactively warn the user in the chat message:
>    > ⚠️ 字体版权提醒：本次生成使用了 Anthropic Sans（Styrene A，Commercial Type 出品）字体，属于付费商业字体。当前输出仅适用于个人学习和内部交流。如需用于商业用途（广告、产品、对外发布等），请购买字体授权或切换到开源方案 C（Inter 字体）。
>
> 2. **In every generated SVG/HTML file**, append this comment before the closing tag:
>    ```
>    <!-- ⚠️ Font License: Anthropic Sans (Styrene A) is a commercial font by Commercial Type. TencentSans is a proprietary font by Monotype/Tencent. This file is for non-commercial use only. For commercial use, purchase a license or switch to Inter (SIL Open Font License). -->
>    ```
>
> 3. **If the user mentions commercial use, distribution, or publishing externally**, the agent MUST immediately recommend switching to Scheme C (Inter) and explain why.
>
> **DO NOT skip the chat warning. DO NOT wait for the user to ask about licensing. Be proactive.**

Supports two modes:
1. **Description mode** — User describes the architecture in natural language
2. **Code-reading mode** — Agent reads source code and auto-generates diagrams

## When to Use

Trigger this skill when the user asks to:
- Create an architecture diagram, system diagram, or deployment diagram
- Draw a flowchart, process flow, or decision tree
- Visualize a data pipeline, request lifecycle, or state machine
- Create a layer/tier diagram (e.g., microservices layers)
- Make a comparison diagram (Before/After, Plan A vs B)
- Draw a sequence/interaction diagram between components
- Generate any technical diagram in "Anthropic style", "clean style", or "modern minimal style"
- **Visualize the architecture of a codebase or project**
- **Generate a diagram from source code** (e.g., "draw the architecture of this project")
- **Show the call flow / data flow / class hierarchy of code**
- **Create a system diagram from a repo structure**

## Reference Examples

This skill ships with example SVGs in the `references/` directory. ALWAYS review them before generating, as they define the visual standard:

- `example-architecture.svg` — Horizontal pipeline with parallel paths and merge (the canonical example)
- `example-flowchart.svg` — Vertical decision flow with branching
- `example-layers.svg` — Stacked layer/tier diagram (接入层 → 服务层 → 数据层 → 基础设施)
- `example-comparison.svg` — Side-by-side comparison (Plan A vs Plan B)
- `example-sequence.svg` — Sequence/interaction diagram with lifelines

**CRITICAL**: Before generating any diagram, read the most relevant reference SVG file to calibrate your output. Match the spacing, sizing, and proportions exactly.

---

## Design System

### Canvas
- **Background**: Warm gray `#f0efed`, rounded corners `rx="22"`
- **Padding**: Minimum 48px from all edges
- **Sizing**: Adapt canvas to content. Common sizes:
  - Horizontal pipeline: `960×640`
  - Vertical flowchart: `640×720` (or taller)
  - Layer diagram: `800×560`
  - Comparison: `900×480`
  - Sequence: `820×580`
  - Scale up height/width as needed, keeping proportions balanced

### Typography

#### Font Preference — Ask the User

Before generating the first diagram in a session, **ask the user which font scheme they prefer**:

| Scheme | Display Font (titles, nodes) | Body Font (labels, hints) | Best For |
|--------|------------------------------|---------------------------|----------|
| **A: Anthropic Style** (default) | Anthropic Sans (via CDN) | Anthropic Sans | Online use, Anthropic brand feel |
| **B: Anthropic + Tencent Mix** | Anthropic Sans (titles) | TencentSans (body/labels) | Tencent internal, premium CJK |
| **C: Open Source Safe** | Inter | Inter | Free commercial use, maximum compatibility |

If the user has no preference, use **Scheme A**.

#### Font Loading Rules

**⚠️ IMPORTANT — Licensing & Distribution:**
- **Anthropic Sans** (actually Styrene A by Commercial Type) — paid commercial font. Load via Anthropic's CDN ONLY for personal/internal use. **Do NOT bundle font files in any distributable package.**
- **TencentSans** (by Monotype for Tencent) — proprietary brand font. Reference as local system font ONLY. **Do NOT bundle, redistribute, or link to unauthorized CDNs.** Users must have it installed locally.
- **Inter** — SIL Open Font License, free for any use.

#### Scheme A: Anthropic Sans (CDN)
```css
@font-face {
  font-family: 'Anthropic Sans';
  src: url('https://cdn.prod.website-files.com/67ce28cfec624e2b733f8a52/69971a00a3295036497e1a28_AnthropicSans-Roman-Web.woff2') format('woff2');
  font-weight: 100 900;
  font-style: normal;
}
@font-face {
  font-family: 'Anthropic Sans';
  src: url('https://cdn.prod.website-files.com/67ce28cfec624e2b733f8a52/69971a016067bf14b9b8f48d_AnthropicSans-Italic-Web.woff2') format('woff2');
  font-weight: 100 900;
  font-style: italic;
}
```
Fallback: `'Anthropic Sans', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Noto Sans SC', sans-serif`

#### Scheme B: Anthropic + TencentSans (Local)
```css
/* Anthropic Sans — loaded from CDN */
@font-face {
  font-family: 'Anthropic Sans';
  src: url('https://cdn.prod.website-files.com/67ce28cfec624e2b733f8a52/69971a00a3295036497e1a28_AnthropicSans-Roman-Web.woff2') format('woff2');
  font-weight: 100 900;
  font-style: normal;
}
/* TencentSans — referenced as local system font, user must have it installed */
```
- Titles, node text: `'Anthropic Sans', 'TencentSans', sans-serif`
- Subtitles, labels, hints: `'TencentSans', 'Anthropic Sans', 'PingFang SC', sans-serif`
- Users without TencentSans installed will seamlessly fallback.

#### Scheme C: Inter (Open Source)
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
```
Fallback: `'Inter', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Noto Sans SC', sans-serif`

#### Offline / Self-Contained Mode
If the user needs a fully offline SVG:
- **Scheme A/B**: Ask the user to provide their own font files (woff2). Then read the file, base64-encode it, and embed via `url(data:font/woff2;base64,...)` in the SVG.
- **Scheme C**: Inter can be freely embedded. Download from Google Fonts, base64-encode, and embed.

The key rule: **never distribute proprietary font files in the skill package itself.**

**Font sizes:**

| Element | Size | Weight | Color | Extra |
|---------|------|--------|-------|-------|
| Title | 21px | 700 | `#1a1a1a` | letter-spacing: 4 |
| Node title | 16px | 600 | (per color group) | |
| Node subtitle | 11.5px | 400 | (per color group) | |
| Group label | 13px | 400 | `#8c8b87` | letter-spacing: 0.5 |
| Hint/annotation | 12.5px | 400 | `#aaa9a5` | italic |
| Footer note | 13px | 400 | `#8c8b87` | letter-spacing: 0.8 |
| Tag text | 12.5px | 500 | `#256b3a` | |
| Sequence label | 12px | 500 | varies | |

### Color Palette

Only use these 5 semantic color groups. The restraint is what makes it look good.

| Role | Background | Title Color | Subtitle Color | Use For |
|------|-----------|-------------|----------------|---------|
| **Blue** | `#cce0f0` | `#1c5a82` | `#5a96b8` | Core processing, retrieval, computation, main pipeline nodes |
| **Red/Warm** | `#f0d5c6` | `#8c3b1a` | `#b86a48` | Special/unique components, external services, attention-needed, negative items |
| **Green/Teal** | `#c8e8da` | `#1a6b50` | `#509878` | Results, output, aggregation, final stages, start/end points, positive items |
| **White** | `#ffffff` + stroke `#d8d7d3` 1.4px | `#1a1a1a` | `#999999` | Input, neutral, user-facing, context, databases, infrastructure |
| **Tag (small)** | `#d4edda` | `#256b3a` | — | Labels, small identifiers, data tags, infrastructure badges |

**CRITICAL**: Do NOT invent new colors. If you need emphasis, use **Red/Warm**. If you need de-emphasis, use **White**. Never use gradients, shadows, or opacity.

### Node Shapes

| Type | Size | Border Radius | Stroke |
|------|------|---------------|--------|
| Standard node | 120–140px × 56–62px | `rx="10"` | None (except White) |
| Small tag | 80–110px × 30–34px | `rx="7"` | None |
| Pill (start/end) | 160px × 48px | `rx="24"` | None |
| Diamond (decision) | ~200px diagonal | polygon | White+stroke |
| Sequence header | 100–140px × 44px | `rx="10"` | None |

All nodes: text centered both horizontally and vertically.

### Group Containers
- **Border**: `stroke="#c4c3bf"`, `stroke-width="1.6"`, `stroke-dasharray="8,5"`
- **Fill**: `none` (transparent — never fill group containers)
- **Border radius**: `rx="12"`
- **Label**: Top-left corner, `top: 12px, left: 18px` from container edge

### Arrows & Connections
- **Stroke**: `#b0afa9`, `stroke-width="1.4"`
- **Arrow marker** — open chevron, NOT filled triangle:
```xml
<marker id="ah" viewBox="0 0 10 7" refX="9.5" refY="3.5"
  markerWidth="7" markerHeight="5.5" orient="auto">
  <path d="M 0 0.6 L 9.5 3.5 L 0 6.4" fill="none" stroke="#b0afa9"
    stroke-width="1.3" stroke-linejoin="round"/>
</marker>
```
- For colored arrows (e.g., in sequence diagrams), create variant markers:
```xml
<marker id="ah-blue" ...><path ... stroke="#5a96b8" .../></marker>
```
- **Routing**: Orthogonal (90° turns) only. No diagonal lines.
- **Line types**: `<line>` for straight, `<polyline>` for multi-segment
- **Gap**: 2–4px between node edge and arrow endpoint
- **Lifelines** (sequence diagrams): `stroke="#d8d7d3"`, `stroke-dasharray="6,4"`, `stroke-width="1"`

### Footer Note
- White background + thin border (same style as White nodes)
- Bottom-left of canvas
- For key takeaways, performance metrics, or design highlights

---

## Diagram Types & Layout Rules

### 1. Architecture / Pipeline Diagram
- **Flow**: Left-to-right
- **Canvas**: ~960×640
- **Pattern**: Input → [Group: Path A] → Merge → Output, with parallel paths stacked vertically
- **Reference**: `example-architecture.svg`

### 2. Flowchart / Decision Flow
- **Flow**: Top-to-bottom
- **Canvas**: ~640×720+ (grow height as needed)
- **Pattern**: Start (pill) → Process → Decision (diamond) → branches → End (pill)
- **Decisions**: Use diamond shape (polygon), branch left/right or continue down
- **Reference**: `example-flowchart.svg`

### 3. Layer / Tier Diagram
- **Flow**: Top-to-bottom layers
- **Canvas**: ~800×560
- **Pattern**: Stacked group containers, each containing horizontally arranged nodes
- **Layer naming**: Label each group container (接入层, 服务层, 数据层, etc.)
- **Inter-layer arrows**: Single centered vertical arrow between layers
- **Reference**: `example-layers.svg`

### 4. Comparison Diagram
- **Flow**: Side-by-side
- **Canvas**: ~900×480
- **Pattern**: Two group containers, left and right, with a "VS" divider
- **Pros/cons**: Use Green tags for ✓ and Red tags for ✗
- **Reference**: `example-comparison.svg`

### 5. Sequence / Interaction Diagram
- **Flow**: Top-to-bottom timeline
- **Canvas**: ~820×580+ (grow height for more steps)
- **Pattern**: Actor headers at top → dashed lifelines → horizontal arrows between lifelines
- **Labels**: Centered on arrows with background rect for readability
- **Step numbering**: Use ①②③ circled numbers
- **Reference**: `example-sequence.svg`

---

## Complex Diagram Layout Rules

When diagrams have **15+ nodes** or **3+ groups**, follow these additional rules to maintain visual quality at scale. These override the basic guidelines above when conflicts arise.

### Node Density Control

| Nodes per row | Action |
|---------------|--------|
| 1–4 | Normal layout, standard node size (120–140px wide) |
| 5 | Slightly reduce node width to 110px, reduce horizontal gap to 24px |
| 6+ | **MUST wrap to next row**. Max 5 nodes per row. Insert 20px vertical gap between rows within the same group |

### Node Text Overflow

- **Title > 5 Chinese chars or > 12 English chars**: Reduce font-size from 16px to 14px
- **Title > 7 Chinese chars or > 16 English chars**: Reduce font-size to 13px AND increase node width to 150px
- **Subtitle**: Always keep at 11px, truncate with "..." if > 20 chars
- **NEVER let text visually overflow** the node boundary. If it still doesn't fit, split into two lines using `<tspan>`:
```xml
<text x="..." y="..." text-anchor="middle">
  <tspan x="..." dy="-6">First Line</tspan>
  <tspan x="..." dy="16">Second Line</tspan>
</text>
```

### Group Container Sizing

- **Group padding**: min 20px from inner nodes to group border on all sides
- **Group label**: must not overlap with any inner node (ensure at least 36px from top of group to top of first node row)
- **Inter-group spacing**: Gap between groups = `max(40px, 0.15 × group_height)`, but **never > 60px**
  - This prevents the "giant white gap" problem between sections

### Canvas Sizing for Complex Diagrams

- **Width**: Scale to fit content. Common widths: 960px (standard), 1100px (wide), 1200px (extra-wide for 6+ columns)
- **Height**: `sum(all_group_heights) + inter_group_gaps + title_area(60px) + footer_area(80px) + padding(96px)`
- **Aspect ratio**: Aim for width:height between 1:1 and 1:2. If height > 2× width, consider splitting into multiple diagrams
- **Fill ratio**: Content should fill ≥70% of the canvas area. If there's > 30% empty space, the canvas is too large — shrink it

### When to Split into Multiple Diagrams

**MUST split** if ANY of these are true:
- Total nodes > 25
- Canvas height > 1600px
- 4+ distinct logical groups that don't share connections
- User's description has clearly separable phases (e.g., "offline training" + "online serving")

When splitting:
- Each sub-diagram should be self-contained and understandable alone
- Use consistent color assignments across sub-diagrams (same component = same color)
- Add a brief title to each that indicates its position: "Part 1: xxx", "Part 2: xxx"

### Arrow Routing for Dense Layouts

- **Avoid arrow crossings** whenever possible. Rearrange node positions to minimize crossings
- When crossings are unavoidable, add a small gap (3px) at the crossing point to show which line is "on top"
- **Long arrows** (spanning > 3 nodes): route along the edges of groups, not through the middle
- **Feedback arrows** (going backwards/upward): route around the outside of groups, use dashed style to distinguish from forward flow

### Annotation Placement

- Place "并行", "Async", step labels **outside** the main flow, not on top of arrows
- Use italic style, muted color `#aaa9a5`, small size (11–12px)
- For decision labels ("是/否", "Yes/No"): place close to the branching arrow, 4px offset from the line

---

## Output Formats

### Pure SVG (default)
Save as `.svg` file. Best for embedding in docs, importing into Figma, version control.

### HTML Preview (when user wants to see it locally)
Wrap the SVG in a minimal HTML page:
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{DIAGRAM_TITLE}</title>
<style>
  body {
    margin: 0; padding: 48px;
    background: #fff;
    display: flex; justify-content: center; align-items: center;
    min-height: 100vh;
  }
</style>
</head>
<body>
  {SVG_CODE_HERE}
</body>
</html>
```

### Self-contained SVG (offline)
Use **Strategy C** (base64 fonts) to produce a single `.svg` file with zero dependencies. The file will be larger (~300KB) but works anywhere — air-gapped networks, email attachments, PDF embeds.

---

## Code-Reading Mode

When the user asks to **visualize code** (e.g., "draw the architecture of this project", "generate a diagram from this codebase"), follow this analysis pipeline:

### Step 1: Scan Project Structure

Read the top-level directory to understand the project shape:
- `package.json` / `go.mod` / `pyproject.toml` / `Cargo.toml` → Identify language & framework
- `src/` / `app/` / `lib/` / `internal/` → Source code layout
- `docker-compose.yml` / `k8s/` / `terraform/` → Infrastructure
- `README.md` → Often describes the architecture in words

### Step 2: Identify Architecture Pattern

Based on what you find, classify the project:

| Pattern | Signals | Best Diagram Type |
|---------|---------|-------------------|
| **Monolith** | Single app directory, one entry point | Layer diagram |
| **Microservices** | Multiple service directories, docker-compose | Architecture (pipeline) |
| **Client-Server** | `frontend/` + `backend/` or `client/` + `server/` | Architecture (pipeline) |
| **Pipeline/ETL** | Sequential data processing stages | Architecture (pipeline) |
| **Event-driven** | Message queues, event handlers, pub/sub | Architecture + Sequence |
| **Serverless** | Lambda/Cloud Functions, API Gateway configs | Layer diagram |
| **Library/SDK** | Exported modules, public API surface | Layer diagram |
| **CLI tool** | Command definitions, argument parsing | Flowchart |

### Step 3: Extract Components

Read key source files to identify the building blocks:

**For Web Services (Node/Python/Go/Java):**
- Route definitions → API endpoints → Blue nodes
- Middleware/interceptors → Processing stages → Blue nodes
- Database connections/ORM models → Data stores → White nodes
- External API calls → External services → Red/Warm nodes
- Cache layers → Infrastructure → Green tags
- Message queue producers/consumers → Async components → Red/Warm nodes

**For Frontend Apps (React/Vue/Angular):**
- Pages/Routes → Top-level views → Blue nodes (grouped)
- State management (Redux/Vuex/Zustand) → Central store → Red/Warm node
- API layer/services → Data fetching → White nodes
- Shared components → Component library → Green tags

**For Data Pipelines:**
- Input sources → Entry points → White nodes
- Transform stages → Processing → Blue nodes
- Output sinks → Destinations → Green nodes

**For Monorepo/Multi-service:**
- Each package/service → One node or group
- Shared libraries → Tags
- Inter-service communication → Arrows

### Step 4: Map Connections

Identify how components interact:
- **Function calls / imports** → Direct arrows
- **HTTP requests** → Labeled arrows ("REST", "gRPC")
- **Message queues** → Dashed or labeled arrows ("Kafka", "Redis Pub/Sub")
- **Database read/write** → Arrows to data store nodes
- **Event emission** → Dashed arrows

### Step 5: Choose Abstraction Level

**CRITICAL**: Don't draw every file. Abstract to the right level:

- **System level** (default): Services, databases, queues, external APIs → 8–15 nodes max
- **Module level**: Major modules within one service → 6–12 nodes max
- **Class/Function level**: Only if user specifically asks → Use flowchart type

Rule of thumb: If you have more than 15 nodes, you need to group or abstract further.

### Step 6: Apply Color Semantics

Map code concepts to the color system:

| Code Concept | Color | Examples |
|-------------|-------|---------|
| Core business logic, API handlers, processing | **Blue** | UserService, OrderController, DataProcessor |
| External/third-party, AI/ML, special | **Red/Warm** | OpenAI API, Payment Gateway, LLM Service |
| Output, results, response, aggregation | **Green** | Response Builder, Result Cache, Final Output |
| Input, config, databases, infrastructure | **White** | MySQL, Redis, S3, User Input, Config |
| Small labels, tech stack badges | **Tag** | K8s, Docker, gRPC, REST |

### Code Analysis Examples

**Example prompt**: "读一下这个项目的代码，画一张架构图"

**Agent should**:
1. Scan `package.json` → Identify it's a Next.js app
2. Read `app/` directory → Find pages, API routes, middleware
3. Read `lib/` → Find database client, external API wrappers
4. Read `docker-compose.yml` → Find PostgreSQL, Redis
5. Map: Pages → API Routes → Business Logic → Database/Cache/External APIs
6. Generate a layer diagram or pipeline diagram

**Example prompt**: "帮我画一下这个 Go 服务的请求处理流程"

**Agent should**:
1. Find the main entry point (`cmd/` or `main.go`)
2. Trace the HTTP handler chain: Router → Middleware → Handler → Service → Repository → DB
3. Identify any async paths (goroutines, channels, message queues)
4. Generate a flowchart or sequence diagram showing the request lifecycle

---

## Process

### Description Mode (user provides text description)
1. **Read references**: Load the most relevant `references/example-*.svg` file
2. **Analyze**: Identify components, connections, groupings, and flow direction
3. **Choose type**: Match to one of the 5 diagram types
4. **Plan layout**: Mental grid — assign X/Y positions, determine canvas size
5. **Assign colors**: Blue=core, Red=special, Green=output, White=neutral, Tags=badges
6. **Choose font strategy**: CDN (default) or base64 (if user needs offline)
7. **Generate SVG**: Write clean, well-commented SVG following the design system exactly

### Code-Reading Mode (user points to code)
1. **Read references**: Load the most relevant `references/example-*.svg` file
2. **Scan**: Read project structure, configs, and key source files
3. **Classify**: Determine architecture pattern and best diagram type
4. **Extract**: Identify components and connections from code
5. **Abstract**: Reduce to 8–15 nodes max, group where needed
6. **Map colors**: Apply semantic color mapping
7. **Plan layout**: Arrange nodes logically based on data/control flow
8. **Generate SVG**: Output following the design system exactly
8. **Verify**: Run through the quality checklist below
9. **Output**: Save as `.svg` (and optionally `.html` for preview)

## Platform Safety Compatibility

Some AI coding platforms have aggressive content security filters that block certain Chinese keywords in generated code — even purely technical terms. This causes repeated generation failures. **Follow these rules strictly to avoid wasted retries.**

### Rule 1: SVG/HTML comments — English ONLY

All XML/HTML comments must use English. Never write Chinese in comments.
- ❌ `<!-- 红色：异常处理节点 -->`
- ❌ `<!-- 校验失败分支 -->`
- ✅ `<!-- Red/Warm node: error-handling path -->`
- ✅ `<!-- Validation branch -->`

### Rule 2: Sensitive Chinese words — Use English equivalents in ALL generated code

These words are known to trigger platform filters. **Always use the English alternative**, even in visible SVG node text and annotations:

| ❌ Blocked Chinese | ✅ Use Instead |
|-------------------|---------------|
| 异常 | Error / Exception |
| 错误 | Error |
| 失败 | Fail / Failed |
| 校验 | Validate / Check |
| 处理路径 | Path / Flow |
| 崩溃 | Crash |
| 死锁 | Deadlock |
| 攻击 | Attack |
| 入侵 | Intrusion |
| 漏洞 | Vulnerability |
| 拒绝 | Reject / Deny |
| 告警 | Alert |
| 熔断 | Circuit Break |
| 降级 | Fallback / Degrade |
| 超时 | Timeout |
| 重试 | Retry |

### Rule 3: Node visible text — Prefer Chinese for readability, but swap blocked words

For node titles and labels that users see, keep Chinese for readability but replace any blocked term:
- "参数校验" → "参数检查" or "Param Check"
- "异常处理" → "边界处理" or "Error Handling"  
- "失败重试" → "重新尝试" or "Retry"
- "请求失败" → "请求未成功" or "Request Failed"

**When in doubt, use English.** English technical terms almost never trigger filters.

### Rule 4: Color descriptions in comments — Use hex codes only

- ❌ `<!-- 红色节点 -->`
- ✅ `<!-- #f0d5c6 node -->`

## Quality Checklist

Before outputting, verify ALL of the following:

- [ ] Anthropic Sans font-face declaration included (CDN or base64)
- [ ] Fallback font stack present
- [ ] Background is `#f0efed` with `rx="22"`
- [ ] Only using the 5 defined color groups — no extra colors
- [ ] Arrow markers use open chevron (not filled triangle)
- [ ] Group containers use dashed border, transparent fill
- [ ] Text properly centered in all nodes (use `text-anchor="middle"`)
- [ ] Minimum 30px spacing between nodes
- [ ] Minimum 48px padding from canvas edges
- [ ] No clipping or overlapping elements
- [ ] Canvas size appropriate for content (not too cramped, not too empty)
- [ ] SVG is valid XML with proper xmlns declaration
- [ ] Comments mark major sections for readability
