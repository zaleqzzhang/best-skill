#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""code-patent-writing 编排器。

本脚本提供四个辅助命令，供 CodeBuddy 等 AI 智能体在执行专利生成 skill 时调用：

  1. extract-context  — 从代码仓库提取上下文，输出 code_context.md
  2. init-patent-run  — 初始化 patent_run 目录结构
  3. build-docx       — 将各章节 .md 组装为标准交底书 .docx
  4. preflight        — Stage 级产出验证（硬守卫）

智能体（CodeBuddy）自身作为 LLM 完成以下工作：
  - 阶段一：读取 code_context.md，分析代码创新点，生成 ideal_output.md
  - 阶段二：按 SKILL.md 中 16 个 Stage（Stage 00-15）的指示撰写各章节 .md，输出到 patent_run 目录
  - 阶段三：生成技术图表和 UI 截图
  - 阶段四：调用 build-docx 组装交底书

用法:
    # 1. 提取代码上下文
    python scripts/orchestrate.py extract-context <repo_path> [--name "发明名称"] [--full]

    # 2. 组装 DOCX（在智能体完成撰写后调用）
    python scripts/orchestrate.py build-docx <work_dir> --name "发明名称"
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Resolve SKILL_DIR (this script's parent's parent) for asset/reference paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def _generate_run_id(name: str) -> str:
    ts = _ts()
    suffix = hashlib.sha256(name.encode()).hexdigest()[:6]
    return f"cpw-{ts}-{suffix}"


def _print_stage(stage: int, total: int, name: str, status: str = "running") -> None:
    print(f"[{stage}/{total}] {name} — {status}")


def _is_remote_git_url(path_or_url: str) -> bool:
    """判断输入是否为远程 Git 仓库 URL。"""
    s = path_or_url.strip()
    return s.startswith(("https://", "http://", "git://", "git@"))


def _repo_name_from_url(url: str) -> str:
    """从远程 Git URL 中提取仓库名（去掉 .git 后缀）。"""
    name = url.rstrip("/").rsplit("/", 1)[-1]
    if name.endswith(".git"):
        name = name[:-4]
    return name or "repo"


