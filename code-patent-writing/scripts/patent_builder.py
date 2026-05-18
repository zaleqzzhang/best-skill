#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""专利交底书构建引擎。

适配专利 pipeline 的输出格式。核心功能：
  - 章节定位兼容 patent_to_json.py 产出的 section key
  - 支持从 pipeline run_dir 直接读取修订后章节
  - 增强的错误处理和日志

读取声明式的 patent_content.json，自动完成 document.xml 的编辑工作：
  - 填写头部表格
  - 删除蓝色提示段落和重要提醒段落
  - 按 sections 定义逐章插入内容（文本、标题、公式、行内公式、图片、空行）
  - 自动注入图片所需的 XML 命名空间

用法:
    python scripts/patent_builder.py <patent_content.json> <unpacked_dir>
    python scripts/patent_builder.py <patent_content.json> --dry-run

示例:
    python scripts/patent_builder.py _patent_xxx/patent_content.json _patent_xxx/unpacked/
    python scripts/patent_builder.py _patent_xxx/patent_content.json --dry-run
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

from lxml import etree

# Ensure scripts/ directory is on sys.path for insert_image import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from insert_image import insert_image  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ============================================================
# 常量：XML 命名空间
# ============================================================
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
nsmap = {"w": W, "m": M, "r": R}

# 各段落类型的必需字段
PARAGRAPH_REQUIRED_FIELDS: dict[str, list[str]] = {
    "text": ["content"],
    "heading": ["content"],
    "formula": ["omml", "num"],
    "inline": ["parts"],
    "image": ["path"],
    "empty": [],
}

# 图片相关命名空间
IMAGE_NSMAP = {
    "w": W,
    "r": R,
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
}

# 章节标题别名映射（支持 patent_to_json.py 的 section key 格式）
SECTION_ALIASES: dict[str, list[str]] = {
    "【关键术语】": ["【关键术语】", "关键术语"],
    "【发明构思】": ["【发明构思】", "发明构思"],
    "3.1": ["3.1相关背景描述", "3.1", "3.1 相关背景描述"],
    "3.2": ["3.2现有技术的缺点", "3.2", "3.2 现有技术的缺点"],
    "4.1": ["4.1产品侧", "4.1", "4.1 产品侧"],
    "4.2": ["4.2技术侧", "4.2", "4.2 技术侧"],
    "4.3": ["4.3专利方案所产生的有益效果", "4.3", "4.3 专利方案"],
    "参考文献": ["5、参考文献", "参考文献（如", "参考文献"],
}


# ============================================================
# XML 元素构建器
# ============================================================

def _esc(text: str) -> str:
    """XML 特殊字符转义。"""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def make_p(text: str, bold: bool = False) -> etree._Element:
    """构建正文段落（楷体 10pt / 微软雅黑加粗 10pt）。"""
    font = "微软雅黑" if bold else "楷体"
    bxml = "<w:b/><w:bCs/>" if bold else ""
    s = (
        f'<w:p xmlns:w="{W}">'
        f'<w:pPr><w:spacing w:beforeLines="50" w:afterLines="50"/>'
        f'<w:rPr><w:rFonts w:ascii="{font}" w:eastAsia="{font}" w:hAnsi="{font}"/>'
        f'<w:color w:val="000000"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:pPr>'
        f'<w:r><w:rPr><w:rFonts w:ascii="{font}" w:eastAsia="{font}"'
        f' w:hAnsi="{font}" w:hint="eastAsia"/>'
        f'{bxml}<w:color w:val="000000"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
        f'<w:t xml:space="preserve">{_esc(text)}</w:t></w:r></w:p>'
    )
    return etree.fromstring(s.encode("utf-8"))


def make_empty_p() -> etree._Element:
    """空行段落。"""
    return etree.fromstring(
        f'<w:p xmlns:w="{W}"><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>'.encode("utf-8")
    )


def make_formula_p(omml: str, num: int) -> etree._Element:
    """独立公式段落（居中 + 右侧编号）。"""
    s = (
        f'<w:p xmlns:w="{W}" xmlns:m="{M}">'
        f'<w:pPr><w:tabs><w:tab w:val="center" w:pos="4153"/>'
        f'<w:tab w:val="right" w:pos="8306"/></w:tabs>'
        f'<w:spacing w:beforeLines="50" w:afterLines="50"/></w:pPr>'
        f"<w:r><w:tab/></w:r>"
        f"<m:oMath>{omml}</m:oMath>"
        f'<w:r><w:rPr><w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>'
        f'<w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:tab/></w:r>'
        f'<w:r><w:rPr><w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>'
        f'<w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
        f"<w:t>\uff08{num}\uff09</w:t></w:r></w:p>"
    )
    return etree.fromstring(s.encode("utf-8"))


