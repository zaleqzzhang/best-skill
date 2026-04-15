#!/usr/bin/env python3
"""
动漫短视频生成脚本
基于腾讯云混元视频生成 API，根据用户提示词生成动漫风格的短视频。

使用方式：
    python3 generate_video.py --prompt "唐三成神" --token <TAIHU_TOKEN> [--output output.mp4] [--resolution 720p|1080p] [--fps 24]

依赖：requests（标准库外唯一依赖）
"""

import argparse
import json
import os
import sys
import time
import requests
from datetime import datetime

# ==================== 配置 ====================
# API 基础地址（优先使用环境变量，支持多种混元 API 端点）
# 混元 OpenAI 兼容接口: https://api.hunyuan.cloud.tencent.com/v1 （需要混元 API Key）
# lkeap 接口: https://api.lkeap.cloud.tencent.com/v1 （需要 lkeap API Key）
TAIHU_API_BASE = os.environ.get(
    "HUNYUAN_API_BASE",
    "https://api.hunyuan.cloud.tencent.com/v1"
)

# 视频生成相关配置
DEFAULT_RESOLUTION = "720p"
DEFAULT_FPS = 24
DEFAULT_DURATION = 5  # 混元视频单次生成时长（秒）
MAX_POLL_ATTEMPTS = 120  # 最大轮询次数
POLL_INTERVAL = 10  # 轮询间隔（秒）

# 分辨率映射
RESOLUTION_MAP = {
    "720p": {"width": 1280, "height": 720},
    "1080p": {"width": 1920, "height": 1080},
    "480p": {"width": 854, "height": 480},
}

# ==================== 提示词优化 ====================
ANIME_STYLE_ENHANCE = """你是一位专业的动漫视频提示词工程师。请将用户的简短描述扩展为适合AI视频生成的详细提示词。

要求：
1. 保留用户原始意图和角色信息
2. 添加动漫/国漫风格描述（如：精美的国漫画风、流畅的动画效果）
3. 添加场景细节（光影、色彩、氛围）
4. 添加动态描述（角色动作、镜头运动）
5. 添加画质描述（高清、精细线条、鲜艳色彩）
6. 输出为英文提示词（视频生成模型对英文效果更好）
7. 控制在 200 词以内

用户描述：{prompt}

请直接输出优化后的英文提示词，不要有其他内容："""


