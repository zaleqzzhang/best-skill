#!/usr/bin/env bash
# TravelCraft v2.0 — Dual-engine deploy: EdgeOne Pages + Vercel
# Usage: deploy_both.sh <trip-dir> <slug>
# Output: JSON { "eop": "...", "vercel": "..." } on stdout
#
# Either engine failing is NON-FATAL — we still return the one that worked.
# Both failing → exit 1.

set -uo pipefail

TRIP_DIR="${1:?missing trip directory}"
SLUG="${2:?missing project slug}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

EOP_URL=""
VERCEL_URL=""

echo "[deploy_both] deploying to EdgeOne Pages..." >&2
if EOP_URL=$("$SCRIPT_DIR/deploy_to_eop.sh" "$TRIP_DIR" "$SLUG" 2>&1 >/dev/null ; \
             "$SCRIPT_DIR/deploy_to_eop.sh" "$TRIP_DIR" "$SLUG" 2>/dev/null); then
  echo "[deploy_both] ✓ EdgeOne: $EOP_URL" >&2
else
  echo "[deploy_both] ✗ EdgeOne failed (continuing with Vercel)" >&2
  EOP_URL=""
fi

echo "[deploy_both] deploying to Vercel..." >&2
if VERCEL_URL=$("$SCRIPT_DIR/deploy_to_vercel.sh" "$TRIP_DIR" "$SLUG" 2>/dev/null); then
  echo "[deploy_both] ✓ Vercel: $VERCEL_URL" >&2
else
  echo "[deploy_both] ✗ Vercel failed" >&2
  VERCEL_URL=""
fi

if [[ -z "$EOP_URL" && -z "$VERCEL_URL" ]]; then
  echo "[deploy_both] ERROR: both engines failed" >&2
  exit 1
fi

# Output JSON
cat <<EOF
{
  "eop": "${EOP_URL}",
  "vercel": "${VERCEL_URL}"
}
EOF
