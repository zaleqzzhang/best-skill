#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将专利 pipeline 输出的各章节 Markdown 文件转换为 patent_content.json。

patent pipeline 的各 stage 输出为 Markdown 格式：
  - Stage 04 (stage-04/) key_terms.md          → 【关键术语】
  - Stage 05 (stage-05/) concept.md            → 【发明构思】
  - Stage 06 (stage-06/) background.md         → 【背景技术】(3.1 + 3.2)
  - Stage 07 (stage-07/) invention_content.md  → 【发明内容】(4.1 + 4.2 + 4.3)
  - Stage 03 (stage-03/) references.md         → 参考文献（优先；回退查找 stage-12）

本脚本解析这些文件，按 patent_content.json 的 schema 组装声明式 JSON，
喂给 patent_builder.py 写入 DOCX 模板。

用法:
    python patent_to_json.py --run-dir <patent_run_dir> --work-dir <work_dir> [options]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Markdown 解析工具
# ---------------------------------------------------------------------------

def _read_file(path: Path) -> str:
    """安全读取文件内容。"""
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8").strip()
    return ""


def _split_md_sections(text: str, level: int = 3) -> dict[str, str]:
    """按 Markdown 标题层级拆分为 {标题: 内容} 映射。

    level=3 表示按 ### 拆分，level=2 表示按 ## 拆分。
    """
    prefix = "#" * level
    pattern = re.compile(rf"^{prefix}\s+(.+)$", re.MULTILINE)
    sections: dict[str, str] = {}

    matches = list(pattern.finditer(text))
    if not matches:
        return {"": text}

    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        sections[title] = content

    return sections


def _md_to_paragraphs(text: str) -> list[dict[str, Any]]:
    """将 Markdown 文本转为 patent_content.json 段落列表。

    识别以下模式：
    - 空行 → empty 段落
    - 以 **加粗** 开头的行 → heading 段落
    - 普通文本 → text 段落
    """
    if not text.strip():
        return []

    paragraphs: list[dict[str, Any]] = []
    lines = text.split("\n")
    current_block: list[str] = []

    def _flush_block() -> None:
        if current_block:
            block_text = "\n".join(current_block).strip()
            if block_text:
                # Check if it's a heading-like paragraph (starts with **bold**)
                if re.match(r"^\*\*[^*]+\*\*", block_text) and len(block_text) < 100:
                    # Strip markdown bold markers for heading
                    clean = re.sub(r"\*\*([^*]+)\*\*", r"\1", block_text)
                    paragraphs.append({"type": "heading", "content": clean})
                else:
                    # Handle inline images: split text by ![alt](url)
                    parts = re.split(r"(!\[[^\]]*\]\([^)]+\))", block_text)
                    for part in parts:
                        part = part.strip()
                        if not part:
                            continue
                        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", part)
                        if m:
                            caption = m.group(1).strip()
                            path = m.group(2).strip()
                            paragraphs.append({
                                "type": "image",
                                "path": path,
                                "caption": caption,
                                "width": 14
                            })
                        else:
                            clean = _clean_md_text(part)
                            if clean:
                                paragraphs.append({"type": "text", "content": clean})
            current_block.clear()

    # Regex for FIGURE placeholder: <!-- FIGURE:figure_type | caption -->
    _figure_placeholder_re = re.compile(
        r"^<!--\s*FIGURE\s*:\s*(\w+)\s*(?:\|\s*(.+?)\s*)?-->$"
    )

    for line in lines:
        stripped = line.strip()

        if not stripped:
            _flush_block()
            # Don't add too many empty paragraphs in a row
            if paragraphs and paragraphs[-1].get("type") != "empty":
                paragraphs.append({"type": "empty"})
            continue

        # FIGURE placeholder: <!-- FIGURE:figure_type | caption -->
        m_fig = _figure_placeholder_re.match(stripped)
        if m_fig:
            _flush_block()
            paragraphs.append({
                "type": "figure_placeholder",
                "figure_type": m_fig.group(1).strip(),
                "caption": (m_fig.group(2) or "").strip(),
            })
            continue

        # Markdown sub-heading (#### level) → heading paragraph
        if stripped.startswith("####"):
            _flush_block()
            heading_text = stripped.lstrip("#").strip()
            paragraphs.append({"type": "heading", "content": heading_text})
            continue

        current_block.append(line)

    _flush_block()

    # Remove trailing empty paragraphs
    while paragraphs and paragraphs[-1].get("type") == "empty":
        paragraphs.pop()

    return paragraphs


def _clean_md_text(text: str) -> str:
    """清理 Markdown 格式标记，保留纯文本。"""
    # Remove bold markers
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    # Remove italic markers
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    # Remove inline code
    text = re.sub(r"`([^`]+)`", r"\1", text)
    # Remove markdown links [text](url) → text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Remove image references ![alt](url)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", "", text)
    # Clean up multiple spaces
    text = re.sub(r"  +", " ", text)
    return text.strip()


def _extract_section_by_pattern(text: str, pattern: str) -> str:
    """从文本中提取匹配特定模式的章节内容。"""
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip() if match.lastindex else match.group(0).strip()
    return ""


# ---------------------------------------------------------------------------
# 5 策略子节提取（从 _patent.py 的 _extract_numbered_subsection 移植）
# ---------------------------------------------------------------------------

