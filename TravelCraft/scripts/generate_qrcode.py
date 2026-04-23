#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TravelCraft v2.0 — Generate QR code(s) with 宋式美学 styling.

Usage:
    # Single QR
    python3 generate_qrcode.py --url https://example.com --output qr.png

    # Dual QR (side by side, with CN/INTL labels)
    python3 generate_qrcode.py \\
        --url-cn https://foo.edgeone.app \\
        --url-intl https://foo.vercel.app \\
        --output qr-dual.png
"""
import argparse
import sys
from pathlib import Path

try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.stderr.write(
        "[generate_qrcode] missing deps. run: pip3 install 'qrcode[pil]' pillow\n"
    )
    sys.exit(1)

# Brand palette
BG = (245, 239, 230)        # 月白 #F5EFE6
BROWN = (176, 123, 95)      # 赭石 #B07B5F
DARK = (51, 51, 51)
GRAY = (102, 102, 102)


def _load_font(size, bold=False):
    """Try to load a Chinese-capable serif font; fallback to default."""
    candidates = [
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.otf" if bold
            else "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.otf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def make_single_qr(url: str, out_path: Path, size: int = 400):
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=BROWN, back_color=BG).convert("RGB")
    img = img.resize((size, size), Image.LANCZOS)
    img.save(out_path, "PNG")
    print(f"[generate_qrcode] saved single QR: {out_path}")


def make_dual_qr(url_cn: str, url_intl: str, out_path: Path):
    W, H = 880, 560
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    # Top ornamental border (simple 云雷纹 simulation with dashed rect)
    draw.rectangle([(20, 20), (W - 20, 24)], fill=BROWN)

    # Generate two QRs
    qr_size = 320
    for idx, (url, label_cn, label_desc) in enumerate([
        (url_cn,  "🇨🇳  国内访问",  "EdgeOne Pages"),
        (url_intl, "🌏  海外访问", "Vercel"),
    ]):
        if not url:
            continue
        qr = qrcode.QRCode(
            version=None, error_correction=ERROR_CORRECT_H,
            box_size=10, border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color=BROWN, back_color=BG).convert("RGB")
        qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

        x = 60 + idx * (qr_size + 80)
        y = 80
        canvas.paste(qr_img, (x, y))

        # Labels
        font_label = _load_font(26, bold=True)
        font_sub = _load_font(18)
        try:
            bbox = draw.textbbox((0, 0), label_cn, font=font_label)
            tw = bbox[2] - bbox[0]
        except AttributeError:
            tw, _ = draw.textsize(label_cn, font=font_label)
        draw.text((x + (qr_size - tw) // 2, y + qr_size + 20),
                  label_cn, fill=DARK, font=font_label)
        try:
            bbox = draw.textbbox((0, 0), label_desc, font=font_sub)
            tw = bbox[2] - bbox[0]
        except AttributeError:
            tw, _ = draw.textsize(label_desc, font=font_sub)
        draw.text((x + (qr_size - tw) // 2, y + qr_size + 60),
                  label_desc, fill=GRAY, font=font_sub)

    # Bottom footer
    draw.rectangle([(20, H - 24), (W - 20, H - 20)], fill=BROWN)
    footer_font = _load_font(16)
    footer = "行迹 · TravelCraft  —  扫码查看完整交互版"
    try:
        bbox = draw.textbbox((0, 0), footer, font=footer_font)
        tw = bbox[2] - bbox[0]
    except AttributeError:
        tw, _ = draw.textsize(footer, font=footer_font)
    draw.text(((W - tw) // 2, H - 60), footer, fill=GRAY, font=footer_font)

    canvas.save(out_path, "PNG")
    print(f"[generate_qrcode] saved dual QR: {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", help="Single URL (use this OR --url-cn/--url-intl)")
    ap.add_argument("--url-cn", dest="url_cn", help="China URL (EdgeOne)")
    ap.add_argument("--url-intl", dest="url_intl", help="International URL (Vercel)")
    ap.add_argument("--output", "-o", required=True, help="Output PNG path")
    ap.add_argument("--size", type=int, default=400, help="Single QR size (px)")
    args = ap.parse_args()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    if args.url_cn or args.url_intl:
        make_dual_qr(args.url_cn or "", args.url_intl or "", out)
    elif args.url:
        make_single_qr(args.url, out, args.size)
    else:
        ap.error("need --url OR --url-cn/--url-intl")


if __name__ == "__main__":
    main()
