# Requirement Clarification — Question Inventory

Use this playbook during Phase 1 to convert a fuzzy travel request into a concrete brief.

## Triage First

Before asking anything, parse the user's message for already-provided info. Do NOT re-ask what is already stated. Classify missing dimensions and ask only for the gaps.

## The 7 Dimensions

Cover all 7 during Phase 1. Bundle 3–5 into a single turn using the `ask_followup_question` tool (or plain text if only one item is unclear).

### 1. WHO (travel party)

- Solo / couple / friends / family / group size?
- Ages — especially **seniors (60+)** and **children (<12)**. These change pacing, meal choices, lodging needs, and ticket discounts drastically.
- Mobility/health constraints (stairs, long walks, altitude).

### 2. WHEN (timing)

- Exact dates OR month + length (e.g. "5月 4天3晚")?
- Holiday overlap? **国庆/春节/五一** require: early booking, crowd-avoidance strategy, 7–30 day advance reservations for popular attractions.
- Arrival/departure flexibility (morning vs evening trains)?

### 3. WHERE (destination granularity)

Three possible states:

- **Locked** — user names exact cities (e.g. "成都+九寨沟"). Skip to research.
- **Rough region** — user names a province/theme (e.g. "河南文化游"/"江南"). Propose 2–4 candidate routes; let user pick.
- **Open** — user has a vibe only (e.g. "5月适合去哪"). Propose 3 regions based on season/budget/party, ask for pick.

### 4. THEME (what to optimize for)

- Culture/history/museums
- Nature/hiking/scenic
- Food
- City walk / shopping
- Photography
- Parent-child / education
- Leisure / resort
- Mixed — ask for weighting

### 5. TRANSPORT

- Starting city for each traveler (may differ — common for 回家团聚场景).
- Preferred long-haul: flight / 高铁 / 卧铺 / 自驾?
- Rent a car on-destination? If so, who is the driver, what age/license constraints?
- Any loops required (start city = end city)?

### 6. BUDGET

- Total budget OR per-person per-day ceiling.
- Hotel tier: economy (200-400) / comfort (400-800) / boutique (800+) / luxury?
- Willingness to splurge on one special meal/experience?

### 7. CONSTRAINTS

- Diet: vegetarian / halal / allergies / 不吃辣 / 忌口?
- Must-see or must-skip list.
- Pace preference: 紧凑 (6–8 spots/day) / 舒适 (3–5) / 宽松 (1–2 + leisure).
- Accommodation preferences: city center vs scenic / chain vs boutique.

## Default Assumptions When User Won't Decide

If the user says "你决定" or refuses a question, adopt these defaults and state them clearly:

| Dimension | Default |
|-----------|---------|
| Pace | 舒适（3–5 景点/天）|
| Hotel | 连锁舒适型（¥400/晚级别） |
| Meals | 当地特色馆子为主，避开景区内餐 |
| Transport | 跨城高铁，城内打车+步行；长距离多点串联用自驾 |
| Must-avoid | Pure tourist traps, overpriced "必游" cards |
| Senior consideration | 若存在60+, 避免爬升>300m、单日步行>10km、晚上超过21:00 |

## Phrasing Patterns

Good question (concrete + multi-choice):

> 你们几位出行？特别想确认是否有60+的长辈或12岁以下孩子，这会影响节奏和门票减免。

Avoid (open-ended + vague):

> 你们是谁？

Good follow-up after rough destination:

> 河南文化线我建议三条候选，选一个：
> A. 石窟建筑线（洛阳+登封+巩义+安阳，重古迹）
> B. 古都博物馆线（郑州+开封+洛阳，重馆藏）
> C. 大宋生活线（开封+洛阳+巩义宋陵，重沉浸）

## When to Stop Asking

Stop when all 7 dimensions have either an explicit answer or a stated default. Additional questions cost user patience — do not ask for preferences that won't materially change the itinerary.