def _extract_numbered_subsection(md_text: str, number: str) -> str:
    """提取编号子节内容（如 4.1 / 4.2 / 3.1），支持 5 种匹配策略。

    策略优先级：
    1. ### 或 ## 标准标题（最可靠）
    2. #### 四级标题
    3. **加粗** 标题（如 **3.1 xxx**）
    4. 裸数字开头（如 3.1 xxx）
    5. 首节无标题回退（仅适用于 x.1 编号）
    """
    if not md_text.strip():
        return ""
    esc = re.escape(number)

    # Build a negative lookahead prefix to exclude sub-numbering of the
    # current section.  For example, when extracting "4.2", we must NOT
    # let the lookahead match "#### 4.2.1" — that is a *child* heading,
    # not the *next sibling* heading.  We only want to stop at a heading
    # whose number is a different sibling (e.g. "### 4.3") or a different
    # parent (e.g. "## 5").
    #
    # The trick: require that the digit sequence after ## does NOT start
    # with the current number followed by a dot (which would be a child).
    # We use a negative lookahead (?!{esc}\.) right after \s* in the
    # termination pattern.
    _not_child = rf"(?!{esc}\.)"

    # Strategy 1: ## / ### / #### heading (2-4 个 # 号)
    # 注意：##{{1,3}} 在 f-string 中实际匹配 ##, ###, ####（即 2-4 个 #），
    # 这是有意设计——覆盖常见的二级、三级、四级标题写法
    #
    # 前瞻修复：排除当前编号的子编号标题（如提取 4.2 时不被 #### 4.2.1 截断）
    m = re.search(
        rf"(?ms)^##{{1,3}}\s*{esc}[^\n]*\n(.*?)(?=^##{{1,3}}\s*{_not_child}\d+\.\d+|\Z)",
        md_text,
    )
    if m and m.group(1).strip():
        return m.group(1).strip()

    # Strategy 2: #### heading
    m = re.search(
        rf"(?ms)^####\s*{esc}[^\n]*\n(.*?)(?=^####?\s*{_not_child}\d+\.\d+|^###?\s*{_not_child}\d+\.\d+|\Z)",
        md_text,
    )
    if m and m.group(1).strip():
        return m.group(1).strip()

    # Strategy 3: **bold** heading
    m = re.search(
        rf"(?ms)^\*\*{esc}[^\n]*\*\*\s*\n(.*?)(?=^\*\*{_not_child}\d+\.\d+[^\n]*\*\*|^##{{1,4}}\s*{_not_child}\d+\.\d+|\Z)",
        md_text,
    )
    if m and m.group(1).strip():
        return m.group(1).strip()

    # Strategy 4: bare number at line start
    m = re.search(
        rf"(?ms)^{esc}\s+[^\n]+\n(.*?)(?=^{_not_child}\d+\.\d+\s+|\Z)",
        md_text,
    )
    if m and m.group(1).strip():
        return m.group(1).strip()

    # Strategy 5: headingless first subsection (e.g. 3.1 content before ### 3.2)
    if number.endswith(".1"):
        prefix = number.rsplit(".", 1)[0]
        next_num = f"{prefix}.2"
        next_esc = re.escape(next_num)
        m5 = re.search(
            rf"(?ms)^(?:##{{1,4}}\s*{next_esc}|\*\*{next_esc})",
            md_text,
        )
        if m5:
            candidate = md_text[:m5.start()].strip()
            if candidate:
                return candidate

    return ""


# ---------------------------------------------------------------------------
# 占位文本检测和子节质量验证
# ---------------------------------------------------------------------------

_PLACEHOLDER_RE = re.compile(
    r"(?:待填写|待补充|待完善|内容待定|此处省略|内容同前|参见原文|详见上文|"
    r"此处.*?省略|此处.*?不再.*?赘述|内容.*?同前|参见.*?原文|详见.*?上文)",
    re.IGNORECASE,
)


def _is_placeholder_text(text: str) -> bool:
    """检测文本是否为占位文本而非实质内容。"""
    if not text or not text.strip():
        return True
    stripped = text.strip()
    # HTML 注释占位（如 <!-- xxx 待智能体填充 -->）
    if stripped.startswith("<!--") and stripped.endswith("-->"):
        return True
    # 纯 HTML 注释后剩余内容太少
    no_comments = re.sub(r"<!--.*?-->", "", stripped, flags=re.DOTALL).strip()
    if not no_comments or len(no_comments) < 30:
        return True
    if _PLACEHOLDER_RE.search(stripped):
        non_placeholder = _PLACEHOLDER_RE.sub("", stripped).strip()
        if len(non_placeholder) < 100:
            return True
    return False


def _validate_subsection_length(
    text: str, number: str, *, min_len: int = 80
) -> bool:
    """验证子节内容是否达到最低长度要求。"""
    if not text or len(text.strip()) < min_len:
        return False
    return not _is_placeholder_text(text)


# ---------------------------------------------------------------------------
# 修订标记清洗（===REVISED_*=== 和 ===REVISION_CHANGELOG===）
# ---------------------------------------------------------------------------

_REVISION_MARKER_RE = re.compile(
    r"^===REVISED_[A-Z_]+===\s*$", re.MULTILINE,
)

_CHANGELOG_RE = re.compile(
    r"^===REVISION_CHANGELOG===.*", re.MULTILINE | re.DOTALL,
)


def _clean_revision_markers(text: str) -> str:
    """清洗修订阶段产出的分隔标记和变更日志尾部。

    Stage 13 修订输出会在文件开头添加 ===REVISED_KEY_TERMS=== 等标记行，
    并在文件末尾附加 ===REVISION_CHANGELOG=== + 变更日志。
    这些标记不应进入最终的 patent_content.json。
    """
    if not text:
        return text
    # 1. 删除 ===REVISION_CHANGELOG=== 及其后的所有内容
    text = _CHANGELOG_RE.sub("", text)
    # 2. 删除 ===REVISED_*=== 标记行
    text = _REVISION_MARKER_RE.sub("", text)
    # 3. 清理多余空行
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


# ---------------------------------------------------------------------------
# 增量修订检测与合并（防止修订增量覆盖完整内容）
# ---------------------------------------------------------------------------

