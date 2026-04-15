#!/usr/bin/env python3
"""
动漫短视频生成器 v8 - 真实音乐节拍卡点版
核心升级：
- 使用真实下载的热门BGM（非合成电子音）
- librosa 精准节拍检测
- 转场精确卡在音乐节拍上
- 支持多首BGM自动评分选择最佳
"""

import math
import os
import random
import time
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

WIDTH, HEIGHT = 1280, 720
FPS = 30

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "anime-video-generator")
FONT_PATH = os.path.join(FONT_CACHE_DIR, "NotoSansSC.ttf")

# ==================== 工具函数 ====================

def _ensure_font():
    """确保中文字体可用，不存在时自动下载"""
    if os.path.exists(FONT_PATH) and os.path.getsize(FONT_PATH) > 1000000:
        return FONT_PATH
    # 先检查系统字体
    sys_fonts = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    ]
    for f in sys_fonts:
        if os.path.exists(f):
            return f
    # 自动下载
    os.makedirs(FONT_CACHE_DIR, exist_ok=True)
    print("📥 首次运行，正在下载中文字体...")
    import subprocess
    url = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansSC-Regular.otf"
    subprocess.run(["curl", "-sL", "-o", FONT_PATH, url], timeout=120)
    if os.path.exists(FONT_PATH) and os.path.getsize(FONT_PATH) > 100000:
        print("✅ 字体下载完成")
        return FONT_PATH
    return None

def get_font(size):
    font_path = _ensure_font()
    if font_path:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            pass
    return ImageFont.load_default()

def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))

def ease_in_out(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def ease_out_cubic(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3

def ease_in_cubic(t):
    t = max(0.0, min(1.0, t))
    return t * t * t

def lerp(a, b, t):
    return a + (b - a) * t

# ==================== 预缓存 ====================

_vignette_cache = None
_bars_cache = None

def get_vignette_mask(strength=0.22):
    global _vignette_cache
    if _vignette_cache is not None:
        return _vignette_cache
    vignette = Image.new("L", (WIDTH, HEIGHT), 0)
    draw_v = ImageDraw.Draw(vignette)
    cx, cy = WIDTH / 2, HEIGHT / 2
    for i in range(50, -1, -1):
        t = i / 50
        rx = int(cx * (0.55 + t * 0.85))
        ry = int(cy * (0.55 + t * 0.85))
        brightness = int(255 * (1.0 - (1.0 - t) ** 1.6 * strength))
        draw_v.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=brightness)
    _vignette_cache = vignette
    return vignette

def apply_vignette(frame):
    mask = get_vignette_mask()
    r, g, b = frame.split()
    black = Image.new("L", (WIDTH, HEIGHT), 0)
    r = Image.composite(r, black, mask)
    g = Image.composite(g, black, mask)
    b = Image.composite(b, black, mask)
    return Image.merge("RGB", (r, g, b))

def get_cinematic_bars():
    global _bars_cache
    if _bars_cache is not None:
        return _bars_cache
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    bar_h = 28
    for y in range(bar_h):
        a = int(0.65 * (1.0 - y / bar_h) * 255)
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, a))
    for y in range(HEIGHT - bar_h, HEIGHT):
        progress = (y - (HEIGHT - bar_h)) / bar_h
        a = int(0.65 * progress * 255)
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, a))
    _bars_cache = overlay
    return overlay

# ==================== 图片处理 ====================

def load_and_prepare_image(path, scale=1.35):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    margin_x = int(w * 0.04)
    margin_y = int(h * 0.04)
    img = img.crop((margin_x, margin_y, w - margin_x, h - margin_y))
    w, h = img.size
    target_ratio = WIDTH / HEIGHT
    img_ratio = w / h

    if img_ratio > target_ratio:
        new_h = h
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    elif img_ratio < target_ratio * 0.65:
        new_w = w
        new_h = int(w / target_ratio)
        top = int(h * 0.08)
        bottom = min(h, top + new_h)
        if bottom - top < new_h:
            top = max(0, h - new_h)
        img = img.crop((0, top, w, min(h, top + new_h)))
    else:
        new_w = w
        new_h = int(w / target_ratio)
        top = max(0, int((h - new_h) * 0.3))
        img = img.crop((0, top, w, min(h, top + new_h)))

    final_w = int(WIDTH * scale)
    final_h = int(HEIGHT * scale)
    img = img.resize((final_w, final_h), Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=25, threshold=2))
    return img

