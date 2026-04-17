#!/usr/bin/env python3
"""
东方财富研报API辅助抓取脚本
用于补充中信建投研报以外的其他券商行业研报

用法:
    python3 eastmoney_fetch.py --industry 448 --days 1
    python3 eastmoney_fetch.py --industry 448 --begin 2026-04-15 --end 2026-04-16
    python3 eastmoney_fetch.py --industry 448 --keyword "光纤" --days 7
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta


API_URL = "https://reportapi.eastmoney.com/report/list"

# 常用行业代码
INDUSTRY_CODES = {
    "通信设备": "448",
    "半导体": "1036",
    "光学光电子": "450",
    "计算机应用": "707",
    "医疗器械": "376",
    "全部": "*",
}


def fetch_reports(industry_code, begin_date, end_date, page=1, page_size=50):
    """调用东方财富研报API获取研报列表"""
    params = {
        "industryCode": industry_code,
        "pageSize": str(page_size),
        "industry": "",
        "rating": "",
        "ratingChange": "",
        "beginTime": begin_date,
        "endTime": end_date,
        "pageNo": str(page),
        "fields": "",
        "qType": "1",
        "orgCode": "",
        "code": "",
        "author": "",
        "p": str(page),
        "pageNum": str(page),
        "_": str(int(datetime.now().timestamp() * 1000)),
    }

    query_string = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{API_URL}?{query_string}"

    # 添加回调函数名
    callback = "datatable" + str(int(datetime.now().timestamp() * 1000))
    url += f"&callback={callback}"

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    req.add_header("Referer", "https://data.eastmoney.com/")

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            text = response.read().decode("utf-8")

        # 解析JSONP: callback({...})
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            print(f"[ERROR] 无法解析API响应", file=sys.stderr)
            return None

        data = json.loads(match.group())
        return data
    except Exception as e:
        print(f"[ERROR] API请求失败: {e}", file=sys.stderr)
        return None


def format_report(report):
    """格式化单条研报信息"""
    title = report.get("title", "未知")
    org = report.get("orgSName", "未知")
    author = report.get("researcher", "未知")
    pub_date = report.get("publishDate", "")[:10]
    info_code = report.get("infoCode", "")
    pdf_url = f"https://pdf.dfcfw.com/pdf/H3_{info_code}_1.pdf" if info_code else ""
    rating = report.get("emRatingName", "")
    pages = report.get("count", 0)

    return {
        "title": title,
        "org": org,
        "author": author,
        "date": pub_date,
        "rating": rating,
        "pages": pages,
        "pdf_url": pdf_url,
        "info_code": info_code,
    }


def download_pdf(report, output_dir):
    """下载单篇研报PDF"""
    if not report["pdf_url"]:
        return False

    os.makedirs(output_dir, exist_ok=True)
    filename = re.sub(r'[\\/:*?"<>|]', "_", report["title"])[:50] + ".pdf"
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath):
        print(f"  [SKIP] 已存在: {filename}")
        return True

    try:
        req = urllib.request.Request(report["pdf_url"])
        req.add_header("User-Agent", "Mozilla/5.0")
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(filepath, "wb") as f:
                f.write(response.read())
        size_kb = os.path.getsize(filepath) / 1024
        print(f"  [OK] {filename} ({size_kb:.1f} KB)")
        return True
    except Exception as e:
        print(f"  [FAIL] {filename}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="东方财富研报API抓取工具")
    parser.add_argument("--industry", default="448", help="行业代码 (默认448=通信设备)")
    parser.add_argument("--days", type=int, default=1, help="查询最近N天 (默认1)")
    parser.add_argument("--begin", help="开始日期 YYYY-MM-DD")
    parser.add_argument("--end", help="结束日期 YYYY-MM-DD")
    parser.add_argument("--keyword", help="关键词过滤")
    parser.add_argument("--download", action="store_true", help="下载PDF")
    parser.add_argument("--output", default=".", help="输出目录")
    parser.add_argument("--limit", type=int, default=20, help="最大返回条数")

    args = parser.parse_args()

    # 处理日期
    if args.begin and args.end:
        begin_date = args.begin
        end_date = args.end
    else:
        end_date = datetime.now().strftime("%Y-%m-%d")
        begin_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")

    # 查行业名称
    industry_name = next(
        (k for k, v in INDUSTRY_CODES.items() if v == args.industry), args.industry
    )

    print(f"=== 东方财富研报 ===")
    print(f"行业: {industry_name} ({args.industry})")
    print(f"日期: {begin_date} ~ {end_date}")
    if args.keyword:
        print(f"关键词: {args.keyword}")
    print()

    data = fetch_reports(args.industry, begin_date, end_date, page_size=args.limit)
    if not data or "data" not in data:
        print("[ERROR] 未获取到数据")
        return

    reports = [format_report(r) for r in data["data"]]

    # 关键词过滤
    if args.keyword:
        reports = [r for r in reports if args.keyword in r["title"]]

    if not reports:
        print("未找到符合条件的研报")
        return

    # 输出结果
    print(f"找到 {len(reports)} 篇研报:\n")
    for i, r in enumerate(reports, 1):
        print(f"{i}. [{r['date']}] {r['title']}")
        print(f"   机构: {r['org']} | 分析师: {r['author']} | 评级: {r['rating']}")
        if r["pdf_url"]:
            print(f"   PDF: {r['pdf_url']}")
        print()

    # 下载PDF
    if args.download:
        pdf_dir = os.path.join(args.output, "pdf", begin_date.replace("-", ""))
        print(f"\n开始下载PDF到 {pdf_dir}/ ...")
        success = 0
        for r in reports:
            if download_pdf(r, pdf_dir):
                success += 1
        print(f"\n下载完成: {success}/{len(reports)}")

    # 保存JSON
    json_path = os.path.join(args.output, f"eastmoney_{args.industry}_{end_date}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(reports, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存: {json_path}")


if __name__ == "__main__":
    main()
