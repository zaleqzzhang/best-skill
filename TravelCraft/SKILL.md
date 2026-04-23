---
name: TravelCraft
version: 2.3.0
description: 行迹 · TravelCraft —— 从一句模糊的出行念头，到一份可以直接转发朋友圈的精美行程。v2.0 起支持云端部署（EdgeOne Pages + Vercel 双引擎）、AES 密码保护和宋式美学旅行书架；v2.1 文档全面升级为「产品说明 + 使用手册」一体化指南；v2.2 集成腾讯位置服务，真实路线校准时长 + 嵌入可交互地图 + 一键导航；v2.3 新增 GitHub Pages 部署引擎（国内访问稳定、免备案、免费）。This skill should be used when a user wants to plan a trip from a rough idea (destination hints, travel party, dates, theme) into a complete, polished itinerary.
---

# 行迹 · TravelCraft  (v2.3.0)

## Overview

Plan a complete trip end-to-end from fuzzy user intent to polished deliverables. The skill converts rough inputs ("带父母去河南看石窟"/"五一三人自驾西北") into a day-by-day itinerary with attractions, food, costs, and travel logistics, then outputs three artifacts: an interactive HTML page, a long-image JPG, and a mobile-friendly PDF.

## Workflow Decision Tree

Execute the phases in order. Do not skip phases; each phase's output feeds the next.

1. **Phase 1 — Clarify** ambiguous requirements through targeted questions.
2. **Phase 2 — Research** destinations, attractions, food, and logistics.
3. **Phase 3 — Compose** day-by-day itinerary with timelines, budget, and photos.
4. **Phase 3.5 — Map Calibration (Optional, v2.2+)** geocode places and call Tencent Location Service driving API to validate distances and durations against Phase 3 estimates. If deviation > 20%, ask user to confirm/adjust the plan.
5. **Phase 4 — Build** the interactive HTML page from the template (v2.2+: embeds interactive map + per-day navigation buttons).
6. **Phase 5 — Export** long JPG + mobile PDF using headless Chrome + PIL.
7. **Phase 6 — Deploy (Optional, v2.0+)** publish to EdgeOne Pages / Vercel / both, with optional password protection and automatic "travel bookshelf" index page update.

Before starting Phase 4, present the composed plan to the user in plain text and let them confirm or request adjustments. Only enter the build phase when the plan is accepted.

Always offer Phase 3.5 map calibration when the itinerary involves driving between multiple cities. For pure in-city walking itineraries, Phase 3.5 is usually unnecessary.

After Phase 5, always offer Phase 6 cloud deployment.

## Phase 1 — Clarify Requirements

Do not start planning with unclear inputs. When the user's request is fuzzy, ask 3–5 targeted questions in a single turn. Read `references/requirement-clarification.md` for the question inventory.

Required dimensions to lock down before research:

- **Who**: Solo / couple / family (include age/mobility constraints — seniors, kids, elderly parents).
- **When**: Specific dates or season + length (days/nights). Note holidays (五一/十一/春节) — they impact crowd, price, availability.
- **Where**: A rough region is acceptable; the skill will propose 2–4 candidate routes if the destination is not fixed.
- **Theme**: Culture / nature / food / city-walk / parent-child / photography / deep-dive, etc.
- **Transport**: Flight+高铁+自驾 combination; whether to rent a car; start/end city (may differ).
- **Budget**: Total or per-person ceiling; accommodation tier preference.
- **Constraints**: Dietary restrictions, must-see/must-skip, fitness level, pace preference (紧凑/宽松).

If the user refuses to specify or says "你决定", make reasonable defaults, state them explicitly, and proceed.

## Phase 2 — Research

Use `references/research-methods.md` for the complete playbook. Key sources in priority order:

1. **小红书（RedNote）** — primary source for attraction tips, avoid-the-pit guides, food recommendations, and real-world photos. Load the `小红书` skill to use its search and post-detail scripts.
2. **Web search** — for opening hours, ticket prices, booking requirements, driving distance, travel time.
3. **Maps / user-known facts** — for route feasibility and driving estimates.

For each major attraction collect:

- Official hours / ticket / reservation requirements (especially reservation windows like 殷墟博物馆提前7天).
- Pro tips from high-like posts (early arrival, best route inside, specific halls/exhibits, hidden gems).
- 2–4 real photos with authorship context — download image URLs from post details. Prefer images showing the environment and scale, not text-overlaid covers.
- Avoid-the-pit warnings (closed Mondays, summer queues, paid guides).

For each city/region collect the **local food shortlist** (4–6 dishes) with at least one high-like blogger recommending each.

Cache important findings in a scratchpad; do not re-query the same post twice.

## Phase 3 — Compose the Plan

Use `references/itinerary-composition.md` for structure and pacing rules.

Per-day composition pattern:

- **Header**: Day N · Date · Route (A→B→C) · Primary color token.
- **今日看点 (Summary)**: 2–3 sentences answering 什么值得看/吃/逛.
- **小红书推荐**: Quote 1–2 bloggers with like-count and key tips.
- **Timeline**: 6–10 entries with time windows, title, one-line desc, tag (drive/museum/food/highlight/free/heritage).
- **Photos**: Embed 1–4 real photos per major attraction inside the timeline entry (not a separate gallery).

Budgeting dimensions (see `references/budget-template.md`):

- Transport (flight/train/car rental + fuel + tolls).
- Tickets (apply senior/student discounts per person — track each traveler's price).
- Accommodation (do NOT display nightly rate inside day itinerary; only in dedicated budget section).
- Food (per-day average × days + special meals like birthday dinner).
- Total + per-person; note which items are padding-able.

After composing, present a concise text summary to the user. Ask: "这个方案可以吗？有什么需要调整的？" Proceed to Phase 3.5 (if multi-city driving) or directly to Phase 4 only on approval.

## Phase 3.5 — Map Calibration (Optional, v2.2+)

Only run when the itinerary involves driving between multiple cities (i.e., has inter-city `drive` segments). Skip for pure in-city walks.

Read `references/map-integration-guide.md` for the full pipeline. Core steps:

### Step 3.5.1 — Prerequisites

Check `~/.codebuddy/skills/TravelCraft/data/.env` for `TMAP_KEY`. If missing, guide user:

1. Visit https://lbs.qq.com/dev/console/key/add
2. Enable **WebService API** + **JavaScript API GL**, leave 域名白名单 empty
3. Visit https://lbs.qq.com/dev/console/quota/manage and allocate quota to geocoder + direction/driving
4. Save key to `data/.env` as `TMAP_KEY=...`

### Step 3.5.2 — Extract and geocode places

From the Phase 3 itinerary, compile a `places.txt` listing every attraction + hotel + station with its city. Run:

```
python3 scripts/geocode_places.py \\
    --key $TMAP_KEY --input places.txt --output places.json
```

Discard entries with `reliability < 7` and re-geocode with more specific address.

### Step 3.5.3 — Build route segments

Compose `route.json` with one segment per driving leg:

```json
{
  "segments": [
    {
      "day": 1, "name": "北京 → 邯郸",
      "from": {"name": "...", "lng": ..., "lat": ...},
      "to":   {"name": "...", "lng": ..., "lat": ...},
      "waypoints": [],
      "estimated_hours": 5.0
    }
  ]
}
```

### Step 3.5.4 — Calibrate

```
python3 scripts/calibrate_route.py \\
    --key $TMAP_KEY --input route.json --output calibrated.json
```

Inspect the output: segments with `deviation_percent` > 20% need attention. Present them to the user:

> "腾讯地图实测发现两段时间偏差较大：
>    Day 2 邯郸→安阳 原估 2h，实测 2.8h（⚠️ +40%）
>    Day 4 登封→巩义 原估 1h，实测 0.7h（⚠️ -30%）
> 是否按实测重新调整当天节奏？"

If user agrees, update Phase 3 itinerary accordingly (cut one attraction or shift timing), then re-run calibration to confirm.

### Step 3.5.5 — Ready for Phase 4

`calibrated.json` will be consumed by Phase 4 to embed the map. No user action needed here.

## Phase 4 — Build Interactive HTML

Copy `assets/template/example-itinerary.html` as the starting HTML for the new trip, then edit content top-down (see `assets/template/README.md` for the editing order). The template already contains:

- Complete CSS using **宋式美学** palette (月白/墨灰 + accent 赭/靛/竹/紫).
- Responsive layout with top tabs + mobile bottom nav.
- 7 day-section slots (overview + day1–6 + budget), placeholders marked with `{{ }}`.
- Timeline, photo grid, summary card, XHS card, warn block, table components.
- Traditional pattern decorations (云雷纹 hero BG, 回字纹 summary corner, 丝绸暗纹 timeline card).
- Lightbox JS for photo zoom; tab/nav click handlers with `currentTarget`.

Read `references/html-template-guide.md` for the placeholder system and how to extend with more days.

Critical rules for photos inside the HTML:

- All paired photos (`.tl-photos`) must be pre-cropped to **4:3 ratio** — use `scripts/normalize_photos.py`.
- Standalone photos (`.tl-photo` not inside `.tl-photos`) keep original aspect ratio.
- Never leave empty `<img>` tags; if no real photo exists, omit the photo container entirely — the pattern background of `.tl-photo` shows through only when an image is present.
- Caption text goes in `<div class="pc">`.

Apply `references/design-principles.md` whenever tempted to deviate from the template — the styling has been carefully tuned through multiple rounds of user feedback (see that doc for the "what NOT to do" list).

### Step 4.5 — Inject map (v2.2+)

If Phase 3.5 ran and produced `calibrated.json`, inject the interactive map:

```
python3 scripts/inject_tmap.py \\
    --html <slug>.html \\
    --route calibrated.json \\
    --key $TMAP_KEY \\
    --output <slug>.html
```

This appends at the top of `<body>`:

- 路线总览 heading (宋式美学 styling consistent with rest of page)
- Embedded TMap container (480px tall, responsive to 360px on mobile)
- Per-day route summary cards with real distance/duration + deviation flag
- Click any marker → opens info-window with 🚗 导航到此 button (launches Tencent Maps app via URI API)
- Per-day 一键导航 button → launches Tencent Maps routing

Verify: open the HTML in browser; confirm map loads without 401/key errors; confirm clicking a marker shows the navigation button.

## Phase 5 — Export Deliverables

Produce three files with consistent names (replace `<slug>` with the trip slug):

- `<slug>.html` — the interactive page.
- `<slug>.jpg` — long image for sharing.
- `<slug>.pdf` — mobile-friendly paginated PDF.

Run `scripts/export_itinerary.sh <html-file> <output-slug>` to produce all three. The script:

1. Generates an export-optimized HTML (all sections expanded, tabs/nav hidden, mobile-scale fonts, `@page 480x800`).
2. Starts a local HTTP server on a free port if none is running.
3. Uses Chrome headless `--screenshot` at `--force-device-scale-factor=2 --window-size=480,20000` for the long JPG.
4. Uses Chrome headless `--print-to-pdf` with the `@page` rule for the PDF.
5. Auto-crops the long screenshot to the content bottom via PIL (`scripts/crop_screenshot.py`).
6. Smart-paginates the long JPG into PDF at blank-row boundaries for small file size.

Verify output:

- JPG: width 960 (@2x of 480), height typically 15000–40000 depending on trip length; file size 1–4 MB.
- PDF: page size 360×600 or 480×800, 15–30 pages, file size 1–3 MB.
- Open all three and spot-check top/middle/bottom on mobile preview.

Clean up: delete the temporary `_itinerary-export.html`, `_full_shot_2x.png`, and any `_sample_*.jpg` files before finishing the task.

## Phase 6 — Deploy to Cloud (Optional, v2.0+)

After Phase 5 completes, ALWAYS offer cloud deployment. This lets the user share a URL + QR code so their family/travel companions can view the interactive itinerary on mobile during the trip itself.

Read `references/deployment-guide.md` for detailed engine comparison, first-time auth steps, and troubleshooting.

### Step 6.1 — Ask user preferences

Ask in a single turn:

> "本地文件已生成。要部署到云端吗？
>
>   1. 🇨🇳 EdgeOne Pages（国内手机 4G/5G 访问飞快，免费）
>   2. 🌏 Vercel（国际稳定，永久保存，免费）
>   3. 📡 双引擎部署（推荐 —— 总有一个能打开）
>   4. 不用了，仅本地文件
>
> 要加密码保护吗？（仅知道密码的人能看到内容）"

Defaults if user says "按推荐来":

- Engine: Option 3 (dual-engine)
- Password: ask whether to set, suggest a 4-6 char password if user defers

### Step 6.2 — First-time authentication

On first deploy, check `~/.codebuddy/skills/TravelCraft/data/.env` for tokens. If missing:

For EdgeOne Pages:
- Guide user: "请点击对话框下方 [集成] 按钮 → 选择 [EdgeOne Pages] → 连接腾讯云账号"
- Wait for user confirmation

For Vercel:
- Guide user: "请在终端运行：`npx vercel login`，用 GitHub 账号完成一次性授权"
- After success, Vercel CLI stores token at `~/.local/share/com.vercel.cli/auth.json` automatically

Save deployment preferences (engine choice, whether to reuse last config) to `data/preferences.json` for future runs.

### Step 6.3 — Client-side encryption (if password enabled)

Use `scripts/inject_password.py`:

1. Read the built `<slug>.html` content
2. AES-256 encrypt with user's password using PBKDF2 key derivation (10000 iterations)
3. Wrap in a gate template containing:
   - Password input form (宋式美学: 月白背景 + 赭石按钮)
   - CDN-loaded `crypto-js` for decryption
   - On correct password: decrypt → `document.documentElement.innerHTML = decrypted`
   - On wrong password: show "密码错误" with shake animation
4. Output protected file replaces original `<slug>.html`

Security note: content is encrypted at rest on CDN. Even viewing page source shows only ciphertext. This is genuinely secure for casual privacy (family-level), NOT for regulatory-grade secrets.

### Step 6.4 — Deploy

Run the appropriate script:

- EdgeOne only: `scripts/deploy_to_eop.sh <trip-dir> <slug>`
- Vercel only: `scripts/deploy_to_vercel.sh <trip-dir> <slug>`
- Both: `scripts/deploy_both.sh <trip-dir> <slug>`

Each script:
1. Validates the directory has an `index.html` or `<slug>.html`
2. Creates minimal platform config (`vercel.json` / EdgeOne project manifest)
3. Runs the CLI deploy command
4. Parses output to extract the deployed URL
5. Writes URL back to stdout for capture

### Step 6.5 — Generate QR codes

Run `scripts/generate_qrcode.py <url1> [<url2>] --output <qr-file.png>`:

- Single URL: 400×400 QR, brand colors (赭石 #B07B5F on 月白 #F5EFE6)
- Dual URL: side-by-side layout 800×500 with "🇨🇳 国内扫此码" / "🌏 海外扫此码" labels
- High error correction (Level H) so QR still works if partially covered

### Step 6.6 — Embed QR in long image

Run `scripts/embed_qr_in_longimage.py <long-jpg> <qr-png> <output-jpg>`:

- Appends a 800×600 share-block to the bottom of the long JPG
- Contains: top 云雷纹 border → QR code(s) → URL text → password hint (if set) → "行迹 · TravelCraft · <year>" footer
- Final filename: `<slug>-cloud.jpg` (keeps the non-cloud version intact)

### Step 6.7 — Update travel bookshelf index

Run `scripts/update_index.py`:

1. Append trip metadata to `data/trips.json`:
   ```json
   {
     "id": "<slug>",
     "title": "...",
     "date_range": "...",
     "days": N,
     "people": N,
     "theme": "...",
     "has_password": bool,
     "cover_image": "...",
     "urls": {"eop": "...", "vercel": "..."},
     "created_at": "<ISO>"
   }
   ```
2. Render `assets/index-template/index.html` via Jinja2 with all trips
3. Deploy the updated index to user's `my-travelcraft` project (separate from individual trip projects)
4. Return the bookshelf URL

### Step 6.8 — Final report to user

Return a structured summary:

```
✅ 部署完成！

🇨🇳 国内访问：<eop_url>
🌏 海外访问：<vercel_url>
🔒 密码：<password>    （如果设置了）

📚 你的旅行书架：<bookshelf_url>
   （共收录 N 份行程）

📱 二维码已嵌入：<slug>-cloud.jpg
📄 分享文件：<slug>-cloud.jpg / <slug>.pdf / 在线版
```

Call `open_result_view` on the `<slug>-cloud.jpg` (the cloud-enhanced long image) as the final deliverable.

## Reusable Resources

### scripts/

- `normalize_photos.py` — Batch-crop photos to a target ratio (default 4:3) for paired display. Preserves subjects by biasing crop toward upper portion for portrait-to-landscape conversion.
- `export_itinerary.sh` — Orchestrates HTML → JPG + PDF pipeline using Chrome headless.
- `crop_screenshot.py` — Trims trailing whitespace from a Chrome long screenshot and produces both the JPG and a smart-paginated PDF.
- `start_preview.sh` — Starts a local HTTP server for previewing the built HTML in browser.
- `deploy_to_eop.sh` — (v2.0+) Deploy trip directory to EdgeOne Pages, returns URL.
- `deploy_to_vercel.sh` — (v2.0+) Deploy trip directory to Vercel, returns URL.
- `deploy_both.sh` — (v2.0+) Dual-engine deploy convenience wrapper.
- `generate_qrcode.py` — (v2.0+) Generate single or dual QR codes with brand styling.
- `inject_password.py` — (v2.0+) AES-256 encrypt an HTML file and wrap with password-gate page.
- `embed_qr_in_longimage.py` — (v2.0+) Append share-block with QR to the bottom of long JPG.
- `update_index.py` — (v2.0+) Update the local trips.json and render/deploy the "travel bookshelf" index page.
- `geocode_places.py` — (v2.2+) Batch geocode place names to lng/lat via Tencent WebService Geocoder API.
- `calibrate_route.py` — (v2.2+) Call Tencent Driving Direction API to validate distances/durations; output includes decoded polyline.
- `inject_tmap.py` — (v2.2+) Inject the interactive TMap GL component + per-day route summary + navigation buttons into the itinerary HTML.

### references/

- `requirement-clarification.md` — Question inventory for Phase 1.
- `research-methods.md` — 小红书 search strategy, image URL extraction, filtering by like-count.
- `itinerary-composition.md` — Daily structure, pacing, tag system, summary writing patterns.
- `budget-template.md` — Budget structure with discount rules for seniors/children.
- `html-template-guide.md` — Placeholder map, how to add/remove days, color token assignments.
- `design-principles.md` — 宋式美学 tokens, visual hierarchy, what NOT to do (accumulated user feedback).
- `deployment-guide.md` — (v2.0+) Engine comparison (EOP vs Vercel), first-time auth flow, password mechanism, troubleshooting.
- `map-integration-guide.md` — (v2.2+) Tencent Location Service setup, API quotas, geocoder + routing + URI API usage, troubleshooting.

### assets/

- `template/example-itinerary.html` — Complete reference implementation (6-day cultural trip). Copy this as starting HTML; edit top-down.
- `template/README.md` — Step-by-step editing guide + what NOT to change.
- `index-template/index.html` — (v2.0+) "Travel bookshelf" index page template (Jinja2).
- `index-template/trip-card.html` — (v2.0+) Individual trip card partial for the index page.

### data/  (user-local, not shipped in zip)

- `.env` — Deployment tokens (auto-generated after first authentication).
- `trips.json` — Metadata of all trips deployed by this user, drives the bookshelf index.
- `preferences.json` — User's default engine choice and password preferences.

## Quick Checklist Before Finishing

- [ ] All Phase 1 dimensions are explicitly resolved (no `TBD` left silently).
- [ ] Every major attraction has ≥1 real photo inside its timeline entry.
- [ ] Every day has a Summary + 小红书推荐 + Timeline block.
- [ ] Budget totals are consistent; senior/child discounts applied.
- [ ] HTML renders on 375px-wide viewport without horizontal scroll.
- [ ] JPG and PDF content ends with the intended last block (no cut-off).
- [ ] Temporary files (`_*.html`, `_*.png`) are removed.
- [ ] If Phase 6 ran: URLs captured, QR embedded, bookshelf updated, password confirmed working.
- [ ] Result is presented to the user via `open_result_view` on the JPG (cloud version if deployed, otherwise local version).
