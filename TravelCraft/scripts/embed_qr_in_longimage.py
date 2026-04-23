#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TravelCraft v2.0 — Append a share-block (with QR + URLs) to the bottom of a long JPG.

Usage:
    python3 embed_qr_in_longimage.py \\
        --long-jpg trip.jpg \\
        --qr qr-dual.png \\
        --output trip-cloud.jpg \\
        [--password hn2026] \\
        [--url-cn https://...] \\
        [--url-intl https://...]
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.stderr.write("[embed_qr] missing deps. run: pip3 install pillow\n")
    sys.exit(1)

BG = (245, 239, 230)
BROWN = (176, 123, 95)
DARK = (51, 51, 51)
GRAY = (102, 102, 102)
INDIGO = (44, 74, 110)


def _load_font(size):
    candidates = [
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.otf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for p in candidates:
        if Path(p).exists():
            try: return ImageFont.truetype(p, size)
            except Exception: continue
    return ImageFont.load_default()


def _text_width(draw, text, font):
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0]
    except AttributeError:
        return draw.textsize(text, font=font)[0]


def build_share_block(width: int, qr_png: Path,
                      url_cn: str = "", url_intl: str = "",
                      password: str = "") -> Image.Image:
    """Build a share-block image with the same width as the long JPG."""
    BLOCK_H = 820
    block = Image.new("RGB", (width, BLOCK_H), BG)
    draw = ImageDraw.Draw(block)

    # Top 云雷纹 divider (simulated with repeating thin segments)
    div_y = 40
    segment_w = 12
    gap = 4
    total_w = width - 120
    start_x = 60
    for i in range(total_w // (segment_w + gap)):
        x = start_x + i * (segment_w + gap)
        draw.rectangle([(x, div_y), (x + segment_w, div_y + 3)], fill=BROWN)

    # Section title
    title = "扫 码 查 看 完 整 交 互 版"
    title_font = _load_font(38)
    tw = _text_width(draw, title, title_font)
    draw.text(((width - tw) // 2, 70), title, fill=BROWN, font=title_font)

    subtitle = "Scan to view interactive itinerary"
    sub_font = _load_font(18)
    sw = _text_width(draw, subtitle, sub_font)
    draw.text(((width - sw) // 2, 130), subtitle, fill=GRAY, font=sub_font)

    # QR code
    qr_img = Image.open(qr_png).convert("RGB")
    qr_w, qr_h = qr_img.size
    # Scale if too wide
    max_qr_w = min(width - 80, 760)
    if qr_w > max_qr_w:
        ratio = max_qr_w / qr_w
        qr_img = qr_img.resize((max_qr_w, int(qr_h * ratio)), Image.LANCZOS)
        qr_w, qr_h = qr_img.size
    qr_x = (width - qr_w) // 2
    qr_y = 180
    block.paste(qr_img, (qr_x, qr_y))

    # URL text(s)
    text_y = qr_y + qr_h + 24
    url_font = _load_font(16)
    if url_cn:
        t = f"🇨🇳 {url_cn}"
        tw = _text_width(draw, t, url_font)
        draw.text(((width - tw) // 2, text_y), t, fill=INDIGO, font=url_font)
        text_y += 30
    if url_intl:
        t = f"🌏 {url_intl}"
        tw = _text_width(draw, t, url_font)
        draw.text(((width - tw) // 2, text_y), t, fill=INDIGO, font=url_font)
        text_y += 30

    # Password hint
    if password:
        pwd_text = f"🔒  访问密码：{password}"
        pwd_font = _load_font(20)
        tw = _text_width(draw, pwd_text, pwd_font)
        draw.text(((width - tw) // 2, text_y + 10), pwd_text, fill=BROWN, font=pwd_font)

    # Footer brand
    footer = "行 迹  ·  TravelCraft  ·  v2.0"
    footer_font = _load_font(16)
    fw = _text_width(draw, footer, footer_font)
    draw.text(((width - fw) // 2, BLOCK_H - 50), footer, fill=GRAY, font=footer_font)

    # Bottom divider
    draw.rectangle([(60, BLOCK_H - 20), (width - 60, BLOCK_H - 17)], fill=BROWN)

    return block


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--long-jpg", required=True, help="Source long JPG file")
    ap.add_argument("--qr", required=True, help="QR PNG file")
    ap.add_argument("--output", required=True, help="Output JPG path")
    ap.add_argument("--url-cn", default="")
    ap.add_argument("--url-intl", default="")
    ap.add_argument("--password", default="")
    args = ap.parse_args()

    long_img = Image.open(args.long_jpg).convert("RGB")
    w, h = long_img.size
    print(f"[embed_qr] long image: {w}×{h}")

    block = build_share_block(w, Path(args.qr),
                              url_cn=args.url_cn,
                              url_intl=args.url_intl,
                              password=args.password)

    combined = Image.new("RGB", (w, h + block.height), BG)
    combined.paste(long_img, (0, 0))
    combined.paste(block, (0, h))

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    combined.save(out, "JPEG", quality=92, optimize=True)
    print(f"[embed_qr] saved → {out}  ({combined.size[0]}×{combined.size[1]})")


if __name__ == "__main__":
    main()
