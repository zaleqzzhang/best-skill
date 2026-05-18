#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""代码仓库上下文提取工具 — 纯 Python stdlib 模块。

提供 extract_code_context() 入口函数，从本地代码仓库（Git 或普通目录）
提取结构化的代码上下文，输出为 code_context.md 文件供智能体分析。

功能：
  - Git 上下文：未推送 commit、diff 统计、完整 diff、变更文件代码
  - 目录上下文：目录树、入口文件、核心代码摘要
  - AST 分析：函数/类签名索引（Python 文件）
  - 模块依赖图：内部 import 关系分析
  - 文档摘要：README 和 Markdown 文件

用法（CLI）：
    python repo_analyzer.py <repo_path> [--output <output_dir>] [--full]

用法（Python API）：
    from repo_analyzer import extract_code_context
    ctx = extract_code_context("/path/to/repo", full_analysis=True)
"""

from __future__ import annotations

import ast
import json
import logging
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_FILE_EXT_WHITELIST: set[str] = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".java", ".kt", ".swift",
    ".c", ".cpp", ".h", ".rs", ".md", ".txt", ".yaml", ".yml", ".json",
    ".toml", ".cfg", ".ini", ".sh",
}

_DIR_BLACKLIST: set[str] = {
    "node_modules", ".venv", "venv", "__pycache__", ".git", ".tox",
    "dist", "build", ".egg-info", ".mypy_cache", ".pytest_cache",
    ".next", ".nuxt", "target", "vendor",
}

_MAX_TOTAL_CONTEXT_CHARS: int = 30_000

_ENTRY_FILE_NAMES: tuple[str, ...] = (
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "package.json",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "Makefile",
    "CMakeLists.txt",
    "requirements.txt",
    "Pipfile",
)

# ---------------------------------------------------------------------------
# Data class
# ---------------------------------------------------------------------------

@dataclass
class CodeContext:
    """从代码仓库提取的上下文信息。"""

    repo_path: str
    is_git_repo: bool
    # Git mode fields
    unpushed_commits: str = ""
    full_diff: str = ""
    diff_stat: str = ""
    has_upstream: bool = False
    has_unpushed: bool = False
    # Non-git mode fields
    dir_tree: str = ""
    entry_files: str = ""
    # Shared fields
    doc_excerpts: str = ""
    code_excerpts: str = ""
    # Full analysis fields (--full mode)
    ast_signatures: str = ""
    import_graph: str = ""
    test_coverage_hints: str = ""


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def _run_git(
    repo_path: Path,
    args: list[str],
    *,
    timeout: int = 15,
) -> str:
    """Run a git command in the given repo and return stdout, or empty string on failure."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path)] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        logger.warning(
            "git %s failed (exit %d): %s",
            " ".join(args[:2]),
            result.returncode,
            result.stderr.strip()[:200],
        )
        return ""
    except subprocess.TimeoutExpired:
        logger.warning("git %s timed out after %ds", " ".join(args[:2]), timeout)
        return ""
    except FileNotFoundError:
        logger.warning("git not found on PATH")
        return ""
    except Exception as exc:
        logger.warning("git command failed: %s", exc)
        return ""


def _has_upstream(repo_path: Path, *, timeout: int = 15) -> bool:
    """Check whether the current branch has an upstream tracking branch."""
    result = _run_git(repo_path, ["rev-parse", "--abbrev-ref", "@{u}"], timeout=timeout)
    return bool(result)


def _collect_recent_commits(
    repo_path: Path,
    *,
    max_commits: int = 30,
    timeout: int = 15,
) -> str:
    """Get recent *unpushed* commit messages as one-line summaries."""
    if _has_upstream(repo_path, timeout=timeout):
        return _run_git(
            repo_path,
            ["log", "@{u}..HEAD", "--oneline", f"-n{max_commits}", "--no-decorate"],
            timeout=timeout,
        )
    else:
        logger.info("No upstream set for %s — treating all commits as local invention", repo_path)
        return _run_git(
            repo_path,
            ["log", "--oneline", f"-n{max_commits}", "--no-decorate"],
            timeout=timeout,
        )


def _collect_diff_summary(
    repo_path: Path,
    *,
    timeout: int = 15,
) -> str:
    """Get file-change statistics for unpushed commits."""
    if _has_upstream(repo_path, timeout=timeout):
        return _run_git(repo_path, ["diff", "@{u}..HEAD", "--stat"], timeout=timeout)
    else:
        return _run_git(repo_path, ["diff", "HEAD~10..HEAD", "--stat"], timeout=timeout)


