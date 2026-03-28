#!/usr/bin/env python3
"""
NotebookLM 自动上传器
将本地文件自动上传到 Google NotebookLM 指定笔记本
依赖：需配置 Google 账号 Cookie 或使用浏览器自动化（Playwright）
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path


NOTEBOOKLM_URL = "https://notebooklm.google.com"


def check_playwright():
    """检查 playwright 是否安装"""
    try:
        import playwright
        return True
    except ImportError:
        return False


def install_playwright():
    """安装 playwright"""
    print("📦 正在安装 playwright...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "-q"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium", "--with-deps"], check=True)
    print("✅ playwright 安装完成")


def upload_to_notebooklm(files: list, notebook_name: str = None, headless: bool = True):
    """
    使用 Playwright 将文件上传到 NotebookLM
    
    参数:
        files: 要上传的文件路径列表
        notebook_name: 目标笔记本名称（None 则创建新笔记本）
        headless: 是否无头模式（云端环境建议 False，需要用户在本地浏览器操作）
    """
    if not check_playwright():
        install_playwright()

    from playwright.sync_api import sync_playwright

    upload_results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )

        # 加载已保存的 cookies（如果有）
        cookie_path = Path.home() / ".sec-to-notebooklm" / "cookies.json"
        if cookie_path.exists():
            with open(cookie_path) as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            print(f"🍪 已加载保存的 Cookie")

        page = context.new_page()

        print(f"\n🌐 打开 NotebookLM...")
        page.goto(NOTEBOOKLM_URL, wait_until="networkidle", timeout=30000)

        # 检查是否需要登录
        if "accounts.google.com" in page.url or "signin" in page.url.lower():
            print("\n⚠️  需要登录 Google 账号")
            print("📌 请在浏览器中完成 Google 登录...")
            print("   登录后脚本将自动继续上传")
            
            # 等待登录完成（最多等 120 秒）
            try:
                page.wait_for_url(f"{NOTEBOOKLM_URL}/**", timeout=120000)
                print("✅ 登录成功")
                # 保存 cookies
                cookie_path.parent.mkdir(parents=True, exist_ok=True)
                cookies = context.cookies()
                with open(cookie_path, "w") as f:
                    json.dump(cookies, f)
                print(f"🍪 Cookie 已保存至 {cookie_path}，下次无需重新登录")
            except Exception as e:
                print(f"❌ 登录超时或失败: {e}")
                browser.close()
                return []

        print(f"✅ 已进入 NotebookLM")

        # 查找或创建笔记本
        try:
            if notebook_name:
                # 搜索已有笔记本
                print(f"\n🔍 查找笔记本: {notebook_name}")
                # 尝试点击匹配的笔记本
                notebook_found = False
                notebooks = page.query_selector_all('[data-notebook-title], .notebook-item, [aria-label*="notebook"]')
                for nb in notebooks:
                    title = nb.get_attribute("data-notebook-title") or nb.inner_text()
                    if notebook_name.lower() in title.lower():
                        nb.click()
                        notebook_found = True
                        print(f"✅ 已打开笔记本: {title}")
                        break

                if not notebook_found:
                    print(f"⚠️  未找到笔记本 '{notebook_name}'，将创建新笔记本")
                    notebook_name = None

            if not notebook_name:
                # 创建新笔记本
                print(f"\n➕ 创建新笔记本...")
                create_btns = page.query_selector_all(
                    'button[aria-label*="new"], button[aria-label*="create"], [data-action="create"]'
                )
                if create_btns:
                    create_btns[0].click()
                else:
                    # 尝试点击 "New notebook" 文字
                    page.get_by_text("New notebook").first.click()
                time.sleep(2)
                print("✅ 新笔记本已创建")

        except Exception as e:
            print(f"⚠️  笔记本操作出错: {e}")
            print("📌 请手动选择或创建笔记本，脚本将等待 30 秒后继续...")
            time.sleep(30)

        # 上传文件
        for file_path in files:
            file_path = Path(file_path)
            if not file_path.exists():
                print(f"⚠️  文件不存在，跳过: {file_path}")
                continue

            print(f"\n📤 上传: {file_path.name}")
            try:
                # 查找上传按钮
                upload_trigger = None
                selectors = [
                    'button[aria-label*="upload"]',
                    'button[aria-label*="Upload"]',
                    '[data-source-type="upload"]',
                    'input[type="file"]',
                    'button:has-text("Upload")',
                    'button:has-text("Add source")',
                    'button:has-text("Add")',
                ]
                for sel in selectors:
                    try:
                        el = page.query_selector(sel)
                        if el:
                            upload_trigger = el
                            break
                    except:
                        pass

                if upload_trigger:
                    if upload_trigger.get_attribute("type") == "file":
                        upload_trigger.set_input_files(str(file_path))
                    else:
                        upload_trigger.click()
                        time.sleep(1)
                        # 查找弹出的文件输入
                        file_input = page.query_selector('input[type="file"]')
                        if file_input:
                            file_input.set_input_files(str(file_path))

                    # 等待上传完成
                    time.sleep(3)
                    print(f"✅ 上传成功: {file_path.name}")
                    upload_results.append({"file": str(file_path), "status": "success"})
                else:
                    print(f"⚠️  未找到上传按钮，请手动上传: {file_path.name}")
                    upload_results.append({"file": str(file_path), "status": "manual_required"})

            except Exception as e:
                print(f"❌ 上传失败 {file_path.name}: {e}")
                upload_results.append({"file": str(file_path), "status": "failed", "error": str(e)})

        print(f"\n📊 上传结果: {len([r for r in upload_results if r['status'] == 'success'])}/{len(upload_results)} 成功")
        
        # 保存最终 URL
        final_url = page.url
        print(f"🔗 NotebookLM 地址: {final_url}")

        browser.close()

    return upload_results


def main():
    parser = argparse.ArgumentParser(
        description="将文件上传到 Google NotebookLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 上传单个文件到新笔记本
  python3 notebooklm_uploader.py report.pdf

  # 上传多个文件到指定笔记本
  python3 notebooklm_uploader.py report1.pdf report2.htm --notebook "AAPL Research"

  # 从清单文件读取文件列表
  python3 notebooklm_uploader.py --manifest ./sec_reports/AAPL/manifest.json

  # 有界面模式（用于首次登录）
  python3 notebooklm_uploader.py report.pdf --no-headless
        """
    )
    parser.add_argument("files", nargs="*", help="要上传的文件路径")
    parser.add_argument("--manifest", "-m", help="从 manifest.json 读取文件列表")
    parser.add_argument("--notebook", "-n", help="目标笔记本名称（不指定则创建新笔记本）")
    parser.add_argument("--no-headless", action="store_true", help="显示浏览器窗口（用于首次登录）")

    args = parser.parse_args()

    files = list(args.files)

    # 从清单文件读取
    if args.manifest:
        manifest_path = Path(args.manifest)
        if manifest_path.exists():
            with open(manifest_path) as f:
                manifest = json.load(f)
            files.extend(manifest.get("files", []))
            print(f"📋 从清单文件读取到 {len(manifest.get('files', []))} 个文件")
        else:
            print(f"❌ 清单文件不存在: {args.manifest}")
            sys.exit(1)

    if not files:
        print("❌ 没有指定要上传的文件")
        parser.print_help()
        sys.exit(1)

    # 过滤存在的文件
    valid_files = [f for f in files if Path(f).exists()]
    if not valid_files:
        print("❌ 没有找到有效的文件")
        sys.exit(1)

    print(f"\n📁 准备上传 {len(valid_files)} 个文件:")
    for f in valid_files:
        size = Path(f).stat().st_size / 1024
        print(f"  • {Path(f).name} ({size:.1f} KB)")

    results = upload_to_notebooklm(
        files=valid_files,
        notebook_name=args.notebook,
        headless=not args.no_headless,
    )

    # 保存上传结果
    result_path = Path("notebooklm_upload_result.json")
    with open(result_path, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n📝 结果已保存: {result_path}")


if __name__ == "__main__":
    main()