# ==================== Ken Burns ====================

def ken_burns_crop(img, t, effect_type="zoom_in", focus=(0.5, 0.4)):
    iw, ih = img.size
    ts = ease_in_out(t)
    fx, fy = focus

    effects = {
        "zoom_in":      lambda: (1.0 - ts * 0.20, lerp(iw*0.5, iw*fx, ts*0.35), lerp(ih*0.5, ih*fy, ts*0.35)),
        "zoom_out":     lambda: (0.80 + ts * 0.20, lerp(iw*fx, iw*0.5, ts*0.35), lerp(ih*fy, ih*0.5, ts*0.35)),
        "pan_left":     lambda: (0.85, iw * (0.55 - ts * 0.10), ih * fy),
        "pan_right":    lambda: (0.85, iw * (0.45 + ts * 0.10), ih * fy),
        "slow_zoom_in": lambda: (1.0 - ts * 0.10, iw * fx, ih * fy),
        "drift_up":     lambda: (0.87, iw * 0.5, ih * (0.52 - ts * 0.06)),
        "drift_down":   lambda: (0.87, iw * 0.5, ih * (0.48 + ts * 0.06)),
    }

    scale, cx, cy = effects.get(effect_type, effects["zoom_in"])()
    crop_w = int(WIDTH / scale)
    crop_h = int(HEIGHT / scale)
    left = max(0, min(iw - crop_w, int(cx - crop_w / 2)))
    top = max(0, min(ih - crop_h, int(cy - crop_h / 2)))
    return img.crop((left, top, left + crop_w, top + crop_h)).resize((WIDTH, HEIGHT), Image.LANCZOS)

# ==================== 转场 ====================

def transition_fade(f1, f2, t):
    return Image.blend(f1, f2, ease_in_out(t))

def transition_dissolve_glow(f1, f2, t):
    ts = ease_in_out(t)
    blend = Image.blend(f1, f2, ts)
    if 0.3 < t < 0.7:
        glow = math.sin((t - 0.3) / 0.4 * math.pi) * 0.10
        white = Image.new("RGB", (WIDTH, HEIGHT), (235, 240, 255))
        blend = Image.blend(blend, white, glow)
    return blend

def transition_slide_left(f1, f2, t):
    ts = ease_out_cubic(t)
    offset = int(WIDTH * ts)
    r = Image.new("RGB", (WIDTH, HEIGHT))
    r.paste(f1, (-offset, 0))
    r.paste(f2, (WIDTH - offset, 0))
    return r

def transition_zoom_blur(f1, f2, t):
    ts = ease_in_out(t)
    if ts < 0.5:
        blur_r = max(1, int(ts * 10))
        return Image.blend(f1.filter(ImageFilter.GaussianBlur(blur_r)), f2, ts * 2)
    else:
        blur_r = max(1, int((1 - ts) * 10))
        return Image.blend(f1, f2.filter(ImageFilter.GaussianBlur(blur_r)), (ts - 0.5) * 2)

def transition_push_up(f1, f2, t):
    ts = ease_out_cubic(t)
    offset = int(HEIGHT * ts)
    r = Image.new("RGB", (WIDTH, HEIGHT))
    r.paste(f1, (0, -offset))
    r.paste(f2, (0, HEIGHT - offset))
    return r

def transition_flash_white(f1, f2, t):
    ts = ease_in_out(t)
    white = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
    if ts < 0.4:
        alpha = ts / 0.4
        return Image.blend(f1, white, alpha * 0.7)
    elif ts < 0.6:
        return Image.blend(white, f2, (ts - 0.4) / 0.2 * 0.5 + 0.5)
    else:
        alpha = (ts - 0.6) / 0.4
        return Image.blend(Image.blend(white, f2, 0.5), f2, alpha)

TRANSITIONS = {
    "fade": transition_fade,
    "dissolve": transition_dissolve_glow,
    "slide_left": transition_slide_left,
    "zoom_blur": transition_zoom_blur,
    "push_up": transition_push_up,
    "flash": transition_flash_white,
}

STRONG_TRANSITIONS = ["flash", "zoom_blur", "slide_left"]
NORMAL_TRANSITIONS = ["fade", "dissolve", "push_up"]

# ==================== 音频分析 ====================

