#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug script to check the actual API parameters"""

import sys
import os
import time
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.sync_api import sync_playwright

def main():
    stock_code = "002415"
    org_id = "9900012688"
    
    print(f"🔍 Inspecting API parameters for {stock_code}...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = context.new_page()
        
        all_requests = []
        
        def capture_request(request):
            if "hisAnnouncement/query" in request.url:
                post_data = request.post_data
                print(f"\n📋 Captured request to: {request.url}")
                print(f"📦 Post data: {post_data}")
                all_requests.append(post_data)
        
        page.on("request", capture_request)
        
        url = f"https://www.cninfo.com.cn/new/disclosure/stock?stockCode={stock_code}&orgId={org_id}"
        print(f"\n🌐 Navigating to: {url}")
        page.goto(url, wait_until="networkidle", timeout=30000)
        time.sleep(2)
        
        # Check page content
        print("\n📄 Checking page elements...")
        
        # Try to find filter options
        filters = page.evaluate('''() => {
            const selects = document.querySelectorAll('select');
            const results = [];
            selects.forEach(s => {
                results.push({
                    id: s.id,
                    name: s.name,
                    options: Array.from(s.options).map(o => ({value: o.value, text: o.text}))
                });
            });
            return results;
        }''')
        
        print("\n🔧 Available filters:")
        for f in filters:
            print(f"  - {f['id'] or f['name']}: {len(f['options'])} options")
            for opt in f['options'][:5]:
                print(f"      {opt['value']}: {opt['text']}")
        
        # Check if there's a date range filter
        print("\n📅 Looking for date inputs...")
        date_inputs = page.evaluate('''() => {
            const inputs = document.querySelectorAll('input[type="text"]');
            return Array.from(inputs).map(i => ({
                id: i.id,
                name: i.name,
                placeholder: i.placeholder,
                value: i.value
            }));
        }''')
        for inp in date_inputs:
            print(f"  - {inp}")
        
        browser.close()

if __name__ == "__main__":
    main()
