"""
Tenchage-ppt v2.0 — QA 截图脚本
使用 PowerPoint COM 逐页导出 PNG，分辨率 1400x788

用法: python qa_screenshot.py <pptx路径> [输出目录]

依赖: pip install pywin32
"""
import os, sys, time


def qa_screenshot(pptx_path, out_dir=None):
    try:
        import win32com.client
    except ImportError:
        print('ERROR: 需要安装 pywin32: pip install pywin32')
        sys.exit(1)

    pptx_path = os.path.abspath(pptx_path)
    if not os.path.exists(pptx_path):
        print(f'ERROR: 文件不存在: {pptx_path}')
        sys.exit(1)

    if out_dir is None:
        base = os.path.splitext(os.path.basename(pptx_path))[0]
        out_dir = os.path.join(os.path.dirname(pptx_path), base + '_qa')

    os.makedirs(out_dir, exist_ok=True)

    print(f'正在打开: {pptx_path}')

    # 尝试复用已运行的 PowerPoint 实例，避免创建新进程
    try:
        ppt = win32com.client.GetActiveObject('PowerPoint.Application')
        ppt_was_running = True
        print('[INFO] 复用已运行的 PowerPoint 实例')
    except Exception:
        ppt = win32com.client.Dispatch('PowerPoint.Application')
        ppt_was_running = False
        print('[INFO] 启动新的 PowerPoint 实例')

    ppt.Visible = True
    prs = ppt.Presentations.Open(pptx_path, ReadOnly=True, WithWindow=False)
    time.sleep(1)

    n = prs.Slides.Count
    print(f'共 {n} 页，开始导出...')
    for i in range(1, n + 1):
        out = os.path.join(out_dir, f'slide_{i:02d}.png')
        prs.Slides(i).Export(out, 'PNG', 1400, 788)
        print(f'  slide {i:02d} -> {out}')

    prs.Close()

    # 关键修复：只在 PowerPoint 是我们自己启动的、且没有其他打开的文件时才 Quit
    # 如果用户正在编辑其他 PPT，绝对不能 Quit！
    if not ppt_was_running and ppt.Presentations.Count == 0:
        ppt.Quit()
        print('[INFO] PowerPoint 已安全退出（无其他打开的文件）')
    else:
        print('[INFO] PowerPoint 保持运行（用户可能有其他文件正在编辑）')
    print(f'\n[OK] QA截图完成! 共 {n} 页')
    print(f'输出目录: {out_dir}')
    print('')
    print('--- 逐页检查清单 ---')
    print('[ ] 标题折行：主标题是否超过1行')
    print('[ ] 元素重叠：文字框/形状是否相互遮挡')
    print('[ ] 文字溢出：文字是否超出边框被裁切')
    print('[ ] 对齐不齐：同类元素左边缘/顶部是否对齐')
    print('[ ] 空白区域：是否有不该空白的区域')
    print('[ ] 页脚碰撞：内容最后一行是否与页码重叠')
    print('[ ] 边距不足：元素是否超出0.5"边距')
    print('[ ] 装饰线完整：顶部蓝绿线+品牌文字是否存在')
    return out_dir


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python qa_screenshot.py <pptx路径> [输出目录]')
        sys.exit(1)
    pptx = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    qa_screenshot(pptx, out)