def analyze_bgm(wav_path):
    """用 librosa 分析BGM，返回节拍时间点和BPM"""
    import librosa
    
    print(f"  🎵 分析音频: {wav_path}")
    y, sr = librosa.load(wav_path, sr=44100, mono=True)
    duration = len(y) / sr
    
    # 节拍检测
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    
    if hasattr(tempo, '__len__'):
        tempo = float(tempo[0]) if len(tempo) > 0 else 120
    else:
        tempo = float(tempo)
    
    # onset 检测（更精确的音乐变化点）
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, wait=10, delta=0.1)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    
    # 能量曲线（用于节拍闪动强度）
    rms = librosa.feature.rms(y=y)[0]
    rms_times = librosa.frames_to_time(np.arange(len(rms)), sr=sr)
    
    print(f"  📊 BPM: {tempo:.0f}, 节拍数: {len(beat_times)}, Onset数: {len(onset_times)}")
    print(f"  📊 时长: {duration:.1f}s")
    
    return {
        'audio': y,
        'sr': sr,
        'duration': duration,
        'tempo': tempo,
        'beat_times': beat_times,
        'onset_times': onset_times,
        'rms': rms,
        'rms_times': rms_times,
    }

def select_transition_beats(beat_times, num_transitions, video_duration, min_gap=2.5):
    """
    从节拍时间点中选择最佳的转场点
    确保：
    1. 跳过前2秒和后3秒
    2. 转场点之间至少间隔 min_gap 秒
    3. 尽量均匀分布
    """
    valid = [bt for bt in beat_times if 2.0 < bt < video_duration - 3.0]
    
    if len(valid) < num_transitions:
        # 节拍不够，均匀分配
        step = (video_duration - 5.0) / (num_transitions + 1)
        return [2.0 + step * (i + 1) for i in range(num_transitions)]
    
    # 理想的均匀间隔
    ideal_gap = (video_duration - 5.0) / (num_transitions + 1)
    
    selected = []
    last_t = 0
    
    for i in range(num_transitions):
        target = 2.0 + ideal_gap * (i + 1)
        # 找最接近 target 的节拍
        best = None
        best_dist = float('inf')
        for bt in valid:
            if bt - last_t < min_gap:
                continue
            dist = abs(bt - target)
            if dist < best_dist:
                best_dist = dist
                best = bt
        
        if best is not None:
            selected.append(best)
            last_t = best
        else:
            # 没找到合适的节拍，用目标时间
            selected.append(target)
            last_t = target
    
    return selected

# ==================== 合并特效层 ====================

def draw_all_effects(overlay_draw, frame_idx, total_frames, t_norm):
    rng = random.Random(42)
    for i in range(25):
        base_x = rng.randint(-30, WIDTH + 30)
        base_y = rng.randint(-30, HEIGHT + 30)
        speed_x = rng.uniform(-0.20, 0.20)
        speed_y = rng.uniform(-0.8, -0.12)
        size = rng.uniform(1.5, 4.0)
        phase = rng.uniform(0, math.pi * 2)
        lifetime = rng.randint(100, 240)
        brightness = rng.uniform(0.35, 0.95)
        t_p = (frame_idx + i * 13) % lifetime
        progress = t_p / lifetime
        alpha = math.sin(progress * math.pi) * brightness
        x = base_x + speed_x * t_p + math.sin(frame_idx * 0.022 + phase) * 22
        y = (base_y + speed_y * t_p) % (HEIGHT + 80) - 40
        if alpha > 0.1 and -5 < x < WIDTH + 5 and -5 < y < HEIGHT + 5:
            s = max(1.0, size * alpha)
            a = int(alpha * 180)
            if s > 1.5:
                ha = max(1, int(a * 0.10))
                hs = s * 2.8
                overlay_draw.ellipse([x-hs, y-hs, x+hs, y+hs], fill=(170, 215, 255, ha))
            overlay_draw.ellipse([x-s, y-s, x+s, y+s], fill=(210, 240, 255, min(255, int(a*0.75))))

    rng2 = random.Random(123)
    for i in range(6):
        sx = rng2.randint(-80, WIDTH+80)
        sy = rng2.randint(-300, -30)
        fs = rng2.uniform(0.5, 1.3)
        sa = rng2.uniform(28, 55)
        sf = rng2.uniform(0.013, 0.035)
        rs = rng2.uniform(0.018, 0.05)
        sz = rng2.uniform(3.5, 7.5)
        tv = frame_idx + i * 41
        y = (sy + fs * tv) % (HEIGHT + 400) - 120
        x = sx + math.sin(tv * sf + i * 0.7) * sa
        if -10 < x < WIDTH+10 and -10 < y < HEIGHT+10:
            rot = tv * rs
            lp = ((sy + fs * tv) % (HEIGHT + 400)) / (HEIGHT + 400)
            pa = math.sin(lp * math.pi) * 0.50
            if pa > 0.06:
                wr = sz * (0.5 + 0.5 * abs(math.cos(rot)))
                hr = sz * 0.4
                a = int(pa * 220)
                pr = min(255, 248 + int(rng2.uniform(-8, 8)))
                pg = min(255, 200 + int(rng2.uniform(-12, 12)))
                pb = min(255, 215 + int(rng2.uniform(-8, 8)))
                overlay_draw.ellipse([x-wr, y-hr, x+wr, y+hr], fill=(pr, pg, pb, a))

    if 0.15 < t_norm < 0.35 or 0.55 < t_norm < 0.80:
        tf = frame_idx / total_frames
        cx = WIDTH*0.72 + math.sin(tf*1.8*math.pi)*75
        cy = HEIGHT*0.20 + math.cos(tf*1.2*math.pi)*35
        pulse = 0.55 + 0.45 * math.sin(frame_idx * 0.055)
        for rm, ab in [(7.0, 6), (4.5, 10), (2.5, 16), (1.2, 28)]:
            r = 12 * rm * pulse
            a = int(ab * pulse)
            overlay_draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(210, 225, 255, a))

