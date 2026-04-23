# Research Methods

Phase 2 playbook. Spend ~60% of planning time here — quality of research directly determines itinerary quality.

## Source Priority

1. **小红书（RedNote）** — ground-truth current travel experience, photos, pit-avoidance tips, food recs.
2. **Web search** — hours, prices, reservations, distances, holiday-specific news.
3. **User knowledge + general reasoning** — route geometry, cross-city travel time.

Do NOT rely on model-internal knowledge for: opening hours, ticket prices, reservation policies, food shop addresses. These change frequently.

## Using the 小红书 Skill

Check if the 小红书 skill is available. If yes, load it with `use_skill 小红书`. If not available, fall back to web search with `site:xiaohongshu.com`.

### Core scripts (after skill load)

Located at `~/.codebuddy/skills/小红书/scripts/`:

- `start-mcp.sh` — start the MCP service.
- `status.sh` — check service + login status.
- `search.sh "<query>"` — return JSON of search results (id, title, likes, xsecToken, cover image).
- `post-detail.sh <note_id> <xsec_token>` — return full post detail including imageList, content, comments.

Run `status.sh` once at the start of Phase 2. If not logged in, tell the user to complete login and wait.

### Search strategy

For each attraction/city, run 2–3 targeted queries:

- `"<地名> 攻略"` — general overview.
- `"<地名> 避坑"` or `"<地名> 踩坑"` — warnings.
- `"<景点名> 路线"` — internal route.
- `"<城市> 美食 必吃"` — food list.
- `"<地名> 五一"` / `"<地名> 淡季"` — seasonal specifics.

### Filtering results

Sort search feeds by `likedCount` (extract with Python/jq). Rules of thumb:

- **>500 likes** — generally reliable, visit frequency high.
- **100–500 likes** — useful for niche tips.
- **<50 likes** — skip unless it's the only source for that spot.
- Reject posts whose title contains obvious 营销号 patterns: 「最全」「必看」「震惊」 without specifics.

### Extracting photo URLs

When a post has real photos worth showing in the HTML, get them via `post-detail.sh`:

```bash
bash post-detail.sh "<note_id>" "<xsec_token>" | \
  python3 -c "
import sys, json
d = json.loads(json.loads(sys.stdin.read())['result']['content'][0]['text'])
n = d['data']['note']
print('Title:', n['title'], '| Likes:', n['interactInfo']['likedCount'])
for i, img in enumerate(n.get('imageList', [])):
    print(f'img{i}: {img[\"urlDefault\"][:180]}')
"
```

Download with `curl -sL <url> -o photos/<filename>.jpg`. **Important**: 小红书 CDN URLs are time-signed; download immediately after extraction, do not cache URLs for later.

Prefer photos that show:
- Environment and scale (landscape context).
- Specific artifact or detail mentioned in the itinerary.
- Multi-panel comparisons (e.g. historical vs current).

Avoid photos that:
- Are pure text overlays / cover templates.
- Show the blogger's face as the main subject.
- Have heavy watermarks obstructing the scene.

## Web Search Queries

Use `web_search` tool for verified facts:

- `"<景点名> 开放时间 门票 2026"` — get current year; model cutoff often stale.
- `"<景点名> 预约"` — find reservation rules (window, platform).
- `"<A地> 到 <B地> 开车 多久"` — for driving estimate.
- `"<景点> 周一 闭馆"` — check closure day.

For Chinese attractions, official `*.gov.cn` or the 景区官网 + 公众号 are most reliable; 携程/马蜂窝 are good secondary.

## Research Output Format

Maintain a working scratchpad for each attraction:

```
### 殷墟博物馆（新馆）
- 时间: 08:30–17:30，周一闭馆
- 票: 免费，需提前7天预约
- 亮点: 妇好墓随葬品、甲骨文厅、车马坑
- 博主推荐: @殷墟课代表(144赞) — 8:30第一批进；二楼车马坑最震撼
- 避坑: 下午14点后人多、预约分时段
- 预留: 2.5小时
- 照片: photos/yinxu_museum.jpg, photos/xhs_yinxu_museum.jpg
```

This scratchpad is the single source of truth fed into Phase 3.

## Food Research

For each city produce a **shortlist of 4–6 dishes**, each with:

- Dish name (local term — e.g. 扁粉菜, 郭八火烧).
- 1 recommended shop if blogger specifies.
- One-line description.
- Blogger attribution when useful (e.g. `@凌晨四点半 818赞 推荐...`).

Do not over-stack food options — 4–6 per city is enough; more becomes overwhelming.

## Crowd & Season Considerations

For each attraction note:

- **Best time of day**: e.g. 少林寺五一必须10点前到塔林.
- **Best time of year**: 永熙陵5月麦田+石像生最美；洛阳牡丹4月底5月初.
- **Closure days**: 大多博物馆周一闭馆 — reshuffle itinerary accordingly.
- **Holiday multiplier**: 国庆/五一期间人流×5–10，酒店价格×2–3.
