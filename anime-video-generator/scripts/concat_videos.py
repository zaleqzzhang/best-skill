#!/usr/bin/env python3
"""
多片段拼接脚本
将多个短视频片段拼接为一个完整的长视频（如 30 秒）。

使用方式：
    python3 concat_videos.py --inputs clip1.mp4 clip2.mp4 clip3.mp4 --output final.mp4

依赖：ffmpeg（系统工具）
"""

import argparse
import os
import subprocess
import sys
import tempfile


def check_ffmpeg():
    """检查 ffmpeg 是否可用"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_video_duration(filepath: str) -> float:
    """获取视频时长（秒）"""
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                filepath,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        import json
        info = json.loads(result.stdout)
        return float(info["format"]["duration"])
    except Exception:
        return 0.0


def concat_videos(input_files: list, output_path: str, target_duration: float = None) -> str:
    """
    拼接多个视频文件
    
    Args:
        input_files: 输入视频文件路径列表
        output_path: 输出文件路径
        target_duration: 目标时长（秒），超出部分会被裁剪
    
    Returns:
        输出文件路径
    """
    if not check_ffmpeg():
        print("❌ 未找到 ffmpeg，请先安装: apt-get install ffmpeg")
        sys.exit(1)
    
    # 验证输入文件
    for f in input_files:
        if not os.path.exists(f):
            print(f"❌ 文件不存在: {f}")
            sys.exit(1)
    
    print(f"🎬 正在拼接 {len(input_files)} 个视频片段...")
    
    # 创建 ffmpeg 拼接列表文件
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        list_file = f.name
        for video_file in input_files:
            abs_path = os.path.abspath(video_file)
            f.write(f"file '{abs_path}'\n")
    
    try:
        # 使用 ffmpeg concat 方式拼接
        cmd = [
            "ffmpeg",
            "-y",  # 覆盖输出
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy",  # 直接复制流，不重新编码
            output_path,
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            # 如果直接复制失败，尝试重新编码
            print("⚠️ 直接拼接失败，尝试重新编码...")
            cmd = [
                "ffmpeg",
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", list_file,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-preset", "fast",
                output_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode != 0:
                print(f"❌ 拼接失败: {result.stderr}")
                sys.exit(1)
        
        # 如果指定了目标时长，裁剪视频
        if target_duration:
            total_duration = get_video_duration(output_path)
            if total_duration > target_duration:
                print(f"✂️ 裁剪视频至 {target_duration} 秒...")
                trimmed_path = output_path + ".trimmed.mp4"
                trim_cmd = [
                    "ffmpeg",
                    "-y",
                    "-i", output_path,
                    "-t", str(target_duration),
                    "-c", "copy",
                    trimmed_path,
                ]
                subprocess.run(trim_cmd, capture_output=True, timeout=120)
                os.replace(trimmed_path, output_path)
        
        duration = get_video_duration(output_path)
        size = os.path.getsize(output_path) / 1024 / 1024
        print(f"✅ 拼接完成: {output_path}")
        print(f"   时长: {duration:.1f}s | 大小: {size:.1f} MB")
        return output_path
        
    finally:
        os.unlink(list_file)


def main():
    parser = argparse.ArgumentParser(description="视频片段拼接工具")
    parser.add_argument(
        "--inputs", "-i",
        nargs="+",
        required=True,
        help="输入视频文件列表",
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="输出视频文件路径",
    )
    parser.add_argument(
        "--duration", "-d",
        type=float,
        default=None,
        help="目标时长（秒），超出部分裁剪",
    )
    
    args = parser.parse_args()
    concat_videos(args.inputs, args.output, args.duration)


if __name__ == "__main__":
    main()
