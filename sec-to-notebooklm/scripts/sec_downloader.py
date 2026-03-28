#!/usr/bin/env python3
"""
SEC EDGAR 美股研报下载器
支持下载 10-K、10-Q、8-K、DEF 14A 等 SEC 披露文件
"""

import os
import re
import sys
import json
import time
import argparse
import warnings
import requests
import urllib3
from pathlib import Path
from urllib.parse import urljoin
from datetime import datetime

# 忽略 SSL 警告（某些网络环境需要）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

EDGAR_BASE = "https://data.sec.gov"
EDGAR_WWW_BASE = "https://www.sec.gov"  # 实际文档托管在 www.sec.gov
EDGAR_FULL_TEXT_SEARCH = "https://efts.sec.gov/LATEST/search-index"
EDGAR_SEARCH = "https://efts.sec.gov/LATEST/search-index?q=%22{query}%22&dateRange=custom&startdt={start}&enddt={end}&forms={form}"
HEADERS = {
    "User-Agent": "SEC-Downloader research@example.com",
    "Accept": "application/json",
}

# SSL 验证设置（如遇到 SSL 错误自动降级）
SSL_VERIFY = True


def safe_get(url, **kwargs) -> requests.Response:
    """带 SSL 降级的 GET 请求"""
    global SSL_VERIFY
    try:
        return requests.get(url, headers=HEADERS, verify=SSL_VERIFY, **kwargs)
    except requests.exceptions.SSLError:
        SSL_VERIFY = False
        print("⚠️  SSL 验证降级（网络代理环境）")
        return requests.get(url, headers=HEADERS, verify=False, **kwargs)

FORM_TYPES = {
    "10-K": "年度报告",
    "10-Q": "季度报告",
    "8-K": "重大事件公告",
    "DEF 14A": "股东大会代理说明书",
    "20-F": "外国私人发行人年度报告（中概股）",
    "6-K": "外国私人发行人中期报告",
    "S-1": "IPO招股说明书",
}


def search_company(ticker_or_name: str) -> dict | None:
    """通过股票代码或公司名搜索公司 CIK"""
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?company={ticker_or_name}&CIK=&type=&dateb=&owner=include&count=10&search_text=&action=getcompany&output=atom"
    # 优先用 company_tickers.json 精确匹配 ticker
    tickers_url = "https://www.sec.gov/files/company_tickers.json"
    try:
        resp = safe_get(tickers_url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        ticker_upper = ticker_or_name.upper()
        for _, info in data.items():
            if info.get("ticker", "").upper() == ticker_upper:
                cik = str(info["cik_str"]).zfill(10)
                print(f"✅ 找到公司: {info['title']} (CIK: {cik})")
                return {"cik": cik, "name": info["title"], "ticker": info["ticker"]}
    except Exception as e:
        print(f"⚠️ ticker 精确搜索失败: {e}")

    # 模糊搜索
    try:
        resp = safe_get(f"https://www.sec.gov/cgi-bin/browse-edgar?company={ticker_or_name}&CIK=&type=10-K&dateb=&owner=include&count=5&search_text=&action=getcompany&output=atom",
                        timeout=15)
        # 简单解析返回的 atom xml
        cik_match = re.search(r'<cik>(\d+)</cik>', resp.text)
        name_match = re.search(r'<conformed-name>(.*?)</conformed-name>', resp.text)
        if cik_match:
            cik = cik_match.group(1).zfill(10)
            name = name_match.group(1) if name_match else ticker_or_name
            print(f"✅ 模糊匹配公司: {name} (CIK: {cik})")
            return {"cik": cik, "name": name, "ticker": ticker_or_name}
    except Exception as e:
        print(f"⚠️ 模糊搜索失败: {e}")
    return None


def get_filings(cik: str, form_type: str = "10-K", count: int = 999,
                start_year: int = None, end_year: int = None) -> list:
    """
    获取公司的 SEC 报告列表

    参数:
        cik:        公司 CIK（10 位字符串）
        form_type:  报告类型，如 10-K / 10-Q
        count:      最多返回条数（默认不限制）
        start_year: 筛选起始年份（含），如 2015
        end_year:   筛选截止年份（含），如 2024
    """
    url = f"{EDGAR_BASE}/submissions/CIK{cik}.json"
    try:
        resp = safe_get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"❌ 获取提交记录失败: {e}")
        return []

    filings = []

    def _parse_section(recent: dict):
        forms = recent.get("form", [])
        accessions = recent.get("accessionNumber", [])
        dates = recent.get("filingDate", [])
        descriptions = recent.get("primaryDocument", [])
        for i, form in enumerate(forms):
            if len(filings) >= count:
                break
            if form.upper() != form_type.upper():
                continue
            filing_date = dates[i] if i < len(dates) else ""
            # 年份过滤
            if filing_date and (start_year or end_year):
                try:
                    year = int(filing_date[:4])
                    if start_year and year < start_year:
                        continue
                    if end_year and year > end_year:
                        continue
                except ValueError:
                    pass
            filings.append({
                "form": form,
                "accession": accessions[i].replace("-", ""),
                "accession_raw": accessions[i],
                "date": filing_date,
                "primary_doc": descriptions[i] if i < len(descriptions) else "",
            })

    # 先解析 recent，再解析历史归档分页（files 字段）
    _parse_section(data.get("filings", {}).get("recent", {}))

    if len(filings) < count:
        for extra_file in data.get("filings", {}).get("files", []):
            if len(filings) >= count:
                break
            extra_url = f"{EDGAR_BASE}/submissions/{extra_file['name']}"
            try:
                r = safe_get(extra_url, timeout=15)
                r.raise_for_status()
                _parse_section(r.json())
            except Exception as e:
                print(f"⚠️ 获取历史归档失败: {e}")
                break

    range_str = ""
    if start_year or end_year:
        range_str = f"（{start_year or ''}～{end_year or ''}年）"
    print(f"📋 找到 {len(filings)} 份 {form_type} 报告{range_str}")
    return filings


