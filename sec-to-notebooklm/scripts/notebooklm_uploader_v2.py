#!/usr/bin/env python3
"""
NotebookLM Uploader V2 - 支持笔记本复用
参考 cninfo-to-notebooklm 的实现方式
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path

# 添加 notebooklm-py 依赖检查
try:
    from notebooklm import NotebookLMClient, auth
except ImportError:
    print("❌ 缺少依赖: notebooklm-py")
    print("安装: pip install notebooklm-py")
    sys.exit(1)


def run_notebooklm_command(args: list) -> tuple[bool, str]:
    """运行 notebooklm CLI 命令"""
    import subprocess
    
    cmd = ["notebooklm"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    return result.returncode == 0, result.stdout + result.stderr


def _verify_notebook_exists(notebook_id: str) -> bool:
    """验证笔记本是否存在"""
    success, output = run_notebooklm_command(["list"])
    if not success:
        return False
    
    # 检查笔记本ID是否在列表中
    return notebook_id[:8] in output  # 使用前8位匹配（CLI输出可能截断）


def find_existing_notebook(notebook_title: str) -> str:
    """查找已存在的笔记本"""
    success, output = run_notebooklm_command(["list"])
    if not success:
        return None
    
    # 解析输出查找匹配的笔记本
    for line in output.split("\n"):
        line = line.strip()
        if not line or not line.startswith("│"):
            continue
        if "ID" in line and "Title" in line:
            continue
        
        if notebook_title in line:
            parts = line.split("│")
            if len(parts) >= 2:
                id_part = parts[1].strip()
                if id_part.endswith("…"):
                    id_part = id_part[:-1]
                if re.match(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}", id_part):
                    print(f"🔍 Found existing notebook: {id_part}...")
                    return id_part
    
    return None


def _get_cache_file(ticker: str) -> Path:
    """获取笔记本缓存文件路径"""
    cache_dir = Path.home() / ".sec-to-notebooklm"
    cache_dir.mkdir(exist_ok=True)
    return cache_dir / f"{ticker.upper()}_notebook.json"


def _get_cached_notebook(ticker: str) -> str:
    """从缓存获取笔记本ID"""
    cache_file = _get_cache_file(ticker)
    if not cache_file.exists():
        return None
    
    try:
        with open(cache_file) as f:
            data = json.load(f)
            return data.get("notebook_id")
    except:
        return None


def _cache_notebook(ticker: str, notebook_id: str, notebook_title: str):
    """缓存笔记本信息"""
    cache_file = _get_cache_file(ticker)
    data = {
        "ticker": ticker.upper(),
        "notebook_id": notebook_id,
        "notebook_title": notebook_title,
        "created_at": __import__("datetime").datetime.now().isoformat()
    }
    with open(cache_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"💾 Cached notebook for {ticker}: {notebook_id}")


def _invalidate_cached_notebook(ticker: str):
    """清除缓存"""
    cache_file = _get_cache_file(ticker)
    if cache_file.exists():
        cache_file.unlink()
        print(f"🗑️  Invalidated cache for {ticker}")


def get_or_create_notebook(ticker: str, notebook_title: str, force_new: bool = False) -> str:
    """获取或创建笔记本"""
    
    # 1. 检查缓存
    if not force_new:
        cached_id = _get_cached_notebook(ticker)
        if cached_id:
            print(f"📋 Found cached notebook for {ticker}: {cached_id}")
            
            # 验证笔记本是否还存在
            print(f"🔍 Verifying notebook exists...")
            if _verify_notebook_exists(cached_id):
                print(f"✅ Using cached notebook: {cached_id}")
                return cached_id
            else:
                print(f"⚠️ Cached notebook no longer exists, invalidating...")
                _invalidate_cached_notebook(ticker)
    
    # 2. 搜索已存在的笔记本
    if not force_new:
        existing_id = find_existing_notebook(notebook_title)
        if existing_id:
            print(f"✅ Found existing notebook: {existing_id}")
            _cache_notebook(ticker, existing_id, notebook_title)
            return existing_id
    
    # 3. 创建新笔记本
    print(f"📚 Creating new notebook: {notebook_title}")
    success, output = run_notebooklm_command(["create", notebook_title])
    
    if not success:
        print(f"❌ Failed to create notebook: {output}")
        return None
    
    # 提取笔记本ID
    match = re.search(r"Created notebook:\s*([a-f0-9-]+)", output)
    if match:
        notebook_id = match.group(1)
        _cache_notebook(ticker, notebook_id, notebook_title)
        return notebook_id
    
    print(f"⚠️ Could not extract notebook ID from: {output}")
    return None


def get_existing_sources(notebook_id: str) -> set:
    """获取笔记本中已有的来源"""
    existing = set()
    
    success, output = run_notebooklm_command(["use", notebook_id])
    if not success:
        return existing
    
    success, output = run_notebooklm_command(["source", "list"])
    if not success:
        return existing
    
    # 解析来源列表
    for line in output.split("\n"):
        line = line.strip()
        if not line or not line.startswith("│"):
            continue
        if "ID" in line and "Title" in line:
            continue
        
        parts = line.split("│")
        if len(parts) >= 3:
            title = parts[2].strip()
            existing.add(title)
    
    return existing


def upload_source(notebook_id: str, file_path: str, skip_existing: bool = True) -> bool:
    """上传来源文件"""
    file_name = Path(file_path).name
    
    # 检查是否已存在
    if skip_existing:
        existing = get_existing_sources(notebook_id)
        # 使用文件名匹配（可能被截断）
        for existing_name in existing:
            if file_name[:30] in existing_name or existing_name[:30] in file_name:
                print(f"⏭️  Already exists: {file_name}")
                return True
    
    print(f"📤 Uploading: {file_name}")
    success, output = run_notebooklm_command(["source", "add", file_path])
    
    if success:
        print(f"✅ Uploaded: {file_name}")
        return True
    else:
        print(f"❌ Failed to upload {file_name}: {output}")
        return False


def configure_notebook(notebook_id: str, prompt_file: str = None) -> bool:
    """配置笔记本的 custom prompt"""
    if not prompt_file:
        prompt_file = Path(__file__).parent.parent / "assets" / "sec_analyst_prompt.txt"
    
    if not Path(prompt_file).exists():
        print(f"⚠️ Prompt file not found: {prompt_file}")
        return False
    
    with open(prompt_file) as f:
        prompt = f.read()
    
    print(f"🔧 Configuring notebook with SEC Analyst prompt...")
    success, output = run_notebooklm_command([
        "configure",
        "--notebook", notebook_id,
        "--persona", prompt,
        "--response-length", "longer"
    ])
    
    if success:
        print(f"✅ Configuration complete")
        return True
    else:
        print(f"⚠️ Configuration failed: {output}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Upload SEC reports to NotebookLM (V2 with notebook reuse)")
    parser.add_argument("--manifest", required=True, help="Manifest JSON file")
    parser.add_argument("--notebook", required=True, help="Notebook name")
    parser.add_argument("--force-new", action="store_true", help="Force create new notebook")
    parser.add_argument("--prompt", help="Custom prompt file (default: SEC Analyst)")
    parser.add_argument("--no-configure", action="store_true", help="Skip notebook configuration")
    parser.add_argument("--skip-existing", action="store_true", default=True, help="Skip existing files")
    
    args = parser.parse_args()
    
    # 读取 manifest
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"❌ Manifest not found: {manifest_path}")
        sys.exit(1)
    
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    ticker = manifest.get("ticker", "UNKNOWN") or manifest.get("company", {}).get("ticker", "UNKNOWN")
    files = manifest.get("files", [])
    
    # 将 HTML 文件路径转换为 PDF 文件路径
    manifest_dir = manifest_path.parent
    pdf_files = []
    
    for file_path in files:
        # 如果是相对路径，直接使用（manifest中的路径已经相对于manifest所在目录）
        path = Path(file_path)
        
        # 如果路径不存在，尝试相对于manifest目录
        if not path.exists():
            path = manifest_dir / file_path
        
        # 如果是 HTML 文件，转换为 PDF 路径
        if path.suffix.lower() in [".htm", ".html"]:
            # PDF 文件在 pdf 子目录
            pdf_path = manifest_dir / "pdf" / f"{path.stem}.pdf"
            if pdf_path.exists():
                pdf_files.append(str(pdf_path.absolute()))
            else:
                print(f"⚠️ PDF not found for {file_path}, skipping")
        else:
            if path.exists():
                pdf_files.append(str(path.absolute()))
            else:
                print(f"⚠️ File not found: {file_path}, skipping")
    
    files = pdf_files
    
    if not files:
        print(f"❌ No files in manifest")
        sys.exit(1)
    
    print(f"\n📊 Processing {ticker}: {len(files)} files")
    
    # 获取或创建笔记本
    notebook_id = get_or_create_notebook(ticker, args.notebook, args.force_new)
    if not notebook_id:
        print(f"❌ Failed to get or create notebook")
        sys.exit(1)
    
    print(f"\n📚 Notebook ID: {notebook_id}")
    print(f"🔗 Access URL: https://notebooklm.google.com/notebook/{notebook_id}")
    
    # 配置笔记本
    if not args.no_configure:
        configure_notebook(notebook_id, args.prompt)
    
    # 切换到笔记本
    success, _ = run_notebooklm_command(["use", notebook_id])
    if not success:
        print(f"❌ Failed to switch to notebook")
        sys.exit(1)
    
    # 上传文件
    print(f"\n📤 Uploading {len(files)} files...")
    success_count = 0
    
    for file_path in files:
        if upload_source(notebook_id, file_path, args.skip_existing):
            success_count += 1
    
    print(f"\n{'=' * 60}")
    print(f"✅ Successfully uploaded {success_count}/{len(files)} files")
    print(f"📚 Notebook: {args.notebook}")
    print(f"🔗 URL: https://notebooklm.google.com/notebook/{notebook_id}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
