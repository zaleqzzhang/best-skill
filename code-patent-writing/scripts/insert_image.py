#!/usr/bin/env python3
"""Insert an image into an unpacked DOCX directory.

Copies the image to word/media/, adds a relationship entry, and prints the
relationship ID plus a ready-to-paste OOXML <w:drawing> snippet.

Usage:
    python scripts/insert_image.py <unpacked_dir> <image_path> [--width WIDTH_CM] [--height HEIGHT_CM]

Example:
    python scripts/insert_image.py unpacked/ flowchart.png --width 15
    # Prints rId and XML snippet to stdout
"""

from __future__ import annotations

import argparse
import re
import shutil
import struct
import sys
from pathlib import Path
from lxml import etree


def get_png_dimensions(path: Path) -> tuple[int, int]:
    """Read width and height from a PNG file header."""
    with open(path, "rb") as f:
        f.read(8)  # skip signature
        f.read(4)  # chunk length
        f.read(4)  # chunk type (IHDR)
        w, h = struct.unpack(">II", f.read(8))
    return w, h


def get_image_dimensions(path: Path) -> tuple[int, int]:
    """Get image dimensions in pixels. Supports PNG and JPEG."""
    suffix = path.suffix.lower()
    if suffix == ".png":
        return get_png_dimensions(path)
    elif suffix in (".jpg", ".jpeg"):
        return _get_jpeg_dimensions(path)
    else:
        # Default fallback
        return 800, 600


def _get_jpeg_dimensions(path: Path) -> tuple[int, int]:
    """Read width and height from a JPEG file."""
    with open(path, "rb") as f:
        f.read(2)  # SOI
        while True:
            marker = f.read(2)
            if len(marker) < 2:
                break
            if marker[0] != 0xFF:
                break
            mtype = marker[1]
            if mtype in (0xC0, 0xC1, 0xC2):
                f.read(3)  # length + precision
                h, w = struct.unpack(">HH", f.read(4))
                return w, h
            else:
                length = struct.unpack(">H", f.read(2))[0]
                f.read(length - 2)
    return 800, 600


def next_relationship_id(rels_path: Path) -> str:
    """Find the next available rId in the relationships file."""
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(str(rels_path), parser)
    root = tree.getroot()
    ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    max_id = 0
    for rel in root.findall(f"{{{ns}}}Relationship"):
        rid = rel.get("Id", "")
        m = re.match(r"rId(\d+)", rid)
        if m:
            max_id = max(max_id, int(m.group(1)))
    return f"rId{max_id + 1}"


def next_media_filename(media_dir: Path, suffix: str) -> str:
    """Find the next available imageN filename in word/media/."""
    existing = set()
    if media_dir.exists():
        for f in media_dir.iterdir():
            m = re.match(r"image(\d+)", f.stem)
            if m:
                existing.add(int(m.group(1)))
    n = 1
    while n in existing:
        n += 1
    return f"image{n}{suffix}"


def next_docpr_id(unpacked_dir: Path) -> int:
    """扫描 document.xml 中已有的 docPr id，返回下一个可用的 id。"""
    doc_path = unpacked_dir / "word" / "document.xml"
    if not doc_path.exists():
        return 1
    # 用正则扫描，避免命名空间解析问题
    content = doc_path.read_text(encoding="utf-8")
    ids = [int(m) for m in re.findall(r'<wp:docPr\s+id="(\d+)"', content)]
    return max(ids, default=0) + 1


def ensure_content_type(unpacked_dir: Path, suffix: str) -> None:
    """确保 [Content_Types].xml 中包含对应图片格式的 Content Type 条目。"""
    ext = suffix.lstrip(".")  # "png" or "jpeg"
    content_type_map = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
    }
    if ext not in content_type_map:
        return

    ct_path = unpacked_dir / "[Content_Types].xml"
    if not ct_path.exists():
        return

    ns = "http://schemas.openxmlformats.org/package/2006/content-types"
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(str(ct_path), parser)
    root = tree.getroot()

    # 检查是否已有对应的 Default 条目
    for default in root.findall(f"{{{ns}}}Default"):
        if default.get("Extension", "").lower() == ext:
            return  # 已存在，无需添加

    # 添加缺失的 Content Type 条目
    new_default = etree.SubElement(root, f"{{{ns}}}Default")
    new_default.set("Extension", ext)
    new_default.set("ContentType", content_type_map[ext])
    tree.write(str(ct_path), xml_declaration=True, encoding="UTF-8")


def cm_to_emu(cm: float) -> int:
    """Convert centimeters to EMU (English Metric Units)."""
    return int(cm * 914400 / 2.54)