def _collect_full_diff(
    repo_path: Path,
    *,
    max_chars: int = 60_000,
    timeout: int = 30,
) -> str:
    """Get full diff code details for unpushed commits."""
    if _has_upstream(repo_path, timeout=timeout):
        raw = _run_git(repo_path, ["diff", "@{u}..HEAD"], timeout=timeout)
    else:
        raw = _run_git(repo_path, ["diff", "HEAD~20..HEAD"], timeout=timeout)
    if not raw:
        return ""
    if len(raw) > max_chars:
        return raw[:max_chars] + f"\n\n... (diff truncated, total {len(raw)} chars) ..."
    return raw


# ---------------------------------------------------------------------------
# File scanning helpers
# ---------------------------------------------------------------------------

def _collect_doc_excerpts(
    repo_path: Path,
    *,
    max_docs: int = 5,
    max_chars_per_doc: int = 2000,
) -> str:
    """Scan for Markdown files in repo root and first-level subdirectories."""
    md_files: list[Path] = []
    for md in sorted(repo_path.glob("*.md")):
        if md.is_file():
            md_files.append(md)
    for subdir in sorted(repo_path.iterdir()):
        if subdir.is_dir() and not subdir.name.startswith("."):
            for md in sorted(subdir.glob("*.md")):
                if md.is_file():
                    md_files.append(md)

    seen: set[Path] = set()
    ordered: list[Path] = []
    for f in md_files:
        resolved = f.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        ordered.append(f)

    def _readme_priority(p: Path) -> tuple[int, str]:
        name_lower = p.name.lower()
        return (0, name_lower) if "readme" in name_lower else (1, name_lower)

    ordered.sort(key=_readme_priority)
    ordered = ordered[:max_docs]

    excerpts: list[str] = []
    for md_path in ordered:
        try:
            content = md_path.read_text(encoding="utf-8", errors="replace")
            truncated = content[:max_chars_per_doc]
            if len(content) > max_chars_per_doc:
                truncated += "\n\n... (内容已截断) ..."
            rel_path = md_path.relative_to(repo_path)
            excerpts.append(f"### {rel_path}\n\n{truncated}")
        except (OSError, ValueError) as exc:
            logger.debug("Failed to read %s: %s", md_path, exc)
    return "\n\n---\n\n".join(excerpts)


def _collect_file_excerpts(
    dir_path: Path,
    *,
    max_files: int = 15,
    max_chars_per_file: int = 2000,
    max_total_chars: int = _MAX_TOTAL_CONTEXT_CHARS,
    max_depth: int = 3,
) -> str:
    """Scan code and doc files recursively (up to *max_depth*)."""
    candidates: list[Path] = []

    def _scan_recursive(d: Path, current_depth: int = 0) -> None:
        if current_depth > max_depth:
            return
        try:
            for entry in sorted(d.iterdir()):
                if entry.name.startswith("."):
                    continue
                if entry.is_file() and entry.suffix.lower() in _FILE_EXT_WHITELIST:
                    candidates.append(entry)
                elif entry.is_dir() and entry.name not in _DIR_BLACKLIST:
                    _scan_recursive(entry, current_depth + 1)
        except PermissionError:
            pass

    _scan_recursive(dir_path)

    seen: set[Path] = set()
    unique: list[Path] = []
    for f in candidates:
        resolved = f.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(f)

    def _priority(p: Path) -> tuple[int, str]:
        name_lower = p.name.lower()
        rel_str = str(p.relative_to(dir_path)).lower()
        if name_lower in ("main.py", "app.py", "cli.py", "__init__.py",
                          "index.ts", "index.js", "server.py", "manage.py"):
            return (0, name_lower)
        if "readme" in name_lower:
            return (1, name_lower)
        if p.suffix.lower() in (".py", ".ts", ".js", ".go", ".java", ".rs",
                                 ".swift", ".kt", ".c", ".cpp", ".jsx", ".tsx"):
            if "test" in rel_str or "spec" in rel_str:
                return (5, name_lower)
            return (2, name_lower)
        if p.suffix.lower() in (".toml", ".yaml", ".yml", ".json", ".cfg", ".ini"):
            return (3, name_lower)
        if p.suffix.lower() in (".md", ".txt"):
            return (4, name_lower)
        return (6, name_lower)

    unique.sort(key=_priority)
    unique = unique[:max_files]

    excerpts: list[str] = []
    total_chars = 0
    for file_path in unique:
        if total_chars >= max_total_chars:
            break
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            remaining = max_total_chars - total_chars
            limit = min(max_chars_per_file, remaining)
            truncated = content[:limit]
            if len(content) > limit:
                truncated += "\n\n... (内容已截断) ..."
            rel_path = file_path.relative_to(dir_path)
            excerpt = f"### {rel_path}\n\n```{file_path.suffix.lstrip('.')}\n{truncated}\n```"
            excerpts.append(excerpt)
            total_chars += len(truncated)
        except (OSError, ValueError) as exc:
            logger.debug("Failed to read %s: %s", file_path, exc)
    return "\n\n---\n\n".join(excerpts)


