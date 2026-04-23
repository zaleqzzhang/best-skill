# Template Assets

## Files

- `example-itinerary.html` — **complete reference implementation** of a 6-day trip (河南文化自驾行程). This is the canonical template: all CSS, all components, all patterns, all JS. Copy it as the starting point for new trips.

## How to Use

### Step 1: Copy the example as the starting HTML for the new trip

```bash
cp "$SKILL_DIR/assets/template/example-itinerary.html" \
   "$PROJECT_DIR/<trip-slug>.html"
```

### Step 2: Replace content top-down

Edit the file in this order to minimize re-reading:

1. `<title>` → new trip title.
2. `.hero h1` / `.sub` / `.badges` → new headline.
3. Overview section — route table, reminders, train/flight info, route map image path.
4. Tab labels (`<div class="tabs-wrap">`) — change tab text to match new trip days.
5. Bottom nav (`<nav class="bottom-nav">`) — change `.bi` labels accordingly.
6. For each day section (`day1`–`day6`):
   - Update `.day-header-text h2` / `.date` / `.route`.
   - Rewrite `.summary` copy.
   - Rewrite `.xhs` blogger quotes.
   - Rewrite timeline entries.
   - Update photo paths (`photos/*.jpg`).
7. Budget section — update all numbers and line items.

### Step 3: Adapt the day count

If trip has fewer days (e.g. 3-day trip):
- Delete `day4`, `day5`, `day6` day-sections.
- Delete corresponding `.tab` and `.bi` elements.

If more days (e.g. 7-day trip):
- Duplicate the `day6` block, rename id/data-day to `day7`.
- Add matching tab + bi entries.
- Pick a 7th color token (add CSS variable if needed).

### Step 4: Color token reassignment (optional)

If your trip's theme suggests different per-day colors, edit the `:root` CSS variables `--d1` through `--d6`. The summary background tints (`.bg-d1` etc.) are separately defined — update those together.

## What NOT to change

These design decisions are locked; see `references/design-principles.md` for rationale:

- ❌ Do not remove the `云雷纹` / `回字纹` / `丝绸暗纹` SVG patterns.
- ❌ Do not swap `Noto Serif SC` for another font family.
- ❌ Do not add Leaflet or interactive maps — use static `photos/route_map.png`.
- ❌ Do not add hotel prices inline in day sections.
- ❌ Do not use `object-fit:cover` on standalone `.tl-photo` (only on `.tl-photos` paired).
- ❌ Do not add new background color tiers beyond the 5 already defined.

## Photos

Place all photos under `<project>/photos/`. Required before HTML build:

- Run `scripts/normalize_photos.py ./photos` to crop paired photos to 4:3.
- Standalone photos keep original ratio (e.g. a tall pagoda photo).
- Captions (`.pc`) should be 4–10 Chinese chars, factual.