# ==================== 字幕 ====================

def draw_subtitle(overlay_draw, frame_idx, clip_start, text, clip_frames):
    local = frame_idx - clip_start
    fi_end = int(FPS * 0.7)
    fo_start = clip_frames - int(FPS * 0.7)
    if local < fi_end:
        alpha = ease_out_cubic(local / fi_end)
    elif local > fo_start:
        alpha = ease_out_cubic((clip_frames - local) / (FPS * 0.7))
    else:
        alpha = 1.0
    if alpha < 0.03:
        return

    font = get_font(28)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    tx = (WIDTH - tw) // 2
    ty = HEIGHT - 52

    for y in range(HEIGHT - 90, HEIGHT):
        p = (y - (HEIGHT - 90)) / 90
        a = int(alpha * p * p * 140)
        overlay_draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, a))

    ta = int(alpha * 255)
    sa = int(alpha * 180)
    for dx, dy in [(-1,-1),(-1,1),(1,-1),(1,1),(-2,0),(2,0),(0,-2),(0,2)]:
        overlay_draw.text((tx+dx, ty+dy), text, font=font, fill=(0, 0, 0, sa))
    overlay_draw.text((tx, ty), text, font=font, fill=(255, 255, 255, ta))

# ==================== 色调 ====================

def apply_color_grade(frame, style="cold_fairy"):
    if style == "cold_fairy":
        frame = ImageEnhance.Color(frame).enhance(1.04)
        frame = ImageEnhance.Contrast(frame).enhance(1.05)
        r, g, b = frame.split()
        r = r.point(lambda x: clamp(x * 0.97))
        b = b.point(lambda x: clamp(x * 1.05))
        frame = Image.merge("RGB", (r, g, b))
    elif style == "moonlight":
        frame = ImageEnhance.Brightness(frame).enhance(0.95)
        frame = ImageEnhance.Contrast(frame).enhance(1.07)
        r, g, b = frame.split()
        r = r.point(lambda x: clamp(x * 0.92))
        g = g.point(lambda x: clamp(x * 0.97))
        b = b.point(lambda x: clamp(x * 1.10))
        frame = Image.merge("RGB", (r, g, b))
    return frame

# ==================== 节拍闪动 ====================

def apply_beat_flash(frame, t_sec, beat_times):
    """在节拍处添加微妙的亮度脉冲"""
    min_dist = float('inf')
    for bt in beat_times:
        dist = abs(t_sec - bt)
        if dist < min_dist:
            min_dist = dist
        if dist > 1.0:
            continue
    
    if min_dist < 0.12:
        intensity = (1.0 - min_dist / 0.12) * 0.08
        enhancer = ImageEnhance.Brightness(frame)
        frame = enhancer.enhance(1.0 + intensity)
    
    return frame

# ==================== 主函数 ====================