# ---------------------------------------------------------------------------
# Changed file extraction (Git mode — read full content of changed files)
# ---------------------------------------------------------------------------

def _extract_changed_file_paths(diff_stat: str) -> list[str]:
    """Extract file paths from ``git diff --stat`` output."""
    paths: list[str] = []
    for line in diff_stat.strip().split("\n"):
        line = line.strip()
        if "|" not in line:
            continue
        path_part = line.split("|")[0].strip()
        if "file" in path_part and "changed" in line:
            continue
        if path_part:
            paths.append(path_part)
    return paths


def _collect_changed_files(
    repo_path: Path,
    changed_paths: list[str],
    *,
    max_files: int = 30,
    max_chars_per_file: int = 5000,
    max_total_chars: int = 80_000,
) -> str:
    """Read full content of files changed in unpushed commits."""
    if not changed_paths:
        return ""

    valid: list[Path] = []
    for rel in changed_paths:
        fp = repo_path / rel
        if fp.is_file() and fp.suffix.lower() in _FILE_EXT_WHITELIST:
            valid.append(fp)
    if not valid:
        return ""

    def _file_priority(p: Path) -> tuple[int, str]:
        name_lower = p.name.lower()
        rel_str = str(p.relative_to(repo_path)).lower()
        if name_lower in ("main.py", "app.py", "cli.py", "__init__.py", "index.ts", "index.js"):
            return (0, name_lower)
        if p.suffix.lower() in (".py", ".ts", ".js", ".go", ".java", ".rs", ".swift", ".kt", ".c", ".cpp"):
            if "test" in rel_str or "spec" in rel_str:
                return (4, name_lower)
            return (1, name_lower)
        if p.suffix.lower() in (".toml", ".yaml", ".yml", ".json", ".cfg"):
            return (2, name_lower)
        if p.suffix.lower() in (".md", ".txt"):
            return (3, name_lower)
        return (5, name_lower)

    valid.sort(key=_file_priority)
    valid = valid[:max_files]

    excerpts: list[str] = []
    total_chars = 0
    for fp in valid:
        if total_chars >= max_total_chars:
            break
        try:
            content = fp.read_text(encoding="utf-8", errors="replace")
            remaining = max_total_chars - total_chars
            limit = min(max_chars_per_file, remaining)
            truncated = content[:limit]
            if len(content) > limit:
                truncated += f"\n\n... (truncated, total {len(content)} chars) ..."
            rel_path = fp.relative_to(repo_path)
            excerpt = f"### {rel_path}\n\n```{fp.suffix.lstrip('.')}\n{truncated}\n```"
            excerpts.append(excerpt)
            total_chars += len(truncated)
        except (OSError, ValueError) as exc:
            logger.debug("Failed to read changed file %s: %s", fp, exc)
    return "\n\n---\n\n".join(excerpts)


# ---------------------------------------------------------------------------
# Directory tree builder
# ---------------------------------------------------------------------------

