#!/usr/bin/env python3
"""
make_export_html.py — Generate an export-optimized copy of the interactive HTML.

Transforms:
- All `.day-section` start expanded (no tab switching required).
- `.tabs-wrap`, `.bottom-nav` hidden.
- Base font enlarged for mobile/long-image readability.
- Container fixed to ~440px for consistent rendering.
- `@page` rule added for mobile-size PDF pagination.
- Images/sections marked `page-break-inside:avoid`.

Usage:
    make_export_html.py <input.html> <output.html>
"""
import sys
import re


EXPORT_STYLE = """
<style id="export-style">
  /* PDF page size (mobile-like) */
  @page{size:480px 800px;margin:0}
  html,body{margin:0;padding:0}

  /* Expand all day sections */
  .day-section{display:block !important;animation:none !important}
  .day-section{padding:28px 0 8px !important;border-top:1px solid rgba(0,0,0,.06)}
  .day-section#overview{border-top:none}

  /* Hide interactive navigation */
  .tabs-wrap,.bottom-nav{display:none !important}
  body{padding-bottom:0 !important;font-size:18px !important}

  /* Fixed mobile container */
  .container{max-width:440px !important;padding:20px 18px !important;margin:0 auto !important}
  .hero{padding:50px 24px 36px !important}
  .hero h1{font-size:2em !important;letter-spacing:8px !important}
  .hero .sub{font-size:.95em !important}

  /* Readable font sizes */
  .day-header-text h2{font-size:1.3em !important}
  .summary-body p{font-size:.95em !important;line-height:1.9 !important}
  .xhs .xc{font-size:.88em !important;line-height:1.95 !important}
  .tl-title{font-size:1em !important}
  .tl-desc{font-size:.82em !important;line-height:1.75 !important}
  .tl-time{font-size:.78em !important}
  .tl-photo .pc{font-size:.78em !important;padding:9px 14px !important}
  .tl-wrap-title{font-size:.85em !important}
  .summary-body .st{font-size:.9em !important}
  .xhs .xt{font-size:.78em !important}
  .badge{font-size:.8em !important;padding:6px 16px !important}
  .info-card,.card{padding:18px 22px !important}
  .info-card h4,.card h4{font-size:1.05em !important}
  .info-card p,.card p{font-size:.88em !important;line-height:1.85 !important}
  .warn p{font-size:.88em !important}
  .warn h4{font-size:1em !important}
  .table{font-size:.85em !important}

  /* Avoid mid-component page breaks */
  img,.tl-item,.tl-photo,.tl-photos,.summary,.xhs,.card,.tl-wrap,.warn,.info-card{
    page-break-inside:avoid;break-inside:avoid;
  }
</style>
"""


JS_PATCH_MARK = 'function switchDay(d){'
JS_PATCH_INJECT = """// Export: expand all day sections
document.querySelectorAll('.day-section').forEach(function(s){s.classList.add('active')});
function switchDay(d){"""


def main():
    if len(sys.argv) != 3:
        print('Usage: make_export_html.py <input.html> <output.html>', file=sys.stderr)
        sys.exit(1)

    inp, outp = sys.argv[1], sys.argv[2]
    with open(inp, 'r', encoding='utf-8') as f:
        html = f.read()

    # Inject expand-all JS
    if JS_PATCH_MARK in html:
        html = html.replace(JS_PATCH_MARK, JS_PATCH_INJECT, 1)

    # Inject style before </head>
    if '</head>' in html:
        html = html.replace('</head>', EXPORT_STYLE + '\n</head>', 1)
    else:
        html = EXPORT_STYLE + html

    with open(outp, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'OK: {outp}')


if __name__ == '__main__':
    main()
