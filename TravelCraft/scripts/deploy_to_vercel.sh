#!/usr/bin/env bash
# TravelCraft v2.0 — Deploy trip directory to Vercel
# Usage: deploy_to_vercel.sh <trip-dir> <slug>
# Output: the deployed URL on stdout

set -euo pipefail

TRIP_DIR="${1:?missing trip directory}"
SLUG="${2:?missing project slug}"

if [[ ! -d "$TRIP_DIR" ]]; then
  echo "[deploy_to_vercel] ERROR: directory not found: $TRIP_DIR" >&2
  exit 1
fi

# Ensure there's an index.html
if [[ ! -f "$TRIP_DIR/index.html" ]]; then
  if [[ -f "$TRIP_DIR/$SLUG.html" ]]; then
    cp "$TRIP_DIR/$SLUG.html" "$TRIP_DIR/index.html"
    echo "[deploy_to_vercel] copied $SLUG.html -> index.html" >&2
  else
    echo "[deploy_to_vercel] ERROR: no index.html or $SLUG.html in $TRIP_DIR" >&2
    exit 1
  fi
fi

# Minimal Vercel config for static hosting with clean URLs + caching
cat > "$TRIP_DIR/vercel.json" <<'EOF'
{
  "cleanUrls": true,
  "trailingSlash": false,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=3600, s-maxage=86400" }
      ]
    },
    {
      "source": "/(.*\\.(jpg|jpeg|png|webp|svg))",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=604800, immutable" }
      ]
    }
  ]
}
EOF

# Use npx so users don't need global install
VERCEL_CMD="npx --yes vercel@latest"

# Check login; Vercel stores auth at ~/.local/share/com.vercel.cli/
if ! $VERCEL_CMD whoami >/dev/null 2>&1; then
  cat >&2 <<EOF
[deploy_to_vercel] You are not logged in to Vercel.
  → Run in terminal:  npx vercel login
  → Choose "Continue with GitHub" (or email)
  → After success, re-run deployment.
EOF
  exit 3
fi

echo "[deploy_to_vercel] deploying project: $SLUG" >&2
cd "$TRIP_DIR"

# Deploy to production
OUTPUT=$($VERCEL_CMD deploy \
  --prod \
  --yes \
  --name "$SLUG" 2>&1) || {
    echo "[deploy_to_vercel] deploy failed:" >&2
    echo "$OUTPUT" >&2
    exit 4
  }

# Extract URL (Vercel prints final URL at the end)
URL=$(echo "$OUTPUT" | grep -oE 'https://[A-Za-z0-9.-]+\.vercel\.app' | tail -1)

if [[ -z "$URL" ]]; then
  echo "[deploy_to_vercel] ERROR: could not parse deployed URL from output" >&2
  echo "$OUTPUT" >&2
  exit 5
fi

echo "$URL"