def _build_dir_tree(
    root: Path,
    *,
    max_depth: int = 3,
    prefix: str = "",
    _current_depth: int = 0,
) -> str:
    """Build a recursive directory tree string (up to *max_depth* levels)."""
    if _current_depth > max_depth:
        return ""

    lines: list[str] = []
    try:
        entries = sorted(root.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except PermissionError:
        return ""

    dirs = [e for e in entries if e.is_dir() and e.name not in _DIR_BLACKLIST and not e.name.startswith(".")]
    files = [e for e in entries if e.is_file() and not e.name.startswith(".")]

    items = dirs + files
    for i, item in enumerate(items):
        is_last = (i == len(items) - 1)
        connector = "└── " if is_last else "├── "
        if item.is_dir():
            lines.append(f"{prefix}{connector}{item.name}/")
            extension = "    " if is_last else "│   "
            subtree = _build_dir_tree(
                item, max_depth=max_depth, prefix=prefix + extension,
                _current_depth=_current_depth + 1,
            )
            if subtree:
                lines.append(subtree)
        else:
            lines.append(f"{prefix}{connector}{item.name}")

    return "\n".join(lines)


def _collect_entry_files(repo_path: Path, *, max_chars: int = 5000) -> str:
    """Read entry/configuration files (pyproject.toml, package.json, etc.)."""
    found: list[str] = []
    for name in _ENTRY_FILE_NAMES:
        fp = repo_path / name
        if fp.is_file():
            try:
                content = fp.read_text(encoding="utf-8", errors="replace")
                if len(content) > max_chars:
                    content = content[:max_chars] + "\n... (truncated)"
                found.append(f"### {name}\n\n```\n{content}\n```")
            except OSError:
                continue
    return "\n\n---\n\n".join(found)


# ---------------------------------------------------------------------------
# AST analysis helpers (--full mode)
# ---------------------------------------------------------------------------

def _format_ast_args(args: ast.arguments) -> str:
    """Format AST function arguments into a compact string."""
    parts: list[str] = []
    for a in args.args:
        name = a.arg
        if name in ("self", "cls"):
            continue
        annotation = ""
        if a.annotation and hasattr(ast, "unparse"):
            annotation = f": {ast.unparse(a.annotation)}"
        parts.append(f"{name}{annotation}")
    if args.vararg:
        parts.append(f"*{args.vararg.arg}")
    if args.kwarg:
        parts.append(f"**{args.kwarg.arg}")
    result = ", ".join(parts)
    if len(result) > 120:
        result = result[:117] + "..."
    return result


def _ast_extract_signatures(file_path: Path, repo_root: Path) -> str:
    """Extract function signatures, class definitions and algorithm features from a Python file using AST."""
    if file_path.suffix.lower() != ".py":
        return ""
    try:
        source = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    try:
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError:
        return ""

    rel_path = file_path.relative_to(repo_root)
    lines: list[str] = [f"### {rel_path}"]
    line_count = len(source.splitlines())
    lines.append(f"# {line_count} lines")

    async_count = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.AsyncFunctionDef, ast.Await, ast.AsyncFor, ast.AsyncWith)))
    if_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.If))
    yield_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.Yield))
    
    features = []
    if async_count > 3:
        features.append(f"异步调度(Asyncx{async_count})")
    if if_count > 10:
        features.append(f"复杂决策树/分支(Ifx{if_count})")
    if yield_count > 0:
        features.append(f"生成器/状态机(Yieldx{yield_count})")
        
    if features:
        lines.append(f"# 探测到关键特征: {', '.join(features)}")

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef):
            bases = ", ".join(
                ast.unparse(b) if hasattr(ast, "unparse") else "..."
                for b in node.bases
            )
            decorators = [
                f"@{ast.unparse(d) if hasattr(ast, 'unparse') else '...'}"
                for d in node.decorator_list
            ]
            dec_str = " ".join(decorators) + " " if decorators else ""
            lines.append(f"  {dec_str}class {node.name}({bases}):")
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    args_str = _format_ast_args(item.args)
                    ret = ""
                    if item.returns and hasattr(ast, "unparse"):
                        ret = f" -> {ast.unparse(item.returns)}"
                    prefix = "async " if isinstance(item, ast.AsyncFunctionDef) else ""
                    lines.append(f"    {prefix}def {item.name}({args_str}){ret}")

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args_str = _format_ast_args(node.args)
            ret = ""
            if node.returns and hasattr(ast, "unparse"):
                ret = f" -> {ast.unparse(node.returns)}"
            decorators = [
                f"@{ast.unparse(d) if hasattr(ast, 'unparse') else '...'}"
                for d in node.decorator_list
            ]
            dec_str = " ".join(decorators) + " " if decorators else ""
            prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
            lines.append(f"  {dec_str}{prefix}def {node.name}({args_str}){ret}")

    if len(lines) <= 2:
        return ""
    return "\n".join(lines)


