from download import CnInfoDownloader

downloader = CnInfoDownloader()
stock_code = '002079'
stock_name = '苏州固锝'

# 获取2025年公告
announcements = downloader._fetch_announcements(stock_code, 'szse', 'sz')
print(f'共获取 {len(announcements)} 条公告')
print()

# 查找2025年一季度相关公告
print('=== 2025年一季度相关公告 ===')
found = False
for ann in announcements:
    title = ann.get('announcementTitle', '')
    if '2025' in title and ('一季' in title or '第一季度' in title):
        print(f'标题: {title}')
        print(f'时间: {ann.get("announcementTime", "")}')
        print(f'URL: {ann.get("adjunctUrl", "")}')
        print('---')
        found = True

if not found:
    print('未找到2025年一季度公告')
    print()
    print('=== 所有2025年公告 ===')
    for ann in announcements:
        title = ann.get('announcementTitle', '')
        if '2025' in title:
            print(f'标题: {title}')
            print(f'时间: {ann.get("announcementTime", "")}')
            print('---')
