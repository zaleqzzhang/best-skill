#!/usr/bin/env python3
"""
批量 SEC → NotebookLM 工作流（流水线模式）
支持多个公司并行下载和转换，流水线上传到独立笔记本
- 下载完成即可开始转换
- 转换完成即可开始上传（上传串行）
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import queue
import time


def run_command(cmd: list, capture_output: bool = True) -> tuple[int, str]:
    """运行命令"""
    if capture_output:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode, result.stdout + result.stderr
    else:
        result = subprocess.run(cmd)
        return result.returncode, ""


def download_reports(ticker: str, output_dir: str) -> dict:
    """下载单个公司的 SEC 财报"""
    print(f"\n{'='*60}")
    print(f"📥 [{ticker}] 开始下载")
    print(f"{'='*60}")
    
    scripts_dir = Path(__file__).parent
    cmd = [
        sys.executable,
        str(scripts_dir / "sec_downloader.py"),
        ticker,
        "--output", output_dir
    ]
    
    rc, output = run_command(cmd, capture_output=False)
    
    if rc != 0:
        print(f"❌ [{ticker}] 下载失败")
        return {"ticker": ticker, "success": False, "error": "Download failed"}
    
    # 读取 manifest
    manifest_path = Path(output_dir) / ticker / "manifest.json"
    if not manifest_path.exists():
        print(f"❌ [{ticker}] 未找到 manifest")
        return {"ticker": ticker, "success": False, "error": "Manifest not found"}
    
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    files = manifest.get("files", [])
    print(f"✅ [{ticker}] 下载完成: {len(files)} 个文件")
    
    return {
        "ticker": ticker,
        "success": True,
        "manifest_path": str(manifest_path),
        "files_count": len(files)
    }


def convert_to_pdf(ticker: str, manifest_path: str) -> dict:
    """将 HTML 转换为 PDF"""
    print(f"\n{'='*60}")
    print(f"📄 [{ticker}] 开始转换 PDF")
    print(f"{'='*60}")
    
    scripts_dir = Path(__file__).parent
    input_dir = Path(manifest_path).parent
    
    cmd = [
        sys.executable,
        str(scripts_dir / "html_to_pdf.py"),
        str(input_dir)
    ]
    
    rc, output = run_command(cmd, capture_output=False)
    
    if rc != 0:
        print(f"❌ [{ticker}] PDF 转换失败")
        return {"ticker": ticker, "success": False, "error": "PDF conversion failed"}
    
    print(f"✅ [{ticker}] PDF 转换完成")
    return {"ticker": ticker, "success": True, "manifest_path": manifest_path}


def upload_to_notebook(ticker: str, manifest_path: str, force_new: bool = False) -> dict:
    """上传到独立的 NotebookLM 笔记本"""
    print(f"\n{'='*60}")
    print(f"📤 [{ticker}] 开始上传到 NotebookLM")
    print(f"{'='*60}")
    
    scripts_dir = Path(__file__).parent
    notebook_name = f"{ticker} SEC Reports"
    
    cmd = [
        sys.executable,
        str(scripts_dir / "notebooklm_uploader_v2.py"),
        "--manifest", manifest_path,
        "--notebook", notebook_name,
    ]
    
    if force_new:
        cmd.append("--force-new")
    
    rc, output = run_command(cmd, capture_output=False)
    
    if rc != 0:
        print(f"❌ [{ticker}] 上传失败")
        return {"ticker": ticker, "success": False, "error": "Upload failed"}
    
    print(f"✅ [{ticker}] 上传完成")
    
    # 获取笔记本 ID
    cache_file = Path.home() / ".sec-to-notebooklm" / f"{ticker}_notebook.json"
    if cache_file.exists():
        with open(cache_file) as f:
            cache_data = json.load(f)
            notebook_id = cache_data.get("notebook_id", "unknown")
    else:
        notebook_id = "unknown"
    
    return {
        "ticker": ticker,
        "success": True,
        "notebook_id": notebook_id,
        "notebook_url": f"https://notebooklm.google.com/notebook/{notebook_id}"
    }


def download_worker(ticker: str, output_dir: str, convert_queue: queue.Queue):
    """下载工作线程：下载完成后放入转换队列"""
    result = download_reports(ticker, output_dir)
    convert_queue.put(result)


def convert_worker(convert_queue: queue.Queue, upload_queue: queue.Queue):
    """转换工作线程：转换完成后放入上传队列"""
    while True:
        result = convert_queue.get()
        
        # 检查结束信号
        if result is None:
            convert_queue.task_done()
            break
        
        ticker = result.get("ticker")
        
        if result.get("success"):
            # 转换 PDF
            convert_result = convert_to_pdf(ticker, result["manifest_path"])
            upload_queue.put(convert_result)
        else:
            # 下载失败，直接放入上传队列（标记失败）
            upload_queue.put(result)
        
        convert_queue.task_done()


def upload_worker(upload_queue: queue.Queue, results: dict, force_new: bool, lock: threading.Lock):
    """上传工作线程：串行上传（单线程）"""
    while True:
        result = upload_queue.get()
        
        # 检查结束信号
        if result is None:
            upload_queue.task_done()
            break
        
        ticker = result.get("ticker")
        
        if result.get("success"):
            # 上传到 NotebookLM
            upload_result = upload_to_notebook(ticker, result["manifest_path"], force_new)
            
            with lock:
                results[ticker] = upload_result
        else:
            # 转换或下载失败
            with lock:
                results[ticker] = result
        
        # 避免 API 限流
        time.sleep(1)
        
        upload_queue.task_done()


def main():
    parser = argparse.ArgumentParser(
        description="批量下载并上传 SEC 财报到 NotebookLM（流水线模式）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 批量处理多个公司
  python3 batch_sec_to_notebooklm.py MSFT GOOGL META
  
  # 强制创建新笔记本
  python3 batch_sec_to_notebooklm.py AAPL TSLA --force-new
  
  # 指定输出目录
  python3 batch_sec_to_notebooklm.py NVDA AMD --output ./my_reports
        """
    )
    parser.add_argument("tickers", nargs="+", help="股票代码列表")
    parser.add_argument("--output", "-o", default="./sec_reports", help="输出目录")
    parser.add_argument("--force-new", action="store_true", help="强制创建新笔记本")
    parser.add_argument("--download-workers", type=int, default=3, help="并行下载数")
    parser.add_argument("--convert-workers", type=int, default=3, help="并行转换数")
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"  批量处理 {len(args.tickers)} 个公司（流水线模式）")
    print(f"  公司列表: {', '.join(args.tickers)}")
    print(f"{'='*60}")
    
    # 创建队列
    convert_queue = queue.Queue()
    upload_queue = queue.Queue()
    results = {}
    results_lock = threading.Lock()
    
    # 启动转换工作线程
    convert_threads = []
    for i in range(args.convert_workers):
        t = threading.Thread(target=convert_worker, args=(convert_queue, upload_queue))
        t.daemon = True
        t.start()
        convert_threads.append(t)
    
    # 启动上传工作线程（单线程，串行上传）
    upload_thread = threading.Thread(
        target=upload_worker, 
        args=(upload_queue, results, args.force_new, results_lock)
    )
    upload_thread.daemon = True
    upload_thread.start()
    
    # ── 流水线阶段 1：并行下载 ─────────────────────────────────────
    print(f"\n\n{'='*60}")
    print(f"  流水线启动：并行下载 → 并行转换 → 串行上传")
    print(f"{'='*60}")
    
    download_threads = []
    for ticker in args.tickers:
        t = threading.Thread(target=download_worker, args=(ticker, args.output, convert_queue))
        t.daemon = True
        t.start()
        download_threads.append(t)
    
    # 等待所有下载完成
    for t in download_threads:
        t.join()
    
    # 发送转换线程结束信号
    for _ in range(args.convert_workers):
        convert_queue.put(None)
    
    # 等待所有转换完成
    for t in convert_threads:
        t.join()
    
    # 发送上传线程结束信号
    upload_queue.put(None)
    
    # 等待上传完成
    upload_thread.join()
    
    # ── 生成汇总报告 ─────────────────────────────────────────────
    print(f"\n\n{'='*60}")
    print(f"  批量处理完成汇总")
    print(f"{'='*60}\n")
    
    success_count = 0
    for ticker in args.tickers:
        result = results.get(ticker, {})
        status = "✅" if result.get("success") else "❌"
        
        if result.get("success"):
            success_count += 1
            print(f"{status} {ticker:6s} - 笔记本: {result.get('notebook_url', 'N/A')}")
        else:
            error = result.get('error', 'Unknown error')
            print(f"{status} {ticker:6s} - 错误: {error}")
    
    print(f"\n{'='*60}")
    print(f"  成功: {success_count}/{len(args.tickers)}")
    print(f"{'='*60}\n")
    
    # 保存汇总结果
    summary = {
        "processed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(args.tickers),
        "success": success_count,
        "results": results
    }
    
    summary_file = Path(args.output) / "batch_summary.json"
    summary_file.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"📊 汇总报告: {summary_file}")


if __name__ == "__main__":
    main()
