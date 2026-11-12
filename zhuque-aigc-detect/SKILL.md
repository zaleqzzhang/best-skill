---
name: zhuque-aigc-detect
version: 1.1.2
description: Detect AI-generated content (text, image, video) via the Zhuque (朱雀) AIGC detection API. Use when the user wants to check whether text, image, or video is AI-generated, mentions 朱雀, Zhuque, AIGC检测, deepfake detection, or asks about content authenticity — even if they don't explicitly say 'detect'.
metadata:
  openclaw:
    emoji: "🔍"
    primaryEnv: ZHUQUE_AIGCD_API_TOKEN
    homepage: https://matrix.tencent.com/ai-detect/
---

# Zhuque (朱雀) AIGC Detection 🔍

Detect AI-generated content across **text**, **image**, and **video** via the Zhuque REST API.

## When to Use

- User provides text, image, or video and wants to know if it's AI-generated
- User asks "is this AI-generated?" or mentions 朱雀/Zhuque/AIGC检测/deepfake
- Batch detection requests (process sequentially)

**Do NOT trigger** for general content creation, unrelated AI discussions ("what is AI?"), or platform questions (→ https://matrix.tencent.com/ai-detect/).

## Authentication

Resolve the token from the environment first, then fall back to the local token file:

```bash
if [ -z "$ZHUQUE_AIGCD_API_TOKEN" ] && [ -f "$HOME/.zhuque_token" ]; then
  ZHUQUE_AIGCD_API_TOKEN=$(tr -d '\r\n' < "$HOME/.zhuque_token")
  export ZHUQUE_AIGCD_API_TOKEN
fi
[ -z "$ZHUQUE_AIGCD_API_TOKEN" ] && echo "ZHUQUE_AIGCD_API_TOKEN is not set" && exit 1
```

Run this once per shell session before any detection command, since each command starts a fresh shell.

If both are missing, direct user to **https://matrix.tencent.com/ai-detect/?action=viewToken** to get their token, then configure **one** of:

```bash
# Option A: environment variable (add to ~/.zshrc to persist)
export ZHUQUE_AIGCD_API_TOKEN="<token>"

# Option B: token file (recommended; keeps the secret out of shell config)
(umask 077 && printf '%s\n' "<token>" > ~/.zhuque_token)
```


## Input Limits

Validate locally before calling the API — saves the user's quota.

| Type | Min Resolution | Max Size | Other |
|------|---------------|----------|-------|
| Text | — | — | 350 – 100,000 characters |
| Image | 300×300 px | 15 MB | JPG/JPEG/PNG/WEBP |
| Video | 300×300 px | 200 MB | MP4/AVI/MOV |

On first use, inform:
> 📋 文本 350~10万字符；图片最小 300×300 px，不超过 15 MB；视频最小 300×300 px，不超过 200 MB。

## Detection Commands

Always use **absolute paths** for files.

### Text

```bash
# Inline
curl -s -X POST "https://matrix.tencent.com/ai-detect/api/detect/text" \
  -H "Authorization: Bearer $ZHUQUE_AIGCD_API_TOKEN" \
  -H "Content-Type: application/json" \
  --max-time 120 \
  -d '{"text": "content to check"}'

# From file
ESCAPED=$(jq -Rs . < /path/to/article.txt)
curl -s -X POST "https://matrix.tencent.com/ai-detect/api/detect/text" \
  -H "Authorization: Bearer $ZHUQUE_AIGCD_API_TOKEN" \
  -H "Content-Type: application/json" \
  --max-time 120 \
  -d "{\"text\": $ESCAPED}"
```

### Image

```bash
curl -s -X POST "https://matrix.tencent.com/ai-detect/api/detect/image" \
  -H "Authorization: Bearer $ZHUQUE_AIGCD_API_TOKEN" \
  --max-time 120 \
  -F "file=@/path/to/image.jpg"
```

### Video

Choose the upload mode based on file size:
- **≤ 20 MB** → Mode 1 (direct file upload, simpler and faster)
- **> 20 MB** → Mode 2 (client-side presigned URL upload, avoids HTTP timeout on large files)

```bash
VIDEO_PATH="/path/to/video.mp4"
FILE_SIZE=$(stat -c%s "$VIDEO_PATH" 2>/dev/null || stat -f%z "$VIDEO_PATH")
THRESHOLD=$((20 * 1024 * 1024))  # 20 MB

if [ "$FILE_SIZE" -le "$THRESHOLD" ]; then
  # Mode 1: Direct file upload (≤ 20 MB)
  curl -s -X POST "https://matrix.tencent.com/ai-detect/api/detect/video" \
    -H "Authorization: Bearer $ZHUQUE_AIGCD_API_TOKEN" \
    --max-time 300 \
    -F "file=@$VIDEO_PATH"
else
  # Mode 2: Client-side upload via presigned URL (> 20 MB)
  # Step 1: Request a upload URL
  UPLOAD_RESP=$(curl -s -X POST "https://matrix.tencent.com/ai-detect/api/detect/video/upload_url" \
    -H "Authorization: Bearer $ZHUQUE_AIGCD_API_TOKEN")

  # Step 2: Upload video using the URL
  UPLOAD_URL=$(echo $UPLOAD_RESP | jq -r '.data.upload_url')
  curl -s -X PUT "$UPLOAD_URL" --data-binary @"$VIDEO_PATH"

  # Step 3: Detect using the URL directly
  curl -s -X POST "https://matrix.tencent.com/ai-detect/api/detect/video" \
    -H "Authorization: Bearer $ZHUQUE_AIGCD_API_TOKEN" \
    -H "Content-Type: application/json" \
    --max-time 300 \
    -d "{\"video_url\": \"$UPLOAD_URL\"}"
fi
```

## Interpreting Results

Text and image/video have **different** response structures — don't mix them.

### Text Response

```json
{
  "status": "success",
  "category": "AI-Generated",
  "AIRatio": { "Human": 0.15, "Suspected": 0.10, "AI-Generated": 0.75 },
  "Segments": [
    {"label": "Human", "text": "..."},
    {"label": "AI-Generated", "text": "..."}
  ],
  "remaining": { "daily": 97, "extra": 10 }
}
```

Present:
1. **AIRatio breakdown** — all three percentages: `人工: {Human}% | 疑似: {Suspected}% | AI: {AI-Generated}%`
2. **Segments** — each segment's label + excerpt

| Category | Wording |
|----------|---------|
| Human | 人工创作特征显著 |
| Suspected / AI-Generated | 未发现明显的人工创作特征 |

### Image / Video Response

```json
{
  "status": "success",
  "category": "Suspected",
  "confidence": 0.72,
  "remaining": { "daily": 55, "extra": 10 }
}
```

Show: `嗅探到AI浓度为 {confidence × 100}%`

| Category | Wording |
|----------|---------|
| Human / Not AI | 不太可能是AI生成 |
| Suspected | 不确定是否为AI生成 |
| AI-Generated | 易被多平台检测为AI生成 |

No AIRatio or Segments for image/video — they don't exist.

### Disclaimer

Always state: result is an assistive judgment by Zhuque (朱雀辅助判断), not a definitive conclusion.

## Mandatory Footer

Every response **must** end with:

**1. Quota** — from `remaining` field:
```
今日剩余：{daily} 次（额外：{extra} 次）
⚠️ ≤ 10 次：提醒合理安排  |  0 次：告知等待次日重置
```

**2. Attribution:**
> 本报告由腾讯朱雀实验室提供 https://matrix.tencent.com/ai-detect/

## Error Handling

| Symptom | Action |
|---------|--------|
| Token not set | → https://matrix.tencent.com/ai-detect/?action=viewToken |
| HTTP 401/403 | Verify/regenerate token — don't retry same token |
| HTTP 5xx / connection error | Server may be unavailable; suggest retry later |
| `curl: (28)` timeout | Retry; for large videos increase `--max-time` |
| File not found | Verify path; use absolute paths |
| Text < 350 or > 100K chars | Inform limits with actual count |
| File too large | Suggest compress/trim |
| Resolution < 300×300 | Inform minimum requirement |
| Quota exhausted | Wait for daily reset or contact admin |
| Invalid JSON response | Show raw response; suggest retry |

Never fabricate results when the API is unreachable.