def _run(text: str) -> str:
    """楷体文本 run XML 片段。"""
    return (
        f"<w:r><w:rPr>"
        f'<w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>'
        f'<w:color w:val="000000"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
        f'<w:t xml:space="preserve">{_esc(text)}</w:t></w:r>'
    )


def make_inline_p(parts: list[str | dict[str, str]]) -> etree._Element:
    """含行内公式的段落。"""
    children = ""
    for part in parts:
        if isinstance(part, str):
            children += _run(part)
        elif isinstance(part, dict) and "omml" in part:
            children += f'<m:oMath>{part["omml"]}</m:oMath>'
        elif isinstance(part, (list, tuple)) and len(part) == 2:
            children += f"<m:oMath>{part[1]}</m:oMath>"
    s = (
        f'<w:p xmlns:w="{W}" xmlns:m="{M}">'
        f'<w:pPr><w:spacing w:beforeLines="50" w:afterLines="50"/>'
        f'<w:rPr><w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>'
        f'<w:color w:val="000000"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:pPr>'
        f"{children}</w:p>"
    )
    return etree.fromstring(s.encode("utf-8"))


def make_caption(text: str) -> etree._Element:
    """居中图片标注段落。"""
    s = (
        f'<w:p xmlns:w="{W}"><w:pPr><w:jc w:val="center"/>'
        f'<w:rPr><w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体"/>'
        f'<w:color w:val="000000"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:pPr>'
        f'<w:r><w:rPr><w:rFonts w:ascii="楷体" w:eastAsia="楷体" w:hAnsi="楷体" w:hint="eastAsia"/>'
        f'<w:color w:val="000000"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
        f"<w:t>{_esc(text)}</w:t></w:r></w:p>"
    )
    return etree.fromstring(s.encode("utf-8"))


def make_image_p(para_xml: str) -> etree._Element:
    """将 insert_image() 返回的段落 XML 注入命名空间后解析为 Element。"""
    ns_attrs = " ".join(f'xmlns:{k}="{v}"' for k, v in IMAGE_NSMAP.items())
    para_xml = para_xml.replace("<w:p>", f"<w:p {ns_attrs}>", 1)
    return etree.fromstring(para_xml.encode("utf-8"))


# ============================================================
# 文档导航
# ============================================================

def find_para(body: etree._Element, text: str, *, starts_with: bool = False) -> etree._Element | None:
    """查找包含指定文本的第一个段落。

    Args:
        text: 搜索文本
        starts_with: True 时要求段落文本以 text 开头（去除前导空白和序号后）
    """
    for p in body.findall(".//w:p", nsmap):
        t = "".join(node.text or "" for node in p.findall(".//w:t", nsmap))
        if starts_with:
            # 去除前导空白、序号（如 "5、"）后匹配开头
            stripped = t.strip().lstrip("0123456789、．. ")
            if stripped.startswith(text):
                return p
        else:
            if text in t:
                return p
    return None


def find_para_with_aliases(body: etree._Element, section_key: str) -> etree._Element | None:
    """通过别名列表查找章节标题段落。优先使用行首匹配避免正文误命中。"""
    aliases = SECTION_ALIASES.get(section_key, [section_key])
    # 第一轮：行首匹配（更精确）
    for alias in aliases:
        p = find_para(body, alias, starts_with=True)
        if p is not None:
            return p
    # 第二轮回退：子串匹配
    for alias in aliases:
        p = find_para(body, alias)
        if p is not None:
            return p
    return None


def insert_after(parent: etree._Element, target: etree._Element, elem: etree._Element) -> None:
    """在 target 后插入 elem。"""
    idx = list(parent).index(target)
    parent.insert(idx + 1, elem)


def insert_many_after(
    parent: etree._Element, target: etree._Element, elems: list[etree._Element]
) -> etree._Element:
    """在 target 后依次插入多个元素，返回最后插入的元素。"""
    cur = target
    for e in elems:
        insert_after(parent, cur, e)
        cur = e
    return cur


# ============================================================
# 清理函数
# ============================================================

def _safe_rm(p: etree._Element) -> None:
    """安全删除段落（表格单元格至少保留一个 w:p）。"""
    parent = p.getparent()
    if parent is None:
        return
    if parent.tag == f"{{{W}}}tc":
        if len(parent.findall(f"{{{W}}}p")) <= 1:
            for ch in list(p):
                if ch.tag != f"{{{W}}}pPr":
                    p.remove(ch)
            pPr = p.find(f"{{{W}}}pPr")
            if pPr is not None:
                for c in pPr.findall(f".//{{{W}}}color"):
                    if c.get(f"{{{W}}}val", "").upper() == "0000FF":
                        c.getparent().remove(c)
            return
    parent.remove(p)


