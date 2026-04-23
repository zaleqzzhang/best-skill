#!/usr/bin/env bash
# TravelCraft v2.0 — Deploy trip directory to EdgeOne Pages
# Usage: deploy_to_eop.sh <trip-dir> <slug>
# Output: the deployed URL on stdout

set -euo pipefail

TRIP_DIR="${1:?missing trip directory}"
SLUG="${2:?missing project slug}"

if [[ ! -d "$TRIP_DIR" ]]; then
  echo "[deploy_to_eop] ERROR: directory not found: $TRIP_DIR" >&2
  exit 1
fi

# Ensure there's an index.html (CDN entry point)
if [[ ! -f "$TRIP_DIR/index.html" ]]; then
  if [[ -f "$TRIP_DIR/$SLUG.html" ]]; then
    cp "$TRIP_DIR/$SLUG.html" "$TRIP_DIR/index.html"
    echo "[deploy_to_eop] copied $SLUG.html -> index.html" >&2
  else
    echo "[deploy_to_eop] ERROR: no index.html or $SLUG.html in $TRIP_DIR" >&2
    exit 1
  fi
fi

# EdgeOne Pages CLI (install once on first use)
if ! command -v edgeone >/dev/null 2>&1; then
  echo "[deploy_to_eop] installing EdgeOne CLI..." >&2
  npm install -g edgeone@latest >&2 || {
    echo "[deploy_to_eop] ERROR: failed to install edgeone CLI. Run: npm i -g edgeone" >&2
    exit 2
  }
fi

# Check login status; if not logged in, prompt and exit
if ! edgeone whoami >/dev/null 2>&1; then
  cat >&2 <<EOF
[deploy_to_eop] You are not logged in to EdgeOne Pages.
  → Option A: click [集成] in the chat UI → EdgeOne Pages → 连接
  → Option B: run in terminal:  edgeone login
Then re-run deployment.
EOF
  exit 3
fi

echo "[deploy_to_eop] deploying project: $SLUG" >&2
cd "$TRIP_DIR"

# Create / update project and upload
OUTPUT=$(edgeone pages deploy . \
  --name "$SLUG" \
  --prod \
  --yes 2>&1) || {
    echo "[deploy_to_eop] deploy failed:" >&2
    echo "$OUTPUT" >&2
    exit 4
  }

# Extract URL (accept both .edgeone.app and .pages.dev patterns)
URL=$(echo "$OUTPUT" | grep -oE 'https://[A-Za-z0-9.-]+\.(edgeone\.app|pages\.dev)' | head -1)

if [[ -z "$URL" ]]; then
  URL="https://${SLUG}.edgeone.app"
  echo "[deploy_to_eop] WARN: URL not parsed from output, using fallback: $URL" >&2
fi

echo "$URL"