def create_beat_synced_video(
    image_paths,
    output_path,
    bgm_wav_path,
    clip_descs=None,
    duration=30,
):
    """
    真实音乐节拍卡点版视频生成
    """
    from moviepy import VideoClip, AudioClip
    
    total_frames = duration * FPS
    
    print(f"{'=' * 60}")
    print(f"🎬 动漫短视频生成器 v8 - 真实音乐节拍卡点版")
    print(f"{'=' * 60}")
    
    # 分析BGM
    print(f"\n🎵 分析背景音乐...")
    bgm_info = analyze_bgm(bgm_wav_path)
    
    bgm_audio = bgm_info['audio']
    sr = bgm_info['sr']
    beat_times = bgm_info['beat_times']
    tempo = bgm_info['tempo']
    
    # 截取视频时长
    audio_samples = int(duration * sr)
    if len(bgm_audio) > audio_samples:
        bgm_audio = bgm_audio[:audio_samples]
    else:
        # 循环填充
        repeats = math.ceil(audio_samples / len(bgm_audio))
        bgm_audio = np.tile(bgm_audio, repeats)[:audio_samples]
    
    # 淡入淡出处理
    fade_in_samples = int(1.5 * sr)
    fade_out_samples = int(2.5 * sr)
    fade_in = np.linspace(0, 1, fade_in_samples)
    fade_out = np.linspace(1, 0, fade_out_samples)
    bgm_audio[:fade_in_samples] *= fade_in
    bgm_audio[-fade_out_samples:] *= fade_out
    
    # 加载图片
    print(f"\n📷 加载图片...")
    images = []
    for p in image_paths:
        try:
            img = load_and_prepare_image(p)
            images.append(img)
            print(f"   ✅ {os.path.basename(p)} -> {img.size}")
        except Exception as e:
            print(f"   ⚠️ {os.path.basename(p)}: {e}")
    
    if not images:
        raise ValueError("没有可用图片！")
    
    num_clips = len(images)
    
    # 选择转场节拍点
    trans_duration = 0.7
    transition_points = select_transition_beats(
        beat_times, num_clips - 1, duration, min_gap=2.5
    )
    
    # 构建片段
    clips = []
    rng = random.Random(99)
    trans_types = []
    for i in range(num_clips):
        start = transition_points[i - 1] if i > 0 else 0.0
        end = transition_points[i] if i < num_clips - 1 else float(duration)
        
        if i == 0:
            trans = "fade"
        elif i == num_clips // 2:
            trans = "flash"
        elif i % 3 == 0:
            trans = rng.choice(STRONG_TRANSITIONS)
        else:
            trans = rng.choice(NORMAL_TRANSITIONS)
        
        clips.append((start, end, trans))
    
    print(f"\n📊 节拍信息:")
    print(f"   BPM: {tempo:.0f}")
    print(f"   检测到节拍数: {len(beat_times)}")
    
    print(f"\n🎯 节拍卡点片段分配:")
    for i, (start, end, trans) in enumerate(clips):
        dur = end - start
        print(f"   图{i+1}: {start:.2f}s ~ {end:.2f}s ({dur:.2f}s) 转场={trans}")
    
    # 预缓存
    get_vignette_mask()
    bars = get_cinematic_bars()
    
    kb_effects = ["slow_zoom_in", "zoom_out", "pan_left", "zoom_in", "pan_right", "drift_up", "slow_zoom_in"]
    color_styles = ["moonlight", "cold_fairy", "moonlight", "cold_fairy", "moonlight", "cold_fairy"]
    
    if not clip_descs or len(clip_descs) < num_clips:
        clip_descs = [
            "月下青云之巅  白衣胜雪",
            "天琊剑出鞘  寒光照九州",
            "剑舞翩翩  如仙子临凡",
            "灵力纵横  剑气划破苍穹",
            "独立山巅  一剑定乾坤",
            "仙路漫漫  不负此生风华",
            "冰心玉骨  超凡入圣",
        ]
        while len(clip_descs) < num_clips:
            clip_descs.append(clip_descs[-1])
    
    start_time = time.time()
    frame_count = [0]
    
    def make_frame(t_sec):
        frame_idx = int(t_sec * FPS)
        frame_count[0] += 1
        
        if frame_count[0] % (FPS * 5) == 0:
            elapsed = time.time() - start_time
            progress = frame_count[0] / total_frames * 100
            eta = elapsed / max(frame_count[0], 1) * (total_frames - frame_count[0])
            print(f"   🎬 {progress:.0f}% ({frame_count[0]}/{total_frames}) ETA:{eta:.0f}s")
        
        # 找当前片段
        clip_idx = 0
        for i, (start, end, _) in enumerate(clips):
            if start <= t_sec < end:
                clip_idx = i
                break
        else:
            clip_idx = num_clips - 1
        
        clip_start, clip_end, trans_type = clips[clip_idx]
        clip_dur = clip_end - clip_start
        clip_t = (t_sec - clip_start) / max(clip_dur, 0.01)
        clip_t = max(0.0, min(1.0, clip_t))
        clip_start_frame = int(clip_start * FPS)
        clip_dur_frames = int(clip_dur * FPS)
        
        # Ken Burns
        effect = kb_effects[clip_idx % len(kb_effects)]
        current_frame = ken_burns_crop(images[clip_idx], clip_t, effect)
        
        # 转场
        time_to_end = clip_end - t_sec
        if time_to_end < trans_duration and clip_idx < num_clips - 1:
            trans_t = 1.0 - time_to_end / trans_duration
            next_idx = clip_idx + 1
            next_effect = kb_effects[next_idx % len(kb_effects)]
            next_frame = ken_burns_crop(images[next_idx], 0, next_effect)
            next_trans = clips[next_idx][2] if next_idx < len(clips) else "fade"
            func = TRANSITIONS.get(next_trans, transition_fade)
            current_frame = func(current_frame, next_frame, trans_t)
        
        # 色调
        cs = color_styles[clip_idx % len(color_styles)]
        current_frame = apply_color_grade(current_frame, cs)
        
        # 暗角
        current_frame = apply_vignette(current_frame)
        
        # 节拍闪动
        current_frame = apply_beat_flash(current_frame, t_sec, beat_times)
        
        # 特效层
        t_norm = frame_idx / total_frames
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        
        draw_all_effects(od, frame_idx, total_frames, t_norm)
        draw_subtitle(od, frame_idx, clip_start_frame, clip_descs[clip_idx], clip_dur_frames)
        
        frame_rgba = current_frame.convert("RGBA")
        frame_rgba = Image.alpha_composite(frame_rgba, overlay)
        frame_rgba = Image.alpha_composite(frame_rgba, bars)
        current_frame = frame_rgba.convert("RGB")
        
        # 全局淡入
        fi_frames = int(FPS * 2.0)
        if frame_idx < fi_frames:
            a = ease_out_cubic(frame_idx / fi_frames)
            black = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
            current_frame = Image.blend(black, current_frame, a)
        
        # 全局淡出
        fo_frames = int(FPS * 2.5)
        if frame_idx > total_frames - fo_frames:
            a = ease_in_cubic((total_frames - frame_idx) / fo_frames)
            black = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
            current_frame = Image.blend(black, current_frame, max(0.0, min(1.0, a)))
        
        return np.array(current_frame)
    
    print(f"\n🎬 开始渲染...")
    clip = VideoClip(make_frame, duration=duration)
    
    def make_audio(t_sec):
        if isinstance(t_sec, np.ndarray):
            indices = (t_sec * sr).astype(int)
            indices = np.clip(indices, 0, len(bgm_audio) - 1)
            return bgm_audio[indices].reshape(-1, 1)
        else:
            idx = max(0, min(len(bgm_audio) - 1, int(t_sec * sr)))
            return [[bgm_audio[idx]]]
    
    audio = AudioClip(make_audio, duration=duration, fps=sr)
    clip = clip.with_audio(audio)
    
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    
    try:
        import imageio_ffmpeg
        os.environ["FFMPEG_BINARY"] = imageio_ffmpeg.get_ffmpeg_exe()
    except:
        pass
    
    print(f"\n📦 编码: {output_path}")
    clip.write_videofile(
        output_path, fps=FPS, codec="libx264",
        audio_codec="aac",
        ffmpeg_params=["-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow"],
        logger="bar",
    )
    
    elapsed = time.time() - start_time
    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f"\n{'=' * 60}")
    print(f"✅ 渲染完成！")
    print(f"   文件: {output_path}")
    print(f"   大小: {size_mb:.1f} MB")
    print(f"   耗时: {elapsed:.1f}s")
    print(f"   BGM: {os.path.basename(bgm_wav_path)} (BPM={tempo:.0f})")
    print(f"   转场卡点: {len(transition_points)} 处")
    print(f"{'=' * 60}")
    return output_path
