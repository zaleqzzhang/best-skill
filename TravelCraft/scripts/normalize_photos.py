#!/usr/bin/env python3
"""
normalize_photos.py — Batch-crop photos to a target aspect ratio.

Use this before embedding photos into `.tl-photos` paired grids, where both images
must share the same ratio to render without gaps. Default target is 4:3 (1.333).

Subjects are preserved by biasing the crop:
- Portrait-to-landscape: keep upper 25%–85% (buildings/people heads commonly upper).
- Landscape-to-landscape: center crop.

Usage:
    normalize_photos.py <photo_dir> [file1 file2 ...] [--ratio 1.333]
    normalize_photos.py ./photos                       # all photos to 4:3
    normalize_photos.py ./photos hero.jpg header.jpg   # specific files
    normalize_photos.py ./photos --ratio 1.5           # 3:2 instead
"""
import os
import sys
import argparse
from PIL import Image


def crop_to_ratio(img: Image.Image, target: float, upper_bias: float = 0.25) -> Image.Image:
    w, h = img.size
    cur = w / h
    if abs(cur - target) < 0.02:
        return img
    if cur < target:
        # too narrow — crop height
        new_h = int(w / target)
        top = int((h - new_h) * upper_bias)
        return img.crop((0, top, w, top + new_h))
    else:
        # too wide — center crop width
        new_w = int(h * target)
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('photo_dir', help='Directory containing photos')
    ap.add_argument('files', nargs='*', help='Specific filenames (relative to photo_dir). Default: all jpg/png.')
    ap.add_argument('--ratio', type=float, default=4/3, help='Target width/height ratio (default 4:3 = 1.333)')
    ap.add_argument('--upper-bias', type=float, default=0.25, help='Portrait→landscape: fraction of removed height taken from top (0..1). Default 0.25 = keep more upper content.')
    ap.add_argument('--quality', type=int, default=88)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    d = args.photo_dir
    if not os.path.isdir(d):
        print(f'ERR: {d} not a directory', file=sys.stderr)
        sys.exit(1)

    if args.files:
        names = args.files
    else:
        names = [f for f in os.listdir(d) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    for name in sorted(names):
        path = os.path.join(d, name)
        if not os.path.isfile(path):
            print(f'SKIP (missing): {name}')
            continue
        try:
            img = Image.open(path)
        except Exception as e:
            print(f'ERR open {name}: {e}')
            continue
        w, h = img.size
        cur = w / h
        if abs(cur - args.ratio) < 0.02:
            print(f'OK {name} ({w}x{h} ratio={cur:.2f})')
            continue
        new = crop_to_ratio(img, args.ratio, args.upper_bias)
        print(f'CROP {name}: {w}x{h} ({cur:.2f}) -> {new.size[0]}x{new.size[1]} ({args.ratio:.2f})')
        if not args.dry_run:
            if new.mode not in ('RGB', 'L'):
                new = new.convert('RGB')
            save_kwargs = {'quality': args.quality, 'optimize': True}
            if name.lower().endswith('.png'):
                save_kwargs = {'optimize': True}
            new.save(path, **save_kwargs)


if __name__ == '__main__':
    main()
