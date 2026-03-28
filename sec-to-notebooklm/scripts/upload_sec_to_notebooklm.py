#!/usr/bin/env python3
"""
上传 SEC 财报到 NotebookLM
支持 HTML 转 PDF + 配置 custom prompt
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path


def run_notebooklm_command(args: list) -> tuple[bool, str]:
    """运行 notebooklm CLI 命令"""
    import subprocess
    
    try:
        result = subprocess.run(
            ["notebooklm"] + args,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)


def get_or_create_notebook(ticker: str, company_name: str = None) -> str:
    """获取或创建笔记本"""
    
    # 查找现有笔记本
    success, output = run_notebooklm_command(["list"])
    if not success:
        print(f"❌ Failed to list notebooks: {output}")
        return None
    
    # 查找匹配的笔记本
    import re
    pattern = rf"([a-f0-9]{{8}}-[a-f0-9]{{4}}-[a-f0-9]{{4}}-[a-f0-9]{{4}}-[a-f0-9]{{12}}).*{ticker}"
    match = re.search(pattern, output, re.IGNORECASE)
    
    if match:
        notebook_id = match.group(1)
        print(f"✅ Found existing notebook: {notebook_id}")
        return notebook_id
    
    # 创建新笔记本
    notebook_title = f"{company_name or ticker} SEC Reports"
    print(f"📝 Creating notebook: {notebook_title}")
    
    success, output = run_notebooklm_command([
        "create",
        notebook_title
    ])
    
    if not success:
        print(f"❌ Failed to create notebook: {output}")
        return None
    
    # 提取笔记本 ID
    match = re.search(r"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})", output)
    if match:
        notebook_id = match.group(1)
        print(f"✅ Created notebook: {notebook_id}")
        return notebook_id
    
    print(f"❌ Failed to extract notebook ID from: {output}")
    return None


def configure_notebook(notebook_id: str, prompt_file: str = None) -> bool:
    """配置笔记本 custom prompt"""
    
    if not prompt_file:
        # 使用默认 prompt
        prompt_file = Path(__file__).parent.parent / "assets" / "sec_analyst_prompt.txt"
    
    if not os.path.exists(prompt_file):
        print(f"⚠️ Prompt file not found: {prompt_file}")
        return False
    
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read()
    except Exception as e:
        print(f"❌ Error reading prompt file: {e}")
        return False
    
    print(f"⚙️ Configuring notebook with SEC analyst prompt...")
    
    # 配置 custom persona
    success, output = run_notebooklm_command([
        "configure",
        "--notebook", notebook_id,
        "--persona", prompt,
        "--response-length", "longer"
    ])
    
    if success:
        print(f"  ✅ Configuration successful")
        return True
    else:
        print(f"  ❌ Configuration failed: {output}")
        return False


def convert_html_to_pdf(html_dir: Path) -> Path:
    """将 HTML 文件转换为 PDF"""
    
    pdf_dir = html_dir / "pdf"
    pdf_dir.mkdir(exist_ok=True)
    
    # 检查是否已安装 WeasyPrint
    try:
        from weasyprint import HTML
    except ImportError:
        print("❌ WeasyPrint not installed. Install with: pip install weasyprint")
        return None
    
    html_files = list(html_dir.glob("*.htm")) + list(html_dir.glob("*.html"))
    
    if not html_files:
        print(f"❌ No HTML files found in: {html_dir}")
        return None
    
    print(f"\n📄 Converting {len(html_files)} HTML files to PDF...")
    
    success_count = 0
    for i, html_file in enumerate(html_files, 1):
        print(f"  [{i}/{len(html_files)}] {html_file.name}...", end=" ", flush=True)
        
        try:
            pdf_file = pdf_dir / f"{html_file.stem}.pdf"
            HTML(filename=str(html_file)).write_pdf(str(pdf_file))
            size_mb = pdf_file.stat().st_size / (1024 * 1024)
            print(f"✅ ({size_mb:.1f} MB)")
            success_count += 1
        except Exception as e:
            print(f"❌ {e}")
    
    print(f"\n✅ Converted {success_count}/{len(html_files)} files")
    
    if success_count == 0:
        return None
    
    return pdf_dir


def upload_pdfs(notebook_id: str, pdf_dir: Path) -> dict:
    """上传 PDF 文件到 NotebookLM"""
    
    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in: {pdf_dir}")
        return {"success": 0, "failed": 0, "skipped": 0}
    
    print(f"\n📤 Uploading {len(pdf_files)} PDF files to NotebookLM...")
    
    results = {"success": 0, "failed": 0, "skipped": 0}
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"  [{i}/{len(pdf_files)}] {pdf_file.name}...", end=" ", flush=True)
        
        success, output = run_notebooklm_command([
            "source", "add",
            "--notebook", notebook_id,
            str(pdf_file)
        ])
        
        if success:
            print("✅")
            results["success"] += 1
        else:
            if "already exists" in output.lower():
                print("⏭️ (already exists)")
                results["skipped"] += 1
            else:
                print(f"❌ {output[:50]}")
                results["failed"] += 1
    
    print(f"\n✅ Upload complete: {results['success']} success, {results['skipped']} skipped, {results['failed']} failed")
    
    return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Upload SEC reports to NotebookLM with custom configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从 manifest.json 上传
  python3 upload_sec_to_notebooklm.py --manifest ./sec_reports/MSFT/manifest.json
  
  # 从目录上传（自动转换 HTML 为 PDF）
  python3 upload_sec_to_notebooklm.py --dir ./sec_reports/MSFT/ --ticker MSFT
  
  # 使用自定义 prompt
  python3 upload_sec_to_notebooklm.py --manifest ./sec_reports/MSFT/manifest.json --prompt ./custom_prompt.txt
  
  # 跳过配置（不设置 custom prompt）
  python3 upload_sec_to_notebooklm.py --manifest ./sec_reports/MSFT/manifest.json --no-configure
        """
    )
    
    parser.add_argument("--manifest", help="Path to manifest.json from sec_downloader")
    parser.add_argument("--dir", help="Directory containing HTML/PDF files")
    parser.add_argument("--ticker", help="Stock ticker symbol (used for notebook name)")
    parser.add_argument("--notebook", help="Notebook name (will create if not exists)")
    parser.add_argument("--notebook-id", help="Existing notebook ID")
    parser.add_argument("--prompt", help="Custom prompt file path")
    parser.add_argument("--no-configure", action="store_true", help="Skip notebook configuration")
    parser.add_argument("--no-convert", action="store_true", help="Skip HTML to PDF conversion (use existing PDFs)")
    
    args = parser.parse_args()
    
    # 验证输入
    if not args.manifest and not args.dir:
        print("❌ Must specify either --manifest or --dir")
        sys.exit(1)
    
    # 读取 manifest
    manifest = None
    if args.manifest:
        manifest_path = Path(args.manifest)
        if not manifest_path.exists():
            print(f"❌ Manifest file not found: {manifest_path}")
            sys.exit(1)
        
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        ticker = manifest.get("ticker", args.ticker or "UNKNOWN")
        company_name = manifest.get("company_name", ticker)
        html_dir = manifest_path.parent
    else:
        html_dir = Path(args.dir)
        if not html_dir.exists():
            print(f"❌ Directory not found: {html_dir}")
            sys.exit(1)
        
        ticker = args.ticker or html_dir.name
        company_name = ticker
    
    # 获取或创建笔记本
    if args.notebook_id:
        notebook_id = args.notebook_id
        print(f"✅ Using existing notebook: {notebook_id}")
    else:
        notebook_id = get_or_create_notebook(ticker, company_name)
        if not notebook_id:
            print("❌ Failed to get or create notebook")
            sys.exit(1)
    
    # 配置笔记本
    if not args.no_configure:
        configure_notebook(notebook_id, args.prompt)
    
    # 查找 PDF 文件
    pdf_dir = html_dir / "pdf"
    
    if not args.no_convert and not pdf_dir.exists():
        # 转换 HTML 为 PDF
        pdf_dir = convert_html_to_pdf(html_dir)
        if not pdf_dir:
            print("❌ Failed to convert HTML to PDF")
            sys.exit(1)
    elif not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        print("   Use --no-convert=false to convert HTML to PDF")
        sys.exit(1)
    
    # 上传 PDF
    results = upload_pdfs(notebook_id, pdf_dir)
    
    # 打印总结
    print(f"\n{'='*60}")
    print(f"  Summary")
    print(f"{'='*60}")
    print(f"  Notebook: {notebook_id}")
    print(f"  ✅ Success: {results['success']}")
    print(f"  ⏭️ Skipped: {results['skipped']}")
    print(f"  ❌ Failed: {results['failed']}")
    print(f"  🔗 View: https://notebooklm.google.com/notebook/{notebook_id}")
    print(f"{'='*60}\n")
    
    # 返回成功状态
    sys.exit(0 if results['failed'] == 0 else 1)


if __name__ == "__main__":
    main()