def _is_incremental_revision(revised_text: str, original_text: str) -> bool:
    """判断修订版是否为增量修订（而非完整全文替换）。

    判定逻辑：
    1. 统计 ===REVISED_ 标记出现次数
       - >= 2 个标记 → 增量（多标记意味着只包含部分章节的拼接片段）
       - 单标记 → 进入步骤 2
    2. 单标记情况下，清除标记后计算净内容长度
       - 净长度 >= 原文 80% → 全文替换（非增量）
       - 净长度 < 原文 80% → 增量
    3. 无标记时，仅按文本大小比对
       - 文本大小 < 原文 80% → 增量
    """
    if not revised_text or not original_text:
        return False

    # 统计修订标记出现次数
    marker_count = len(_REVISION_MARKER_RE.findall(revised_text))

    if marker_count >= 2:
        # 多个修订标记 → 增量（只包含部分章节的拼接片段）
        return True

    if marker_count == 1:
        # 单标记：清除标记和 changelog 后计算净内容长度
        clean_text = _clean_revision_markers(revised_text)
        if len(clean_text) >= len(original_text) * 0.8:
            # 净长度 >= 80% → 全文替换（非增量）
            return False
        # 净长度 < 80% → 增量
        return True

    # 无标记：按文本大小比对
    if len(revised_text) < len(original_text) * 0.8:
        return True
    return False


def _merge_revised_into_original(
    original_text: str,
    revised_text: str,
    section_numbers: tuple[str, ...] = ("4.1", "4.2", "4.3"),
) -> str:
    """将增量修订中的子节精确替换到原始全文中。

    遍历 section_numbers，对每个编号：
    - 从 revised_text 提取该子节内容
    - 如果非空且非占位，替换 original_text 中对应子节
    - 否则保留原始子节
    返回合并后的完整文本。
    """
    # 先清洗修订标记
    cleaned_revised = _clean_revision_markers(revised_text)
    if not cleaned_revised:
        return original_text

    merged = original_text
    merge_count = 0

    # 尝试按 S 步骤合并（如 S3、S4 等修订）
    s_pattern = re.compile(r"\bS(\d+)\b")
    s_matches = s_pattern.findall(cleaned_revised)

    if s_matches:
        # 修订中提到了具体 S 步骤，尝试逐步替换
        for s_num in s_matches:
            s_key = f"S{s_num}"
            # 从修订中提取该步骤的修订说明
            step_pattern = re.compile(
                rf"{s_key}\s+(?:步骤中|中)[，,]?\s*(.*?)(?=\n\n|S\d+\s+步骤|S\d+\s+中|===|$)",
                re.DOTALL,
            )
            m = step_pattern.search(cleaned_revised)
            if m:
                merge_count += 1

    # 尝试按子节编号合并（如 4.1、4.2、4.3）
    for number in section_numbers:
        revised_section = _extract_numbered_subsection(cleaned_revised, number)
        if revised_section and not _is_placeholder_text(revised_section):
            original_section = _extract_numbered_subsection(merged, number)
            if original_section and len(revised_section) > len(original_section) * 0.3:
                merged = merged.replace(original_section, revised_section)
                merge_count += 1

    if merge_count > 0:
        print(f"  🔀 [MERGE] 合并了 {merge_count} 个修订子节到原始全文")
    else:
        print(f"  ⚠️  [MERGE] 未能提取到可合并的子节，保留原始全文")

    return merged


# ---------------------------------------------------------------------------
# 章节读取与转换
# ---------------------------------------------------------------------------

def _find_stage_file(run_dir: Path, stage_num: int, filename: str) -> Path | None:
    """在 pipeline run 目录中查找 stage 输出文件。"""
    # Try standard path first
    path = run_dir / f"stage-{stage_num:02d}" / filename
    if path.exists():
        return path

    # Try with different stage numbering patterns
    for d in run_dir.iterdir():
        if d.is_dir() and d.name.startswith(f"stage-{stage_num:02d}"):
            candidate = d / filename
            if candidate.exists():
                return candidate

    return None


def _read_revised_or_original(
    run_dir: Path, original_stage: int, original_file: str, revised_key: str
) -> str:
    """优先读取修订后的内容（Stage 10, stage-10），回退到原始内容。

    修订版文件必须通过占位文本检测（非占位、非 HTML 注释）才会被采用，
    否则回退到原始阶段的文件。

    增量修订防护：当修订版为增量片段（含 ===REVISED_ 标记或大小显著偏小）时，
    自动与原始全文做子节级合并，避免完整内容被增量覆盖。
    """
    # Read original first (needed for incremental detection)
    original_text = ""
    orig_path = _find_stage_file(run_dir, original_stage, original_file)
    if orig_path:
        original_text = _read_file(orig_path)

    # Check for revised version in stage-10 (Stage 10 专利修订)
    revised_dir = run_dir / "stage-10"
    if revised_dir.exists():
        for f in revised_dir.iterdir():
            if f.is_file() and revised_key.lower() in f.name.lower():
                revised_content = _read_file(f)
                if revised_content and not _is_placeholder_text(revised_content):
                    # 增量修订检测与合并
                    if original_text and _is_incremental_revision(revised_content, original_text):
                        print(f"  🔍 [MERGE] 检测到增量修订: {f.name}"
                              f" ({len(revised_content)} 字符 vs 原始 {len(original_text)} 字符)")
                        merged = _merge_revised_into_original(original_text, revised_content)
                        return _clean_revision_markers(merged)
                    # 完整全文替换：直接使用修订版
                    return _clean_revision_markers(revised_content)
                break  # 找到匹配文件但内容无效，跳出循环

    # Fall back to original
    if original_text:
        return _clean_revision_markers(original_text)

    return ""


