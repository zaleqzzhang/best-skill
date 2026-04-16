---
name: awesome-design-md
description: |
  Access 62+ curated DESIGN.md files from real-world websites (Claude, Notion, Linear, Stripe, Apple, Vercel, Figma, Spotify, Tesla, Nike, etc.) and use them to generate pixel-perfect UI that matches the visual style of these sites.
  
  Use this skill whenever the user wants to:
  - Build a UI in the style of a specific brand or website (e.g. "make it look like Notion", "use Linear's design style", "build something that feels like Stripe")
  - Browse available design styles and pick one
  - Apply a specific visual language, color palette, or typography system to a new page or component
  - Describe a design direction and find a matching DESIGN.md (e.g. "minimal dark terminal style", "warm editorial layout", "fintech precision")
  - Generate consistent UI by telling the AI to follow a DESIGN.md spec
  
  Trigger keywords: design style, UI style, looks like, design system, visual style, DESIGN.md, styled like, build me a page that looks like, design inspiration, color palette of, typography like, brand aesthetic
---

# Awesome DESIGN.md

A curated collection of 62+ DESIGN.md files extracted from real-world websites. Each file is a plain-text design system document that defines color palettes, typography, components, spacing, and layout principles — ready for AI agents to read and generate consistent UI.

## What is DESIGN.md?

DESIGN.md is a concept from Google Stitch: a plain markdown file that defines how a UI should look. Drop it in your project and any AI coding agent instantly understands the visual system — colors, fonts, components, spacing, and design philosophy.

**Source**: [github.com/VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)  
**API**: `https://getdesign.md/design-md/{slug}/DESIGN.md` (no auth required)

---

## How to Use This Skill

### Step 1: Identify the desired style

When the user mentions a style or brand, map it to a slug from the catalog below. If the user describes a vibe (e.g., "dark terminal aesthetic"), suggest the best match.

### Step 2: Fetch the DESIGN.md

Use the terminal to fetch the raw DESIGN.md content:

```bash
curl -sL "https://getdesign.md/design-md/{SLUG}/DESIGN.md"
```

Example:
```bash
curl -sL "https://getdesign.md/design-md/linear.app/DESIGN.md"
```

### Step 3: Read and apply it

Once fetched, read the DESIGN.md carefully. It contains:
1. **Visual Theme & Atmosphere** — the overall mood and design philosophy
2. **Color Palette & Roles** — exact hex values for every semantic color
3. **Typography Rules** — font families, size scale, weight, line-height
4. **Component Stylings** — buttons, cards, inputs, navigation with states
5. **Layout Principles** — spacing, grid, whitespace philosophy
6. **Depth & Elevation** — shadow system, surface hierarchy
7. **Do's and Don'ts** — guardrails and anti-patterns
8. **Responsive Behavior** — breakpoints and mobile strategy
9. **Agent Prompt Guide** — quick-start prompts and color reference

Then generate the UI by strictly following the design spec.

### Step 4: Tell the user

Let the user know which style was applied, including a brief summary of the key visual characteristics (e.g., "Applied Linear's design: ultra-minimal dark theme, Inter font, purple #5E6AD2 accent, tight spacing").

---

## Full Design Catalog

Read `references/catalog.md` for the complete catalog with slugs, categories, and style descriptions.

### Quick Reference by Category

| Category | Designs Available |
|----------|------------------|
| AI & LLM | Claude, Cohere, ElevenLabs, Minimax, Mistral AI, Ollama, OpenCode AI, Replicate, RunwayML, Together AI, VoltAgent, xAI |
| Dev Tools | Cursor, Expo, Lovable, Raycast, Superhuman, Vercel, Warp |
| Backend/DB | ClickHouse, Composio, HashiCorp, MongoDB, PostHog, Sanity, Sentry, Supabase |
| Productivity | Cal.com, Intercom, Linear, Mintlify, Notion, Resend, Zapier |
| Design Tools | Airtable, Clay, Figma, Framer, Miro, Webflow |
| Fintech | Binance, Coinbase, Kraken, Revolut, Stripe, Wise |
| E-commerce | Airbnb, Meta, Nike, Shopify |
| Media/Tech | Apple, IBM, NVIDIA, Pinterest, SpaceX, Spotify, Uber |
| Automotive | BMW, Ferrari, Lamborghini, Renault, Tesla |

---

## Style Vibe → Recommended DESIGN.md

When the user describes a feeling rather than a brand, use this mapping:

| Vibe Description | Best Match | Slug |
|-----------------|-----------|------|
| Warm, editorial, intellectual | Claude / Notion | `claude` / `notion` |
| Ultra-minimal, precise, dark | Linear / Vercel | `linear.app` / `vercel` |
| Dark terminal, hacker aesthetic | Ollama / Warp / VoltAgent | `ollama` / `warp` / `voltagent` |
| Premium dark, cinematic | Tesla / SpaceX / Shopify | `tesla` / `spacex` / `shopify` |
| Clean developer docs | Mintlify / Supabase / MongoDB | `mintlify` / `supabase` / `mongodb` |
| Fintech precision | Stripe / Revolut / Kraken | `stripe` / `revolut` / `kraken` |
| Bold, energetic, sports | Nike / Spotify | `nike` / `spotify` |
| Apple-style premium white | Apple | `apple` |
| Playful, colorful, SaaS | Figma / Lovable / PostHog | `figma` / `lovable` / `posthog` |
| Luxury automotive | Ferrari / Lamborghini / BMW | `ferrari` / `lamborghini` / `bmw` |
| Green tech startup | Supabase / Wise / Mintlify | `supabase` / `wise` / `mintlify` |
| Orange/warm SaaS | Zapier / Airbnb | `zapier` / `airbnb` |
| Data-rich analytics | Sentry / PostHog / ClickHouse | `sentry` / `posthog` / `clickhouse` |

---

## Workflow Examples

### User says: "Build me a dashboard that looks like Linear"
1. Fetch: `curl -sL "https://getdesign.md/design-md/linear.app/DESIGN.md"`
2. Read the full spec — Linear uses: dark surface `#16161a`, purple accent `#5E6AD2`, Inter font, ultra-minimal components
3. Generate the HTML/CSS following Linear's exact design tokens
4. Tell user: "Applied Linear's design system — ultra-minimal dark UI, purple accent, Inter font"

### User says: "I want a Notion-style layout"
1. Fetch: `curl -sL "https://getdesign.md/design-md/notion/DESIGN.md"`
2. Apply warm minimalism, serif headings, soft surfaces as defined in the spec
3. Generate the component

### User says: "Show me all available dark styles"
- Suggest: Linear, Vercel, Tesla, SpaceX, Shopify, Ollama, Warp, VoltAgent, Cursor, Raycast, Revolut, Kraken, Superhuman, Sentry, Spotify, BMW, Ferrari, Lamborghini

---

## Important Notes

- **Custom fonts**: Many DESIGN.md files reference proprietary typefaces (Anthropic Serif, SF Pro, etc.). Always include system/Google Font fallbacks when implementing.
- **Not official**: These are curated design system approximations, not official brand guidelines.
- **Preview available**: Each design has a preview at `https://getdesign.md/{slug}/design-md`
- **62 designs total**: If a slug doesn't work, check `references/catalog.md` for the exact slug.