def _resolve_repo_source(
    repo_path_or_url: str,
    work_dir: Path,
) -> tuple[Path, bool]:
    """解析输入源：本地路径直接返回，远程 URL 则克隆到本地。"""
    if not _is_remote_git_url(repo_path_or_url):
        repo = Path(repo_path_or_url).expanduser().resolve()
        if not repo.exists():
            print(f"Error: repo path does not exist: {repo}", file=sys.stderr)
            sys.exit(1)
        return repo, False

    clone_dir = work_dir / "_cloned_repo"
    if clone_dir.exists():
        print(f"  → 已存在克隆目录，跳过重新克隆: {clone_dir}")
        return clone_dir, True

    print(f"  → 正在克隆远程仓库: {repo_path_or_url}")
    work_dir.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["git", "clone", "--depth=1", repo_path_or_url, str(clone_dir)],
            check=True, capture_output=True, text=True, timeout=120,
        )
        print(f"  ✅ 克隆完成: {clone_dir}")
    except subprocess.CalledProcessError as exc:
        print(f"Error: git clone failed: {exc.stderr}", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: git clone timed out (120s)", file=sys.stderr)
        sys.exit(1)

    return clone_dir, True


def _detect_repo_mode(repo: Path) -> str:
    """检测仓库模式：full_ownership | diff_only"""
    git_dir = repo / ".git"
    if not git_dir.exists():
        print("  📂 模式: 普通目录（无 .git）→ 整个项目视为用户自有发明")
        return "full_ownership"

    try:
        subprocess.run(
            ["git", "rev-parse", "--verify", "@{u}"],
            cwd=repo, check=True, capture_output=True, text=True, timeout=10,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        print("  📂 模式: Git 仓库（无远程追踪分支）→ 整个项目视为用户自有发明")
        return "full_ownership"

    try:
        result = subprocess.run(
            ["git", "rev-list", "@{u}..HEAD"],
            cwd=repo, check=True, capture_output=True, text=True, timeout=10,
        )
        unpushed = result.stdout.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        print("  📂 模式: Git 仓库（无法检测未推送状态）→ 整个项目视为用户自有发明")
        return "full_ownership"

    if not unpushed:
        print("  📂 模式: Git 仓库（无未推送 commit）→ 整个项目视为用户自有发明")
        return "full_ownership"

    commit_count = len(unpushed.splitlines())
    print(f"  📂 模式: Git 仓库（{commit_count} 个未推送 commit）→ 仅未推送部分视为发明")
    return "diff_only"


# ---------------------------------------------------------------------------
# LLM output prefix cleanup
# ---------------------------------------------------------------------------

_LLM_PREFIX_PATTERNS = [
    "我先读取", "我来读取", "让我先", "好的，", "好的,", "当然，", "当然,",
    "以下是", "下面是", "根据你的", "按照你的", "我已经", "我会",
    "先读取你指定的", "按其中的", "我先按照",
]


def strip_llm_prefix(content: str) -> str:
    """Strip conversational LLM prefixes and artifacts from structured output."""
    lines = content.split("\n")
    while lines:
        line = lines[0].strip()
        if not line:
            lines.pop(0)
            continue
        if any(line.startswith(p) for p in _LLM_PREFIX_PATTERNS):
            lines.pop(0)
            continue
        break
    content = "\n".join(lines)

    content = re.sub(r"```[\w]*\n.*?\n```", "", content, flags=re.DOTALL)
    content = re.sub(r"\[(?:推断|估算|inferred|N/A)\]", "", content)
    content = re.sub(r"\[代码参考:\s*[^\]]+\]", "", content)
    content = re.sub(r"\[ref:\s*[^\]]+\]", "", content)
    content = re.sub(r"\[file:\s*[^\]]+\]", "", content)
    content = re.sub(r"\n{4,}", "\n\n\n", content)
    return content.strip()


# ---------------------------------------------------------------------------
# Output validation & anti-fabrication checks
# ---------------------------------------------------------------------------

_REQUIRED_IDEAL_SECTIONS: list[tuple[str, str]] = [
    ("发明名称", "发明名称"),
    ("我的发明点", "我的发明点"),
    ("核心创新点", "核心创新点"),
    ("检索关键词", "检索关键词"),
    ("应用场景", "应用场景"),
    ("技术领域", "一、技术领域"),
    ("背景技术", "二、背景技术"),
    ("发明内容", "三、发明内容"),
    ("核心发明点详述", "3.2 核心发明点详述"),
    ("量化效果对比", "3.3 量化效果对比"),
    ("技术方案整体架构", "四、技术方案整体架构"),
    ("与现有技术的区别", "五、与现有技术的区别"),
    ("产品表现特征", "产品表现特征"),
    ("附图设计建议", "附图设计建议"),
]

_RECOMMENDED_IDEAL_SECTIONS: list[tuple[str, str]] = []

_AI_TASTE_BLACKLIST = [
    "随着", "近年来", "不断发展", "日益重要", "显著", "大幅",
    "有效", "高效", "智能化", "鲁棒性", "可扩展性", "此外",
    "从而", "进而", "综上所述", "综上", "存在诸多不足",
    "本发明具有以下有益效果", "已成为",
]


def validate_ideal_output(content: str) -> dict[str, Any]:
    """Validate ideal document structural completeness and quality."""
    content_lower = content.lower()
    missing: list[str] = []
    warnings: list[str] = []

    for search_key, display_name in _REQUIRED_IDEAL_SECTIONS:
        if search_key.lower() not in content_lower:
            missing.append(display_name)
            warnings.append(f"缺少必需章节: {display_name}")

    for search_key, display_name in _RECOMMENDED_IDEAL_SECTIONS:
        if search_key.lower() not in content_lower:
            warnings.append(f"缺少推荐章节: {display_name}（建议使用 --full 模式生成更完整的 Ideal 文档）")

    line_count = len(content.split("\n"))
    char_count = len(content)
    if line_count < 300:
        warnings.append(f"Ideal 文档行数偏少: {line_count} 行（期望 ≥ 300 行，建议使用 --full 模式）")
    if char_count < 8000:
        warnings.append(f"Ideal 文档字数偏少: {char_count} 字（期望 ≥ 8000 字）")

    innovation_count = len(re.findall(r"#{2,3}\s*创新点\s*[一二三四五六七八九十\d]", content))
    if innovation_count < 2:
        warnings.append(f"创新点数量偏少: {innovation_count}（期望 3-5 个）")
    elif innovation_count > 5:
        warnings.append(f"创新点数量过多: {innovation_count}（期望 3-5 个）")

    keyword_rows = 0
    in_keyword_section = False
    for line in content.split("\n"):
        if "检索关键词" in line:
            in_keyword_section = True
            continue
        if in_keyword_section:
            if line.strip().startswith("#"):
                in_keyword_section = False
                continue
            if (line.strip().startswith("|") and "---" not in line
                    and "中文术语" not in line and "English" not in line):
                keyword_rows += 1
    if keyword_rows < 8:
        warnings.append(f"检索关键词行数偏少: {keyword_rows}（期望 ≥ 8）")

    code_block_count = len(re.findall(r"```\w*\n", content))
    if code_block_count > 0:
        warnings.append(f"检测到 {code_block_count} 个代码块残留（专利正文不应包含代码块）")

    marker_count = len(re.findall(r"\[(?:推断|估算|inferred|N/A|代码参考:|ref:|file:)[^\]]*\]", content))
    if marker_count > 0:
        warnings.append(f"检测到 {marker_count} 个内部标记残留（如 [推断]、[代码参考: ...]）")

    return {
        "pass": len(missing) == 0,
        "missing_sections": missing,
        "warnings": warnings,
        "innovation_count": innovation_count,
        "keyword_rows": keyword_rows,
        "line_count": line_count,
        "char_count": char_count,
    }


def validate_patent_content_json(json_path: Path) -> dict[str, Any]:
    """Validate patent_content.json structure and content quality."""
    issues: list[str] = []
    content = json.loads(json_path.read_text(encoding="utf-8"))
    sections = content.get("sections", {})

    required = ["【关键术语】", "【发明构思】", "3.1", "3.2", "4.1", "4.2", "4.3"]
    for key in required:
        paras = sections.get(key, [])
        if not paras:
            issues.append(f"章节 {key!r} 为空")
        else:
            texts = [p.get("content", "") for p in paras if p.get("type") == "text"]
            if all("待填写" in t for t in texts):
                issues.append(f"章节 {key!r} 全部为占位文本")

    sec_43_text = " ".join(
        p.get("content", "") for p in sections.get("4.3", []) if p.get("type") == "text"
    )
    if len(sec_43_text) < 200:
        issues.append(f"4.3 有益效果字数不足（{len(sec_43_text)} 字 < 200 字）")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "section_count": len(sections),
        "total_paragraphs": sum(len(p) for p in sections.values()),
    }


def run_anti_fabrication_checks(
    patent_run_dir: Path,
    json_path: Path,
) -> list[str]:
    """Run anti-fabrication consistency checks on patent output."""
    issues: list[str] = []
    content = json.loads(json_path.read_text(encoding="utf-8"))
    sections = content.get("sections", {})

    key_terms_text = " ".join(
        p.get("content", "") for p in sections.get("【关键术语】", [])
        if p.get("type") == "text"
    )
    inv_text = " ".join(
        p.get("content", "") for sec_key in ["4.1", "4.2", "4.3"]
        for p in sections.get(sec_key, []) if p.get("type") == "text"
    )
    defined_terms = re.findall(r"[「【]([^」】]{2,20})[」】]", key_terms_text)
    if defined_terms:
        unused = [t for t in defined_terms if t not in inv_text]
        if unused and len(unused) > len(defined_terms) * 0.5:
            issues.append(
                f"关键术语使用率低: {len(unused)}/{len(defined_terms)} 个术语未在发明内容中使用"
            )

    all_text = " ".join(
        p.get("content", "") for sec_paras in sections.values()
        for p in sec_paras if p.get("type") == "text"
    )
    # 先模拟执行清洗（与 patent_to_json._sanitize_final_json 保持一致的三轮清洗），
    # 然后仅对清洗后仍残留的词报告问题，避免"检测能发现但清洗清不掉"的不一致。
    try:
        from patent_to_json import (
            _AI_TASTE_RE as _PTJ_AI_TASTE_RE,
            _AI_TASTE_GLOBAL_RE as _PTJ_AI_TASTE_GLOBAL_RE,
            _AI_TASTE_INSENTENCE_RE as _PTJ_AI_TASTE_INSENTENCE_RE,
        )
        simulated_clean = _PTJ_AI_TASTE_RE.sub("", all_text)
        simulated_clean = _PTJ_AI_TASTE_GLOBAL_RE.sub("", simulated_clean)
        simulated_clean = _PTJ_AI_TASTE_INSENTENCE_RE.sub("", simulated_clean)
    except ImportError:
        # 回退：无法导入时直接用原始文本检测
        simulated_clean = all_text
    found_ai_words = [w for w in _AI_TASTE_BLACKLIST if w in simulated_clean]
    if found_ai_words:
        issues.append(f"检测到 AI 味高频词（清洗后仍残留）: {', '.join(found_ai_words[:5])}")

    for sec_key, paras in sections.items():
        for i, p in enumerate(paras):
            text = p.get("content", "")
            if "待填写" in text or "待补充" in text:
                issues.append(f"占位文本: sections[{sec_key!r}][{i}]")

    return issues


# ---------------------------------------------------------------------------
# Sub-command: extract-context
# ---------------------------------------------------------------------------

def cmd_extract_context(args: argparse.Namespace) -> int:
    """子命令：从代码仓库提取上下文。"""
    # Import local repo_analyzer module
    sys.path.insert(0, str(SCRIPT_DIR))
    from repo_analyzer import extract_code_context, format_code_context_markdown

    repo_str = args.repo_path.strip()
    is_remote = _is_remote_git_url(repo_str)

    invention_name = args.name
    if not invention_name:
        if is_remote:
            invention_name = _repo_name_from_url(repo_str)
        else:
            invention_name = Path(repo_str).expanduser().resolve().name

    # Resolve repo path for default work_dir (SKILL.md: WORK_DIR = REPO_PATH/_patent_docx)
    if not is_remote:
        resolved_repo = Path(repo_str).expanduser().resolve()
    else:
        resolved_repo = None

    if args.output:
        work_dir = Path(args.output)
    elif resolved_repo and resolved_repo.is_dir():
        work_dir = resolved_repo / "_patent_docx"
    else:
        work_dir = Path.cwd() / "_patent_docx"
    work_dir.mkdir(parents=True, exist_ok=True)

    # Resolve input source
    try:
        repo, was_cloned = _resolve_repo_source(repo_str, work_dir)
    except SystemExit:
        return 1

    repo_mode = _detect_repo_mode(repo)

    print(f"code-patent-writing — 代码上下文提取")
    print(f"  Repo:      {repo}")
    if was_cloned:
        print(f"  Source:    {repo_str} (远程克隆)")
    print(f"  Mode:      {repo_mode}")
    print(f"  Name:      {invention_name}")
    print(f"  Output:    {work_dir}")
    print()

    ctx = extract_code_context(
        repo,
        full_analysis=args.full and not args.no_full,
        topic=invention_name,
    )

    # Write code_context.md
    ideal_dir = work_dir / "ideal"
    ideal_dir.mkdir(parents=True, exist_ok=True)

    md_content = format_code_context_markdown(ctx, topic=invention_name)
    context_file = ideal_dir / "code_context.md"
    context_file.write_text(md_content, encoding="utf-8")

    # Write metadata
    metadata = {
        "repo_path": str(repo),
        "repo_mode": repo_mode,
        "is_git_repo": ctx.is_git_repo,
        "has_upstream": ctx.has_upstream,
        "full_analysis": args.full and not args.no_full,
        "invention_name": invention_name,
        "context_chars": len(md_content),
    }
    metadata_file = ideal_dir / "context_metadata.json"
    metadata_file.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n✅ 代码上下文提取完成: {context_file}")
    print(f"   大小: {len(md_content):,} 字符")
    print(f"\n📝 下一步：智能体请阅读 {context_file}，按照 SKILL.md 阶段一的指示分析代码创新点，")
    print(f"   生成 {ideal_dir / 'ideal_output.md'}")

    return 0


# ---------------------------------------------------------------------------
# Deliverables assembly — 交付物汇聚
# ---------------------------------------------------------------------------

def _is_deliverable_placeholder(text: str) -> bool:
    """检测文本是否为占位文本（用于 deliverables sections 拷贝过滤）。

    与 patent_to_json.py 的 _is_placeholder_text 逻辑一致：
    HTML 注释、纯占位关键词、内容过短均视为占位。
    """
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
    # 占位关键词检测
    placeholder_re = re.compile(
        r"(?:待填写|待补充|待完善|内容待定|此处省略|待智能体填充)",
        re.IGNORECASE,
    )
    if placeholder_re.search(stripped):
        non_placeholder = placeholder_re.sub("", stripped).strip()
        if len(non_placeholder) < 100:
            return True
    return False


# sections/ 提取映射：(deliverables 内文件名, 修订 stage, 修订文件关键词, 原始 stage, 原始文件名)
_SECTION_MAP: list[tuple[str, int, str, int, str]] = [
    ("key_terms.md",         10, "key_terms",         4, "key_terms.md"),
    ("concept.md",           10, "concept",            5, "concept.md"),
    ("background.md",        10, "background",         6, "background.md"),
    ("invention_content.md", 10, "invention_content",  7, "invention_content.md"),
]


def _assemble_deliverables(
    work_dir: Path,
    patent_run_dir: Path,
    docx_path: Path,
    invention_name: str,
) -> None:
    """将最终交付物汇聚到 work_dir/deliverables/ 目录。

    在 DOCX 打包成功且验证通过后调用。DOCX 文件已直接生成在
    deliverables/ 目录中，本函数只负责汇聚其余交付物并生成 manifest.json。
    """
    deliv = work_dir / "deliverables"

    # deliverables/ 应已存在（DOCX 在里面），但确保目录存在
    deliv.mkdir(parents=True, exist_ok=True)

    # 清理旧的非 DOCX 交付物（保留刚生成的 DOCX）
    for item in list(deliv.iterdir()):
        if item.suffix.lower() == ".docx":
            continue  # 保留 DOCX
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    copied_files: list[str] = []

    def _safe_copy(src: Path, dst: Path, label: str) -> bool:
        """拷贝单个文件，失败不阻断。"""
        try:
            if src.is_file():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                copied_files.append(label)
                return True
        except OSError as exc:
            print(f"  ⚠ 拷贝 {label} 失败: {exc}")
        return False

    def _safe_copytree(src: Path, dst: Path, label: str) -> bool:
        """拷贝整个目录，失败不阻断。"""
        try:
            if src.is_dir() and any(src.iterdir()):
                shutil.copytree(src, dst, dirs_exist_ok=True)
                copied_files.append(label)
                return True
        except OSError as exc:
            print(f"  ⚠ 拷贝 {label} 失败: {exc}")
        return False

    print("\n📦 汇聚 deliverables/ ...")

    # 1. DOCX 已直接生成在 deliverables/{发明名称}.docx，无需拷贝
    docx_label = docx_path.name
    copied_files.append(docx_label)

    # 2. charts/ — 仅拷贝 PNG 技术图表（排除 .html/.js 等中间产物）
    charts_src = work_dir / "charts"
    if charts_src.is_dir():
        charts_dst = deliv / "charts"
        charts_dst.mkdir(exist_ok=True)
        for png in charts_src.glob("*.png"):
            if png.stat().st_size > 0:
                shutil.copy2(png, charts_dst / png.name)
        if any(charts_dst.iterdir()):
            copied_files.append("charts/")
    else:
        # 回退：从根目录收集独立 PNG（排除 screenshots 目录）
        charts_dst = deliv / "charts"
        charts_dst.mkdir(exist_ok=True)
        for png in work_dir.glob("*.png"):
            shutil.copy2(png, charts_dst / png.name)
        if any(charts_dst.iterdir()):
            copied_files.append("charts/")

    # 3. code/ — HTML 原型（排除空文件）
    code_src = patent_run_dir / "stage-08" / "code"
    if code_src.is_dir():
        code_dst = deliv / "code"
        code_dst.mkdir(exist_ok=True)
        for f in code_src.rglob("*"):
            if f.is_file() and f.stat().st_size > 0:
                rel = f.relative_to(code_src)
                dest = code_dst / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
        if any(code_dst.rglob("*")):
            copied_files.append("code/")

    # 4. screenshots/ — UI 截图
    screenshots_src = patent_run_dir / "stage-08" / "screenshots"
    _safe_copytree(screenshots_src, deliv / "screenshots", "screenshots/")

    # 5. sections/ — 各章节最终版 MD（优先修订版，带占位检测 + 大小比对回退）
    sections_dst = deliv / "sections"
    sections_dst.mkdir(exist_ok=True)
    for dest_name, rev_stage, rev_key, orig_stage, orig_name in _SECTION_MAP:
        # 先读取原始版大小作为参考
        orig_content = ""
        orig_file_path = None
        orig_dir = patent_run_dir / f"stage-{orig_stage:02d}"
        if orig_dir.is_dir():
            for f in orig_dir.iterdir():
                if f.is_file() and orig_name.lower() in f.name.lower():
                    orig_content = f.read_text(encoding="utf-8").strip()
                    orig_file_path = f
                    break

        # 优先查修订版（必须通过占位检测 + 大小比对）
        found = False
        rev_dir = patent_run_dir / f"stage-{rev_stage:02d}"
        if rev_dir.is_dir():
            for f in rev_dir.iterdir():
                if f.is_file() and rev_key.lower() in f.name.lower():
                    content = f.read_text(encoding="utf-8").strip()
                    if content and not _is_deliverable_placeholder(content):
                        # 大小比对：修订版明显小于原始版时回退
                        if orig_content and len(content) < len(orig_content) * 0.5:
                            print(f"  ⚠ sections/{dest_name}: 修订版仅 {len(content)} 字符"
                                  f"（原始版 {len(orig_content)} 字符），回退到原始版")
                            break  # 跳过修订版，走回退逻辑
                        shutil.copy2(f, sections_dst / dest_name)
                        found = True
                    break
        # 回退到原始版（同样做占位检测）
        if not found and orig_file_path and orig_content:
            if not _is_deliverable_placeholder(orig_content):
                shutil.copy2(orig_file_path, sections_dst / dest_name)
                found = True
    if any(sections_dst.iterdir()):
        copied_files.append("sections/")

    # 6. references.md
    refs_src = patent_run_dir / "stage-03" / "references.md"
    if not refs_src.is_file():
        # 模糊查找
        stage03 = patent_run_dir / "stage-03"
        if stage03.is_dir():
            for f in stage03.iterdir():
                if f.is_file() and "reference" in f.name.lower():
                    refs_src = f
                    break
    _safe_copy(refs_src, deliv / "references.md", "references.md")

    # 7. figure_registry.json（仅拷贝非空文件）
    fig_reg = patent_run_dir / "stage-08" / "figure_registry.json"
    if fig_reg.is_file() and fig_reg.stat().st_size > 0:
        _safe_copy(fig_reg, deliv / "figure_registry.json", "figure_registry.json")

    # 8. ideal/ — Ideal 文档及代码上下文
    ideal_src = work_dir / "ideal"
    _safe_copytree(ideal_src, deliv / "ideal", "ideal/")

    # 9. manifest.json
    manifest = {
        "pipeline": "code-patent-writing",
        "topic": invention_name,
        "files": [f for f in copied_files],
        "generated": datetime.now(timezone.utc).isoformat(),
        "notes": {
            docx_label: "专利交底书 (Word 格式，含图表)",
            "references.md": "参考文献列表",
            "charts/": "技术图表 (流程图、架构图等)",
            "code/": "产品原型 Demo 代码",
            "sections/": "各章节最终版 Markdown",
            "screenshots/": "产品交互步骤截图",
            "ideal/": "Ideal 文档、代码上下文及元数据",
            "figure_registry.json": "附图注册表 (图号↔截图↔章节映射)",
        },
    }
    manifest_path = deliv / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    copied_files.append("manifest.json")

    print(f"  → deliverables/ 汇聚完成 ({len(copied_files)} 项)")
    for item in copied_files:
        print(f"    ✓ {item}")


# ---------------------------------------------------------------------------
# Sub-command: build-docx
# ---------------------------------------------------------------------------

def cmd_build_docx(args: argparse.Namespace) -> int:
    """子命令：将 patent_run 各章节 .md 组装为 DOCX。"""
    work_dir = Path(args.work_dir).expanduser().resolve()
    if not work_dir.exists():
        print(f"Error: work_dir does not exist: {work_dir}", file=sys.stderr)
        return 1

    patent_run_dir = work_dir / "patent_run"
    if not patent_run_dir.exists():
        print(f"Error: patent_run directory not found: {patent_run_dir}", file=sys.stderr)
        return 1

    invention_name = args.name or "发明专利"

    print(f"code-patent-writing — DOCX 组装")
    print(f"  Work dir:  {work_dir}")
    print(f"  Name:      {invention_name}")

    # === 全链路前置守卫（硬守卫） ===
    force_mode = getattr(args, "force", False)
    if force_mode:
        print("\n⚠️  --force 模式: 跳过全链路前置检查")
    else:
        blocking_errors = build_docx_preflight(work_dir, patent_run_dir)
        if blocking_errors:
            return 1
    print()

    # Import local modules
    sys.path.insert(0, str(SCRIPT_DIR))
    from patent_to_json import convert_patent_sections_to_json
    from patent_builder import build_patent

    # Collect flowcharts (legacy: .mmd and flowchart*.png)
    flowcharts: list[Path] = []
    for mmd in work_dir.glob("*.mmd"):
        png_path = mmd.with_suffix(".png")
        if not png_path.exists() and shutil.which("mmdc"):
            try:
                subprocess.run(
                    ["mmdc", "-i", str(mmd), "-o", str(png_path)],
                    check=True, capture_output=True, timeout=60,
                )
                flowcharts.append(png_path)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                pass
    for png in work_dir.glob("flowchart*.png"):
        flowcharts.append(png)

    # Stage 12 (export) charts → 拷贝到 charts/ 子目录（而非根目录散落）
    charts_dir = patent_run_dir / "stage-12" / "charts"
    if charts_dir.is_dir():
        charts_dest_dir = work_dir / "charts"
        charts_dest_dir.mkdir(parents=True, exist_ok=True)
        for png in charts_dir.glob("*.png"):
            dest = charts_dest_dir / png.name
            shutil.copy2(png, dest)
            flowcharts.append(dest)

    # ------------------------------------------------------------------
    # Collect charts (技术图表) and screenshots (UI 截图)
    # ------------------------------------------------------------------
    # Load figure_registry.json for ordering and captions (if exists)
    fig_registry: list[dict] = []
    fig_reg_path = patent_run_dir / "stage-08" / "figure_registry.json"
    if fig_reg_path.is_file():
        try:
            fig_registry = json.loads(fig_reg_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            fig_registry = []

    # Build a lookup: screenshot_file -> caption_cn from registry
    _fig_captions: dict[str, str] = {}
    for entry in fig_registry:
        sf = entry.get("screenshot_file")
        if sf:
            _fig_captions[sf] = entry.get("caption_cn", "")

    # Collect tech charts from work_dir/charts/*.png
    chart_paths: list[Path] = list(flowcharts)  # start with legacy flowcharts
    _already_collected = {p.resolve() for p in chart_paths}
    charts_src_dir = work_dir / "charts"
    if charts_src_dir.is_dir():
        for png in sorted(charts_src_dir.glob("*.png")):
            if png.resolve() not in _already_collected:
                chart_paths.append(png)
                _already_collected.add(png.resolve())

    # Collect UI screenshots from patent_run/stage-08/screenshots/*.png
    screenshot_paths: list[Path] = []
    ss_dir = patent_run_dir / "stage-08" / "screenshots"
    if ss_dir.is_dir():
        ss_pngs = sorted(ss_dir.glob("*.png"))
        # Sort by figure_registry order if available
        if fig_registry:
            ordered_files = [
                e.get("screenshot_file") for e in
                sorted(fig_registry, key=lambda e: e.get("figure_num", 999))
                if e.get("screenshot_file")
            ]
            ordered_set = set(ordered_files)
            # Registry-ordered files first, then remaining by name
            for fname in ordered_files:
                p = ss_dir / fname
                if p.exists():
                    screenshot_paths.append(p)
            for p in ss_pngs:
                if p.name not in ordered_set:
                    screenshot_paths.append(p)
        else:
            screenshot_paths = ss_pngs

    if chart_paths:
        print(f"  📊 技术图表: {len(chart_paths)} 张")
    if screenshot_paths:
        print(f"  🖼️  UI 截图: {len(screenshot_paths)} 张")

    # Step 1: Convert Markdown sections to patent_content.json
    _print_stage(1, 5, "转换 MD → JSON")
    json_path = convert_patent_sections_to_json(
        run_dir=patent_run_dir,
        work_dir=work_dir,
        invention_name=invention_name,
        product_and_tech=args.product or "",
        patent_purpose=args.purpose or "原创产品功能或技术",
        flowchart_paths=chart_paths or None,
        screenshot_paths=screenshot_paths or None,
        figure_captions=_fig_captions or None,
        figure_registry=fig_registry or None,
    )

    if json_path is None or not json_path.exists():
        print("  ⚠ Failed to generate patent_content.json")
        return 1
    print(f"  → patent_content.json generated: {json_path}")

    # Step 1.5: 前置内容质量阻断（在构建 DOCX 之前检查关键章节）
    if not force_mode:
        json_validation = validate_patent_content_json(json_path)
        if not json_validation["valid"]:
            blocking_issues = [i for i in json_validation["issues"]
                               if "4.3" in i or "为空" in i or "占位文本" in i]
            if blocking_issues:
                print(f"\n❌ [GUARD] patent_content.json 内容质量不合格（阻断构建）:")
                for issue in blocking_issues:
                    print(f"    - {issue}")
                print(f"\n💡 修复建议: 请检查 Stage 09（发明内容）和 Stage 13（修订）的产出")
                return 1
            # 非阻断级问题：打印警告但继续
            print(f"  ⚠ JSON 内容质量警告:")
            for issue in json_validation["issues"]:
                print(f"    - {issue}")

    # Step 2: Unpack DOCX template
    _print_stage(2, 5, "解压模板")
    template_path = SKILL_DIR / "assets" / "发明专利技术交底书模板.docx"
    unpacked_dir = work_dir / "unpacked"

    sys.path.insert(0, str(SCRIPT_DIR / "office"))
    from unpack import unpack

    _, msg = unpack(str(template_path), str(unpacked_dir))
    print(f"  → {msg}")

    # Step 3: Build patent content into template
    _print_stage(3, 5, "构建内容")
    build_patent(json_path, unpacked_dir)
    print("  → patent_builder completed")

    # Step 4: Pack to .docx
    from pack import pack

    _print_stage(4, 5, "打包 DOCX")
    docx_name = f"{invention_name}.docx" if invention_name else "专利交底书.docx"
    # 直接输出到 deliverables/ 目录，避免根目录散落再事后拷贝
    deliv_dir = work_dir / "deliverables"
    deliv_dir.mkdir(parents=True, exist_ok=True)
    docx_path = deliv_dir / docx_name

    _, msg = pack(
        str(unpacked_dir),
        str(docx_path),
        original_file=str(template_path),
    )
    print(f"  → {msg}")

    if docx_path.exists():
        size_kb = docx_path.stat().st_size / 1024
        print(f"\n✅ DOCX output: {docx_path} ({size_kb:.1f} KB)")

        # Quality validation
        json_validation = validate_patent_content_json(json_path)
        if json_validation["valid"]:
            print(f"  ✅ JSON 结构验证通过 ({json_validation['section_count']} 章节, {json_validation['total_paragraphs']} 段落)")
        else:
            print(f"  ⚠ JSON 结构验证发现问题:")
            for issue in json_validation["issues"]:
                print(f"    - {issue}")

        fab_issues = run_anti_fabrication_checks(patent_run_dir, json_path)
        if fab_issues:
            print(f"  ⚠ 反造假检查发现 {len(fab_issues)} 个问题:")
            for issue in fab_issues[:5]:
                print(f"    - {issue}")
        else:
            print(f"  ✅ 反造假检查通过")

        print(f"\n   提醒: 请手动补充撰写人姓名、联络方式等个人信息")

        # Step 5: Assemble deliverables
        _assemble_deliverables(work_dir, patent_run_dir, docx_path, invention_name)

        # Step 6: Clean up unpacked/ intermediate directory
        if unpacked_dir.exists():
            shutil.rmtree(unpacked_dir, ignore_errors=True)
            print("  → unpacked/ 中间目录已清理")

        # Step 7: DOCX size guard (硬守卫)
        if size_kb < 200:
            print(f"\n⚠️  [GUARD] DOCX 仅 {size_kb:.1f}KB（需要 ≥200KB）")
            print("   可能原因: 截图/图表未嵌入，请检查 Stage 10/11 产出")
            return 2

        return 0
    else:
        print("\n⚠ DOCX 组装过程出现问题，请检查中间产物")
        return 1


# ---------------------------------------------------------------------------
# Sub-command: init-patent-run
# ---------------------------------------------------------------------------

def cmd_init_patent_run(args: argparse.Namespace) -> int:
    """子命令：初始化 patent_run 目录结构（供智能体填充各章节）。"""
    work_dir = Path(args.work_dir).expanduser().resolve()
    work_dir.mkdir(parents=True, exist_ok=True)

    patent_run = work_dir / "patent_run"
    patent_run.mkdir(parents=True, exist_ok=True)

    # 创建 12 个 Stage 的输出目录
    stage_dirs = {
        "stage-01": "goal_text.md",          # Stage 01: 发明范围
        "stage-02": "prior_art.md",          # Stage 02: 现有技术分析
        "stage-03": None,                     # Stage 03: 文献收集（无固定输出文件）
        "stage-04": "key_terms.md",          # Stage 04: 关键术语
        "stage-05": "concept.md",            # Stage 05: 发明构思
        "stage-06": "background.md",         # Stage 06: 背景技术
        "stage-07": "invention_content.md",  # Stage 07: 发明内容
        "stage-08": None,                     # Stage 08: UI 配图（可选）
        "stage-09": "reviews.md",            # Stage 09: 专利评审
        "stage-10": None,                     # Stage 10: 专利修订（多个 revised_*.md）
        "stage-11": "quality_report.json",   # Stage 11: 质量门禁
        "stage-12": None,                     # Stage 12: 文档组装（由 build-docx 生成）
    }

    for stage_name, default_file in stage_dirs.items():
        d = patent_run / stage_name
        d.mkdir(parents=True, exist_ok=True)
        if default_file:
            placeholder = d / default_file
            if not placeholder.exists():
                placeholder.write_text(f"<!-- {default_file} — 待智能体填充 -->\n", encoding="utf-8")

    print(f"✅ patent_run 目录结构已初始化: {patent_run}")
    print(f"   包含 {len(stage_dirs)} 个 Stage 目录")
    print(f"\n📝 下一步：智能体按 SKILL.md 阶段二的指示，逐个 Stage 填充各章节 .md 文件")

    return 0


# ---------------------------------------------------------------------------
# Preflight: Stage-level output validation (hard guards)
# ---------------------------------------------------------------------------

def _file_exists_and_min_chars(path: Path, min_chars: int) -> tuple[bool, str]:
    """Check file exists and has at least min_chars characters."""
    if not path.exists():
        return False, f"文件不存在: {path.name}"
    content = path.read_text(encoding="utf-8", errors="replace")
    if len(content) < min_chars:
        return False, f"{path.name} 仅 {len(content)} 字符（需要 ≥{min_chars}）"
    return True, ""


def _file_contains(path: Path, *markers: str) -> tuple[bool, list[str]]:
    """Check file contains all specified markers."""
    if not path.exists():
        return False, [f"文件不存在: {path.name}"]
    content = path.read_text(encoding="utf-8", errors="replace")
    missing = [m for m in markers if m not in content]
    if missing:
        return False, [f"{path.name} 缺少标记: {m}" for m in missing]
    return True, []


@dataclass
class PngCheckResult:
    """PNG 文件检查结果（结构化，取代纯文本 issue 列表）。"""
    total: int
    too_small: list[str]      # 过小文件名及描述
    duplicates: list[str]     # 内容重复文件对描述
    all_files: list[str]      # 所有 PNG 文件名


def _count_pngs(directory: Path, min_size_kb: int = 0) -> PngCheckResult:
    """Count PNGs in directory. Returns structured PngCheckResult."""
    if not directory.is_dir():
        return PngCheckResult(total=0, too_small=[], duplicates=[], all_files=[])
    pngs = sorted(directory.glob("*.png"))
    total = len(pngs)
    all_files = [p.name for p in pngs]

    # Check for too-small files
    small_issues: list[str] = []
    for p in pngs:
        sz = p.stat().st_size
        if sz < min_size_kb * 1024:
            small_issues.append(f"{p.name} 仅 {sz // 1024}KB（需要 ≥{min_size_kb}KB）")

    # Check for duplicate content using MD5 hash (not file size)
    dup_issues: list[str] = []
    seen_hashes: dict[str, str] = {}
    for p in pngs:
        file_hash = hashlib.md5(p.read_bytes()).hexdigest()
        if file_hash in seen_hashes:
            dup_issues.append(
                f"疑似重复截图: {p.name} 与 {seen_hashes[file_hash]} 内容哈希完全相同"
            )
        else:
            seen_hashes[file_hash] = p.name

    return PngCheckResult(
        total=total,
        too_small=small_issues,
        duplicates=dup_issues,
        all_files=all_files,
    )


def preflight_check_stage(
    work_dir: Path,
    stage: int,
    patent_run_dir: Path | None = None,
) -> dict[str, Any]:
    """Check whether a Stage's output satisfies its skip-conditions.

    Returns {"stage": N, "status": "PASS"|"FAIL", "missing": [...], "details": {...}}
    """
    if patent_run_dir is None:
        patent_run_dir = work_dir / "patent_run"

    missing: list[str] = []
    details: dict[str, Any] = {}

    if stage == 0:
        # Stage 00: never skip — always return FAIL to force execution
        missing.append("Stage 00 永不跳过，始终执行环境检查")

    elif stage == 1:
        p = work_dir / "ideal" / "code_context.md"
        ok, msg = _file_exists_and_min_chars(p, 1000)
        details["file"] = str(p)
        details["exists"] = p.exists()
        details["chars"] = len(p.read_text(encoding="utf-8", errors="replace")) if p.exists() else 0
        if not ok:
            missing.append(msg)
        else:
            # SKILL.md 要求：必须包含 ## 智能体语义增强 章节标题
            ok2, msgs2 = _file_contains(p, "## 智能体语义增强")
            if not ok2:
                missing.extend(msgs2)

    elif stage == 2:
        p = work_dir / "ideal" / "ideal_output.md"
        ok, msgs = _file_contains(p, "## 产品表现特征", "## 附图设计建议")
        details["file"] = str(p)
        details["exists"] = p.exists()
        if not ok:
            missing.extend(msgs)

    elif stage == 3:
        p = patent_run_dir / "stage-01" / "goal_text.md"
        ok, msg = _file_exists_and_min_chars(p, 200)
        details["file"] = str(p)
        if not ok:
            missing.append(msg)

    elif stage == 4:
        p = patent_run_dir / "stage-02" / "prior_art.md"
        ok, msg = _file_exists_and_min_chars(p, 500)
        details["file"] = str(p)
        if not ok:
            missing.append(msg)

    elif stage == 5:
        # references.md >= 5 links + web_search_results.json >= 5 results
        refs = patent_run_dir / "stage-03" / "references.md"
        wsj = patent_run_dir / "stage-03" / "web_search_results.json"
        if not refs.exists():
            missing.append("references.md 不存在")
        else:
            content = refs.read_text(encoding="utf-8", errors="replace")
            link_count = len(re.findall(r"https?://", content))
            details["ref_link_count"] = link_count
            if link_count < 8:
                missing.append(f"references.md 仅含 {link_count} 条带链接文献（需要 ≥8）")
        if not wsj.exists():
            missing.append("web_search_results.json 不存在")
        else:
            try:
                data = json.loads(wsj.read_text(encoding="utf-8"))
                results_count = len(data.get("results", []))
                details["search_results_count"] = results_count
                if results_count < 20:
                    missing.append(f"web_search_results.json 仅含 {results_count} 条结果（需要 ≥20）")
            except (json.JSONDecodeError, OSError):
                missing.append("web_search_results.json 解析失败")

    elif stage == 6:
        p = patent_run_dir / "stage-04" / "key_terms.md"
        if not p.exists():
            missing.append("key_terms.md 不存在")
        else:
            content = p.read_text(encoding="utf-8", errors="replace")
            # Count term definition paragraphs: **bold** headings or #### headings
            term_count = len(re.findall(
                r"(?:^\*\*[^*]+\*\*|^####\s+\S)",
                content, re.MULTILINE,
            ))
            # Fallback: count paragraphs separated by blank lines with substantial content
            if term_count < 3:
                paragraphs = [p.strip() for p in content.split("\n\n") if len(p.strip()) > 30]
                term_count = max(term_count, len(paragraphs))
            details["term_count"] = term_count
            if term_count < 5:
                missing.append(f"key_terms.md 仅含 {term_count} 个术语段落（需要 ≥5）")

    elif stage == 7:
        p = patent_run_dir / "stage-05" / "concept.md"
        ok, msgs = _file_contains(p, "2.1", "2.2")
        details["file"] = str(p)
        if not ok:
            missing.extend(msgs)

    elif stage == 8:
        p = patent_run_dir / "stage-06" / "background.md"
        ok, msgs = _file_contains(p, "### 3.1", "### 3.2")
        details["file"] = str(p)
        if not ok:
            missing.extend(msgs)

    elif stage == 9:
        p = patent_run_dir / "stage-07" / "invention_content.md"
        ok, msgs = _file_contains(p, "### 4.1", "### 4.2", "### 4.3")
        details["file"] = str(p)
        if not ok:
            missing.extend(msgs)

    elif stage == 10:
        ss_dir = patent_run_dir / "stage-08" / "screenshots"
        result = _count_pngs(ss_dir, min_size_kb=50)
        details["screenshots_count"] = result.total
        details["screenshots_too_small"] = len(result.too_small)

        # Dynamic minimum: read FIGURE placeholder count from invention_content.md
        min_screenshots = 10  # absolute minimum
        for inv_path in [
            patent_run_dir / "stage-07" / "invention_content.md",
            patent_run_dir / "stage-10" / "revised_invention_content.md",
        ]:
            if inv_path.exists():
                inv_text = inv_path.read_text(encoding="utf-8", errors="replace")
                placeholder_count = len(re.findall(
                    r"<!--\s*FIGURE\s*:\s*\w+\s*(?:\|[^>]*)?\s*-->", inv_text
                ))
                if placeholder_count > 0:
                    min_screenshots = max(min(placeholder_count, 14), 10)
                    details["figure_placeholder_count"] = placeholder_count
                break
        details["min_screenshots_required"] = min_screenshots

        if result.total < min_screenshots:
            missing.append(f"screenshots/ 下仅 {result.total} 张 PNG（需要 ≥{min_screenshots}）")
        if result.too_small:
            missing.extend(result.too_small)
        if result.duplicates:
            missing.extend(result.duplicates)
        # figure_registry.json
        reg = patent_run_dir / "stage-08" / "figure_registry.json"
        details["figure_registry_exists"] = reg.exists()
        if not reg.exists():
            missing.append("figure_registry.json 不存在")
        else:
            try:
                entries = json.loads(reg.read_text(encoding="utf-8"))
                types = {e.get("figure_type") for e in entries if isinstance(e, dict)}
                details["figure_types"] = sorted(types)
                if "product_output_preview" not in types:
                    missing.append("figure_registry.json 缺少 product_output_preview 类型条目")
                if "innovation_linkage" not in types:
                    missing.append("figure_registry.json 缺少 innovation_linkage 类型条目")
            except (json.JSONDecodeError, OSError):
                missing.append("figure_registry.json 解析失败")

    elif stage == 11:
        charts_dir = work_dir / "charts"
        result = _count_pngs(charts_dir, min_size_kb=30)
        details["charts_count"] = result.total
        details["charts_too_small"] = len(result.too_small)
        if result.total < 4:
            missing.append(f"charts/ 下仅 {result.total} 张 PNG（需要 ≥4）")
        if result.too_small:
            missing.extend(result.too_small)

    elif stage == 12:
        p = patent_run_dir / "stage-09" / "reviews.md"
        if not p.exists():
            missing.append("reviews.md 不存在")
        else:
            content = p.read_text(encoding="utf-8", errors="replace")
            check_marks = len(re.findall(r"[✅⚠️❌]", content))
            details["check_mark_count"] = check_marks
            if check_marks < 3:
                missing.append(f"reviews.md 仅含 {check_marks} 个检查项标记（需要 ≥3）")

    elif stage == 13:
        rev_dir = patent_run_dir / "stage-10"
        if not rev_dir.is_dir():
            missing.append("stage-10/ 目录不存在")
        else:
            revised_files = list(rev_dir.glob("revised_*.md"))
            details["revised_file_count"] = len(revised_files)
            if not revised_files:
                missing.append("stage-10/ 下无 revised_*.md 文件")
            else:
                ok_files = [f for f in revised_files
                            if len(f.read_text(encoding="utf-8", errors="replace")) >= 500]
                if not ok_files:
                    missing.append("所有 revised_*.md 文件均 <500 字符")
                # 大小比对检查：修订版不应显著小于原始版
                size_warnings: list[str] = []
                _rev_orig_map = {
                    "invention_content": ("stage-07", "invention_content.md"),
                    "background": ("stage-06", "background.md"),
                    "key_terms": ("stage-04", "key_terms.md"),
                    "concept": ("stage-05", "concept.md"),
                }
                for rev_f in revised_files:
                    rev_size = len(rev_f.read_text(encoding="utf-8", errors="replace"))
                    for rev_key, (orig_stage, orig_name) in _rev_orig_map.items():
                        if rev_key.lower() in rev_f.name.lower():
                            orig_path = patent_run_dir / orig_stage / orig_name
                            if orig_path.exists():
                                orig_size = len(orig_path.read_text(encoding="utf-8", errors="replace"))
                                details[f"revised_{rev_key}_size"] = rev_size
                                details[f"original_{rev_key}_size"] = orig_size
                                if orig_size > 0 and rev_size < orig_size * 0.8:
                                    size_warnings.append(
                                        f"{rev_f.name} 仅 {rev_size} 字符"
                                        f"（原始版 {orig_size} 字符，占比 {rev_size*100//orig_size}%）"
                                        f"——疑似增量修订而非完整替换"
                                    )
                            break
                if size_warnings:
                    details["size_warnings"] = size_warnings
                    for w in size_warnings:
                        missing.append(f"修订版大小异常: {w}")

                # 修订实质性检查：修订版不应与原始版几乎相同
                similarity_warnings: list[str] = []
                for rev_f in revised_files:
                    rev_text = rev_f.read_text(encoding="utf-8", errors="replace")
                    # 清除修订标记后比较：
                    # 1. 删除 REVISION_CHANGELOG 及后续内容
                    rev_clean = re.sub(r"===REVISION_CHANGELOG===.*", "", rev_text, flags=re.DOTALL).strip()
                    # 2. 删除 REVISED_*=== 标记行（仅删行，不删后续内容）
                    rev_clean = re.sub(r"^===REVISED_[A-Z_]+===\s*$", "", rev_clean, flags=re.MULTILINE).strip()
                    for rev_key, (orig_stage, orig_name) in _rev_orig_map.items():
                        if rev_key.lower() in rev_f.name.lower():
                            orig_path = patent_run_dir / orig_stage / orig_name
                            if orig_path.exists():
                                orig_text = orig_path.read_text(encoding="utf-8", errors="replace").strip()
                                if orig_text and rev_clean:
                                    # 按行集合比较（去除空行和前后空白）
                                    rev_lines = {l.strip() for l in rev_clean.splitlines() if l.strip()}
                                    orig_lines = {l.strip() for l in orig_text.splitlines() if l.strip()}
                                    if rev_lines and orig_lines:
                                        overlap = len(rev_lines & orig_lines)
                                        total = max(len(rev_lines), len(orig_lines))
                                        similarity = overlap / total if total > 0 else 0
                                    else:
                                        similarity = 0
                                    details[f"similarity_{rev_key}"] = round(similarity, 3)
                                    if similarity > 0.95:
                                        similarity_warnings.append(
                                            f"{rev_f.name} 与原始版相似度 {similarity:.1%}——修订未产生实质变更"
                                        )
                            break
                if similarity_warnings:
                    details["similarity_warnings"] = similarity_warnings
                    for w in similarity_warnings:
                        missing.append(f"修订实质性不足: {w}")

    elif stage == 14:
        p = patent_run_dir / "stage-11" / "quality_report.json"
        if not p.exists():
            missing.append("quality_report.json 不存在")
        else:
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                for field in ("score_1_to_10", "verdict", "dimension_scores"):
                    if field not in data:
                        missing.append(f"quality_report.json 缺少必填字段: {field}")
                details["score"] = data.get("score_1_to_10")
                details["verdict"] = data.get("verdict")
            except (json.JSONDecodeError, OSError):
                missing.append("quality_report.json 解析失败")

        # 增强检查：验证 patent_content.json 内容质量（如果已生成）
        json_path = work_dir / "patent_content.json"
        if json_path.exists():
            try:
                pdata = json.loads(json_path.read_text(encoding="utf-8"))
                sections = pdata.get("sections", {})
                # 检查 4.3 有益效果字数
                sec_43_text = " ".join(
                    p.get("content", "") for p in sections.get("4.3", [])
                    if p.get("type") == "text"
                )
                details["sec_43_chars"] = len(sec_43_text)
                if len(sec_43_text) < 200:
                    missing.append(f"4.3 有益效果仅 {len(sec_43_text)} 字符（需要 ≥200）")
                # 检查标记残留
                all_text = json.dumps(pdata, ensure_ascii=False)
                if "===REVISED_" in all_text or "===REVISION_CHANGELOG===" in all_text:
                    missing.append("patent_content.json 中残留 ===REVISED_ 或 ===REVISION_CHANGELOG=== 标记")
                # 检查占位文本
                for sec_key, paras in sections.items():
                    texts = [p.get("content", "") for p in paras if p.get("type") == "text"]
                    if texts and all("待填写" in t for t in texts):
                        missing.append(f"章节 {sec_key!r} 全部为占位文本")
            except (json.JSONDecodeError, OSError):
                pass  # patent_content.json 尚未生成，跳过

    elif stage == 15:
        deliv = work_dir / "deliverables"
        if not deliv.is_dir():
            missing.append("deliverables/ 目录不存在")
        else:
            docx_files = list(deliv.glob("*.docx"))
            if not docx_files:
                missing.append("deliverables/ 下无 .docx 文件")
            else:
                largest = max(docx_files, key=lambda f: f.stat().st_size)
                size_kb = largest.stat().st_size / 1024
                details["docx_size_kb"] = round(size_kb, 1)
                if size_kb < 200:
                    missing.append(f"DOCX 仅 {size_kb:.1f}KB（需要 ≥200KB，可能缺少图片）")

    else:
        missing.append(f"未知 Stage 编号: {stage}")

    status = "PASS" if not missing else "FAIL"

    # Generate fix_hint for FAIL cases
    fix_hint = ""
    if status == "FAIL" and stage > 0:
        _FIX_HINTS: dict[int, str] = {
            1: "重新执行 Stage 01: 运行 orchestrate.py extract-context 提取代码上下文，然后执行智能体语义增强",
            2: "重新执行 Stage 02: 阅读 code_context.md 分析创新点，生成 ideal/ideal_output.md（必须包含 '## 产品表现特征' 和 '## 附图设计建议'）",
            3: "重新执行 Stage 03: 撰写发明范围 → patent_run/stage-01/goal_text.md（≥200 字符）",
            4: "重新执行 Stage 04: 撰写现有技术分析 → patent_run/stage-02/prior_art.md（≥500 字符）",
            5: "重新执行 Stage 05: 使用 Playwright 检索文献（≥20 条原始结果），精选 ≥8 条写入 references.md，同时生成 web_search_results.json",
            6: "重新执行 Stage 06: 撰写关键术语 → patent_run/stage-04/key_terms.md（≥5 个术语定义段落）",
            7: "重新执行 Stage 07: 撰写发明构思 → patent_run/stage-05/concept.md（含 2.1 和 2.2 子节）",
            8: "重新执行 Stage 08: 撰写背景技术 → patent_run/stage-06/background.md（含 ### 3.1 和 ### 3.2）",
            9: "重新执行 Stage 09: 撰写发明内容 → patent_run/stage-07/invention_content.md（含 ### 4.1、### 4.2、### 4.3）",
            10: "重新执行 Stage 10: 1) 生成 HTML 原型并用 wc -c 验证非空；2) Playwright 截图（数量须匹配占位符）；3) 生成 figure_registry.json。注意：先写 HTML 到 $PLAYWRIGHT_DIR/ 再 cp 到目标路径",
            11: "重新执行 Stage 11: 1) 生成 charts/tech_charts.html 并用 wc -c 验证非空；2) Playwright 元素级截图 4 张（≥30KB/张）。注意：先写 HTML 到 $PLAYWRIGHT_DIR/ 再 cp 到目标路径",
            12: "重新执行 Stage 12: 执行 16 项专利评审，生成 reviews.md（含 ≥3 个 ✅/⚠️/❌ 标记）",
            13: "重新执行 Stage 13: 根据评审意见修订各章节，生成 revised_*.md（每个文件须为完整替换，≥原文 80%）",
            14: "重新执行 Stage 14: 执行质量门禁评估，生成 quality_report.json（含 score_1_to_10、verdict、dimension_scores）",
            15: "重新执行 Stage 15: 运行 orchestrate.py build-docx 组装 DOCX（deliverables/ 下须有 ≥200KB 的 .docx）",
        }
        fix_hint = _FIX_HINTS.get(stage, f"请检查并修复 Stage {stage:02d} 的产出")

    return {"stage": stage, "status": status, "missing": missing, "details": details, "fix_hint": fix_hint}


# ---------------------------------------------------------------------------
# build-docx preflight: full pipeline guard
# ---------------------------------------------------------------------------

# Stage → severity mapping for build-docx preflight
_BUILD_GUARD_ERROR_STAGES = {1, 2, 9, 10, 11}  # Must pass or build-docx refuses
_BUILD_GUARD_WARN_STAGES = {3, 4, 5, 6, 7, 8, 12, 13, 14}  # Print warning but continue


def build_docx_preflight(
    work_dir: Path,
    patent_run_dir: Path,
) -> list[str]:
    """Full pipeline preflight before build-docx. Returns blocking errors."""
    errors: list[str] = []
    warnings: list[str] = []

    print("\n🔍 [PREFLIGHT] build-docx 全链路前置检查...")

    for stage_num in range(1, 15):
        result = preflight_check_stage(work_dir, stage_num, patent_run_dir)
        if result["status"] == "FAIL":
            prefix = f"  Stage {stage_num:02d}"
            if stage_num in _BUILD_GUARD_ERROR_STAGES:
                for m in result["missing"]:
                    errors.append(f"{prefix} [ERROR]: {m}")
            else:
                for m in result["missing"]:
                    warnings.append(f"{prefix} [WARN]:  {m}")

    if warnings:
        print("\n⚠️  [PREFLIGHT] 发现非阻断级问题:")
        for w in warnings:
            print(w)

    if errors:
        print("\n❌ [PREFLIGHT] 发现阻断级问题（build-docx 拒绝执行）:")
        for e in errors:
            print(e)
        print("\n💡 修复建议: 请先完成上述缺失的 Stage，再重新运行 build-docx")
        print("   或使用 --force 参数跳过检查（降级模式）")
    else:
        print("\n✅ [PREFLIGHT] 全链路检查通过")

    return errors


# ---------------------------------------------------------------------------
# Sub-command: preflight
# ---------------------------------------------------------------------------

def cmd_preflight(args: argparse.Namespace) -> int:
    """子命令：preflight — Stage 产出验证。"""
    work_dir = Path(args.work_dir).expanduser().resolve()
    if not work_dir.exists():
        print(f"Error: work_dir does not exist: {work_dir}", file=sys.stderr)
        return 1

    patent_run_dir = work_dir / "patent_run"

    if args.all:
        # Full pipeline scan
        results = []
        for stage_num in range(0, 16):
            results.append(preflight_check_stage(work_dir, stage_num, patent_run_dir))
        print(json.dumps(results, ensure_ascii=False, indent=2))
        failed = [r for r in results if r["status"] == "FAIL"]
        return 1 if failed else 0
    else:
        result = preflight_check_stage(work_dir, args.stage, patent_run_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "PASS" else 1


# ---------------------------------------------------------------------------
# Sub-command: verify-write — 文件写入验证
# ---------------------------------------------------------------------------

def verify_write(
    file_path: Path,
    min_size: int = 1,
    check_json: bool = False,
    check_md_markers: list[str] | None = None,
    check_png_min_kb: int = 0,
) -> dict[str, Any]:
    """Verify a file write was successful. Returns structured JSON result.

    Checks performed (in order):
    1. File exists
    2. File size >= min_size bytes
    3. (Optional) JSON parse validity
    4. (Optional) Markdown markers present
    5. (Optional) PNG minimum KB size
    """
    result: dict[str, Any] = {
        "file": str(file_path),
        "status": "FAIL",
        "checks": [],
        "fix_hint": "",
    }

    # Check 1: existence
    if not file_path.exists():
        result["checks"].append({"check": "exists", "pass": False, "detail": "文件不存在"})
        result["fix_hint"] = f"文件不存在，请重新写入: {file_path.name}"
        return result
    result["checks"].append({"check": "exists", "pass": True})

    # Check 2: min size
    actual_size = file_path.stat().st_size
    result["size_bytes"] = actual_size
    if actual_size < min_size:
        result["checks"].append({
            "check": "min_size",
            "pass": False,
            "detail": f"文件仅 {actual_size} 字节（需要 ≥{min_size}）",
        })
        result["fix_hint"] = (
            f"文件过小（{actual_size}B < {min_size}B），可能写入失败。"
            f"建议先写到 $PLAYWRIGHT_DIR/{file_path.name}，用 wc -c 确认后再 cp 到目标路径"
        )
        return result
    result["checks"].append({"check": "min_size", "pass": True, "detail": f"{actual_size} 字节"})

    # Check 3: JSON validity
    if check_json:
        try:
            content = file_path.read_text(encoding="utf-8")
            json.loads(content)
            result["checks"].append({"check": "json_parse", "pass": True})
        except (json.JSONDecodeError, OSError) as exc:
            result["checks"].append({
                "check": "json_parse",
                "pass": False,
                "detail": f"JSON 解析失败: {exc}",
            })
            result["fix_hint"] = f"JSON 格式错误，请检查并重写: {file_path.name}"
            return result

    # Check 4: Markdown markers
    if check_md_markers:
        try:
            content = file_path.read_text(encoding="utf-8")
            missing_markers = [m for m in check_md_markers if m not in content]
            if missing_markers:
                result["checks"].append({
                    "check": "md_markers",
                    "pass": False,
                    "detail": f"缺少标记: {', '.join(missing_markers)}",
                })
                result["fix_hint"] = f"文件缺少必需结构标记: {', '.join(missing_markers)}"
                return result
            result["checks"].append({"check": "md_markers", "pass": True})
        except OSError as exc:
            result["checks"].append({
                "check": "md_markers",
                "pass": False,
                "detail": f"读取失败: {exc}",
            })
            return result

    # Check 5: PNG minimum KB
    if check_png_min_kb > 0:
        size_kb = actual_size / 1024
        if size_kb < check_png_min_kb:
            result["checks"].append({
                "check": "png_min_kb",
                "pass": False,
                "detail": f"PNG 仅 {size_kb:.1f}KB（需要 ≥{check_png_min_kb}KB）",
            })
            result["fix_hint"] = (
                f"PNG 文件过小（{size_kb:.1f}KB），内容可能为空白或渲染失败。"
                f"请检查 HTML 源文件是否非空，重新执行 Playwright 截图"
            )
            return result
        result["checks"].append({"check": "png_min_kb", "pass": True, "detail": f"{size_kb:.1f}KB"})

    # All checks passed
    result["status"] = "PASS"
    return result


def cmd_verify_write(args: argparse.Namespace) -> int:
    """子命令：verify-write — 验证文件写入是否成功。"""
    file_path = Path(args.file).expanduser().resolve()

    # Parse optional MD markers
    md_markers: list[str] | None = None
    if args.md_markers:
        md_markers = [m.strip() for m in args.md_markers.split(",") if m.strip()]

    result = verify_write(
        file_path=file_path,
        min_size=args.min_size,
        check_json=args.json,
        check_md_markers=md_markers,
        check_png_min_kb=args.png_min_kb,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="orchestrate",
        description="code-patent-writing: 智能体驱动的专利交底书生成辅助工具",
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # extract-context
    p_ctx = subparsers.add_parser("extract-context", help="从代码仓库提取上下文")
    p_ctx.add_argument("repo_path", help="代码仓库本地路径或远程 Git URL")
    p_ctx.add_argument("--name", "-n", default="", help="发明名称")
    p_ctx.add_argument("--output", "-o", default=None, help="输出目录")
    p_ctx.add_argument("--full", action="store_true", default=True,
                        help="启用完整代码分析（AST+依赖图，默认开启）")
    p_ctx.add_argument("--no-full", action="store_true", help="禁用完整代码分析")

    # init-patent-run
    p_init = subparsers.add_parser("init-patent-run", help="初始化 patent_run 目录结构")
    p_init.add_argument("work_dir", help="专利工作目录路径")

    # build-docx
    p_docx = subparsers.add_parser("build-docx", help="将各章节 .md 组装为 DOCX")
    p_docx.add_argument("work_dir", help="专利工作目录路径")
    p_docx.add_argument("--name", "-n", default="", help="发明名称")
    p_docx.add_argument("--product", default="", help="涉及的产品和技术")
    p_docx.add_argument("--purpose", default="原创产品功能或技术", help="专利保护目的")
    p_docx.add_argument("--force", action="store_true",
                        help="跳过全链路前置检查（降级模式）")

    # preflight
    p_pre = subparsers.add_parser("preflight", help="Stage 产出验证（硬守卫）")
    p_pre.add_argument("work_dir", help="专利工作目录路径")
    p_pre.add_argument("--stage", "-s", type=int, default=None, help="检查指定 Stage（0-15）")
    p_pre.add_argument("--all", "-a", action="store_true", help="检查全部 Stage（0-15）")

    # verify-write
    p_vw = subparsers.add_parser("verify-write", help="验证文件写入是否成功")
    p_vw.add_argument("file", help="要验证的文件路径")
    p_vw.add_argument("--min-size", type=int, default=1,
                       help="最小文件大小（字节），默认 1")
    p_vw.add_argument("--json", action="store_true",
                       help="验证 JSON 格式合法性")
    p_vw.add_argument("--md-markers", default=None,
                       help="验证 Markdown 包含指定标记（逗号分隔），如 '### 4.1,### 4.2'")
    p_vw.add_argument("--png-min-kb", type=int, default=0,
                       help="验证 PNG 文件最小 KB 数（如 50 表示 ≥50KB）")

    args = parser.parse_args(argv)

    if args.command == "extract-context":
        return cmd_extract_context(args)
    elif args.command == "init-patent-run":
        return cmd_init_patent_run(args)
    elif args.command == "build-docx":
        return cmd_build_docx(args)
    elif args.command == "preflight":
        if args.stage is None and not args.all:
            print("Error: preflight 需要 --stage N 或 --all 参数", file=sys.stderr)
            return 1
        return cmd_preflight(args)
    elif args.command == "verify-write":
        return cmd_verify_write(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
