#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download A-share and Hong Kong stock reports from cninfo.com.cn
Uses Playwright for browser automation with proper API calls
"""

import sys
import os
import json
import tempfile
import datetime
import time
import httpx
from playwright.sync_api import sync_playwright

STOCKS_JSON = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "stocks.json"
)


def to_chinese_year(year: int) -> str:
    mapping = {"0": "零", "1": "一", "2": "二", "3": "三", "4": "四",
               "5": "五", "6": "六", "7": "七", "8": "八", "9": "九"}
    return "".join(mapping[d] for d in str(year))


class CnInfoDownloader:
    def __init__(self):
        self.market_to_stocks = self._load_stocks()
        self.timeout = 60.0

    def _load_stocks(self) -> dict:
        if os.path.exists(STOCKS_JSON):
            with open(STOCKS_JSON, "r") as f:
                return json.load(f)
        return {}

    def find_stock(self, stock_input: str) -> tuple:
        for market in ["szse", "hke"]:
            stocks = self.market_to_stocks.get(market, {})
            if stock_input in stocks:
                return stock_input, stocks[stock_input], market
        for market in ["szse", "hke"]:
            stocks = self.market_to_stocks.get(market, {})
            for code, info in stocks.items():
                if stock_input in info.get("zwjc", "") or stock_input.lower() == info.get("pinyin", "").lower():
                    return code, info, market
        if len(stock_input) == 5 and stock_input.startswith(("00", "01", "02", "09")):
            return stock_input, {"zwjc": stock_input}, "hke"
        return stock_input, {"zwjc": stock_input}, "szse"

    def _get_exchange_info(self, stock_code: str) -> tuple:
        """Get column and plate based on stock code"""
        # Hong Kong stocks: 5-digit codes starting with 00, 01, 02, 09
        if len(stock_code) == 5 and stock_code.startswith(("00", "01", "02", "09")):
            return "hke", "hk"
        # Shanghai stocks: 6xxxxx
        elif stock_code.startswith("6"):
            return "sse", "sh"
        # Shenzhen stocks: 0xxxxx, 3xxxxx
        elif stock_code.startswith(("0", "3")):
            return "szse", "sz"
        # Beijing stocks: 4xxxxx, 8xxxxx
        elif stock_code.startswith(("4", "8")):
            return "bse", "bj"
        # Default to Hong Kong for other 5-digit codes
        elif len(stock_code) == 5:
            return "hke", "hk"
        else:
            return "szse", "sz"
    
    def _fetch_hk_announcements(self, stock_code: str, search_key: str, max_pages: int = 10) -> list:
        """Fetch Hong Kong stock announcements using search API"""
        import urllib.parse
        all_announcements = []
        seen_ids = set()
        
        encoded_key = urllib.parse.quote(search_key)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            page = context.new_page()
            
            try:
                # Access HK disclosure page first
                page.goto(
                    "https://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice#hke%2F1_hkeMain",
                    wait_until="networkidle",
                    timeout=30000
                )
                time.sleep(1)
                
                for page_num in range(1, max_pages + 1):
                    result = page.evaluate('''async (params) => {
                        try {
                            const response = await fetch('/new/hisAnnouncement/query', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                                body: `stock=&tabName=fulltext&pageSize=30&pageNum=${params.page}&column=hke&plate=hk&category=&seDate=&searchkey=${params.key}&secid=&sortName=&sortType=&isHLtitle=true`
                            });
                            return await response.json();
                        } catch (e) {
                            return { error: e.toString() };
                        }
                    }''', {"page": page_num, "key": encoded_key})
                    
                    anns = result.get('announcements') or []
                    if not anns:
                        break
                    
                    new_count = 0
                    for ann in anns:
                        ann_id = ann.get('announcementId')
                        if ann_id and ann_id not in seen_ids:
                            seen_ids.add(ann_id)
                            all_announcements.append(ann)
                            new_count += 1
                    
                    if new_count == 0:
                        break
                        
            except Exception as e:
                print(f"      Error fetching HK announcements: {e}")
            
            browser.close()
        
        return all_announcements
    
    def _fetch_announcements_by_category(self, stock_code: str, org_id: str, category: str, 
                                          column: str, plate: str, max_pages: int = 20) -> list:
        """Fetch announcements with specific category filter"""
        all_announcements = []
        seen_ids = set()
        
        # Build the post data template
        post_data_template = (
            f"stock={stock_code}%2C{org_id}"
            f"&tabName=fulltext"
            f"&pageSize=30"
            f"&pageNum=1"
            f"&column={column}"
            f"&category={category}"
            f"&plate={plate}"
            f"&seDate="
            f"&searchkey="
            f"&secid="
            f"&sortName="
            f"&sortType="
            f"&isHLtitle=true"
        )
        
        print(f"    Fetching with category={category}...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            page = context.new_page()
            
            try:
                url = f"https://www.cninfo.com.cn/new/disclosure/stock?stockCode={stock_code}&orgId={org_id}"
                page.goto(url, wait_until="networkidle", timeout=30000)
                time.sleep(1)
                
                for page_num in range(1, max_pages + 1):
                    post_data = post_data_template.replace('pageNum=1', f'pageNum={page_num}')
                    
                    result = page.evaluate('''async (postData) => {
                        try {
                            const response = await fetch('/new/hisAnnouncement/query', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/x-www-form-urlencoded',
                                    'X-Requested-With': 'XMLHttpRequest'
                                },
                                body: postData
                            });
                            return await response.json();
                        } catch (e) {
                            return { error: e.toString() };
                        }
                    }''', post_data)
                    
                    anns = result.get('announcements') or []
                    if not anns:
                        print(f"      Page {page_num}: no results, stopping")
                        break
                    
                    # Deduplicate
                    new_anns = []
                    for ann in anns:
                        ann_id = ann.get('announcementId')
                        if ann_id and ann_id not in seen_ids:
                            seen_ids.add(ann_id)
                            new_anns.append(ann)
                    
                    if new_anns:
                        all_announcements.extend(new_anns)
                        print(f"      Page {page_num}: {len(new_anns)} new items, total: {len(all_announcements)}")
                    else:
                        print(f"      Page {page_num}: no new items, stopping")
                        break
                    
                    if len(anns) < 30:
                        break
                        
            except Exception as e:
                print(f"      Error: {e}")
            
            browser.close()
        
        return all_announcements

    def _fetch_all_announcements(self, stock_code: str, org_id: str, column: str, plate: str) -> list:
        """Fetch all announcements by combining results from different categories"""
        all_announcements = []
        seen_ids = set()
        
        # Categories for different report types
        categories = [
            "category_ndbg_szsh",  # 年度报告
            "category_bndbg_szsh",  # 半年度报告
            "category_yjdbg_szsh",  # 一季度报告
            "category_sjdbg_szsh",  # 三季度报告
        ]
        
        for category in categories:
            anns = self._fetch_announcements_by_category(stock_code, org_id, category, column, plate, max_pages=20)
            for ann in anns:
                ann_id = ann.get('announcementId')
                if ann_id and ann_id not in seen_ids:
                    seen_ids.add(ann_id)
                    all_announcements.append(ann)
        
        print(f"  Total unique announcements: {len(all_announcements)}")
        return all_announcements

    def _is_annual_report(self, title: str, year: int) -> bool:
        year_cn = to_chinese_year(year)
        # Check for year in title
        if str(year) not in title and year_cn not in title:
            return False
        # Must be annual report
        if "年度报告" not in title:
            return False
        # Exclude non-full reports (must check 半年度 before 年度)
        if any(kw in title for kw in ["半年度", "摘要", "英文", "节选", "审计报告", "内部控制", "社会责任", "环境", "ESG"]):
            return False
        return True

    def _is_periodic_report(self, title: str, year: int, rtype: str) -> bool:
        if str(year) not in title:
            return False
        if any(kw in title for kw in ["摘要", "英文", "节选"]):
            return False
        keywords = {
            "Q1": ["第一季度报告", "第一季度报", "一季度报告", "一季度报", "一季报"],
            "semi": ["半年度报告", "半年度报", "中期报告"],
            "Q3": ["第三季度报告", "第三季度报", "三季度报告", "三季度报", "三季报"],
        }
        return any(kw in title for kw in keywords.get(rtype, []))

    def _download_pdf(self, url: str, output_path: str) -> bool:
        try:
            # Ensure proper URL format
            if url.startswith("http://static.cninfo.com.cn/"):
                url = url
            elif url.startswith("/"):
                url = f"http://static.cninfo.com.cn{url}"
            else:
                url = f"http://static.cninfo.com.cn/{url}"
            
            resp = httpx.get(url, follow_redirects=True, timeout=self.timeout)
            if resp.status_code == 200 and b"%PDF" in resp.content[:1024]:
                with open(output_path, "wb") as f:
                    f.write(resp.content)
                return True
        except Exception as e:
            print(f"      Download error: {e}")
        return False

    def _is_hk_annual_report(self, title: str, year: int) -> bool:
        """Check if title is a Hong Kong annual report for given year"""
        import re
        title_clean = title.replace('<em>', '').replace('</em>', '')
        
        # Check for year in both Arabic and Chinese numerals
        year_str = str(year)
        chinese_year = to_chinese_year(year)
        if year_str not in title_clean and chinese_year not in title_clean:
            return False
        
        # HK annual report patterns
        patterns = [
            r'年报',
            r'年度报告',
            r'财务年度报告',
            r'annual\s*report',
        ]
        
        if not any(re.search(p, title_clean, re.IGNORECASE) for p in patterns):
            return False
        
        # Exclude non-full reports
        exclude_keywords = [
            "摘要", "英文", "节选", "中期报告", "季度", "季报",
            "半年度", "半年报", "ESG", "社会责任", "内部控制"
        ]
        if any(kw in title_clean for kw in exclude_keywords):
            return False
        
        return True

    def _is_hk_periodic_report(self, title: str, year: int, rtype: str) -> bool:
        """Check if title is a Hong Kong periodic report
        
        HK stocks use different formats:
        - Q1: 截至X年3月31日止三个月的业绩公告
        - semi: X年中期报告 或 截至X年6月30日止三个月及六个月的业绩公告
        - Q3: 截至X年9月30日止三个月及九个月的业绩公告
        - Q4: X年第四季度及全年未经审计财务业绩公告
        """
        title_clean = title.replace('<em>', '').replace('</em>', '')
        
        # Check year in both Arabic and Chinese numerals
        year_str = str(year)
        chinese_year = to_chinese_year(year)
        if year_str not in title_clean and chinese_year not in title_clean:
            return False
        
        # Map months to report types
        # Q1: March (3月)
        # semi: June (6月) 
        # Q3: September (9月)
        # Q4: December (12月) - 全年业绩
        month_patterns = {
            "Q1": [r'3月31日', r'3月30日', r'第一季', r'一季报', '三月三十一日', '第一季度'],
            "semi": [r'6月30日', r'中期报告', r'半年报', r'半年度', r'中期', '六月三十日', '第二季度'],
            "Q3": [r'9月30日', r'第三季', r'三季报', '九月三十日', '第三季度'],
            "Q4": [r'12月31日', r'第四季', r'四季报', '十二月三十一日', '第四季度', '全年'],
        }
        
        # Check for "业绩公告" or "业绩公布" with matching month
        if '业绩' in title_clean:
            for pattern in month_patterns.get(rtype, []):
                if pattern in title_clean:
                    return True
        
        # Also check traditional patterns
        patterns = {
            "Q1": [r'第一季', r'一季'],
            "semi": [r'中期报告', r'半年', r'interim', r'中期'],
            "Q3": [r'第三季', r'三季'],
            "Q4": [r'第四季', r'四季', r'全年'],
        }
        
        return any(p in title_clean.lower() for p in patterns.get(rtype, []))

    def download_annual_reports(self, stock_code: str, org_id: str, years: list, 
                                  output_dir: str, market: str) -> list:
        column, plate = self._get_exchange_info(stock_code)
        
        # Hong Kong stocks use search API
        if market == "hke" or column == "hke":
            print(f"  Fetching HK stock announcements (stock={stock_code})...")
            anns = self._fetch_hk_announcements(stock_code, stock_code, max_pages=10)
            
            files = []
            found_years = set()
            
            for ann in anns:
                # Filter by stock code
                if ann.get('secCode') != stock_code:
                    continue
                    
                title = ann.get("announcementTitle", "")
                title_clean = title.replace('<em>', '').replace('</em>', '')
                
                for year in years:
                    if year in found_years:
                        continue
                    if self._is_hk_annual_report(title, year):
                        url = ann.get('adjunctUrl', '')
                        path = os.path.join(output_dir, f"{stock_code}_{year}_annual.pdf")
                        if self._download_pdf(url, path):
                            print(f"    ✅ {title_clean}")
                            files.append(path)
                            found_years.add(year)
                            break
            
            return files
        
        # A-share stocks use category-based API
        print(f"  Fetching announcements (column={column}, plate={plate})...")
        anns = self._fetch_all_announcements(stock_code, org_id, column, plate)
        
        files = []
        for year in years:
            print(f"  Looking for {year} annual report...")
            for ann in anns:
                title = ann.get("announcementTitle", "")
                if self._is_annual_report(title, year):
                    url = ann.get('adjunctUrl', '')
                    path = os.path.join(output_dir, f"{stock_code}_{year}_annual.pdf")
                    if self._download_pdf(url, path):
                        print(f"    ✅ {title}")
                        files.append(path)
                        break
        return files

    def download_periodic_reports(self, stock_code: str, org_id: str, year: int,
                                    output_dir: str, market: str) -> list:
        column, plate = self._get_exchange_info(stock_code)
        
        # Hong Kong stocks use search API
        if market == "hke" or column == "hke":
            print(f"  Fetching HK periodic reports (stock={stock_code})...")
            anns = self._fetch_hk_announcements(stock_code, stock_code, max_pages=10)
            
            files = []
            for rtype in ["Q1", "semi", "Q3", "Q4"]:
                for ann in anns:
                    if ann.get('secCode') != stock_code:
                        continue
                        
                    title = ann.get("announcementTitle", "")
                    title_clean = title.replace('<em>', '').replace('</em>', '')
                    
                    if self._is_hk_periodic_report(title, year, rtype):
                        url = ann.get('adjunctUrl', '')
                        # Q4财报包含全年数据，保存为annual
                        save_type = "annual" if rtype == "Q4" else rtype
                        path = os.path.join(output_dir, f"{stock_code}_{year}_{save_type}.pdf")
                        if self._download_pdf(url, path):
                            print(f"    ✅ {title_clean}")
                            files.append(path)
                            break
            return files
        
        # A-share stocks use category-based API
        print(f"  Fetching announcements for periodic reports (column={column}, plate={plate})...")
        anns = self._fetch_all_announcements(stock_code, org_id, column, plate)
        
        files = []
        for rtype in ["Q1", "semi", "Q3"]:
            print(f"  Looking for {year} {rtype} report...")
            for ann in anns:
                title = ann.get("announcementTitle", "")
                if self._is_periodic_report(title, year, rtype):
                    url = ann.get('adjunctUrl', '')
                    path = os.path.join(output_dir, f"{stock_code}_{year}_{rtype}.pdf")
                    if self._download_pdf(url, path):
                        print(f"    ✅ {title}")
                        files.append(path)
                        break
        return files


def main():
    if len(sys.argv) < 2:
        print("Usage: python download.py <stock_code_or_name> [output_dir]")
        sys.exit(1)

    stock_input = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else tempfile.mkdtemp(prefix="cninfo_reports_")

    dl = CnInfoDownloader()
    code, info, market = dl.find_stock(stock_input)
    name = info.get("zwjc", code)
    org_id = info.get("orgId", "")
    
    print(f"📊 Stock: {code} ({name}) [{market}]")
    print(f"📁 Output: {output_dir}")

    now = datetime.datetime.now().year
    # 默认下载近10年年报
    years = list(range(now - 9, now + 1))

    print(f"\n📥 Annual reports: {years}")
    annual = dl.download_annual_reports(code, org_id, years, output_dir, market)

    print(f"\n📥 Periodic reports {now}...")
    periodic = dl.download_periodic_reports(code, org_id, now, output_dir, market)
    
    if not periodic:
        print(f"  Trying {now-1}...")
        periodic = dl.download_periodic_reports(code, org_id, now-1, output_dir, market)

    all_files = annual + periodic
    print(f"\n{'='*50}")
    print(f"✅ Downloaded {len(all_files)} reports")
    for f in all_files:
        print(f"  {os.path.basename(f)}")

    result = {"stock_code": code, "stock_name": name, "market": market, 
              "output_dir": output_dir, "files": all_files}
    print(f"\n---JSON_OUTPUT---")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
