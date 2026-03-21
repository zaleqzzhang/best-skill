#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNinfo to NotebookLM - Main Orchestration Script
Downloads A-share and Hong Kong stock reports from cninfo.com.cn and uploads to NotebookLM.
"""

import sys
import os
import json
import tempfile
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from download import CnInfoDownloader
import datetime

def download_reports_for_stock(downloader, stock_input, stock_index=None, total_stocks=None):
    """Download reports for a single stock (can run in parallel)
    
    Args:
        downloader: CnInfoDownloader instance
        stock_input: Stock code or name
        stock_index: Current stock index (for batch processing display)
        total_stocks: Total number of stocks (for batch processing display)
    
    Returns:
        dict with download results (files not uploaded yet)
    """
    # Show progress for batch processing
    if stock_index is not None and total_stocks is not None:
        print(f"\n{'=' * 60}")
        print(f"📥 [{stock_index}/{total_stocks}] Downloading: {stock_input}")
        print(f"{'=' * 60}")
    
    # Find stock (now returns market too)
    stock_code, stock_info, market = downloader.find_stock(stock_input)
    if not stock_code:
        print(f"❌ Stock not found: {stock_input}", file=sys.stderr)
        return {"success": False, "stock_input": stock_input, "error": f"Stock not found: {stock_input}"}

    stock_name = stock_info.get("zwjc", stock_code)
    org_id = stock_info.get("orgId", "")
    market_display = "Hong Kong" if market == "hke" else "A-share"
    print(f"📊 Found stock: {stock_code} ({stock_name}) [{market_display}]")

    # Create temp directory
    output_dir = tempfile.mkdtemp(prefix="cninfo_reports_")
    print(f"📁 Temp directory: {output_dir}")

    # Calculate years (last 9 years to current year)
    current_year = datetime.datetime.now().year
    annual_years = list(range(current_year - 9, current_year + 1))

    # Download annual reports
    print(f"\n📥 Downloading annual reports for: {annual_years}")
    annual_files = downloader.download_annual_reports(
        stock_code, org_id, annual_years, output_dir, market
    )

    # Download periodic reports
    print(f"\n📥 Downloading periodic reports (Q1, semi-annual, Q3)...")
    periodic_files = downloader.download_periodic_reports(
        stock_code, org_id, current_year, output_dir, market
    )
    
    if not periodic_files:
        print(f"  No {current_year} reports yet, trying {current_year - 1}...")
        periodic_files = downloader.download_periodic_reports(
            stock_code, org_id, current_year - 1, output_dir, market
        )
    elif len(periodic_files) < 3:
        print(f"  Checking {current_year - 1} for additional reports...")
        prev_year_files = downloader.download_periodic_reports(
            stock_code, org_id, current_year - 1, output_dir, market
        )
        periodic_files.extend(prev_year_files)

    all_files = annual_files + periodic_files

    if not all_files:
        print("❌ No reports downloaded")
        shutil.rmtree(output_dir)
        return {"success": False, "stock_input": stock_input, "error": "No reports downloaded"}

    print(f"\n✅ Downloaded {len(all_files)} reports for {stock_name}")
    
    return {
        "success": True,
        "stock_input": stock_input,
        "stock_code": stock_code,
        "stock_name": stock_name,
        "market": market,
        "market_display": market_display,
        "output_dir": output_dir,
        "files": all_files
    }

def upload_reports_for_stock(download_result, stock_index=None, total_stocks=None):
    """Upload reports to NotebookLM (must run sequentially)
    
    Args:
        download_result: Result dict from download_reports_for_stock
        stock_index: Current stock index (for batch processing display)
        total_stocks: Total number of stocks (for batch processing display)
    
    Returns:
        dict with final results
    """
    if not download_result.get("success"):
        return download_result
    
    stock_input = download_result["stock_input"]
    stock_code = download_result["stock_code"]
    stock_name = download_result["stock_name"]
    market_display = download_result["market_display"]
    output_dir = download_result["output_dir"]
    all_files = download_result["files"]
    
    # Show progress for batch processing
    if stock_index is not None and total_stocks is not None:
        print(f"\n{'=' * 60}")
        print(f"📤 [{stock_index}/{total_stocks}] Uploading: {stock_name}")
        print(f"{'=' * 60}")
    
    # Check if notebooklm is available
    if not shutil.which("notebooklm"):
        print("\n⚠️ NotebookLM CLI not found!")
        print("Install with: pip install notebooklm-py playwright")
        print("Then: playwright install chromium")
        print("Then authenticate with: notebooklm login")
        print(f"\n📁 Files saved to: {output_dir}")
        print("You can manually upload these PDFs to NotebookLM")
        
        return {
            "success": False, 
            "stock_input": stock_input,
            "stock_name": stock_name,
            "error": "NotebookLM CLI not found",
            "output_dir": output_dir,
            "files": all_files
        }

    # Upload to NotebookLM
    print(f"\n📤 Uploading {len(all_files)} files to NotebookLM...")
    
    from upload import (
        get_or_create_notebook,
        upload_all_sources,
        cleanup_temp_files,
        configure_notebook,
    )

    # Use cached notebook if available
    notebook_id = get_or_create_notebook(stock_code, stock_name)
    
    if not notebook_id:
        print("❌ Failed to create notebook")
        print(f"📁 Files saved to: {output_dir}")
        return {
            "success": False, 
            "stock_input": stock_input,
            "stock_name": stock_name,
            "error": "Failed to create notebook", 
            "output_dir": output_dir
        }
    
    notebook_title = f"{stock_name} 财务报告"

    # Configure custom prompt
    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "assets",
        "financial_analyst_prompt.txt",
    )
    if os.path.exists(prompt_path):
        configure_notebook(notebook_id, prompt_path)
    else:
        print(f"⚠️ Prompt file not found at: {prompt_path}")

    results = upload_all_sources(notebook_id, all_files)

    # Cleanup
    cleanup_temp_files(all_files, output_dir)

    # Summary
    print(f"\n✅ {stock_name}: Uploaded {len(results['success'])} reports")
    
    if results.get("skipped"):
        print(f"   ⏭️ Skipped (already exists): {len(results['skipped'])} reports")
    
    if results["failed"]:
        print(f"   ❌ Failed: {len(results['failed'])} reports")
    
    return {
        "success": True,
        "stock_input": stock_input,
        "stock_code": stock_code,
        "stock_name": stock_name,
        "notebook_id": notebook_id,
        "uploaded": len(results['success']),
        "skipped": len(results.get('skipped', [])),
        "failed": len(results['failed'])
    }

def main():
    """Main entry point - supports single or multiple stocks
    
    For multiple stocks:
    - Downloads run in PARALLEL (faster)
    - Uploads run SEQUENTIALLY (avoid NotebookLM context conflicts)
    """
    if len(sys.argv) < 2:
        print("Usage: python run.py <stock_code_or_name> [stock2] [stock3] ...")
        print("")
        print("Examples:")
        print("  python run.py 600519                  # Single A-share by code")
        print("  python run.py 贵州茅台                 # Single A-share by name")
        print("  python run.py 00700                   # Single Hong Kong stock")
        print("  python run.py 仙坛股份 百川畅银        # Multiple stocks")
        print("  python run.py 600519 00700 腾讯控股    # Mixed codes and names")
        print("")
        print("For multiple stocks:")
        print("  - Downloads run in PARALLEL (faster)")
        print("  - Uploads run SEQUENTIALLY (avoid conflicts)")
        sys.exit(1)

    # Get all stock inputs (support multiple stocks)
    stock_inputs = sys.argv[1:]
    total_stocks = len(stock_inputs)
    
    # Initialize downloader (shared across all stocks)
    downloader = CnInfoDownloader()
    
    # ===== PHASE 1: PARALLEL DOWNLOAD =====
    print(f"\n{'=' * 60}")
    print(f"📥 PHASE 1: DOWNLOADING (parallel, {total_stocks} stocks)")
    print(f"{'=' * 60}")
    
    download_results = []
    
    if total_stocks == 1:
        # Single stock: no need for parallel
        result = download_reports_for_stock(downloader, stock_inputs[0], 1, 1)
        download_results.append(result)
    else:
        # Multiple stocks: download in parallel
        with ThreadPoolExecutor(max_workers=min(total_stocks, 4)) as executor:
            futures = {
                executor.submit(download_reports_for_stock, downloader, stock_input, i, total_stocks): stock_input
                for i, stock_input in enumerate(stock_inputs, 1)
            }
            
            for future in as_completed(futures):
                result = future.result()
                download_results.append(result)
        
        # Sort by original order
        stock_input_to_index = {s: i for i, s in enumerate(stock_inputs)}
        download_results.sort(key=lambda r: stock_input_to_index.get(r.get("stock_input", ""), 999))
    
    # ===== PHASE 2: SEQUENTIAL UPLOAD =====
    print(f"\n{'=' * 60}")
    print(f"📤 PHASE 2: UPLOADING (sequential, {total_stocks} stocks)")
    print(f"{'=' * 60}")
    
    final_results = []
    
    for i, download_result in enumerate(download_results, 1):
        result = upload_reports_for_stock(download_result, i, total_stocks)
        final_results.append(result)
        
        # Add delay between uploads to ensure NotebookLM context is clear
        if i < total_stocks and result.get("success"):
            delay = 2
            print(f"\n⏳ Waiting {delay} seconds before next upload...")
            time.sleep(delay)
    
    # ===== FINAL SUMMARY =====
    if total_stocks > 1:
        print(f"\n{'=' * 60}")
        print(f"📋 BATCH SUMMARY ({total_stocks} stocks)")
        print(f"{'=' * 60}")
        
        successful = sum(1 for r in final_results if r.get("success"))
        failed = total_stocks - successful
        
        for i, (stock_input, result) in enumerate(zip(stock_inputs, final_results), 1):
            status = "✅" if result.get("success") else "❌"
            if result.get("success"):
                print(f"  {status} {i}. {result.get('stock_name', stock_input)}: {result.get('uploaded', 0)} uploaded")
            else:
                print(f"  {status} {i}. {stock_input}: {result.get('error', 'Unknown error')}")
        
        print(f"\n  Total: {successful} successful, {failed} failed")
    else:
        # Single stock summary
        result = final_results[0]
        if result.get("success"):
            print(f"\n{'=' * 50}")
            print(f"🎉 COMPLETE!")
            print(f"{'=' * 50}")
            print(f"📊 Stock: {result.get('stock_code')} ({result.get('stock_name')})")
            print(f"📚 Notebook: {result.get('stock_name')} 财务报告")
            print(f"📄 Uploaded: {result.get('uploaded', 0)} reports")
            if result.get("skipped"):
                print(f"⏭️ Skipped: {result.get('skipped')} reports")
            print(f"\n💡 Open NotebookLM and ask questions about {result.get('stock_name')}'s financials!")

if __name__ == "__main__":
    main()
