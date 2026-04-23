#!/usr/bin/env bash
# export_itinerary.sh — Generate JPG long-image + PDF from an interactive HTML.
#
# Usage:
#   export_itinerary.sh <html-file> <output-slug>
#
# Produces in the same directory as the input HTML:
#   <slug>.jpg   — long image (480w × variable h, @2x = 960w)
#   <slug>.pdf   — paginated mobile PDF (pages ~480×800)
#
# Requires:
#   - Google Chrome (macOS default path) or $CHROME env var pointing to chrome binary
#   - Python 3 with Pillow (pip install pillow numpy)
#   - A running local HTTP server serving the HTML (or will auto-start one)

set -euo pipefail

HTML_INPUT="${1:?Usage: export_itinerary.sh <html-file> <output-slug>}"
SLUG="${2:?Usage: export_itinerary.sh <html-file> <output-slug>}"

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WORK_DIR="$(cd "$(dirname "$HTML_INPUT")" && pwd)"
HTML_BASENAME="$(basename "$HTML_INPUT")"

cd "$WORK_DIR"

# Resolve Chrome
if [[ -n "${CHROME:-}" ]]; then
    :
elif [[ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]]; then
    CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
elif command -v google-chrome >/dev/null; then
    CHROME="$(command -v google-chrome)"
elif command -v chromium >/dev/null; then
    CHROME="$(command -v chromium)"
else
    echo "ERR: Chrome not found. Set \$CHROME to chrome/chromium binary." >&2
    exit 1
fi

echo "[1/5] Generating export HTML"
EXPORT_HTML="_${SLUG}-export.html"
python3 "$SKILL_DIR/scripts/make_export_html.py" "$HTML_BASENAME" "$EXPORT_HTML"

echo "[2/5] Starting preview server (if needed)"
# Start server on any free port
SERVER_LOG="$(mktemp)"
PORT=8765
for p in 8765 8766 8767 8768; do
    if ! lsof -iTCP:"$p" -sTCP:LISTEN -Pn >/dev/null 2>&1; then
        nohup python3 -m http.server "$p" >"$SERVER_LOG" 2>&1 &
        SERVER_PID=$!
        PORT=$p
        sleep 1
        break
    else
        PORT=$p   # reuse
        break
    fi
done
BASE_URL="http://localhost:$PORT"
echo "  server: $BASE_URL"

echo "[3/5] Rendering long screenshot (@2x)"
SHOT_PNG="_${SLUG}-shot.png"
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
    --virtual-time-budget=25000 --run-all-compositor-stages-before-draw \
    --force-device-scale-factor=2 --window-size=480,20000 \
    --screenshot="$SHOT_PNG" "$BASE_URL/$EXPORT_HTML" 2>/dev/null
echo "  shot: $SHOT_PNG ($(stat -f%z "$SHOT_PNG" 2>/dev/null || stat -c%s "$SHOT_PNG") bytes)"

echo "[4/5] Cropping + paginating"
python3 "$SKILL_DIR/scripts/crop_screenshot.py" \
    "$SHOT_PNG" "${SLUG}.jpg" --pdf "${SLUG}.pdf" \
    --bg "246,244,240" --page-h 1600 --footer 80 --quality 85

echo "[5/5] Cleanup"
rm -f "$EXPORT_HTML" "$SHOT_PNG"

echo "----"
echo "Done:"
echo "  $WORK_DIR/${SLUG}.jpg"
echo "  $WORK_DIR/${SLUG}.pdf"
ls -la "${SLUG}.jpg" "${SLUG}.pdf"
