#!/usr/bin/env python3
"""
screenshot_html.py - 将 HTML 文件截图为长图 PNG

用法：
  python3 screenshot_html.py <html_file_path> [output_png_path] [--width 1200]

依赖：
  pip install pyppeteer
  或直接用 node + puppeteer（自动检测）
"""

import sys
import os
import subprocess
import argparse
import json
import tempfile

def take_screenshot_via_node(html_path, output_path, width=1200):
    """使用 node + puppeteer 截图"""
    abs_html = os.path.abspath(html_path)
    abs_out  = os.path.abspath(output_path)

    js = f"""
const puppeteer = require('puppeteer');
const path = require('path');
(async () => {{
  const browser = await puppeteer.launch({{ args: ['--no-sandbox', '--disable-setuid-sandbox'] }});
  const page = await browser.newPage();
  await page.goto('file://{abs_html}', {{ waitUntil: 'networkidle0' }});
  await page.setViewport({{ width: {width}, height: 800 }});
  const bodyHeight = await page.evaluate(() => document.body.scrollHeight);
  await page.setViewport({{ width: {width}, height: bodyHeight }});
  await page.screenshot({{ path: '{abs_out}', fullPage: true }});
  console.log(JSON.stringify({{ ok: true, height: bodyHeight, output: '{abs_out}' }}));
  await browser.close();
}})();
"""
    # 写临时 js 文件
    tmp = tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='w')
    tmp.write(js)
    tmp.close()

    try:
        result = subprocess.run(['node', tmp.name], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Node 执行失败：{result.stderr}", file=sys.stderr)
            sys.exit(1)
        info = json.loads(result.stdout.strip())
        print(f"✅ 截图完成！尺寸：{width}x{info['height']}px")
        print(f"📄 输出文件：{info['output']}")
    finally:
        os.unlink(tmp.name)


def main():
    parser = argparse.ArgumentParser(description='将 HTML 文件截图为长图 PNG')
    parser.add_argument('html_file', help='输入 HTML 文件路径')
    parser.add_argument('output', nargs='?', help='输出 PNG 路径（默认：同名 .png）')
    parser.add_argument('--width', type=int, default=1200, help='截图宽度（默认 1200px）')
    args = parser.parse_args()

    if not os.path.exists(args.html_file):
        print(f"❌ 文件不存在：{args.html_file}", file=sys.stderr)
        sys.exit(1)

    output = args.output or os.path.splitext(args.html_file)[0] + '_长图.png'
    take_screenshot_via_node(args.html_file, output, args.width)


if __name__ == '__main__':
    main()