def _parse_background(text: str) -> tuple[list[dict], list[dict]]:
    """解析背景技术，拆分为 3.1 和 3.2 两部分。

    优先使用 5 策略子节提取，回退到 ### 标题匹配。
    """
    section_31: list[dict] = []
    section_32: list[dict] = []

    # Try enhanced extraction first (5 strategies)
    bg_31 = _extract_numbered_subsection(text, "3.1")
    bg_32 = _extract_numbered_subsection(text, "3.2")

    if bg_31 and not _is_placeholder_text(bg_31):
        section_31 = _md_to_paragraphs(bg_31)
    if bg_32 and not _is_placeholder_text(bg_32):
        section_32 = _md_to_paragraphs(bg_32)

    if section_31 and section_32:
        return section_31, section_32

    # Fallback: split by ### headings with keyword matching
    # (only for sub-sections that were NOT already extracted above)
    parts = _split_md_sections(text, level=3)

    for title, content in parts.items():
        title_lower = title.lower()
        if not section_31 and ("3.1" in title_lower or "相关背景" in title or "现有技术的技术方案" in title):
            section_31 = _md_to_paragraphs(content)
        elif not section_32 and ("3.2" in title_lower or "缺点" in title or "尚未解决" in title):
            section_32 = _md_to_paragraphs(content)

    # If 3.1 extraction fails but 3.2 succeeds, use portion before 3.2
    if not section_31 and section_32 and bg_32 and bg_32 in text:
        pos = text.find(bg_32)
        if pos > 0:
            section_31 = _md_to_paragraphs(text[:pos].strip())

    # Last fallback: put everything in 3.1
    if not section_31 and not section_32:
        section_31 = _md_to_paragraphs(text)

    return section_31, section_32


def _parse_invention_content(text: str) -> tuple[list[dict], list[dict], list[dict]]:
    """解析发明内容，拆分为 4.1、4.2、4.3 三部分。

    优先使用 5 策略子节提取，回退到 ### 和 ## 标题匹配。
    含占位文本检测和自动回退。
    """
    section_41: list[dict] = []
    section_42: list[dict] = []
    section_43: list[dict] = []

    # Try enhanced extraction first (5 strategies)
    inv_41 = _extract_numbered_subsection(text, "4.1")
    inv_42 = _extract_numbered_subsection(text, "4.2")
    inv_43 = _extract_numbered_subsection(text, "4.3")

    if inv_41 and not _is_placeholder_text(inv_41):
        section_41 = _md_to_paragraphs(inv_41)
    if inv_42 and not _is_placeholder_text(inv_42):
        section_42 = _md_to_paragraphs(inv_42)
    if inv_43 and not _is_placeholder_text(inv_43):
        section_43 = _md_to_paragraphs(inv_43)

    if section_41 and section_42 and section_43:
        return section_41, section_42, section_43

    # If 4.1 fails but 4.2 succeeds, use portion before 4.2 as 4.1
    if not section_41 and inv_42 and inv_42 in text:
        pos = text.find(inv_42)
        if pos > 0:
            section_41 = _md_to_paragraphs(text[:pos].strip())

    # If some sub-sections are still empty, try fallback strategies
    # Fallback: ### heading matching (only for empty sub-sections)
    if not section_41 or not section_42 or not section_43:
        parts = _split_md_sections(text, level=3)
        for title, content in parts.items():
            title_lower = title.lower()
            if not section_41 and ("4.1" in title_lower or "产品侧" in title):
                section_41 = _md_to_paragraphs(content)
            elif not section_42 and ("4.2" in title_lower or "技术侧" in title):
                section_42 = _md_to_paragraphs(content)
            elif not section_43 and ("4.3" in title_lower or "有益效果" in title):
                section_43 = _md_to_paragraphs(content)

    # Fallback: ## level matching (only for still-empty sub-sections)
    if not section_41 or not section_42 or not section_43:
        parts = _split_md_sections(text, level=2)
        for title, content in parts.items():
            title_lower = title.lower()
            if not section_41 and ("4.1" in title_lower or "产品" in title):
                section_41 = _md_to_paragraphs(content)
            elif not section_42 and ("4.2" in title_lower or "技术" in title):
                section_42 = _md_to_paragraphs(content)
            elif not section_43 and ("4.3" in title_lower or "效果" in title):
                section_43 = _md_to_paragraphs(content)

    # Last fallback: put everything in 4.2
    if not section_41 and not section_42 and not section_43:
        section_42 = _md_to_paragraphs(text)

    return section_41, section_42, section_43


# ---------------------------------------------------------------------------
# 最终 JSON 兜底清洗（幂等）
# ---------------------------------------------------------------------------

_FINAL_MARKER_RE = re.compile(
    r"===(?:REVISED_[A-Z_]+|REVISION_CHANGELOG)===.*",
    re.DOTALL,
)

_MD_HEADING_RE = re.compile(r"^#{1,6}\s+.+$")

# AI 味高频词黑名单（与 orchestrate.py 保持一致）
_AI_TASTE_BLACKLIST = [
    "随着", "近年来", "不断发展", "日益重要", "显著", "大幅",
    "有效", "高效", "智能化", "鲁棒性", "可扩展性", "此外",
    "从而", "进而", "综上所述", "综上", "存在诸多不足",
    "本发明具有以下有益效果", "已成为",
]

# --- 第一组：可全局安全删除的词（独立使用无歧义，任何位置都是 AI 套话） ---
_AI_TASTE_GLOBAL_WORDS = [
    "随着", "近年来", "不断发展", "日益重要", "大幅",
    "智能化", "鲁棒性", "可扩展性", "综上所述", "综上",
    "存在诸多不足", "本发明具有以下有益效果", "已成为",
]

# --- 第二组：需上下文判断的修饰词（句中也需清除，但需避免误删技术术语） ---
# 如"有效期""有效值"等不应被删除，通过负向前瞻排除
_AI_TASTE_MODIFIER_WORDS = ["显著", "有效", "高效", "此外", "从而", "进而"]

# 构建第一组正则：全局删除（不要求句首/标点前置）
_AI_TASTE_GLOBAL_RE = re.compile(
    r"(?:" + "|".join(re.escape(w) for w in _AI_TASTE_GLOBAL_WORDS) + r")(?:，|,)?\s*",
)

