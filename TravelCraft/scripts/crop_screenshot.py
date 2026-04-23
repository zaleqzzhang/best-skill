#!/usr/bin/env python3
"""
crop_screenshot.py — Trim trailing whitespace from a Chrome long screenshot
                     and produce a smart-paginated PDF.

Chrome's `--screenshot` with `--window-size=W,H` produces a PNG of size W×H, but
the actual content may end much earlier. This script:

1. Finds the last row containing non-background pixels.
2. Crops the PNG to that row + a small footer margin.
3. Saves a JPG with reasonable quality/size.
4. Smart-paginates into a PDF (break pages at blank rows).

Usage:
    crop_screenshot.py <input.png> <out.jpg> [--pdf out.pdf]
                       [--bg "246,244,240"] [--page-h 1600]
                       [--footer 80] [--quality 85]
"""
import os
import sys
import argparse
from PIL import Image
import numpy as np


def find_content_bottom(arr: np.ndarray, bg: np.ndarray, threshold: int = 30, min_pixels: int = 5) -> int:
    h = arr.shape[0]
    for y in range(h - 1, -1, -1):
        row = arr[y]
        diff = np.abs(row[:, :3].astype(int) - bg).sum(axis=1)
        if (diff > threshold).sum() > min_pixels:
            return y
    return 0


def smart_paginate(img: Image.Image, page_h: int, bg: np.ndarray) -> list:
    """Split img vertically into pages. Prefer break at blank rows."""
    w, total = img.size
    arr = np.array(img)
    pages = []
    y = 0
    while y < total:
        end = min(y + page_h, total)
        if end < total:
            search_start = max(y + page_h - 150, y + int(page_h * 0.5))
            search_end = min(y + page_h + 150, total)
            best_y = end
            best_score = float('inf')
            for candidate in range(search_start, search_end):
                row = arr[candidate]
                diff = np.abs(row[:, :3].astype(int) - bg).sum(axis=1)
                score = diff.sum()
                if score < best_score:
                    best_score = score
                    best_y = candidate
            end = best_y
        pages.append(img.crop((0, y, w, end)))
        y = end
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', help='Input PNG path')
    ap.add_argument('output', help='Output JPG path')
    ap.add_argument('--pdf', help='If given, also write a paginated PDF here')
    ap.add_argument('--bg', default='246,244,240', help='Background RGB as "r,g,b"')
    ap.add_argument('--page-h', type=int, default=1600, help='PDF page height in pixels')
    ap.add_argument('--footer', type=int, default=80, help='Extra pixels to keep below content')
    ap.add_argument('--quality', type=int, default=85)
    args = ap.parse_args()

    bg = np.array([int(x) for x in args.bg.split(',')])
    im = Image.open(args.input)
    arr = np.array(im)
    w, h = im.size

    end = find_content_bottom(arr, bg)
    end = min(end + args.footer, h)

    cropped = im.crop((0, 0, w, end))
    if cropped.mode != 'RGB':
        cropped = cropped.convert('RGB')
    cropped.save(args.output, 'JPEG', quality=args.quality, optimize=True, progressive=True)
    print(f'JPG {cropped.size[0]}x{cropped.size[1]} -> {args.output} ({os.path.getsize(args.output)/1024/1024:.1f} MB)')

    if args.pdf:
        pages = smart_paginate(cropped, args.page_h, bg)
        pages[0].save(
            args.pdf, 'PDF', save_all=True, append_images=pages[1:],
            quality=80, optimize=True,
        )
        print(f'PDF {len(pages)} pages -> {args.pdf} ({os.path.getsize(args.pdf)/1024/1024:.1f} MB)')


if __name__ == '__main__':
    main()
