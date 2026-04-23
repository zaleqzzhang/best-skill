# Phase 6 Deployment Guide

> Reference for Phase 6 (cloud deployment) in SKILL.md.
> Read this only when running Phase 6. Not needed for Phases 1–5.

## Engine Selection Matrix

| Scenario | Recommended Engine |
|----------|-------------------|
| Primary audience is in China, traveling on 4G/5G | **EdgeOne Pages** |
| Audience includes overseas or requires long-term archival | **Vercel** |
| Family shared trip, want max reliability | **Dual engine (both)** ⭐ recommended |
| User already connected CloudBase, wants one-stop | Fallback: CloudBase Static Hosting |

**Default when user says "按推荐"**: dual-engine with password.

---

## First-Time Authentication

### EdgeOne Pages

Two paths (either works):

**Path A — CodeBuddy UI Integration (recommended for non-technical users):**
1. Click [集成] button at the bottom of the chat
2. Find [EdgeOne Pages] → click [连接]
3. Login with 腾讯云 account (WeChat / QQ / email supported)
4. Skill can now call `edgeone` CLI

**Path B — Terminal CLI:**
```bash
npm i -g edgeone
edgeone login
```

Check status:
```bash
edgeone whoami
```

### Vercel

```bash
npx vercel login
# → choose "Continue with GitHub" (easiest)
# → browser will open, click Authorize
# → return to terminal, "Success" shown
```

Token is stored at `~/.local/share/com.vercel.cli/auth.json` (macOS/Linux) or `%APPDATA%\com.vercel.cli\auth.json` (Windows).

Check status:
```bash
npx vercel whoami
```

---

## Deployment Flow (Technical)

```
Phase 5 outputs: <slug>.html + <slug>.jpg + <slug>.pdf
         │
         ▼
[Phase 6.1] Ask user: engine? password?
         │
         ▼
[Phase 6.2] First-time auth (if needed)
         │
         ▼
[Phase 6.3] If password: inject_password.py
            → <slug>.html now has encrypted gate
         │
         ▼
[Phase 6.4] deploy_to_eop.sh / deploy_to_vercel.sh / deploy_both.sh
            → captures URL(s)
         │
         ▼
[Phase 6.5] generate_qrcode.py → qr-dual.png
         │
         ▼
[Phase 6.6] embed_qr_in_longimage.py
            → <slug>-cloud.jpg  (long image + share block)
         │
         ▼
[Phase 6.7] update_index.py
            → data/trips.json updated
            → bookshelf-build/index.html rendered
            → deploy bookshelf to "my-travelcraft" project
         │
         ▼
[Phase 6.8] Final report + open_result_view(<slug>-cloud.jpg)
```

---

## Password Protection Mechanism

### What it does

- Wraps the HTML content in a client-side AES-256 encrypted capsule
- User sees a 宋式美学 password gate on load
- Correct password → content is decrypted in browser and rendered
- Wrong password → "密码错误" with shake animation

### What it does NOT do

- Does NOT authenticate against any server (fully static)
- Does NOT prevent someone with the password from sharing HTML source
- Suitable for: family/friend privacy, "don't show colleagues" level
- NOT suitable for: legally-sensitive or PII-regulated content

### Crypto details

- Key derivation: PBKDF2-SHA256, 10000 iterations
- Random 16-byte salt per page, random 16-byte IV
- Cipher: AES-256-CBC with PKCS7 padding
- Decryption library: `crypto-js` 4.2 from cdnjs

### Password hygiene

- Minimum length: 4 chars (enforced in script)
- Recommend 4-8 chars for convenience (this is casual-level protection)
- Skill should NEVER persist the password — ask user each time, or let them write it in their own notes
- Show password once in the final report, then forget

---

## Bookshelf Index Page

### What gets deployed

The `my-travelcraft` (or user-specified) project hosts:
- `index.html` — auto-generated from `data/trips.json`
- Groups trips by year
- Sorts by `created_at` descending
- Shows lock icon for password-protected trips
- Two buttons per card: 🇨🇳 国内版 / 🌏 海外版

### Where it lives

- Local data: `~/.codebuddy/skills/TravelCraft/data/trips.json`
- Deploy target: a SEPARATE EOP/Vercel project named `my-travelcraft` (or user's choice)
- URL looks like: `https://my-travelcraft.edgeone.app` or `https://my-travelcraft.vercel.app`

### Privacy options

- Bookshelf is PUBLIC by default (shows trip titles + metadata, but trip content is still gated)
- To keep bookshelf private too: apply `inject_password.py` on `index.html` before deploying
- Or: don't deploy bookshelf, tell user "本地访问 data/trips.json"

---

## Troubleshooting

### `edgeone: command not found`

```bash
npm i -g edgeone
# or use npx:
npx edgeone whoami
```

If `npm` is also missing, install Node.js: https://nodejs.org/

### Vercel deploy hangs at "Setting up project"

- First deploy requires selecting scope (personal vs team). The `--yes` flag usually auto-selects personal scope.
- If still hanging: `Ctrl+C`, then run `npx vercel` once manually to complete project setup, then retry.

### Password gate shows but decryption fails even with correct password

- Check browser console for crypto-js load error (network blocked?)
- crypto-js CDN: `cdnjs.cloudflare.com` — if blocked, switch to jsdelivr in `inject_password.py`
- Verify salt/iv/ct are valid base64 (no trailing whitespace injection)

### Chinese characters in title show as `&#x...`

- Jinja2 autoescape is on for HTML templates — this is correct, browsers will render them fine.
- If displayed as literal entities in a text viewer, that's expected; open in a real browser.

### Deploy succeeded but URL returns 404

- EdgeOne Pages: first deploy of a new project takes 1–2 min for CDN propagation. Wait and retry.
- Vercel: usually instant, but may need a hard refresh if browser cached old 404.

### Can I use a custom domain?

Yes — both engines support custom domains on free tier:
- EdgeOne Pages: project settings → 自定义域名 → add CNAME
- Vercel: project settings → Domains → add + update DNS

Not automated by this skill; configure manually after first deploy.

---

## Future Extensions (not yet implemented)

- Auto-expire trips older than 90 days (GDPR-like cleanup)
- Import existing trips from local file system (retroactive bookshelf build)
- Export bookshelf as a single-file HTML for offline viewing
- Multi-language gate page (currently 中文 only)
