#!/usr/bin/env python3
"""
智能视频抽帧器 - 从影视剧集中自动提取高能/精彩/唯美场景帧
使用多维度评分：色彩饱和度、亮度对比、场景变化、画面清晰度、美学评分
"""

import cv2
import numpy as np
import os
import json
import math
from PIL import Image

def compute_frame_scores(frame_bgr):
    """
    计算单帧的多维度美学评分
    返回: dict of scores (0~1)
    """
    h, w = frame_bgr.shape[:2]
    
    # 转换色彩空间
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    
    scores = {}
    
    # 1. 色彩饱和度评分 - 饱和度越高越鲜艳
    saturation = frame_hsv[:, :, 1].astype(float)
    scores['saturation'] = np.mean(saturation) / 255.0
    
    # 2. 色彩丰富度 - 色相分布的标准差
    hue = frame_hsv[:, :, 0].astype(float)
    # 排除低饱和度像素（灰色区域）
    mask = saturation > 30
    if np.sum(mask) > 100:
        hue_std = np.std(hue[mask])
        scores['color_richness'] = min(1.0, hue_std / 50.0)
    else:
        scores['color_richness'] = 0.0
    
    # 3. 亮度适中度 - 不过亮不过暗
    brightness = frame_hsv[:, :, 2].astype(float)
    mean_brightness = np.mean(brightness) / 255.0
    # 最佳亮度在0.4-0.7之间
    scores['brightness'] = 1.0 - abs(mean_brightness - 0.55) * 2.5
    scores['brightness'] = max(0, scores['brightness'])
    
    # 4. 对比度评分
    contrast = np.std(frame_gray.astype(float)) / 128.0
    scores['contrast'] = min(1.0, contrast)
    
    # 5. 画面清晰度 (Laplacian方差)
    laplacian_var = cv2.Laplacian(frame_gray, cv2.CV_64F).var()
    scores['sharpness'] = min(1.0, laplacian_var / 500.0)
    
    # 6. 边缘密度 - 人物/物体丰富度
    edges = cv2.Canny(frame_gray, 50, 150)
    scores['edge_density'] = np.mean(edges > 0)
    
    # 7. 三分法构图评分 - 检查关键区域是否有高对比内容
    h3, w3 = h // 3, w // 3
    # 检查九宫格交叉点附近的内容丰富度
    interest_regions = [
        frame_gray[h3-20:h3+20, w3-20:w3+20],
        frame_gray[h3-20:h3+20, 2*w3-20:2*w3+20],
        frame_gray[2*h3-20:2*h3+20, w3-20:w3+20],
        frame_gray[2*h3-20:2*h3+20, 2*w3-20:2*w3+20],
    ]
    region_scores = []
    for region in interest_regions:
        if region.size > 0:
            region_scores.append(np.std(region.astype(float)) / 128.0)
    scores['composition'] = np.mean(region_scores) if region_scores else 0.0
    
    # 8. 蓝色/冷色调占比（仙侠风格偏好）
    blue_channel = frame_rgb[:, :, 2].astype(float)
    red_channel = frame_rgb[:, :, 0].astype(float)
    cool_ratio = np.mean(blue_channel > red_channel + 20)
    scores['cool_tone'] = cool_ratio
    
    # 9. 暗角/电影感（中心比边缘亮）
    center_region = frame_gray[h//4:3*h//4, w//4:3*w//4]
    border_region = np.concatenate([
        frame_gray[:h//4, :].flatten(),
        frame_gray[3*h//4:, :].flatten(),
        frame_gray[:, :w//4].flatten(),
        frame_gray[:, 3*w//4:].flatten(),
    ])
    if len(border_region) > 0:
        center_mean = np.mean(center_region.astype(float))
        border_mean = np.mean(border_region.astype(float))
        scores['cinematic'] = min(1.0, max(0, (center_mean - border_mean) / 80.0))
    else:
        scores['cinematic'] = 0.0
    
    # 综合美学评分（加权）
    weights = {
        'saturation': 0.15,
        'color_richness': 0.10,
        'brightness': 0.12,
        'contrast': 0.12,
        'sharpness': 0.15,
        'edge_density': 0.10,
        'composition': 0.08,
        'cool_tone': 0.08,
        'cinematic': 0.10,
    }
    
    total = sum(scores[k] * weights[k] for k in weights)
    scores['total'] = total
    
    return scores


def detect_scene_changes(video_path, threshold=30.0):
    """
    检测场景变化点
    返回: list of (frame_idx, change_magnitude)
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []
    
    prev_gray = None
    changes = []
    frame_idx = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (160, 90))  # 降分辨率加速
        
        if prev_gray is not None:
            diff = cv2.absdiff(gray, prev_gray)
            mean_diff = np.mean(diff)
            if mean_diff > threshold:
                changes.append((frame_idx, mean_diff))
        
        prev_gray = gray
        frame_idx += 1
    
    cap.release()
    return changes


def extract_best_frames(video_path, output_dir, max_frames=20, min_interval_sec=2.0):
    """
    从视频中智能提取最佳帧
    
    流程:
    1. 检测场景变化点
    2. 在每个场景中采样帧并评分
    3. 选择评分最高的帧
    4. 确保帧之间有最小间隔
    
    Args:
        video_path: 视频文件路径
        output_dir: 输出目录
        max_frames: 最多提取帧数
        min_interval_sec: 帧之间的最小间隔（秒）
    
    Returns:
        list of (frame_path, score, timestamp)
    """
    os.makedirs(output_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"  ❌ 无法打开视频: {video_path}")
        return []
    
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"  📹 视频信息: {width}x{height} @ {fps:.1f}fps, {duration:.1f}s, {total_frames}帧")
    
    min_interval_frames = int(min_interval_sec * fps)
    
    # 步骤1: 每隔一定帧数采样并评分
    sample_interval = max(1, int(fps * 0.5))  # 每0.5秒采样一帧
    
    all_scored_frames = []
    frame_idx = 0
    sampled = 0
    
    print(f"  🔍 采样评分中（每{sample_interval}帧采样一次）...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_idx % sample_interval == 0:
            scores = compute_frame_scores(frame)
            all_scored_frames.append({
                'frame_idx': frame_idx,
                'timestamp': frame_idx / fps,
                'scores': scores,
                'total': scores['total'],
            })
            sampled += 1
            
            if sampled % 50 == 0:
                print(f"    已采样 {sampled} 帧 (进度 {frame_idx/total_frames*100:.0f}%)")
        
        frame_idx += 1
    
    cap.release()
    print(f"  ✅ 共采样 {len(all_scored_frames)} 帧")
    
    if not all_scored_frames:
        return []
    
    # 步骤2: 按评分排序，选择最佳帧（保证最小间隔）
    all_scored_frames.sort(key=lambda x: x['total'], reverse=True)
    
    selected = []
    selected_indices = set()
    
    for item in all_scored_frames:
        if len(selected) >= max_frames:
            break
        
        # 检查是否与已选帧太近
        too_close = False
        for sel in selected:
            if abs(item['frame_idx'] - sel['frame_idx']) < min_interval_frames:
                too_close = True
                break
        
        if not too_close:
            selected.append(item)
            selected_indices.add(item['frame_idx'])
    
    # 按时间顺序排列
    selected.sort(key=lambda x: x['frame_idx'])
    
    print(f"  🎯 选出 {len(selected)} 个最佳帧:")
    for i, item in enumerate(selected):
        ts = item['timestamp']
        score = item['total']
        print(f"    #{i+1} t={ts:.1f}s score={score:.3f} "
              f"(sat={item['scores']['saturation']:.2f} "
              f"sharp={item['scores']['sharpness']:.2f} "
              f"contrast={item['scores']['contrast']:.2f})")
    
    # 步骤3: 提取并保存这些帧
    print(f"\n  💾 提取并保存帧...")
    cap = cv2.VideoCapture(video_path)
    results = []
    
    for i, item in enumerate(selected):
        cap.set(cv2.CAP_PROP_POS_FRAMES, item['frame_idx'])
        ret, frame = cap.read()
        if ret:
            filename = f"frame_{i+1:03d}_t{item['timestamp']:.1f}s_s{item['total']:.3f}.jpg"
            filepath = os.path.join(output_dir, filename)
            
            # 保存高质量JPEG
            cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            
            size_kb = os.path.getsize(filepath) // 1024
            results.append({
                'path': filepath,
                'score': item['total'],
                'timestamp': item['timestamp'],
                'scores': item['scores'],
                'size_kb': size_kb,
            })
            print(f"    ✅ {filename} ({size_kb}KB)")
    
    cap.release()
    return results


def extract_from_multiple_videos(video_paths, output_dir, frames_per_video=8, min_interval=2.0):
    """
    从多个视频中提取最佳帧
    """
    os.makedirs(output_dir, exist_ok=True)
    all_results = []
    
    for i, vpath in enumerate(video_paths):
        print(f"\n{'='*50}")
        print(f"📹 处理视频 {i+1}/{len(video_paths)}: {os.path.basename(vpath)}")
        print(f"{'='*50}")
        
        vid_output = os.path.join(output_dir, f"video_{i+1}")
        results = extract_best_frames(
            vpath, vid_output,
            max_frames=frames_per_video,
            min_interval_sec=min_interval
        )
        all_results.extend(results)
    
    # 全局排序，选出最佳的
    all_results.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\n{'='*50}")
    print(f"📊 全部视频抽帧结果: 共 {len(all_results)} 帧")
    print(f"{'='*50}")
    
    # 保存元数据
    meta_path = os.path.join(output_dir, "extraction_meta.json")
    meta = {
        'total_frames': len(all_results),
        'frames': [
            {
                'path': r['path'],
                'score': r['score'],
                'timestamp': r['timestamp'],
                'size_kb': r['size_kb'],
            }
            for r in all_results
        ]
    }
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    return all_results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="智能视频抽帧器")
    parser.add_argument("--videos", "-v", nargs="+", required=True, help="视频文件路径")
    parser.add_argument("--output", "-o", default="extracted_frames", help="输出目录")
    parser.add_argument("--frames", "-n", type=int, default=10, help="每个视频提取帧数")
    parser.add_argument("--interval", "-i", type=float, default=2.0, help="最小帧间隔(秒)")
    args = parser.parse_args()
    
    extract_from_multiple_videos(
        args.videos, args.output,
        frames_per_video=args.frames,
        min_interval=args.interval
    )