def rm_blue(body: etree._Element) -> int:
    """删除蓝色提示段落（w:color w:val="0000FF"）。"""
    to_rm = []
    for p in body.findall(".//w:p", nsmap):
        for c in p.findall(".//w:color", nsmap):
            if c.get(f"{{{W}}}val", "").upper() == "0000FF":
                to_rm.append(p)
                break
    for p in to_rm:
        _safe_rm(p)
    logger.info("删除蓝色提示段落: %s 个", len(to_rm))
    return len(to_rm)


def rm_reminder(body: etree._Element) -> int:
    """删除"重要提醒"到"【关键术语】"之间的段落。"""
    to_rm = []
    active = False
    for p in body.findall(".//w:p", nsmap):
        t = "".join(n.text or "" for n in p.findall(".//w:t", nsmap))
        if "重要提醒" in t:
            active = True
        if active:
            if "【关键术语】" in t:
                break
            to_rm.append(p)
    for p in to_rm:
        _safe_rm(p)
    logger.info("删除重要提醒段落: %s 个", len(to_rm))
    return len(to_rm)


# ============================================================
# 表头填写
# ============================================================

def fill_header(root: etree._Element, header_data: dict[str, str]) -> None:
    """填写头部表格字段。"""
    if not header_data:
        logger.warning("header_data 为空，跳过表头填写")
        return

    for tbl in root.findall(".//w:tbl", nsmap):
        for row in tbl.findall(".//w:tr", nsmap):
            cells = row.findall(".//w:tc", nsmap)
            for i, cell in enumerate(cells):
                ct = "".join(n.text or "" for n in cell.findall(".//w:t", nsmap))
                for label, val in header_data.items():
                    if label in ct and i + 1 < len(cells):
                        vc = cells[i + 1]
                        ps = vc.findall(f"{{{W}}}p")
                        if ps:
                            run = etree.fromstring(
                                f'<w:r xmlns:w="{W}"><w:rPr>'
                                f'<w:rFonts w:ascii="楷体" w:eastAsia="楷体" '
                                f'w:hAnsi="楷体" w:hint="eastAsia"/>'
                                f'<w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
                                f"<w:t>{_esc(val)}</w:t></w:r>".encode("utf-8")
                            )
                            ps[0].append(run)
                            logger.info("填写表头: %s = %s", label, val[:30])
        break


# ============================================================
# 命名空间注入
# ============================================================