def optimize_prompt(user_prompt: str, token: str) -> str:
    """使用混元大模型优化用户提示词"""
    print(f"🎨 正在优化提示词...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "hunyuan-turbos-latest",
        "messages": [
            {
                "role": "user",
                "content": ANIME_STYLE_ENHANCE.format(prompt=user_prompt),
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500,
    }
    
    try:
        resp = requests.post(
            f"{TAIHU_API_BASE}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        result = resp.json()
        optimized = result["choices"][0]["message"]["content"].strip()
        print(f"✅ 提示词优化完成")
        print(f"   原始提示词: {user_prompt}")
        print(f"   优化后提示词: {optimized[:100]}...")
        return optimized
    except Exception as e:
        print(f"⚠️ 提示词优化失败，将使用原始提示词: {e}")
        # 回退：手动添加动漫风格关键词
        return f"anime style, high quality animation, {user_prompt}, vibrant colors, detailed art, smooth motion, cinematic lighting, 4K quality"


def submit_video_task(prompt: str, token: str, resolution: str = "720p") -> str:
    """提交视频生成任务，返回任务 ID"""
    print(f"🎬 正在提交视频生成任务...")
    
    res = RESOLUTION_MAP.get(resolution, RESOLUTION_MAP["720p"])
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "hunyuan-video",
        "prompt": prompt,
        "width": res["width"],
        "height": res["height"],
    }
    
    try:
        resp = requests.post(
            f"{TAIHU_API_BASE}/videos/generations",
            headers=headers,
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
        result = resp.json()
        
        task_id = result.get("id") or result.get("task_id") or result.get("request_id")
        if not task_id:
            # 某些 API 直接返回视频 URL
            video_url = None
            if "data" in result and len(result["data"]) > 0:
                video_url = result["data"][0].get("url")
            if video_url:
                return f"DIRECT_URL:{video_url}"
            print(f"📋 API 响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            raise ValueError("无法从响应中获取任务 ID")
        
        print(f"✅ 任务已提交，任务 ID: {task_id}")
        return task_id
    except requests.exceptions.HTTPError as e:
        print(f"❌ 提交任务失败 (HTTP {e.response.status_code})")
        print(f"   响应内容: {e.response.text}")
        raise
    except Exception as e:
        print(f"❌ 提交任务失败: {e}")
        raise


def poll_video_task(task_id: str, token: str) -> str:
    """轮询任务状态，返回视频下载 URL"""
    
    if task_id.startswith("DIRECT_URL:"):
        return task_id[len("DIRECT_URL:"):]
    
    print(f"⏳ 正在等待视频生成（预计需要 2-5 分钟）...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    for attempt in range(1, MAX_POLL_ATTEMPTS + 1):
        try:
            resp = requests.get(
                f"{TAIHU_API_BASE}/videos/generations/{task_id}",
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            result = resp.json()
            
            status = result.get("status", "").lower()
            
            if status in ("succeeded", "success", "completed", "complete"):
                video_url = None
                if "data" in result and len(result["data"]) > 0:
                    video_url = result["data"][0].get("url")
                elif "output" in result:
                    video_url = result["output"].get("video_url") or result["output"].get("url")
                elif "video_url" in result:
                    video_url = result["video_url"]
                
                if video_url:
                    print(f"\n✅ 视频生成完成！")
                    return video_url
                else:
                    print(f"⚠️ 任务完成但未找到视频 URL")
                    print(f"   响应: {json.dumps(result, ensure_ascii=False)}")
                    raise ValueError("视频 URL 未找到")
            
            elif status in ("failed", "error", "cancelled"):
                error_msg = result.get("error", {}).get("message", "未知错误")
                raise RuntimeError(f"视频生成失败: {error_msg}")
            
            else:
                # 仍在处理中
                progress = result.get("progress", "")
                progress_str = f" ({progress}%)" if progress else ""
                elapsed = attempt * POLL_INTERVAL
                print(f"   ⏳ [{elapsed}s] 生成中{progress_str}...", end="\r")
                time.sleep(POLL_INTERVAL)
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"   ⏳ 任务尚未就绪，继续等待...")
                time.sleep(POLL_INTERVAL)
            else:
                raise
    
    raise TimeoutError(f"视频生成超时（等待超过 {MAX_POLL_ATTEMPTS * POLL_INTERVAL} 秒）")


def download_video(url: str, output_path: str) -> str:
    """下载视频到本地"""
    print(f"📥 正在下载视频...")
    
    try:
        resp = requests.get(url, stream=True, timeout=300)
        resp.raise_for_status()
        
        total_size = int(resp.headers.get("content-length", 0))
        downloaded = 0
        
        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        pct = downloaded / total_size * 100
                        print(f"   📥 下载进度: {pct:.1f}%", end="\r")
        
        file_size = os.path.getsize(output_path)
        print(f"\n✅ 视频已保存: {output_path} ({file_size / 1024 / 1024:.1f} MB)")
        return output_path
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        raise


def generate_anime_video(
    prompt: str,
    token: str,
    output: str = None,
    resolution: str = "720p",
    optimize: bool = True,
) -> str:
    """
    完整的动漫短视频生成流程
    
    Args:
        prompt: 用户提示词（如 "唐三成神"）
        token: 太湖平台 API Token
        output: 输出文件路径（默认自动生成）
        resolution: 分辨率 (480p/720p/1080p)
        optimize: 是否优化提示词
    
    Returns:
        生成的视频文件路径
    """
    print("=" * 60)
    print(f"🎬 动漫短视频生成器")
    print(f"=" * 60)
    print(f"📝 输入提示词: {prompt}")
    print(f"📐 分辨率: {resolution}")
    print(f"🔧 提示词优化: {'开启' if optimize else '关闭'}")
    print(f"-" * 60)
    
    # 生成默认输出路径
    if not output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = prompt[:20].replace(" ", "_").replace("/", "_")
        output = os.path.join(os.getcwd(), f"anime_{safe_name}_{timestamp}.mp4")
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # 步骤 1: 优化提示词
    if optimize:
        final_prompt = optimize_prompt(prompt, token)
    else:
        final_prompt = f"anime style, high quality animation, {prompt}, vibrant colors, detailed art, smooth motion, cinematic lighting"
    
    # 步骤 2: 提交视频生成任务
    task_id = submit_video_task(final_prompt, token, resolution)
    
    # 步骤 3: 轮询等待生成完成
    video_url = poll_video_task(task_id, token)
    
    # 步骤 4: 下载视频
    result_path = download_video(video_url, output)
    
    print(f"\n{'=' * 60}")
    print(f"🎉 动漫短视频生成完成！")
    print(f"📁 文件路径: {result_path}")
    print(f"{'=' * 60}")
    
    return result_path


def main():
    parser = argparse.ArgumentParser(
        description="动漫短视频生成器 - 基于混元视频 AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s --prompt "唐三成神" --token YOUR_TOKEN
  %(prog)s --prompt "哪吒闹海" --token YOUR_TOKEN --resolution 1080p
  %(prog)s --prompt "孙悟空大闹天宫" --token YOUR_TOKEN --output monkey_king.mp4 --no-optimize
        """,
    )
    
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="视频描述提示词（如：唐三成神、哪吒闹海）",
    )
    parser.add_argument(
        "--token", "-t",
        required=True,
        help="太湖平台 API Token",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="输出视频文件路径（默认自动生成）",
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["480p", "720p", "1080p"],
        default="720p",
        help="视频分辨率（默认: 720p）",
    )
    parser.add_argument(
        "--no-optimize",
        action="store_true",
        help="跳过提示词优化步骤",
    )
    
    args = parser.parse_args()
    
    try:
        result = generate_anime_video(
            prompt=args.prompt,
            token=args.token,
            output=args.output,
            resolution=args.resolution,
            optimize=not args.no_optimize,
        )
        print(f"\n输出文件: {result}")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