def _analyze_import_graph(
    repo_root: Path,
    *,
    max_files: int = 80,
    max_depth: int = 4,
) -> str:
    """Build a module import dependency graph from Python files."""
    py_files: list[Path] = []

    def _scan(d: Path, depth: int = 0) -> None:
        if depth > max_depth:
            return
        try:
            for entry in sorted(d.iterdir()):
                if entry.name.startswith(".") or entry.name in _DIR_BLACKLIST:
                    continue
                if entry.is_file() and entry.suffix == ".py":
                    py_files.append(entry)
                elif entry.is_dir():
                    _scan(entry, depth + 1)
        except PermissionError:
            pass

    _scan(repo_root)
    py_files = py_files[:max_files]

    module_names: dict[str, str] = {}
    for f in py_files:
        try:
            rel = f.relative_to(repo_root)
            parts = list(rel.parts)
            if parts[-1] == "__init__.py":
                parts = parts[:-1]
            else:
                parts[-1] = parts[-1].replace(".py", "")
            module_names[str(f)] = ".".join(parts)
        except ValueError:
            continue

    all_modules = set(module_names.values())
    graph: dict[str, set[str]] = {}

    for f in py_files:
        mod_name = module_names.get(str(f), "")
        if not mod_name:
            continue
        graph[mod_name] = set()
        try:
            source = f.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source, filename=str(f))
        except (SyntaxError, OSError):
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported = alias.name
                    for internal in all_modules:
                        if imported == internal or imported.startswith(internal + "."):
                            graph[mod_name].add(internal)
                            break
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported = node.module
                    for internal in all_modules:
                        if imported == internal or imported.startswith(internal + "."):
                            graph[mod_name].add(internal)
                            break

    lines: list[str] = ["## 模块 Import 依赖图\n"]
    fan_in: dict[str, int] = {m: 0 for m in all_modules}
    for mod, deps in graph.items():
        for dep in deps:
            if dep in fan_in:
                fan_in[dep] += 1

    sorted_modules = sorted(all_modules, key=lambda m: fan_in.get(m, 0), reverse=True)
    core_modules = [(m, fan_in[m]) for m in sorted_modules if fan_in.get(m, 0) >= 2]
    if core_modules:
        lines.append("### 核心模块（被 ≥2 个模块依赖）")
        for mod, fi in core_modules[:15]:
            fan_out = len(graph.get(mod, set()))
            lines.append(f"  - **{mod}** (fan-in={fi}, fan-out={fan_out})")
        lines.append("")

    lines.append("### 依赖关系")
    for mod in sorted_modules[:30]:
        deps = graph.get(mod, set())
        if deps:
            dep_list = ", ".join(sorted(deps))
            lines.append(f"  {mod} → [{dep_list}]")

    return "\n".join(lines)


def _collect_test_coverage_hints(repo_root: Path, *, max_depth: int = 4) -> str:
    """Infer functional coverage from test file names and extract performance metrics."""
    test_files: list[Path] = []

    def _scan(d: Path, depth: int = 0) -> None:
        if depth > max_depth:
            return
        try:
            for entry in sorted(d.iterdir()):
                if entry.name.startswith(".") or entry.name in _DIR_BLACKLIST:
                    continue
                if entry.is_file() and entry.suffix == ".py":
                    name = entry.name
                    if name.startswith("test_") or name.endswith("_test.py") or "benchmark" in str(d).lower():
                        test_files.append(entry)
                elif entry.is_dir():
                    _scan(entry, depth + 1)
        except PermissionError:
            pass

    _scan(repo_root)

    if not test_files:
        return ""

    lines: list[str] = ["## 测试文件与性能数据（Benchmark）提取\n"]
    lines.append(f"共扫描 {len(test_files)} 个测试/基准文件。\n")
    
    perf_metrics: list[str] = []
    
    for tf in test_files[:30]:
        name = tf.stem
        if name.startswith("test_"):
            tested = name[5:]
        elif name.endswith("_test"):
            tested = name[:-5]
        else:
            tested = name
        
        rel_path = str(tf.relative_to(repo_root))
        lines.append(f"  - `{rel_path}` → 测试目标: **{tested}**")
        
        # 简单正则提取耗时、QPS等性能断言
        try:
            content = tf.read_text(encoding="utf-8", errors="replace")
            for line in content.splitlines():
                if "assert" in line and ("time" in line.lower() or "duration" in line.lower() or "speed" in line.lower()):
                    perf_metrics.append(f"    - [{rel_path}] 性能断言: `{line.strip()}`")
                elif "benchmark" in rel_path.lower() and ("print" in line or "log" in line) and ("ms" in line or "sec" in line or "qps" in line.lower()):
                    perf_metrics.append(f"    - [{rel_path}] 基准测试输出: `{line.strip()}`")
        except Exception:
            pass

    if perf_metrics:
        lines.append("\n### 提取到的性能指标与断言（用于专利效果量化）")
        lines.extend(perf_metrics[:20])  # 限制输出数量
        
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Context extraction main functions
# ---------------------------------------------------------------------------