def ensure_image_namespaces(doc_path: Path) -> None:
    """往 document.xml 根元素注入图片所需的 xmlns 声明。"""
    content = doc_path.read_text(encoding="utf-8")
    ns_to_inject = {
        'xmlns:a': "http://schemas.openxmlformats.org/drawingml/2006/main",
        'xmlns:pic': "http://schemas.openxmlformats.org/drawingml/2006/picture",
        'xmlns:wp': "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    }
    modified = False
    for attr, uri in ns_to_inject.items():
        if f'{attr}="{uri}"' not in content:
            content = content.replace(
                "<w:document ", f'<w:document {attr}="{uri}" ', 1
            )
            modified = True
            logger.info("注入命名空间: %s=%s", attr, uri)
    if modified:
        doc_path.write_text(content, encoding="utf-8")


# ============================================================
# 输入校验
# ============================================================

def validate_paragraph(desc: dict[str, Any], section_key: str, idx: int) -> list[str]:
    """校验单个段落描述，返回错误信息列表。"""
    errors: list[str] = []
    loc = f"sections[{section_key!r}][{idx}]"

    if not isinstance(desc, dict):
        errors.append(f"{loc}: 段落描述必须是 dict，实际为 {type(desc).__name__}")
        return errors

    ptype = desc.get("type", "text")
    if ptype not in PARAGRAPH_REQUIRED_FIELDS:
        errors.append(f"{loc}: 未知段落类型 {ptype!r}")
        return errors

    for field_name in PARAGRAPH_REQUIRED_FIELDS[ptype]:
        if field_name not in desc:
            errors.append(f"{loc}: 类型 {ptype!r} 缺少必需字段 {field_name!r}")

    if ptype == "formula" and "num" in desc:
        if not isinstance(desc["num"], int):
            errors.append(f"{loc}: formula.num 必须为整数")

    if ptype == "inline" and "parts" in desc:
        if not isinstance(desc["parts"], list):
            errors.append(f"{loc}: inline.parts 必须为 list")

    if ptype == "image" and "path" in desc:
        if not isinstance(desc["path"], str) or not desc["path"].strip():
            errors.append(f"{loc}: image.path 必须为非空字符串")

    return errors


def validate_content(content: dict[str, Any]) -> list[str]:
    """校验整个 patent_content.json 结构。"""
    errors: list[str] = []

    if not isinstance(content, dict):
        errors.append(f"顶层结构必须是 dict")
        return errors

    header = content.get("header")
    if header is not None and not isinstance(header, dict):
        errors.append(f"header 必须是 dict")

    sections = content.get("sections")
    if sections is None:
        errors.append("缺少 'sections' 字段")
        return errors

    if not isinstance(sections, dict):
        errors.append(f"sections 必须是 dict")
        return errors

    for section_key, paragraphs in sections.items():
        if not isinstance(paragraphs, list):
            errors.append(f"sections[{section_key!r}] 必须是 list")
            continue
        for i, desc in enumerate(paragraphs):
            errors.extend(validate_paragraph(desc, section_key, i))

    return errors


# ============================================================
# 段落分发器
# ============================================================

def build_paragraph(
    desc: dict[str, Any], work_dir: Path, unpacked_dir: Path
) -> list[etree._Element]:
    """根据段落描述字典构建一个或多个 XML 元素。"""
    ptype = desc.get("type", "text")

    if ptype == "text":
        return [make_p(desc.get("content", ""))]

    if ptype == "heading":
        return [make_p(desc.get("content", ""), bold=True)]

    if ptype == "formula":
        return [make_formula_p(desc.get("omml", ""), desc.get("num", 0))]

    if ptype == "inline":
        return [make_inline_p(desc.get("parts", []))]

    if ptype == "image":
        elems: list[etree._Element] = []
        img_rel_path = desc.get("path", "")
        if not img_rel_path:
            logger.error("image 段落缺少 path 字段")
            return []
        img_path = work_dir / img_rel_path
        width = desc.get("width", 14.0)
        caption_text = desc.get("caption", "")

        if not img_path.exists():
            logger.error("图片文件不存在: %s", img_path)
            return []

        _, para_xml = insert_image(unpacked_dir, img_path, width_cm=float(width))
        elems.append(make_empty_p())
        elems.append(make_image_p(para_xml))
        if caption_text:
            elems.append(make_caption(caption_text))
        elems.append(make_empty_p())
        return elems

    if ptype == "empty":
        return [make_empty_p()]

    if ptype == "figure_placeholder":
        caption = desc.get("caption", "")
        figure_type = desc.get("figure_type", "")
        fallback_text = f"（附图待补充：{caption}）" if caption else f"（附图待补充：{figure_type}）"
        logger.warning("figure_placeholder 未转换为 image（type=%s, caption=%s），降级为文字提示", figure_type, caption)
        return [make_p(fallback_text)]

    logger.warning("未知段落类型: %s", ptype)
    return []


# ============================================================
# 核心引擎
# ============================================================

def build_patent(content_path: Path, unpacked_dir: Path) -> None:
    """根据 patent_content.json 构建专利交底书。"""
    logger.info("加载内容文件: %s", content_path)
    with open(content_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    errors = validate_content(content)
    if errors:
        for err in errors:
            logger.error("校验失败: %s", err)
        sys.exit(1)
    logger.info("JSON 内容校验通过")

    work_dir = content_path.parent
    doc_path = unpacked_dir / "word" / "document.xml"
    if not doc_path.exists():
        logger.error("document.xml 不存在: %s", doc_path)
        sys.exit(1)

    # === 第一遍：清理 + 填表头 ===
    logger.info("解析 document.xml")
    tree = etree.parse(str(doc_path))
    root = tree.getroot()
    body = root.find(".//w:body", nsmap)
    if body is None:
        logger.error("document.xml 中未找到 w:body")
        sys.exit(1)

    rm_blue(body)
    rm_reminder(body)
    fill_header(root, content.get("header", {}))

    tree.write(str(doc_path), xml_declaration=True, encoding="UTF-8", standalone=True)
    logger.info("清理完成，已保存")

    # === 检查图片 ===
    sections = content.get("sections", {})
    has_images = any(
        desc.get("type") == "image"
        for paras in sections.values()
        for desc in paras
    )

    # === 插入各章节内容 ===
    logger.info("开始插入章节内容，共 %s 个 section", len(sections))

    # 图片缺失统计
    total_images = 0
    missing_images = 0
    missing_image_paths: list[str] = []
    for paras in sections.values():
        for desc in paras:
            if isinstance(desc, dict) and desc.get("type") == "image":
                total_images += 1
                img_rel_path = desc.get("path", "")
                if img_rel_path and not (work_dir / img_rel_path).exists():
                    missing_images += 1
                    missing_image_paths.append(img_rel_path)

    if missing_images:
        logger.warning("⚠️  发现 %s/%s 张图片路径不存在（将被跳过）:", missing_images, total_images)
        for mp in missing_image_paths:
            logger.warning("    ❌ %s", mp)

    tree = etree.parse(str(doc_path))
    root = tree.getroot()
    body = root.find(".//w:body", nsmap)

    for section_key, paragraphs in sections.items():
        # Use alias-based lookup for flexible section matching
        title_p = find_para_with_aliases(body, section_key)
        if title_p is None:
            logger.warning("章节标题未找到: %r", section_key)
            continue

        # 验证定位准确性：章节标题段落应为短文本（<100 字符）
        title_text = "".join(
            n.text or "" for n in title_p.findall(".//w:t", nsmap)
        )
        if len(title_text) > 150:
            logger.warning(
                "章节 %r 定位到的段落过长（%d 字符），可能误命中正文段落: %s",
                section_key, len(title_text), title_text[:80],
            )

        parent = title_p.getparent()
        if parent is None:
            parent = body

        all_elems: list[etree._Element] = []
        for desc in paragraphs:
            all_elems.extend(build_paragraph(desc, work_dir, unpacked_dir))

        if all_elems:
            insert_many_after(parent, title_p, all_elems)
            logger.info("章节 %r: 插入 %s 个段落", section_key, len(all_elems))

    tree.write(str(doc_path), xml_declaration=True, encoding="UTF-8", standalone=True)
    logger.info("document.xml 已保存")

    if has_images:
        ensure_image_namespaces(doc_path)
        logger.info("图片命名空间注入完成")

    # 构建后图片统计告警
    embedded = total_images - missing_images
    if missing_images > 0:
        logger.error("🚨 构建完成但有 %s 张图片缺失（仅嵌入 %s/%s 张）！", missing_images, embedded, total_images)
        logger.error("   请检查截图/图表是否已生成，路径是否与 patent_content.json 匹配")
    else:
        logger.info("✅ 构建完成！全部 %s 张图片已嵌入", total_images)


# ============================================================
# CLI 入口
# ============================================================

def dry_run(content_path: Path) -> None:
    """干运行模式：仅校验 patent_content.json 格式。"""
    logger.info("[dry-run] 加载内容文件: %s", content_path)
    with open(content_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    errors = validate_content(content)
    if errors:
        logger.error("[dry-run] 发现 %s 个错误:", len(errors))
        for err in errors:
            logger.error("  - %s", err)
        sys.exit(1)

    sections = content.get("sections", {})
    total_paragraphs = sum(len(p) for p in sections.values())
    type_counts: dict[str, int] = {}
    for paras in sections.values():
        for desc in paras:
            t = desc.get("type", "text") if isinstance(desc, dict) else "unknown"
            type_counts[t] = type_counts.get(t, 0) + 1

    logger.info("[dry-run] 校验通过 ✓")
    logger.info("[dry-run] header 字段数: %s", len(content.get("header", {})))
    logger.info("[dry-run] 章节数: %s", len(sections))
    logger.info("[dry-run] 段落总数: %s", total_paragraphs)
    logger.info("[dry-run] 段落类型分布: %s", type_counts)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="专利交底书构建引擎：读取 patent_content.json 构建 DOCX"
    )
    parser.add_argument("content_path", type=Path, help="patent_content.json 文件路径")
    parser.add_argument(
        "unpacked_dir", type=Path, nargs="?", default=None,
        help="解压后的 DOCX 目录路径（--dry-run 时可省略）",
    )
    parser.add_argument("--dry-run", action="store_true", help="仅校验 JSON 格式")
    args = parser.parse_args()

    if not args.content_path.exists():
        logger.error("内容文件不存在: %s", args.content_path)
        sys.exit(1)

    if args.dry_run:
        dry_run(args.content_path)
        return

    if args.unpacked_dir is None:
        logger.error("正常构建模式下 unpacked_dir 为必需参数")
        sys.exit(1)
    if not args.unpacked_dir.exists():
        logger.error("解压目录不存在: %s", args.unpacked_dir)
        sys.exit(1)

    build_patent(args.content_path, args.unpacked_dir)


if __name__ == "__main__":
    main()
