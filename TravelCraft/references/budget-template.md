# Budget Template

Standard cost structure used in Phase 3 budget section.

## Categories

Track costs in this fixed order so totals roll up consistently.

### 1. 交通 (Transport)

- 跨城：高铁 / 飞机 / 卧铺
- 内部：自驾（含油费+过路费） / 打车 / 公交
- 列为 per-person line items; sum to category total.

### 2. 租车 (Car rental) — separate line if 自驾

- 车型 + 天数 = 总租金
- 油费估算：`总里程 ÷ 100 × 每百公里油耗 × 油价`. Typical small SUV: 8L/100km × ¥8/L.
- 过路费估算：高速里程 × ¥0.5/km (adjust for actual).
- 异地还车费 if applicable.

### 3. 门票 (Tickets)

Produce a per-person table. Columns: `景点 | 成员1 | 成员2 | 成员3 | 小计`.

Apply discount rules per traveler (see `itinerary-composition.md` for rules).

### 4. 住宿 (Accommodation)

- List each hotel: `城市 · 品牌 · 房间数 × 晚数 = 单价 × 数量`.
- Do NOT display nightly cost inside individual day timeline entries — only in this section.

### 5. 餐饮 (Food)

- Simpler: use `日均 ¥X × N天 + 特餐` pattern.
- Daily food average guidelines:
  - 三线/小城: ¥80–120/人/天
  - 二线: ¥120–200/人/天
  - 一线/景区: ¥180–300/人/天
- Special meals (birthday dinner, 米其林 etc.) as separate line with estimate.

### 6. 杂项 / 备用金

- 停车费、小额门票、纪念品。
- Recommended: **5% of total** as buffer.

## Output Format

At top level:

```
合计 ¥X,XXX · 人均 ¥Y,YYY
控制餐饮可至 ~¥Z,ZZZ
```

Include in a highlighted card (see template's `.total-card`).

Separately note which line items are **padding-able** (can shrink if budget-tight) and which are **fixed** (transport booked, tickets required).

## Discount Cheatsheet

Apply these automatically when member ages are known:

| Category | Free | Half |
|----------|------|------|
| 国保/省保景区 | 70+, <6岁/<1.2m | 60–69 |
| 博物馆 | 大多数本来就免费 | — |
| 高铁 | <1.2m, 现役军人 | 1.2–1.5m |
| 飞机 | <2岁（占位） | — |
| 景区摆渡车 | 通常不打折 | — |

Always note: 需带身份证/老年证/学生证. 殷墟等仍需预约即便免票.

## Sample Output (Markdown form)

```markdown
## 费用明细

### 交通 ¥2,847
- 你 G1405 北京西→邯郸东: ¥312
- 父母 咸阳西→邯郸东（经西安北换乘）: ¥580 × 2 = ¥1,160
- 你+父母 巩义南→西安北: ¥198 × 3 = ¥594
- 你 咸阳→北京机票: ¥581
- 父母咸阳↔家打车: ¥400

### 租车 ¥2,590
- BMW 3系 × 5天: ¥2,000
- 油费 + 过路费（~650km）: ¥590

### 门票 ¥541
| 景点 | 你 | 母(60-69) | 父(70+) | 计 |
|------|----|----|----|----|
| 响堂山 | ¥80 | ¥15（半票+观光车） | 免 | ¥95 |
| 殷墟 | ¥80 | 免 | 免 | ¥80 |
| ... | | | | |

### 住宿 ¥3,142
- 邯郸亚朵 × 2间 × 1晚: ¥718
- 安阳亚朵 × 2间 × 1晚: ¥682
- 登封星程三人间 × 1晚: ¥342
- 巩义全季 × 2间 × 2晚: ¥1,400

### 餐饮 ~¥2,900
- 日均 ¥450 × 6 + 生日蛋糕 ¥200

### 合计 ¥10,712 · 人均 ¥3,571
控制餐饮可至 ~¥9,800
```