def _extract_git_context(
    repo_path: Path,
    *,
    max_commits: int = 50,
    max_docs: int = 5,
    doc_max_chars: int = 3000,
    git_timeout: int = 30,
    max_diff_chars: int = 60_000,
    max_changed_files: int = 30,
    changed_file_max_chars: int = 5000,
) -> CodeContext:
    """Extract context from a Git repository."""
    commits = _collect_recent_commits(repo_path, max_commits=max_commits, timeout=git_timeout)
    diff_stat = _collect_diff_summary(repo_path, timeout=git_timeout)
    full_diff = _collect_full_diff(repo_path, max_chars=max_diff_chars, timeout=git_timeout)
    doc_excerpts = _collect_doc_excerpts(repo_path, max_docs=max_docs, max_chars_per_doc=doc_max_chars)
    has_up = _has_upstream(repo_path, timeout=git_timeout)

    changed_paths = _extract_changed_file_paths(diff_stat)
    code_excerpts = _collect_changed_files(
        repo_path, changed_paths,
        max_files=max_changed_files, max_chars_per_file=changed_file_max_chars,
    )

    return CodeContext(
        repo_path=str(repo_path),
        is_git_repo=True,
        unpushed_commits=commits,
        full_diff=full_diff,
        diff_stat=diff_stat,
        has_upstream=has_up,
        has_unpushed=bool(commits and commits.strip()),
        doc_excerpts=doc_excerpts,
        code_excerpts=code_excerpts,
    )


def _extract_dir_context(
    repo_path: Path,
    *,
    max_tree_depth: int = 3,
    max_files: int = 20,
    file_max_chars: int = 3000,
    max_docs: int = 5,
    doc_max_chars: int = 3000,
) -> CodeContext:
    """Extract context from a plain directory (no Git)."""
    dir_tree = _build_dir_tree(repo_path, max_depth=max_tree_depth)
    entry_files = _collect_entry_files(repo_path)
    doc_excerpts = _collect_doc_excerpts(repo_path, max_docs=max_docs, max_chars_per_doc=doc_max_chars)
    code_excerpts = _collect_file_excerpts(
        repo_path, max_files=max_files, max_chars_per_file=file_max_chars,
    )

    return CodeContext(
        repo_path=str(repo_path),
        is_git_repo=False,
        dir_tree=dir_tree,
        entry_files=entry_files,
        doc_excerpts=doc_excerpts,
        code_excerpts=code_excerpts,
    )


