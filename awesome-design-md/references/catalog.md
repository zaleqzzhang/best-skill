# Complete Design Catalog

All 62 DESIGN.md files from [awesome-design-md](https://github.com/VoltAgent/awesome-design-md).

**API Pattern**: `https://getdesign.md/design-md/{SLUG}/DESIGN.md`

---

## AI & LLM Platforms

| Name | Slug | Style Description |
|------|------|------------------|
| Claude (Anthropic) | `claude` | Warm parchment canvas (#f5f4ed), terracotta accent (#c96442), Anthropic Serif, editorial layout |
| Cohere | `cohere` | Enterprise AI, vibrant gradients, data-rich dashboard |
| ElevenLabs | `elevenlabs` | Dark cinematic UI, audio-waveform aesthetics |
| Minimax | `minimax` | Bold dark interface with neon accents |
| Mistral AI | `mistral.ai` | French-engineered minimalism, purple-toned |
| Ollama | `ollama` | Terminal-first, monochrome simplicity |
| OpenCode AI | `opencode.ai` | Developer-centric dark theme |
| Replicate | `replicate` | Clean white canvas, code-forward |
| RunwayML | `runwayml` | Cinematic dark UI, media-rich layout |
| Together AI | `together.ai` | Technical, blueprint-style design |
| VoltAgent | `voltagent` | Void-black canvas, emerald accent, terminal-native |
| xAI | `x.ai` | Stark monochrome, futuristic minimalism |

---

## Developer Tools & IDEs

| Name | Slug | Style Description |
|------|------|------------------|
| Cursor | `cursor` | Sleek dark interface, gradient accents |
| Expo | `expo` | Dark theme, tight letter-spacing, code-centric |
| Lovable | `lovable` | Playful gradients, friendly dev aesthetic |
| Raycast | `raycast` | Sleek dark chrome, vibrant gradient accents |
| Superhuman | `superhuman` | Premium dark UI, keyboard-first, purple glow |
| Vercel | `vercel` | Black and white precision, Geist font |
| Warp | `warp` | Dark IDE-like interface, block-based command UI |

---

## Backend, Database & DevOps

| Name | Slug | Style Description |
|------|------|------------------|
| ClickHouse | `clickhouse` | Yellow-accented, technical documentation style |
| Composio | `composio` | Modern dark with colorful integration icons |
| HashiCorp | `hashicorp` | Enterprise-clean, black and white |
| MongoDB | `mongodb` | Green leaf branding, developer documentation focus |
| PostHog | `posthog` | Playful hedgehog branding, developer-friendly dark UI |
| Sanity | `sanity` | Red accent, content-first editorial layout |
| Sentry | `sentry` | Dark dashboard, data-dense, pink-purple accent |
| Supabase | `supabase` | Dark emerald theme, code-first |

---

## Productivity & SaaS

| Name | Slug | Style Description |
|------|------|------------------|
| Cal.com | `cal` | Clean neutral UI, developer-oriented simplicity |
| Intercom | `intercom` | Friendly blue palette, conversational UI patterns |
| Linear | `linear.app` | Ultra-minimal, precise, purple accent (#5E6AD2) |
| Mintlify | `mintlify` | Clean, green-accented, reading-optimized |
| Notion | `notion` | Warm minimalism, serif headings, soft surfaces |
| Resend | `resend` | Minimal dark theme, monospace accents |
| Zapier | `zapier` | Warm orange, friendly illustration-driven |

---

## Design & Creative Tools

| Name | Slug | Style Description |
|------|------|------------------|
| Airtable | `airtable` | Colorful, friendly, structured data aesthetic |
| Clay | `clay` | Organic shapes, soft gradients, art-directed layout |
| Figma | `figma` | Vibrant multi-color, playful yet professional |
| Framer | `framer` | Bold black and blue, motion-first, design-forward |
| Miro | `miro` | Bright yellow accent, infinite canvas aesthetic |
| Webflow | `webflow` | Blue-accented, polished marketing site aesthetic |

---

## Fintech & Crypto

| Name | Slug | Style Description |
|------|------|------------------|
| Binance | `binance` | Binance Yellow on monochrome, trading-floor urgency |
| Coinbase | `coinbase` | Clean blue identity, trust-focused, institutional feel |
| Kraken | `kraken` | Purple-accented dark UI, data-dense dashboards |
| Revolut | `revolut` | Sleek dark interface, gradient cards, fintech precision |
| Stripe | `stripe` | Signature purple gradients (#635bff), weight-300 elegance |
| Wise | `wise` | Bright green accent, friendly and clear |

---

## E-commerce & Retail

| Name | Slug | Style Description |
|------|------|------------------|
| Airbnb | `airbnb` | Warm coral accent, photography-driven, rounded UI |
| Meta | `meta` | Photography-first, binary light/dark, Meta Blue CTAs |
| Nike | `nike` | Monochrome UI, massive uppercase Futura, full-bleed photography |
| Shopify | `shopify` | Dark-first cinematic, neon green accent, ultra-light display type |

---

## Media & Consumer Tech

| Name | Slug | Style Description |
|------|------|------------------|
| Apple | `apple` | Premium white space, SF Pro, cinematic imagery |
| IBM | `ibm` | Carbon design system, structured blue palette |
| NVIDIA | `nvidia` | Green-black energy, technical power aesthetic |
| Pinterest | `pinterest` | Red accent, masonry grid, image-first |
| SpaceX | `spacex` | Stark black and white, full-bleed imagery, futuristic |
| Spotify | `spotify` | Vibrant green on dark, bold type, album-art-driven |
| Uber | `uber` | Bold black and white, tight type, urban energy |

---

## Automotive

| Name | Slug | Style Description |
|------|------|------------------|
| BMW | `bmw` | Dark premium surfaces, precise German engineering aesthetic |
| Ferrari | `ferrari` | Chiaroscuro black-white editorial, Ferrari Red, extreme sparseness |
| Lamborghini | `lamborghini` | True black cathedral, gold accent, Neo-Grotesk type |
| Renault | `renault` | Vivid aurora gradients, NouvelR proprietary typeface |
| Tesla | `tesla` | Radical subtraction, cinematic full-viewport photography |

---

## Usage Tips

### Fetching a DESIGN.md
```bash
# Single design
curl -sL "https://getdesign.md/design-md/linear.app/DESIGN.md"

# Save to file
curl -sL "https://getdesign.md/design-md/stripe/DESIGN.md" > DESIGN.md
```

### Slug format notes
- Most slugs are just the brand name in lowercase: `claude`, `notion`, `stripe`
- Some use domain format: `linear.app`, `mistral.ai`, `together.ai`, `opencode.ai`, `x.ai`
- Automotive: `bmw`, `ferrari`, `lamborghini`, `renault`, `tesla`
- Use `cal` not `cal.com`

### If a slug fails
Try variations: `{brand}` → `{brand.com}` → check this catalog for the exact slug.