# 构建句首/标点后正则：仅包含第一组词（第二组由 _AI_TASTE_INSENTENCE_RE 带负向前瞻处理）
_AI_TASTE_RE = re.compile(
    r"(?:^|(?<=。)|(?<=，)|(?<=,)|(?<=；))\s*(?:" +
    "|".join(re.escape(w) for w in _AI_TASTE_GLOBAL_WORDS) +
    r")(?:，|,)?\s*",
)

# 构建第二组正则：句中修饰词清除
# "显著" / "大幅" 在句中作修饰时直接删除（如"效果显著提升"→"效果提升"）
# "有效" 需排除"有效期""有效值""有效位"等技术术语
_AI_TASTE_INSENTENCE_RE = re.compile(
    r"显著(?:地|的)?|"
    r"有效(?!期|值|位|数|载荷|负载|面积|长度|功率|带宽|容量)(?:地|的)?|"
    r"高效(?:地|的)?|"
    r"此外(?:，|,)\s*|"
    r"从而(?:，|,)?\s*|"
    r"进而(?:，|,)?\s*",
)


def _sanitize_final_json(
    content: dict[str, Any], *, invention_name: str = ""
) -> dict[str, Any]:
    """对组装完成的 patent_content.json 做最终清洗（幂等操作）。

    清洗内容：
    1. 遍历所有 sections 的段落，清除 ===REVISED_xxx=== 和
       ===REVISION_CHANGELOG=== 残留（含 changelog 后续文本）
    2. 删除 content 为空或仅含标记/标题行的段落
    3. 清除 Markdown 标题行（# xxx）残留
    4. 自动填充 header 中的「（待填写）」字段
    5. 删除连续的 empty 段落（保留最多 1 个）
    """
    # --- Header 自动填充 ---
    header = content.get("header", {})
    if header.get("交底书名称") in ("", "（待填写）") and invention_name:
        header["交底书名称"] = invention_name
    if header.get("本发明涉及产品和技术") in ("", "（待填写）") and invention_name:
        header["本发明涉及产品和技术"] = f"{invention_name}相关产品和技术"

    # --- 段落级清洗 ---
    sections = content.get("sections", {})
    for sec_key, paras in sections.items():
        cleaned: list[dict[str, Any]] = []
        for para in paras:
            if para.get("type") not in ("text", "heading"):
                cleaned.append(para)
                continue

            text: str = para.get("content", "")

            # 清除 ===REVISED_xxx=== / ===REVISION_CHANGELOG=== 及后续内容
            text = _FINAL_MARKER_RE.sub("", text).strip()

            # 清除 AI 味高频词（三轮清洗，幂等：多次执行结果一致）
            # 第一轮：原有正则（句首/标点后）
            text = _AI_TASTE_RE.sub("", text).strip()
            # 第二轮：全局安全删除（任何位置）
            text = _AI_TASTE_GLOBAL_RE.sub("", text).strip()
            # 第三轮：句中修饰词清除（如"效果显著提升"→"效果提升"）
            text = _AI_TASTE_INSENTENCE_RE.sub("", text).strip()

            # 清除 Markdown 标题行残留（如 "# 关键术语"）
            if _MD_HEADING_RE.match(text):
                continue  # 跳过纯标题行段落

            # 跳过空段落
            if not text:
                continue

            para = {**para, "content": text}
            cleaned.append(para)

        # 删除连续 empty 段落（保留最多 1 个）
        deduped: list[dict[str, Any]] = []
        for para in cleaned:
            if para.get("type") == "empty":
                if deduped and deduped[-1].get("type") == "empty":
                    continue  # 跳过连续 empty
            deduped.append(para)

        # 删除首尾的 empty 段落
        while deduped and deduped[0].get("type") == "empty":
            deduped.pop(0)
        while deduped and deduped[-1].get("type") == "empty":
            deduped.pop()

        sections[sec_key] = deduped

    return content


# ---------------------------------------------------------------------------
# 核心转换函数
# ---------------------------------------------------------------------------

