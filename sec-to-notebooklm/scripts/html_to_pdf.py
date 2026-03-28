#!/usr/bin/env python3
"""
HTML 转 PDF 工具
使用 WeasyPrint 将 SEC HTML 财报转换为 PDF 格式
"""

import os
import sys
from pathlib import Path


def convert_html_to_pdf(html_file: Path, pdf_file: Path) -> bool:
    """将 HTML 文件转换为 PDF"""
    try:
        from weasyprint import HTML, CSS
        
        print(f"  转换中: {html_file.name}...", end=" ", flush=True)
        
        # 读取 HTML 并转换为 PDF
        html = HTML(filename=str(html_file))
        html.write_pdf(str(pdf_file))
        
        # 获取文件大小
        pdf_size = pdf_file.stat().st_size / (1024 * 1024)  # MB
        print(f"✅ ({pdf_size:.1f} MB)")
        return True
        
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False


def batch_convert(input_dir: Path, output_dir: Path = None) -> dict:
    """批量转换目录中的 HTML 文件"""
    
    if output_dir is None:
        output_dir = input_dir / "pdf"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 查找所有 HTML 文件
    html_files = sorted(input_dir.glob("*.htm")) + sorted(input_dir.glob("*.html"))
    
    if not html_files:
        print(f"❌ 未找到 HTML 文件: {input_dir}")
        return {"total": 0, "success": 0, "failed": 0}
    
    print(f"\n{'='*60}")
    print(f"  开始批量转换 HTML → PDF")
    print(f"{'='*60}")
    print(f"  输入目录: {input_dir}")
    print(f"  输出目录: {output_dir}")
    print(f"  文件数量: {len(html_files)}")
    print(f"{'='*60}\n")
    
    results = {"total": len(html_files), "success": 0, "failed": 0, "files": []}
    
    for i, html_file in enumerate(html_files, 1):
        print(f"[{i}/{len(html_files)}] {html_file.name}")
        
        pdf_file = output_dir / f"{html_file.stem}.pdf"
        
        if convert_html_to_pdf(html_file, pdf_file):
            results["success"] += 1
            results["files"].append({
                "html": str(html_file),
                "pdf": str(pdf_file),
                "size_mb": pdf_file.stat().st_size / (1024 * 1024)
            })
        else:
            results["failed"] += 1
    
    # 打印统计
    print(f"\n{'='*60}")
    print(f"  转换完成")
    print(f"{'='*60}")
    print(f"  ✅ 成功: {results['success']}")
    print(f"  ❌ 失败: {results['failed']}")
    print(f"  📊 总计: {results['total']}")
    
    if results["success"] > 0:
        total_size = sum(f["size_mb"] for f in results["files"])
        print(f"  📁 总大小: {total_size:.1f} MB")
        print(f"  📂 输出目录: {output_dir}")
    
    print(f"{'='*60}\n")
    
    return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="HTML 转 PDF 批量转换工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 转换单个文件
  python3 html_to_pdf.py report.htm
  
  # 批量转换目录
  python3 html_to_pdf.py ./sec_reports/MSFT/
  
  # 指定输出目录
  python3 html_to_pdf.py ./sec_reports/MSFT/ --output ./pdf/
        """
    )
    
    parser.add_argument("input", help="HTML 文件或目录路径")
    parser.add_argument("--output", "-o", help="输出目录（默认: 输入目录/pdf/）")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None
    
    if not input_path.exists():
        print(f"❌ 路径不存在: {input_path}")
        sys.exit(1)
    
    if input_path.is_file():
        # 单文件转换
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}.pdf"
        else:
            output_path = output_path / f"{input_path.stem}.pdf"
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        success = convert_html_to_pdf(input_path, output_path)
        sys.exit(0 if success else 1)
    
    elif input_path.is_dir():
        # 批量转换
        results = batch_convert(input_path, output_path)
        sys.exit(0 if results["failed"] == 0 else 1)
    
    else:
        print(f"❌ 无效路径: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
