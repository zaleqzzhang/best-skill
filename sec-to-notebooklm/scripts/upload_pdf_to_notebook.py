#!/usr/bin/env python3
"""
上传 PDF 文件到已存在的 NotebookLM 笔记本
"""

import os
import sys
from pathlib import Path


def upload_pdfs_to_notebook(pdf_dir: Path, notebook_id: str):
    """上传 PDF 文件到指定笔记本"""
    
    from notebooklm import NotebookLM
    from rich.console import Console
    
    console = Console()
    
    # 查找所有 PDF 文件
    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        console.print(f"[red]❌ 未找到 PDF 文件: {pdf_dir}[/red]")
        return False
    
    console.print(f"\n[bold cyan]{'='*60}[/bold cyan]")
    console.print(f"[bold cyan]  上传 PDF 到 NotebookLM[/bold cyan]")
    console.print(f"[bold cyan]{'='*60}[/bold cyan]")
    console.print(f"  笔记本 ID: {notebook_id}")
    console.print(f"  PDF 目录: {pdf_dir}")
    console.print(f"  文件数量: {len(pdf_files)}")
    console.print(f"[bold cyan]{'='*60}[/bold cyan]\n")
    
    try:
        # 初始化 NotebookLM
        nblm = NotebookLM()
        
        # 获取笔记本信息
        console.print("[yellow]→ 连接到笔记本...[/yellow]")
        notebook = nblm.get_notebook(notebook_id)
        console.print(f"[green]✅ 已连接: {notebook.get('title', 'Untitled')}[/green]\n")
        
        # 上传文件
        success_count = 0
        for i, pdf_file in enumerate(pdf_files, 1):
            console.print(f"[{i}/{len(pdf_files)}] 上传: {pdf_file.name}...", end=" ")
            
            try:
                nblm.add_source(notebook_id, str(pdf_file))
                size_mb = pdf_file.stat().st_size / (1024 * 1024)
                console.print(f"[green]✅ ({size_mb:.1f} MB)[/green]")
                success_count += 1
            except Exception as e:
                console.print(f"[red]❌ 失败: {e}[/red]")
        
        # 打印统计
        console.print(f"\n[bold cyan]{'='*60}[/bold cyan]")
        console.print(f"[bold cyan]  上传完成[/bold cyan]")
        console.print(f"[bold cyan]{'='*60}[/bold cyan]")
        console.print(f"  ✅ 成功: {success_count}")
        console.print(f"  ❌ 失败: {len(pdf_files) - success_count}")
        console.print(f"  📊 总计: {len(pdf_files)}")
        console.print(f"  🔗 查看笔记本: https://notebooklm.google.com/notebook/{notebook_id}")
        console.print(f"[bold cyan]{'='*60}[/bold cyan]\n")
        
        return success_count == len(pdf_files)
        
    except Exception as e:
        console.print(f"[red]❌ 上传失败: {e}[/red]")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="上传 PDF 文件到 NotebookLM 笔记本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 上传 PDF 到指定笔记本
  python3 upload_pdf_to_notebook.py ./sec_reports/MSFT/pdf/ --notebook-id 0dcf32ad-7dd5-4106-b320-f7ee3a2ce949
  
  # 使用笔记本名称（需先创建）
  python3 upload_pdf_to_notebook.py ./pdf/ --notebook "Microsoft SEC Reports"
        """
    )
    
    parser.add_argument("pdf_dir", help="PDF 文件目录")
    parser.add_argument("--notebook-id", help="NotebookLM 笔记本 ID")
    parser.add_argument("--notebook", help="NotebookLM 笔记本名称（将创建新笔记本）")
    
    args = parser.parse_args()
    
    pdf_dir = Path(args.pdf_dir)
    
    if not pdf_dir.exists():
        print(f"❌ 目录不存在: {pdf_dir}")
        sys.exit(1)
    
    if not args.notebook_id and not args.notebook:
        print("❌ 必须指定 --notebook-id 或 --notebook")
        sys.exit(1)
    
    if args.notebook_id:
        # 上传到已存在的笔记本
        success = upload_pdfs_to_notebook(pdf_dir, args.notebook_id)
        sys.exit(0 if success else 1)
    
    elif args.notebook:
        # 创建新笔记本并上传
        from notebooklm import NotebookLM
        nblm = NotebookLM()
        
        print(f"创建笔记本: {args.notebook}")
        notebook = nblm.create_notebook(args.notebook)
        notebook_id = notebook["id"]
        
        print(f"✅ 笔记本已创建: {notebook_id}")
        
        success = upload_pdfs_to_notebook(pdf_dir, notebook_id)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
