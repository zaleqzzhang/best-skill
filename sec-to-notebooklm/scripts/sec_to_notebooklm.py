#!/usr/bin/env python3
"""
SEC → NotebookLM 一键工作流
自动完成：搜索公司 → 下载报告 → 上传 NotebookLM
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path


def run_script(script_path: str, args: list) -> tuple[int, str]:
    """运行子脚本"""
    cmd = [sys.executable, script_path] + args
    result = subprocess.run(cmd, capture_output=False, text=True)
    return result.returncode, ""


def main():
    parser = argparse.ArgumentParser(
        description="SEC → NotebookLM 一键工作流",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 默认模式：近10年10-K + 最近1年10-Q + 最近1年DEF 14A，自动上传到 NotebookLM
  python3 sec_to_notebooklm.py AAPL

  # 手动指定：下载特斯拉5份季报
  python3 sec_to_notebooklm.py TSLA --form 10-Q --count 5 --notebook "TSLA Research"

  # 中概股（阿里巴巴）20-F 年报
  python3 sec_to_notebooklm.py BABA --form 20-F

  # 首次使用（需 Google 登录）
  python3 sec_to_notebooklm.py AAPL --no-headless

  # 只下载不上传
  python3 sec_to_notebooklm.py AAPL --download-only
        """
    )
    parser.add_argument("ticker", help="股票代码（如 AAPL、TSLA、NVDA）")
    parser.add_argument("--form", "-f", default=None,
                        choices=["10-K", "10-Q", "8-K", "DEF 14A", "20-F", "6-K", "S-1"],
                        help="报告类型（不指定则下载全部：10-K、10-Q、8-K、DEF 14A）")
    parser.add_argument("--count", "-n", type=int, default=None,
                        help="每种类型最大下载数量（默认不限制，下载全部）")
    parser.add_argument("--output", "-o", default="./sec_reports",
                        help="本地保存目录（默认: ./sec_reports）")
    parser.add_argument("--notebook", help="NotebookLM 笔记本名称（不填则自动创建）")
    parser.add_argument("--no-headless", action="store_true",
                        help="显示浏览器窗口（首次登录 Google 时使用）")
    parser.add_argument("--download-only", action="store_true",
                        help="只下载，不上传到 NotebookLM")

    args = parser.parse_args()

    scripts_dir = Path(__file__).parent

    # ── 步骤 1：下载 ──────────────────────────────────────────────────
    print("=" * 60)
    form_label = args.form or "10-K（近10年）+ 10-Q（最近1年）"
    print(f"  步骤 1/2  从 SEC EDGAR 下载 {args.ticker} {form_label}")
    print("=" * 60)

    download_args = [args.ticker, "--output", args.output]
    if args.form:
        download_args += ["--form", args.form]
    if args.count is not None:
        download_args += ["--count", str(args.count)]

    rc, _ = run_script(str(scripts_dir / "sec_downloader.py"), download_args)
    if rc != 0:
        print(f"\n❌ 下载失败（exit code: {rc}）")
        sys.exit(rc)

    # 读取 manifest 确认下载文件
    ticker_safe = args.ticker.upper().replace("/", "_")
    manifest_path = Path(args.output) / ticker_safe / "manifest.json"
    if not manifest_path.exists():
        print(f"\n❌ 未找到下载清单: {manifest_path}")
        sys.exit(1)

    with open(manifest_path) as f:
        manifest = json.load(f)

    downloaded_files = manifest.get("files", [])
    if not downloaded_files:
        print("\n❌ 没有下载到任何文件")
        sys.exit(1)

    print(f"\n✅ 步骤 1 完成，共下载 {len(downloaded_files)} 个文件")

    if args.download_only:
        print("\n📌 --download-only 模式，跳过上传步骤")
        print(f"📁 文件保存在: {Path(args.output) / ticker_safe}")
        return

    # ── 步骤 2：上传到 NotebookLM ─────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"  步骤 2/2  上传到 NotebookLM")
    print("=" * 60)

    # 设置默认笔记本名称
    form_label_nb = args.form or "All-Filings"
    notebook_name = args.notebook or f"{args.ticker.upper()} {form_label_nb} SEC Reports"

    upload_args = [
        "--manifest", str(manifest_path),
        "--notebook", notebook_name,
    ]
    if args.no_headless:
        upload_args.append("--no-headless")

    # 使用 V2 上传器（支持笔记本复用）
    uploader_script = scripts_dir / "notebooklm_uploader_v2.py"
    if not uploader_script.exists():
        # 降级到 V1
        uploader_script = scripts_dir / "notebooklm_uploader.py"
    
    rc, _ = run_script(str(uploader_script), upload_args)
    if rc != 0:
        print(f"\n⚠️  上传过程中出现问题（exit code: {rc}）")
        print(f"📁 文件已保存至: {Path(args.output) / ticker_safe}")
        print(f"💡 可手动运行上传：python3 {scripts_dir}/notebooklm_uploader.py --manifest {manifest_path}")
    else:
        print(f"\n🎉 全部完成！{args.ticker} 报告已上传到 NotebookLM 笔记本 '{notebook_name}'")


if __name__ == "__main__":
    main()
