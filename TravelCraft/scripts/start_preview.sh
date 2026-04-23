#!/usr/bin/env bash
# start_preview.sh — Start a local HTTP server for the given directory.
# Prints the URL on success. Safe to re-run (reuses existing server if one is up).
#
# Usage:
#   start_preview.sh <dir> [port]
#   start_preview.sh .          # port auto (8765 if free)
#   start_preview.sh . 8766
set -euo pipefail

DIR="${1:-.}"
PORT="${2:-8765}"

cd "$DIR"

# Check if port already in use
if lsof -iTCP:"$PORT" -sTCP:LISTEN -Pn >/dev/null 2>&1; then
    echo "server already running on port $PORT"
    echo "URL: http://localhost:$PORT/"
    exit 0
fi

# Try the requested port; fall back to next free port if busy
for p in "$PORT" 8766 8767 8768 8769; do
    if ! lsof -iTCP:"$p" -sTCP:LISTEN -Pn >/dev/null 2>&1; then
        nohup python3 -m http.server "$p" >/tmp/_preview_$p.log 2>&1 &
        sleep 0.5
        echo "started server on port $p (pid $!)"
        echo "URL: http://localhost:$p/"
        exit 0
    fi
done

echo "No free port available" >&2
exit 1