def insert_image(unpacked_dir: Path, image_path: Path,
                 width_cm: float | None = None,
                 height_cm: float | None = None) -> tuple[str, str]:
    """Insert an image into the unpacked DOCX and return (rId, xml_snippet).

    Args:
        unpacked_dir: Path to the unpacked DOCX directory
        image_path: Path to the image file
        width_cm: Desired width in cm (default: 15)
        height_cm: Desired height in cm (auto-calculated from aspect ratio if not specified)

    Returns:
        Tuple of (relationship_id, xml_snippet)
    """
    word_dir = unpacked_dir / "word"
    media_dir = word_dir / "media"
    rels_path = word_dir / "_rels" / "document.xml.rels"

    # Ensure media directory exists
    media_dir.mkdir(parents=True, exist_ok=True)

    # Copy image to media directory
    suffix = image_path.suffix.lower()
    media_filename = next_media_filename(media_dir, suffix)
    dest = media_dir / media_filename
    shutil.copy2(image_path, dest)

    # Get image dimensions for aspect ratio
    px_w, px_h = get_image_dimensions(image_path)

    # Calculate EMU dimensions
    if width_cm is None and height_cm is None:
        width_cm = 15.0  # Default: ~15cm wide (fits A4 with margins)

    if width_cm is not None and height_cm is not None:
        # Both specified: use as-is
        width_emu = cm_to_emu(width_cm)
        height_emu = cm_to_emu(height_cm)
    elif width_cm is not None:
        # Only width specified: preserve aspect ratio
        width_emu = cm_to_emu(width_cm)
        height_emu = int(width_emu * px_h / px_w) if px_w > 0 else width_emu
    else:
        # Only height specified: preserve aspect ratio
        assert height_cm is not None
        height_emu = cm_to_emu(height_cm)
        width_emu = int(height_emu * px_w / px_h) if px_h > 0 else height_emu

    # Constrain to reasonable page dimensions (A4 with margins: ~17cm x 24cm)
    max_width_emu = cm_to_emu(17.0)
    max_height_emu = cm_to_emu(24.0)
    if width_emu > max_width_emu:
        scale = max_width_emu / width_emu
        width_emu = max_width_emu
        height_emu = int(height_emu * scale)
    if height_emu > max_height_emu:
        scale = max_height_emu / height_emu
        height_emu = max_height_emu
        width_emu = int(width_emu * scale)

    # Add relationship
    rid = next_relationship_id(rels_path)
    ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(str(rels_path), parser)
    root = tree.getroot()
    new_rel = etree.SubElement(root, f"{{{ns}}}Relationship")
    new_rel.set("Id", rid)
    new_rel.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image")
    new_rel.set("Target", f"media/{media_filename}")
    tree.write(str(rels_path), xml_declaration=True, encoding="UTF-8")

    # 确保 [Content_Types].xml 包含对应图片格式
    ensure_content_type(unpacked_dir, suffix)

    # 获取下一个可用的 docPr id，避免多图插入时 id 冲突
    doc_pr_id = next_docpr_id(unpacked_dir)

    # Generate the drawing XML snippet
    # Use <a:srcRect/> instead of <a:stretch><a:fillRect/></a:stretch> to preserve
    # the original image aspect ratio and prevent distortion of tall/long images.
    xml_snippet = f'''<w:drawing>
  <wp:inline distT="0" distB="0" distL="0" distR="0">
    <wp:extent cx="{width_emu}" cy="{height_emu}"/>
    <wp:effectExtent l="0" t="0" r="0" b="0"/>
    <wp:docPr id="{doc_pr_id}" name="{media_filename}"/>
    <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
      <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
        <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
          <pic:nvPicPr>
            <pic:cNvPr id="0" name="{media_filename}"/>
            <pic:cNvPicPr>
              <a:picLocks noChangeAspect="1"/>
            </pic:cNvPicPr>
          </pic:nvPicPr>
          <pic:blipFill>
            <a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>
            <a:srcRect/>
            <a:stretch/>
          </pic:blipFill>
          <pic:spPr bwMode="auto">
            <a:xfrm>
              <a:off x="0" y="0"/>
              <a:ext cx="{width_emu}" cy="{height_emu}"/>
            </a:xfrm>
            <a:prstGeom prst="rect">
              <a:avLst/>
            </a:prstGeom>
            <a:noFill/>
            <a:ln>
              <a:noFill/>
            </a:ln>
          </pic:spPr>
        </pic:pic>
      </a:graphicData>
    </a:graphic>
  </wp:inline>
</w:drawing>'''

    # Also generate the full paragraph XML for convenience
    para_xml = f'''<w:p>
  <w:pPr>
    <w:jc w:val="center"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="微软雅黑" w:eastAsia="微软雅黑" w:hAnsi="微软雅黑"/>
      <w:noProof/>
    </w:rPr>
    {xml_snippet}
  </w:r>
</w:p>'''

    return rid, para_xml


def _parse_dimension(value: str) -> float:
    """Parse a dimension string that may include unit suffix (e.g. '14cm', '5.5in', '14').

    Supported units: cm (default), in (inches → converted to cm).
    Plain numbers are treated as cm.
    """
    if value is None:
        return None
    s = str(value).strip().lower()
    if s.endswith("cm"):
        return float(s[:-2])
    if s.endswith("in"):
        return float(s[:-2]) * 2.54
    return float(s)


def main():
    parser = argparse.ArgumentParser(description="Insert image into unpacked DOCX")
    parser.add_argument("unpacked_dir", type=Path, help="Path to unpacked DOCX directory")
    parser.add_argument("image_path", type=Path, help="Path to image file")
    parser.add_argument("--width", type=str, default="15", help="Width in cm, supports unit suffix (e.g. 14cm, 15, 5.5in)")
    parser.add_argument("--height", type=str, default=None, help="Height in cm (auto if not set)")
    args = parser.parse_args()
    args.width = _parse_dimension(args.width)
    args.height = _parse_dimension(args.height) if args.height else None

    if not args.unpacked_dir.exists():
        print(f"Error: {args.unpacked_dir} does not exist", file=sys.stderr)
        sys.exit(1)
    if not args.image_path.exists():
        print(f"Error: {args.image_path} does not exist", file=sys.stderr)
        sys.exit(1)

    rid, para_xml = insert_image(args.unpacked_dir, args.image_path, args.width, args.height)
    print(f"Relationship ID: {rid}")
    print(f"Image copied to: word/media/")
    print(f"\nParagraph XML (paste into document.xml at desired location):\n")
    print(para_xml)


if __name__ == "__main__":
    main()
