#!/bin/bash
# Generate a flowchart PNG from Mermaid syntax (high-quality output).
#
# Usage:
#   scripts/gen_flowchart.sh <output.png> <<'EOF'
#   flowchart TD
#       A[开始] --> B{判断}
#       B -->|是| C[处理1]
#       B -->|否| D[处理2]
#   EOF
#
# Or with a file:
#   scripts/gen_flowchart.sh output.png -f input.mmd
#
# Prerequisites:
#   npm install -g @mermaid-js/mermaid-cli
#   npx puppeteer browsers install chrome-headless-shell
#
# Rendering params:
#   -b white     : white background (better for DOCX embedding)
#   --scale 3    : 3x resolution for high-DPI / print quality
#   -w 1600      : 1600px width to avoid text cramping

set -euo pipefail

OUTPUT="$1"
shift

if [ "${1:-}" = "-f" ]; then
    INPUT_FILE="$2"
    mmdc --input "$INPUT_FILE" -o "$OUTPUT" -b white --scale 3 -w 1600
else
    # Read from stdin
    mmdc --input - -o "$OUTPUT" -b white --scale 3 -w 1600
fi

echo "Generated: $OUTPUT"
