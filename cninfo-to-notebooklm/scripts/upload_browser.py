#!/usr/bin/env python3
"""
Upload files to NotebookLM using browser automation
"""
import sys
import os
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Playwright not installed")
    sys.exit(1)

def upload_files(notebook_id, files):
    """Upload files using browser automation"""

    notebook_url = f"https://notebooklm.google.com/notebook/{notebook_id}"

    print(f"🌐 Opening browser...")
    print(f"📚 Notebook: {notebook_url}")
    print(f"📁 Files: {len(files)}\n")

    with sync_playwright() as p:
        # Launch browser with persistent context
        context = p.chromium.launch_persistent_context(
            user_data_dir=os.path.expanduser("~/.notebooklm/browser_profile"),
            headless=False,
            viewport={"width": 1400, "height": 900},
            accept_downloads=True
        )

        page = context.pages[0] if context.pages else context.new_page()

        # Navigate to notebook
        print(f"📍 Navigating to notebook...")
        try:
            page.goto(notebook_url, wait_until="domcontentloaded", timeout=30000)
        except:
            pass
        time.sleep(5)  # Wait for page to load

        # Check if login needed
        if "accounts.google.com" in page.url:
            print("\n⚠️  Please login to Google in the browser window...")
            print("⏳ Waiting for login (up to 5 minutes)...\n")
            try:
                page.wait_for_url("**/notebooklm.google.com/**", timeout=300000)
                print("✅ Login successful!\n")
            except:
                print("❌ Login timeout")
                context.close()
                return False

        # Upload each file
        success_count = 0
        for i, file_path in enumerate(files, 1):
            filename = os.path.basename(file_path)
            print(f"[{i}/{len(files)}] Uploading: {filename}")

            try:
                # Find hidden file input
                file_input = page.query_selector('input[type="file"]')

                if file_input:
                    # Upload file directly to hidden input
                    file_input.set_input_files(file_path)
                    print(f"  ✅ File uploaded, processing...")
                    success_count += 1
                    time.sleep(5)
                else:
                    print(f"  ❌ Could not find file input")

            except Exception as e:
                print(f"  ❌ Error: {e}")

            if i < len(files):
                print("  ⏳ Waiting 3 seconds...\n")
                time.sleep(3)

        print(f"\n✅ Upload process completed!")
        print(f"📊 Successfully uploaded: {success_count}/{len(files)} files")

        print("\n⏳ Browser will close in 5 seconds...")
        time.sleep(5)

        context.close()
        return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python upload_browser.py <notebook_id> <file1> [file2] ...")
        sys.exit(1)

    notebook_id = sys.argv[1]
    files = [os.path.abspath(f) for f in sys.argv[2:]]

    # Verify files exist
    for f in files:
        if not os.path.exists(f):
            print(f"❌ File not found: {f}")
            sys.exit(1)

    upload_files(notebook_id, files)

if __name__ == "__main__":
    main()