def download_filing(cik: str, filing: dict, output_dir: str) -> list:
    """下载单份 SEC 报告，返回下载的文件路径列表"""
    accession = filing["accession"]
    accession_raw = filing["accession_raw"]
    date = filing["date"]
    form = filing["form"]

    # 获取报告索引
    index_url = f"{EDGAR_WWW_BASE}/Archives/edgar/data/{int(cik)}/{accession}/{accession_raw}-index.json"
    try:
        resp = safe_get(index_url, timeout=15)
        resp.raise_for_status()
        index = resp.json()
    except Exception as e:
        print(f"⚠️ 获取索引失败，尝试备用方式: {e}")
        index = {"documents": []}

    downloaded = []
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 优先下载主文档
    primary_doc = filing.get("primary_doc", "")
    if primary_doc:
        doc_url = f"{EDGAR_WWW_BASE}/Archives/edgar/data/{int(cik)}/{accession}/{primary_doc}"
        ext = Path(primary_doc).suffix or ".txt"
        safe_form = form.replace(" ", "_").replace("/", "_")
        filename = f"{safe_form}_{date}_{primary_doc}"
        save_path = output_path / filename

        try:
            print(f"📥 下载: {doc_url}")
            r = safe_get(doc_url, timeout=30)
            r.raise_for_status()
            save_path.write_bytes(r.content)
            print(f"✅ 已保存: {save_path}")
            downloaded.append(str(save_path))
        except Exception as e:
            print(f"❌ 下载失败 {doc_url}: {e}")

    # 如果没有主文档，尝试从索引获取
    if not downloaded:
        for doc in index.get("documents", [])[:3]:
            doc_name = doc.get("document", "")
            doc_type = doc.get("type", "")
            if not doc_name:
                continue
            doc_url = f"{EDGAR_WWW_BASE}/Archives/edgar/data/{int(cik)}/{accession}/{doc_name}"
            safe_form = form.replace(" ", "_").replace("/", "_")
            filename = f"{safe_form}_{date}_{doc_name}"
            save_path = output_path / filename
            try:
                print(f"📥 下载: {doc_url}")
                r = safe_get(doc_url, timeout=30)
                r.raise_for_status()
                save_path.write_bytes(r.content)
                print(f"✅ 已保存: {save_path}")
                downloaded.append(str(save_path))
                break
            except Exception as e:
                print(f"❌ 下载失败: {e}")

    time.sleep(0.5)  # 遵守 SEC EDGAR 访问频率限制
    return downloaded


