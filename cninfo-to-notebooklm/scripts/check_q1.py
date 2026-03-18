from download import CnInfoDownloader

downloader = CnInfoDownloader()
stock_code = '601636'
stock_name = '旗滨集团'

# 获取股票信息
code, info, market = downloader.find_stock(stock_name)
print(f"股票代码: {code}, 市场: {market}")
column, plate = downloader._get_exchange_info(code)
print(f"column: {column}, plate: {plate}")

# 获取公告
anns = downloader._fetch_all_announcements(code, "9900021239", column, plate)
print(f'共获取 {len(anns)} 条公告')
print()

# 查找2025年一季度相关公告
print('=== 2025年一季度相关公告 ===')
for ann in anns:
    title = ann.get('announcementTitle', '')
    if '2025' in title and ('一季' in title or '第一季' in title):
        print(f'标题: {title}')
        print(f'ID: {ann.get("announcementId", "")}')
        print(f'URL: {ann.get("adjunctUrl", "")}')
        print('---')
        # 测试识别
        is_q1 = downloader._is_periodic_report(title, 2025, "Q1")
        print(f'识别结果: {is_q1}')
        print()