def _run_full_analysis(repo_path: Path) -> dict[str, str]:
    """Run AST + import graph + test coverage analysis for --full mode."""
    py_files: list[Path] = []

    def _scan_py(d: Path, depth: int = 0) -> None:
        if depth > 4:
            return
        try:
            for entry in sorted(d.iterdir()):
                if entry.name.startswith(".") or entry.name in _DIR_BLACKLIST:
                    continue
                if entry.is_file() and entry.suffix == ".py":
                    py_files.append(entry)
                elif entry.is_dir():
                    _scan_py(entry, depth + 1)
        except PermissionError:
            pass

    _scan_py(repo_path)

    sig_parts: list[str] = []
    total_sig_chars = 0
    for f in py_files[:80]:
        if total_sig_chars > 50_000:
            break
        sig = _ast_extract_signatures(f, repo_path)
        if sig:
            sig_parts.append(sig)
            total_sig_chars += len(sig)

    return {
        "ast_signatures": "\n\n".join(sig_parts),
        "import_graph": _analyze_import_graph(repo_path, max_files=80),
        "test_coverage_hints": _collect_test_coverage_hints(repo_path),
        "all_code_excerpts": _collect_file_excerpts(
            repo_path, max_files=40, max_chars_per_file=5000, max_total_chars=200_000, max_depth=4,
        ),
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def extract_code_context(
    repo_path: str | Path,
    *,
    full_analysis: bool = False,
    topic: str = "",
) -> CodeContext:
    """从代码仓库提取上下文信息。

    Parameters
    ----------
    repo_path : 代码仓库路径
    full_analysis : 启用 AST+依赖图+全量代码扫描
    topic : 发明主题（用于上下文标注）

    Returns
    -------
    CodeContext
        结构化的代码上下文
    """
    repo = Path(repo_path).expanduser().resolve()
    if not repo.exists():
        raise FileNotFoundError(f"Repository path does not exist: {repo}")

    is_git = (repo / ".git").exists()

    if is_git:
        print(f"  → Git repository detected: {repo}")
        ctx = _extract_git_context(repo)
        if ctx.has_upstream and ctx.has_unpushed:
            commit_count = len(ctx.unpushed_commits.strip().split("\n"))
            print(f"  → Found {commit_count} unpushed commit(s) — only unpushed code treated as invention")
        elif ctx.has_upstream:
            print("  → Has upstream but no unpushed commits — all code treated as local invention")
        else:
            print("  → No upstream branch — all commits treated as local invention")
    else:
        print(f"  → Plain directory (no Git): {repo}")
        ctx = _extract_dir_context(repo)

    if full_analysis:
        print("  → Running full analysis (AST + import graph + test coverage)...")
        fa = _run_full_analysis(repo)
        ctx.ast_signatures = fa["ast_signatures"]
        ctx.import_graph = fa["import_graph"]
        ctx.test_coverage_hints = fa["test_coverage_hints"]

        if fa["all_code_excerpts"] and is_git:
            existing_code = ctx.code_excerpts or ""
            full_code = fa["all_code_excerpts"]
            if len(existing_code) + len(full_code) > 150_000:
                full_code = full_code[:150_000 - len(existing_code)]
            ctx.code_excerpts = (
                existing_code + "\n\n---\n\n## 全量代码补充（--full）\n\n" + full_code
                if existing_code else full_code
            )

        sig_count = ctx.ast_signatures.count("def ") + ctx.ast_signatures.count("class ")
        print(f"  → AST signatures: {sig_count} definitions extracted")

    return ctx


def _extract_project_tagline(doc_excerpts: str, *, max_len: int = 200) -> str:
    """Extract a one-line project tagline from README/doc excerpts.

    Looks for common patterns: first non-empty line after '# ProjectName',
    or content of <h2> tags, or first sentence of the README body.
    Returns empty string if nothing useful found.
    """
    if not doc_excerpts:
        return ""
    for line in doc_excerpts.split("\n"):
        stripped = line.strip()
        # Skip headings, badges, empty lines, HTML image tags
        if not stripped or stripped.startswith("#") or stripped.startswith("!") or stripped.startswith("<"):
            continue
        if stripped.startswith("|") or stripped.startswith("```") or stripped.startswith("---"):
            continue
        # Skip lines that are clearly badges/links only
        if stripped.startswith("[") and "](" in stripped and len(stripped) < 100:
            continue
        # Found a candidate tagline
        candidate = stripped[:max_len]
        if len(candidate) > 10:
            return candidate
    return ""


def format_code_context_markdown(ctx: CodeContext, *, topic: str = "") -> str:
    """将 CodeContext 格式化为 Markdown 文档供智能体阅读。"""
    parts: list[str] = []
    parts.append("# 代码仓库分析上下文\n")
    parts.append(f"**仓库路径**: `{ctx.repo_path}`\n")
    if topic:
        parts.append(f"**发明主题**: {topic}\n")

    # --- 项目价值分析提示段（引导 LLM 先理解项目整体价值） ---
    tagline = _extract_project_tagline(ctx.doc_excerpts)
    parts.append("## ⚡ 项目价值分析提示（优先阅读）\n")
    parts.append(
        "> **重要**：在分析具体代码文件之前，请先从**项目整体**的角度回答以下三个问题。\n"
        "> 这些问题的答案应作为**候选创新点的第一优先级来源**——产品级/系统级创新\n"
        "> 的专利价值通常高于单个模块的算法优化。\n"
    )
    if tagline:
        parts.append(f"> \n> **项目定位**（摘自 README）：{tagline}\n")
    parts.append(
        "\n"
        "1. **这个项目作为一个整体，为用户解决了什么前所未有的问题？**\n"
        "2. **在这个项目出现之前，用户是怎么做这件事的？（Before/After）**\n"
        "3. **这个项目最大的「不可能变成可能」是什么？**（多个模块协同产生的涌现能力）\n"
        "\n"
        "> 将上述系统级能力作为候选创新点的第一优先级。即使某个能力无法归属于单个代码文件，\n"
        "> 只要它是多模块协同产生的新能力，就比单文件的算法改进更有专利价值。\n"
    )

    if ctx.is_git_repo:
        parts.append("**模式**: Git 仓库\n")
        if ctx.has_upstream and ctx.has_unpushed:
            parts.append("> 该仓库有远端追踪分支且存在未推送的 commit。远端代码视为开源现有技术，仅本地未推送的 commit 代表用户自己的发明。\n")
        elif ctx.has_upstream and not ctx.has_unpushed:
            parts.append("> 该仓库有远端追踪分支但无未推送的 commit。整个项目视为用户自有发明。\n")
        else:
            parts.append("> 该仓库无远端追踪分支。所有 commit 均视为用户自己的发明。\n")

        if ctx.unpushed_commits:
            parts.append("## 本地 commit 记录\n")
            parts.append(f"```\n{ctx.unpushed_commits}\n```\n")
        if ctx.diff_stat:
            parts.append("## 代码变更统计\n")
            parts.append(f"```\n{ctx.diff_stat}\n```\n")
        if ctx.code_excerpts:
            parts.append("## 变更文件完整代码\n")
            parts.append(
                "> 以下是本地未推送 commit 涉及的文件的完整代码内容。\n"
                "> **分析提示**：文件行数多≠创新度高。executor/runner/stages 等文件行数通常最多，"
                "但往往是流水线基础设施代码。请重点关注那些实现了独特算法逻辑、"
                "数据分析方法、智能生成策略的模块文件。\n"
            )
            parts.append(ctx.code_excerpts + "\n")
        if ctx.full_diff:
            parts.append("## 完整代码改动详情（diff）\n")
            parts.append(f"```diff\n{ctx.full_diff}\n```\n")
    else:
        parts.append("**模式**: 普通目录（无 Git，整个项目视为用户自有发明）\n")
        if ctx.dir_tree:
            parts.append("## 项目目录结构\n")
            parts.append(f"```\n{ctx.dir_tree}\n```\n")
        if ctx.entry_files:
            parts.append("## 项目入口/配置文件\n")
            parts.append(ctx.entry_files + "\n")
        if ctx.code_excerpts:
            parts.append("## 核心代码文件摘要\n")
            parts.append(ctx.code_excerpts + "\n")

    if ctx.doc_excerpts:
        parts.append("## 项目文档摘要\n")
        parts.append(ctx.doc_excerpts + "\n")

    # Full analysis sections
    if ctx.ast_signatures:
        parts.append("## AST 函数/类签名索引\n")
        sigs = ctx.ast_signatures
        if len(sigs) > 30_000:
            sigs = sigs[:30_000] + "\n... (已截断)"
        parts.append(sigs + "\n")

    if ctx.import_graph:
        parts.append("\n" + ctx.import_graph + "\n")

    if ctx.test_coverage_hints:
        parts.append("\n" + ctx.test_coverage_hints + "\n")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        prog="repo_analyzer",
        description="从代码仓库提取结构化上下文（Git commit、diff、AST 签名、依赖图等）",
    )
    parser.add_argument("repo_path", help="代码仓库本地路径")
    parser.add_argument("--output", "-o", default=None, help="输出目录（默认在仓库旁创建）")
    parser.add_argument("--full", action="store_true", default=False,
                        help="启用完整分析（AST+依赖图+全量代码扫描）")
    parser.add_argument("--topic", default="", help="发明主题（用于上下文标注）")

    args = parser.parse_args()

    repo = Path(args.repo_path).expanduser().resolve()
    if not repo.exists():
        print(f"Error: repo path does not exist: {repo}", file=sys.stderr)
        return 1

    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = repo.parent / f"_context_{repo.name}"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"repo_analyzer — 代码上下文提取")
    print(f"  Repo:   {repo}")
    print(f"  Output: {output_dir}")
    print(f"  Full:   {args.full}")
    print()

    ctx = extract_code_context(repo, full_analysis=args.full, topic=args.topic)

    # Write code_context.md
    md_content = format_code_context_markdown(ctx, topic=args.topic)
    context_file = output_dir / "code_context.md"
    context_file.write_text(md_content, encoding="utf-8")
    print(f"\n✅ Code context saved to {context_file}")
    print(f"   Size: {len(md_content):,} chars")

    # Write metadata
    metadata = {
        "repo_path": str(repo),
        "is_git_repo": ctx.is_git_repo,
        "has_upstream": ctx.has_upstream,
        "full_analysis": args.full,
        "topic": args.topic,
        "context_chars": len(md_content),
    }
    metadata_file = output_dir / "context_metadata.json"
    metadata_file.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