def main():
    current_year = datetime.now().year

    parser = argparse.ArgumentParser(
        description="从 SEC EDGAR 下载美股研报",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
支持的报告类型:
{chr(10).join(f'  {k:12s} - {v}' for k, v in FORM_TYPES.items())}

默认行为（不指定 --form）:
  · 近10年 10-K 年报
  · 最近1年 10-Q 季报（约4份）
  · 最近1年 DEF 14A 股东大会代理说明书

示例:
  # 默认模式
  python3 sec_downloader.py AAPL

  # 只下载 10-K 年报
  python3 sec_downloader.py TSLA --form 10-K

  # 指定年份范围
  python3 sec_downloader.py NVDA --form 10-K --start-year 2018 --end-year 2023

  # 每类最多N份
  python3 sec_downloader.py TSLA --count 5

  # 中概股年报
  python3 sec_downloader.py BABA --form 20-F
        """
    )
    parser.add_argument("ticker", help="股票代码（如 AAPL、TSLA）或公司名称")
    parser.add_argument("--form", "-f", default=None,
                        choices=list(FORM_TYPES.keys()),
                        help="报告类型（不指定则下载全部：10-K、10-Q、8-K、DEF 14A）")
    parser.add_argument("--count", "-n", type=int, default=None,
                        help="每种报告类型的最大下载数量（默认不限制，下载全部）")
    parser.add_argument("--start-year", type=int, default=None,
                        help="筛选起始年份，如 2015")
    parser.add_argument("--end-year", type=int, default=None,
                        help="筛选截止年份，如 2024")
    parser.add_argument("--output", "-o", default="./sec_reports",
                        help="输出目录（默认: ./sec_reports）")

    args = parser.parse_args()

    print(f"\n🔍 搜索公司: {args.ticker}")
    company = search_company(args.ticker)
    if not company:
        print(f"❌ 未找到公司: {args.ticker}")
        sys.exit(1)

    ticker_safe = args.ticker.replace("/", "_").upper()
    output_dir = os.path.join(args.output, ticker_safe)
    all_files = []

    # ── 确定要下载的任务列表 ──────────────────────────────────────────
    # 默认行为：近10年 10-K + 最近1年 10-Q + 最近1年 DEF 14A
    tasks = []
    if args.form is None:
        tasks.append({
            "form": "10-K",
            "count": args.count or 999,
            "start_year": args.start_year or (current_year - 10),
            "end_year": args.end_year or current_year,
            "label": f"近10年年报 10-K（{current_year - 10}～{current_year}）",
        })
        tasks.append({
            "form": "10-Q",
            "count": args.count or 999,
            "start_year": args.start_year or (current_year - 1),
            "end_year": args.end_year or current_year,
            "label": f"最近1年季报 10-Q（{current_year - 1}～{current_year}）",
        })
        tasks.append({
            "form": "DEF 14A",
            "count": args.count or 999,
            "start_year": args.start_year or (current_year - 1),
            "end_year": args.end_year or current_year,
            "label": f"最近1年股东大会代理说明书 DEF 14A（{current_year - 1}～{current_year}）",
        })
    else:
        # 用户手动指定 form
        tasks.append({
            "form": args.form,
            "count": args.count or 999,
            "start_year": args.start_year,
            "end_year": args.end_year,
            "label": f"{args.form} 报告",
        })

    # ── 逐任务下载 ────────────────────────────────────────────────────
    for task in tasks:
        print(f"\n{'='*55}")
        print(f"  📂 {task['label']}")
        print(f"{'='*55}")

        filings = get_filings(
            company["cik"],
            form_type=task["form"],
            count=task["count"],
            start_year=task.get("start_year"),
            end_year=task.get("end_year"),
        )
        if not filings:
            print(f"⚠️  未找到 {task['form']} 报告，跳过")
            continue

        print(f"\n⬇️  开始下载到 {output_dir} ...")
        for filing in filings:
            print(f"\n  📑 {filing['form']} | {filing['date']} | {filing['accession_raw']}")
            files = download_filing(company["cik"], filing, output_dir)
            all_files.extend(files)

    if not all_files:
        print("\n❌ 没有成功下载任何文件")
        sys.exit(1)

    # ── 写入结果清单 ──────────────────────────────────────────────────
    manifest = {
        "company": company,
        "tasks": [t["label"] for t in tasks],
        "downloaded_at": datetime.now().isoformat(),
        "files": all_files,
    }
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    manifest_path = os.path.join(output_dir, "manifest.json")
    Path(manifest_path).write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

    print(f"\n🎉 下载完成！共 {len(all_files)} 个文件")
    print(f"📁 保存目录: {output_dir}")
    print(f"📋 清单文件: {manifest_path}")

    # 输出文件列表供后续脚本使用
    print("\n=== DOWNLOADED_FILES_START ===")
    for f in all_files:
        print(f)
    print("=== DOWNLOADED_FILES_END ===")

    return all_files


if __name__ == "__main__":
    main()