def convert_patent_sections_to_json(
    run_dir: Path,
    work_dir: Path,
    *,
    invention_name: str = "",
    product_and_tech: str = "",
    patent_purpose: str = "原创产品功能或技术",
    flowchart_paths: list[Path] | None = None,
    screenshot_paths: list[Path] | None = None,
    figure_captions: dict[str, str] | None = None,
    figure_registry: list[dict] | None = None,
) -> Path | None:
    """将 patent pipeline 各章节 .md 转换为 patent_content.json。

    Parameters
    ----------
    run_dir : patent pipeline 的 run 目录
    work_dir : 专利工作目录（输出 patent_content.json）
    invention_name : 发明名称
    product_and_tech : 涉及的产品和技术
    patent_purpose : 专利保护目的
    flowchart_paths : 技术图表 PNG 文件路径列表（插入 section 4.2）
    screenshot_paths : UI 截图 PNG 文件路径列表（插入 section 4.1）
    figure_captions : 文件名 → 中文图注映射（来自 figure_registry.json）
    figure_registry : figure_registry.json 的完整条目列表（含 placeholder_index）

    Returns
    -------
    patent_content.json 文件路径
    """
    # Read sections from pipeline output
    # Prefer revised versions (Stage 10, stage-10) over originals
    key_terms_text = _read_revised_or_original(run_dir, 4, "key_terms.md", "key_terms")
    concept_text = _read_revised_or_original(run_dir, 5, "concept.md", "concept")
    background_text = _read_revised_or_original(run_dir, 6, "background.md", "background")
    invention_text = _read_revised_or_original(run_dir, 7, "invention_content.md", "invention_content")

    # References — check multiple possible stage locations
    # Stage 03 (文献检索阶段) or Stage 12 (legacy export 阶段)
    references_path = None
    for stage_num in (3, 12):
        references_path = _find_stage_file(run_dir, stage_num, "references.md")
        if references_path:
            break
    references_text = _read_file(references_path) if references_path else ""

    # 参考文献 DOI 格式校验
    if references_text:
        suspicious_dois = re.findall(r"10\.\d{4}/[^\s,)]+", references_text)
        for doi in suspicious_dois:
            # 检测尾部数字过于规整的可疑 DOI（如 102345, 103456）
            m = re.search(r"(\d{5,})$", doi)
            if m and len(set(m.group(1))) <= 6 and int(m.group(1)) % 11111 < 2:
                print(f"  ⚠️  [GUARD] 可疑 DOI（尾部数字过于规整）: {doi}")

    # 参考文献数量守卫：检查引用是否充足
    if not references_text or len(references_text.strip()) < 50:
        print("  ⚠️  [GUARD] 参考文献为空！请先执行 Stage 05 文献检索")
    else:
        # 统计带链接的引用数量（http 开头的行或含 http 的行）
        ref_link_count = len(re.findall(r"https?://", references_text))
        if ref_link_count < 3:
            print(f"  ⚠️  [GUARD] 参考文献仅含 {ref_link_count} 条带链接引用（要求 ≥3），请补充文献")
        elif ref_link_count < 5:
            print(f"  ⚠️  [GUARD] 参考文献含 {ref_link_count} 条带链接引用（建议 ≥5）")

    # Also check patent_draft.md for any missing sections
    draft_path = _find_stage_file(run_dir, 12, "patent_draft.md")
    draft_text = _read_file(draft_path) if draft_path else ""

    # If individual sections are empty, try extracting from the full draft
    if not key_terms_text and draft_text:
        match = re.search(r"(?:关键术语|第[一1]章).*?\n(.*?)(?=\n#{1,3}\s|$)", draft_text, re.DOTALL)
        if match:
            key_terms_text = match.group(1).strip()

    if not concept_text and draft_text:
        match = re.search(r"(?:发明构思|第[二2]章).*?\n(.*?)(?=\n#{1,3}\s|$)", draft_text, re.DOTALL)
        if match:
            concept_text = match.group(1).strip()

    # Build sections
    key_terms_paras = _md_to_paragraphs(key_terms_text) if key_terms_text else [{"type": "text", "content": "（待填写）"}]
    concept_paras = _md_to_paragraphs(concept_text) if concept_text else [{"type": "text", "content": "（待填写）"}]

    section_31, section_32 = _parse_background(background_text) if background_text else ([], [])
    if not section_31:
        section_31 = [{"type": "text", "content": "（待填写）"}]
    if not section_32:
        section_32 = [{"type": "text", "content": "（待填写）"}]

    section_41, section_42, section_43 = _parse_invention_content(invention_text) if invention_text else ([], [], [])
    if not section_41:
        section_41 = [{"type": "text", "content": "（待填写）"}]
    if not section_42:
        section_42 = [{"type": "text", "content": "（待填写）"}]
    if not section_43:
        section_43 = [{"type": "text", "content": "（待填写）"}]

    # Add flowcharts / tech charts to section 4.2 (技术侧)
    if flowchart_paths:
        _captions = figure_captions or {}
        for i, fc_path in enumerate(flowchart_paths):
            # Use relative path from work_dir
            try:
                rel_path = fc_path.relative_to(work_dir)
            except ValueError:
                rel_path = fc_path.name
            caption = _captions.get(fc_path.name, "")
            if not caption:
                caption = f"图{i + 1} 技术方案流程图" if len(flowchart_paths) == 1 else f"图{i + 1} 技术方案图{i + 1}"
            section_42.append({"type": "empty"})
            section_42.append({
                "type": "image",
                "path": str(rel_path),
                "width": 14,
                "caption": caption,
            })

    # Add UI screenshots to section 4.1 (产品侧)
    # ── 硬守卫：基于 figure_registry 确定性注入（不依赖 LLM 自律）──
    #
    # 优先使用新版联动模式（FIGURE 占位符 + figure_registry）：
    #   Stage 09 在 invention_content.md 中写 <!-- FIGURE:type | caption -->
    #   Stage 10 按需截图，figure_registry.json 中 placeholder_index 与占位符一一对应
    #   Stage 15（这里）根据 placeholder_index 精确替换占位符为实际图片
    #
    # 兼容旧版模式：如果没有 figure_placeholder 但有 inline images，走旧版路径修正

    _registry = figure_registry or []
    _captions = figure_captions or {}
    has_figure_placeholders = any(
        p.get("type") == "figure_placeholder" for p in section_41
    )
    has_inline_images = any(p.get("type") == "image" for p in section_41)

    if has_figure_placeholders and _registry:
        # ━━ 新版联动模式：figure_placeholder → 确定性注入 ━━
        # Build placeholder_index → registry entry mapping
        _idx_to_entry: dict[int, dict] = {}
        for entry in _registry:
            pidx = entry.get("placeholder_index")
            if pidx is not None:
                _idx_to_entry[pidx] = entry

        # Build screenshot_file → relative path mapping
        _ss_relpath: dict[str, str] = {}
        if screenshot_paths:
            for ss_p in screenshot_paths:
                try:
                    _ss_relpath[ss_p.name] = str(ss_p.relative_to(work_dir))
                except ValueError:
                    _ss_relpath[ss_p.name] = str(
                        Path("patent_run") / "stage-08" / "screenshots" / ss_p.name
                    )

        # Replace each figure_placeholder with the actual image
        placeholder_idx = 0
        injected_count = 0
        missing_count = 0
        new_section_41: list[dict[str, Any]] = []

        for para in section_41:
            if para.get("type") != "figure_placeholder":
                new_section_41.append(para)
                continue

            entry = _idx_to_entry.get(placeholder_idx)
            if entry:
                ss_file = entry.get("screenshot_file")
                rel_path = _ss_relpath.get(ss_file or "", "")

                if rel_path and (work_dir / rel_path).exists():
                    caption = entry.get("caption_cn", "") or para.get("caption", "")
                    new_section_41.append({"type": "empty"})
                    new_section_41.append({
                        "type": "image",
                        "path": rel_path,
                        "width": 14,
                        "caption": caption,
                    })
                    injected_count += 1
                else:
                    # Screenshot file missing on disk
                    print(f"  ⚠️  [GUARD] 占位符 #{placeholder_idx} 对应的截图文件不存在: {ss_file}")
                    missing_count += 1
                    # Keep the placeholder caption as text fallback
                    cap = para.get("caption", "")
                    if cap:
                        new_section_41.append({"type": "text", "content": f"（附图待补充：{cap}）"})
            else:
                # No registry entry for this placeholder index
                print(f"  ⚠️  [GUARD] 占位符 #{placeholder_idx} (type={para.get('figure_type')}) 在 figure_registry 中无对应条目")
                missing_count += 1
                cap = para.get("caption", "")
                if cap:
                    new_section_41.append({"type": "text", "content": f"（附图待补充：{cap}）"})

            placeholder_idx += 1

        section_41 = new_section_41

        if injected_count:
            print(f"  ✅ [GUARD] 确定性注入了 {injected_count} 张产品侧截图（基于 figure_registry 占位符联动）")
        if missing_count:
            print(f"  ⚠️  [GUARD] {missing_count} 个占位符未能匹配截图")

    elif has_inline_images and screenshot_paths:
        # ━━ 兼容旧版：修正 LLM inline image 路径 ━━
        _ss_name_to_relpath: dict[str, str] = {}
        for ss_p in screenshot_paths:
            try:
                _ss_name_to_relpath[ss_p.name] = str(ss_p.relative_to(work_dir))
            except ValueError:
                _ss_name_to_relpath[ss_p.name] = str(
                    Path("patent_run") / "stage-08" / "screenshots" / ss_p.name
                )

        _keyword_to_name: dict[str, str] = {}
        for name in _ss_name_to_relpath:
            m_kw = re.match(r"step_\d+_fig_(.+)\.png$", name, re.IGNORECASE)
            if m_kw:
                _keyword_to_name[m_kw.group(1).lower()] = name

        fixed_count = 0
        for para in section_41:
            if not isinstance(para, dict) or para.get("type") != "image":
                continue
            orig_path = para.get("path", "")
            full_path = work_dir / orig_path
            if full_path.exists():
                continue

            basename = Path(orig_path).name
            if basename in _ss_name_to_relpath:
                para["path"] = _ss_name_to_relpath[basename]
                fixed_count += 1
                continue

            m_kw2 = re.match(r"step_\d+_fig_(.+)\.png$", basename, re.IGNORECASE)
            if m_kw2:
                keyword = m_kw2.group(1).lower()
                if keyword in _keyword_to_name:
                    para["path"] = _ss_name_to_relpath[_keyword_to_name[keyword]]
                    fixed_count += 1
                    continue

            caption = para.get("caption", "")
            if caption and _captions:
                for fname, fcap in _captions.items():
                    if caption in fcap or fcap in caption:
                        if fname in _ss_name_to_relpath:
                            para["path"] = _ss_name_to_relpath[fname]
                            fixed_count += 1
                            break

        if fixed_count:
            print(f"  🔧 [GUARD] 修正了 {fixed_count} 个产品侧截图路径（旧版 inline image 兼容模式）")

        broken = [
            p for p in section_41
            if isinstance(p, dict)
            and p.get("type") == "image"
            and not (work_dir / p.get("path", "")).exists()
        ]
        if broken:
            print(f"  ⚠️  [GUARD] 仍有 {len(broken)} 个产品侧截图路径无法匹配:")
            for b in broken:
                print(f"      ❌ {b.get('path')}")

    elif screenshot_paths:
        # ━━ 回退：无占位符也无 inline images，追加到末尾 ━━
        section_41.append({"type": "empty"})
        section_41.append({"type": "heading", "content": "附图展示"})
        for i, ss_path in enumerate(screenshot_paths):
            try:
                rel_path = ss_path.relative_to(work_dir)
            except ValueError:
                rel_path = Path("patent_run") / "stage-08" / "screenshots" / ss_path.name
            caption = _captions.get(ss_path.name, "")
            if not caption:
                caption = f"图{i + 1} 产品交互截图"
            section_41.append({"type": "empty"})
            section_41.append({
                "type": "image",
                "path": str(rel_path),
                "width": 14,
                "caption": caption,
            })

    # References
    references_paras = _md_to_paragraphs(references_text) if references_text else [{"type": "text", "content": "无"}]

    # Assemble patent_content.json (交底书标准 8 章节)
    # Auto-fill header fields: use invention_name to derive missing values
    header_name = invention_name or "（待填写）"
    header_product = product_and_tech
    if not header_product or header_product == "（待填写）":
        # Derive from invention_name if available
        header_product = f"{invention_name}相关产品和技术" if invention_name else "（待填写）"

    content: dict[str, Any] = {
        "header": {
            "交底书名称": header_name,
            "本发明涉及产品和技术": header_product,
            "专利保护的目的": patent_purpose,
        },
        "sections": {
            "【关键术语】": key_terms_paras,
            "【发明构思】": concept_paras,
            "3.1": section_31,
            "3.2": section_32,
            "4.1": section_41,
            "4.2": section_42,
            "4.3": section_43,
            "参考文献": references_paras,
        },
    }

    # ── 全 section figure_placeholder → image 转换（补充产品侧之外的其他章节） ──
    # 产品侧（section_41）的占位符已在前面处理，这里处理技术侧等其他 section 中
    # 残留的 figure_placeholder（如 4.2 技术侧中引用的架构图、流程图等）
    _all_ss_relpath: dict[str, str] = {}
    if screenshot_paths:
        for ss_p in screenshot_paths:
            try:
                _all_ss_relpath[ss_p.name] = str(ss_p.relative_to(work_dir))
            except ValueError:
                _all_ss_relpath[ss_p.name] = str(
                    Path("patent_run") / "stage-08" / "screenshots" / ss_p.name
                )

    # Build charts filename lookup: figure_type → charts/*.png path
    _charts_type_to_path: dict[str, str] = {}
    charts_dir = work_dir / "charts"
    if charts_dir.is_dir():
        _chart_type_map = {
            "tech_architecture": "system_architecture.png",
            "tech_flowchart": "technical_flowchart.png",
            "tech_sequence": "module_sequence.png",
            "tech_dataflow": "data_flow_diagram.png",
            "flow_overview": "data_flow_diagram.png",
        }
        for ftype, fname in _chart_type_map.items():
            chart_path = charts_dir / fname
            if chart_path.exists():
                try:
                    _charts_type_to_path[ftype] = str(chart_path.relative_to(work_dir))
                except ValueError:
                    _charts_type_to_path[ftype] = f"charts/{fname}"
        # Also index by actual filename stem for flexible matching
        for png in charts_dir.glob("*.png"):
            stem = png.stem.lower()
            for ftype in ("tech_architecture", "tech_flowchart", "tech_sequence", "tech_dataflow", "flow_overview"):
                if ftype.replace("tech_", "") in stem or stem in ftype:
                    if ftype not in _charts_type_to_path:
                        try:
                            _charts_type_to_path[ftype] = str(png.relative_to(work_dir))
                        except ValueError:
                            _charts_type_to_path[ftype] = f"charts/{png.name}"

    _global_registry = figure_registry or []
    _global_idx_to_entry: dict[int, dict] = {}
    for entry in _global_registry:
        pidx = entry.get("placeholder_index")
        if pidx is not None:
            _global_idx_to_entry[pidx] = entry

    global_placeholder_idx = 0
    global_injected = 0
    global_missing = 0
    sections = content.get("sections", {})
    for sec_key, paras in sections.items():
        new_paras: list[dict[str, Any]] = []
        for para in paras:
            if para.get("type") != "figure_placeholder":
                new_paras.append(para)
                continue

            # Try registry-based injection
            entry = _global_idx_to_entry.get(global_placeholder_idx)
            injected = False

            if entry:
                ss_file = entry.get("screenshot_file")
                rel_path = _all_ss_relpath.get(ss_file or "", "") if ss_file else ""

                if rel_path and (work_dir / rel_path).exists():
                    caption = entry.get("caption_cn", "") or para.get("caption", "")
                    new_paras.append({"type": "empty"})
                    new_paras.append({
                        "type": "image",
                        "path": rel_path,
                        "width": 14,
                        "caption": caption,
                    })
                    global_injected += 1
                    injected = True

            # Fallback: try charts directory for tech figure types
            if not injected:
                fig_type = para.get("figure_type", "")
                chart_rel = _charts_type_to_path.get(fig_type, "")
                if chart_rel and (work_dir / chart_rel).exists():
                    caption = para.get("caption", "")
                    if entry:
                        caption = entry.get("caption_cn", "") or caption
                    new_paras.append({"type": "empty"})
                    new_paras.append({
                        "type": "image",
                        "path": chart_rel,
                        "width": 14,
                        "caption": caption,
                    })
                    global_injected += 1
                    injected = True

            if not injected:
                global_missing += 1
                cap = para.get("caption", "")
                if cap:
                    new_paras.append({"type": "text", "content": f"（附图待补充：{cap}）"})

            global_placeholder_idx += 1

        sections[sec_key] = new_paras

    if global_injected:
        print(f"  ✅ [GUARD] 全局确定性注入了 {global_injected} 张图片（跨所有 section）")
    if global_missing:
        print(f"  ⚠️  [GUARD] {global_missing} 个占位符未能匹配图片")

    # Final sanitization pass: clean up any residual markers, placeholders, etc.
    content = _sanitize_final_json(content, invention_name=invention_name)

    # Write JSON
    json_path = work_dir / "patent_content.json"
    json_path.write_text(
        json.dumps(content, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Print summary and detect quality issues
    total_paras = sum(len(p) for p in content["sections"].values())
    type_counts: dict[str, int] = {}
    placeholder_sections: list[str] = []
    for sec_key, paras in content["sections"].items():
        for desc in paras:
            t = desc.get("type", "text")
            type_counts[t] = type_counts.get(t, 0) + 1
        # Check for placeholder-only sections
        texts = [p.get("content", "") for p in paras if p.get("type") == "text"]
        if texts and all("待填写" in t or "待补充" in t for t in texts):
            placeholder_sections.append(sec_key)

    print(f"  patent_content.json: {len(content['sections'])} sections, {total_paras} paragraphs")
    print(f"  段落类型: {type_counts}")

    if placeholder_sections:
        print(f"  ⚠ 以下章节仅含占位文本: {', '.join(placeholder_sections)}")

    return json_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="将 patent pipeline 输出转换为 patent_content.json"
    )
    parser.add_argument("--run-dir", type=Path, required=True, help="patent pipeline run 目录")
    parser.add_argument("--work-dir", type=Path, required=True, help="输出工作目录")
    parser.add_argument("--name", default="", help="发明名称")
    parser.add_argument("--product", default="", help="涉及的产品和技术")
    parser.add_argument("--purpose", default="原创产品功能或技术", help="专利保护目的")
    parser.add_argument("--flowchart", type=Path, nargs="*", default=[], help="流程图 PNG 路径")

    args = parser.parse_args(argv)

    result = convert_patent_sections_to_json(
        run_dir=args.run_dir,
        work_dir=args.work_dir,
        invention_name=args.name,
        product_and_tech=args.product,
        patent_purpose=args.purpose,
        flowchart_paths=args.flowchart or None,
    )

    if result and result.exists():
        print(f"✅ {result}")
        return 0
    print("❌ 转换失败")
    return 1


if __name__ == "__main__":
    sys.exit(main())
