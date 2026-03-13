#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug script to check announcement titles"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from download import CnInfoDownloader

def main():
    if len(sys.argv) < 2:
        print("Usage: python debug_titles.py <stock_code_or_name>")
        sys.exit(1)

    stock_input = sys.argv[1]
    
    dl = CnInfoDownloader()
    code, info, market = dl.find_stock(stock_input)
    name = info.get("zwjc", code)
    org_id = info.get("orgId", "")
    
    print(f"📊 Stock: {code} ({name}) [{market}]")
    print(f"🔑 orgId: {org_id}")
    print(f"\n🔍 Fetching announcements...\n")
    
    anns = dl._fetch_announcements(code, org_id, max_pages=20)
    
    # Filter for annual reports
    print("=" * 60)
    print("年报相关公告 (包含'年度报告'):")
    print("=" * 60)
    for ann in anns:
        title = ann.get("announcementTitle", "")
        if "年度报告" in title:
            print(f"  - {title}")
    
    print("\n" + "=" * 60)
    print("季报/半年报相关公告:")
    print("=" * 60)
    for ann in anns:
        title = ann.get("announcementTitle", "")
        if any(kw in title for kw in ["季度", "半年度", "一季报", "三季报", "半年报"]):
            print(f"  - {title}")

if __name__ == "__main__":
    main()
