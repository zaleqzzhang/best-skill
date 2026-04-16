#!/usr/bin/env python3
"""
scan_media.py — Scan a directory for media files and generate MEDIA_INVENTORY.md

Usage:
    python scan_media.py [directory] [--depth N]

If no directory is given, scans the current working directory.
Tries ffprobe first; falls back to `npx remotion ffprobe` if ffprobe is not installed.
"""

import subprocess
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.ts', '.m4v', '.wmv', '.mxf', '.mpg', '.mpeg'}
AUDIO_EXTS = {'.mp3', '.wav', '.aac', '.flac', '.m4a', '.ogg', '.wma', '.opus'}
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.webp'}
SUBTITLE_EXTS = {'.srt', '.ass', '.ssa', '.vtt', '.sub', '.idx'}

# Detect which probe command is available (resolved once at import time)
_PROBE_CMD = None
_PROBE_NOTE = None

def _detect_probe():
    """Detect available ffprobe command: native > npx remotion > None."""
    global _PROBE_CMD, _PROBE_NOTE
    
    # 1. Try native ffprobe
    if shutil.which('ffprobe'):
        _PROBE_CMD = ['ffprobe']
        _PROBE_NOTE = None
        return
    
    # 2. Try npx remotion ffprobe (Remotion v4.0+ bundles FFmpeg 7.1)
    #    Note: npx remotion only supports H.264, H.265, VP8, VP9, ProRes codecs
    if shutil.which('npx'):
        try:
            # Use --yes to auto-install remotion if not present
            result = subprocess.run(
                ['npx', '--yes', 'remotion', 'ffprobe', '-version'],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0 and 'ffprobe' in result.stdout.lower():
                _PROBE_CMD = ['npx', '--yes', 'remotion', 'ffprobe']
                _PROBE_NOTE = "⚠️ Using `npx remotion ffprobe` — codec support limited to H.264, H.265, VP8, VP9, ProRes. Install FFmpeg (`brew install ffmpeg`) for full support."
                return
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    
    # 3. Nothing available
    _PROBE_CMD = None
    _PROBE_NOTE = "⚠️ ffprobe is not available. Install FFmpeg for full media analysis:\n>   • macOS: `brew install ffmpeg`\n>   • Ubuntu: `sudo apt install ffmpeg`\n>   • Or use npx: `npm install -g remotion` then re-run scan"

_detect_probe()

def probe_file(filepath):
    """Run ffprobe (or npx remotion ffprobe) on a file and return parsed JSON, or None on failure."""
    if _PROBE_CMD is None:
        return None
    try:
        cmd = _PROBE_CMD + ['-v', 'error', '-print_format', 'json',
                            '-show_format', '-show_streams', str(filepath)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        pass
    return None

def format_duration(seconds):
    """Convert seconds to HH:MM:SS or MM:SS."""
    if seconds is None:
        return "N/A"
    s = int(float(seconds))
    h, remainder = divmod(s, 3600)
    m, sec = divmod(remainder, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{sec:02d}"
    return f"{m:02d}:{sec:02d}"

def format_size(size_bytes):
    """Convert bytes to human-readable size."""
    if size_bytes is None:
        return "N/A"
    size = int(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}" if unit != 'B' else f"{size} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def get_stream_info(probe_data, stream_type):
    """Extract info for the first stream of given type."""
    if not probe_data or 'streams' not in probe_data:
        return None
    for s in probe_data['streams']:
        if s.get('codec_type') == stream_type:
            return s
    return None

def scan_directory(directory, max_depth=2):
    """Find all media files in directory up to max_depth."""
    files = {'video': [], 'audio': [], 'image': [], 'subtitle': []}
    root = Path(directory).resolve()
    
    for path in sorted(root.rglob('*')):
        if not path.is_file():
            continue
        # Check depth
        try:
            rel = path.relative_to(root)
            if len(rel.parts) > max_depth:
                continue
        except ValueError:
            continue
        # Skip hidden directories
        if any(part.startswith('.') for part in rel.parts):
            continue
        
        ext = path.suffix.lower()
        if ext in VIDEO_EXTS:
            files['video'].append(path)
        elif ext in AUDIO_EXTS:
            files['audio'].append(path)
        elif ext in IMAGE_EXTS:
            files['image'].append(path)
        elif ext in SUBTITLE_EXTS:
            files['subtitle'].append(path)
    
    return files

def generate_inventory(directory, max_depth=2):
    """Generate MEDIA_INVENTORY.md content."""
    root = Path(directory).resolve()
    files = scan_directory(directory, max_depth)
    
    lines = []
    lines.append("# 📂 Media Inventory\n")
    lines.append(f"> Auto-generated by Video Editor • {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"> Working directory: `{root}`")
    
    # Show which probe tool is being used
    if _PROBE_CMD:
        probe_name = ' '.join(_PROBE_CMD)
        lines.append(f"> Probe tool: `{probe_name}`")
    if _PROBE_NOTE:
        lines.append(f"> {_PROBE_NOTE}")
    lines.append("")
    
    total_files = sum(len(v) for v in files.values())
    if total_files == 0:
        lines.append("**No media files found in this directory.**\n")
        lines.append("Tip: Place your video, audio, image, or subtitle files here, then re-run the scan.\n")
        return '\n'.join(lines)
    
    # Summary
    counts = []
    if files['video']:
        counts.append(f"{len(files['video'])} video(s)")
    if files['audio']:
        counts.append(f"{len(files['audio'])} audio file(s)")
    if files['image']:
        counts.append(f"{len(files['image'])} image(s)")
    if files['subtitle']:
        counts.append(f"{len(files['subtitle'])} subtitle file(s)")
    lines.append(f"**Summary**: {', '.join(counts)}\n")
    
    # Video files
    if files['video']:
        lines.append(f"## 🎬 Video Files ({len(files['video'])})\n")
        lines.append("| # | File | Duration | Resolution | FPS | Video Codec | Audio Codec | Size |")
        lines.append("|---|------|----------|------------|-----|-------------|-------------|------|")
        for i, path in enumerate(files['video'], 1):
            rel = path.relative_to(root)
            probe = probe_file(path)
            fmt = probe.get('format', {}) if probe else {}
            vs = get_stream_info(probe, 'video')
            aus = get_stream_info(probe, 'audio')
            
            duration = format_duration(fmt.get('duration'))
            size = format_size(fmt.get('size') or path.stat().st_size)
            
            width = vs.get('width', '?') if vs else '?'
            height = vs.get('height', '?') if vs else '?'
            resolution = f"{width}×{height}" if width != '?' else "N/A"
            
            fps_str = "N/A"
            if vs and vs.get('r_frame_rate'):
                try:
                    num, den = vs['r_frame_rate'].split('/')
                    fps_val = int(num) / int(den)
                    fps_str = f"{fps_val:.0f}" if fps_val == int(fps_val) else f"{fps_val:.2f}"
                except (ValueError, ZeroDivisionError):
                    fps_str = vs['r_frame_rate']
            
            v_codec = vs.get('codec_name', 'N/A') if vs else 'N/A'
            a_codec = aus.get('codec_name', 'none') if aus else 'none'
            
            lines.append(f"| {i} | `{rel}` | {duration} | {resolution} | {fps_str} | {v_codec} | {a_codec} | {size} |")
        lines.append("")
    
    # Audio files
    if files['audio']:
        lines.append(f"## 🎵 Audio Files ({len(files['audio'])})\n")
        lines.append("| # | File | Duration | Sample Rate | Channels | Codec | Size |")
        lines.append("|---|------|----------|-------------|----------|-------|------|")
        for i, path in enumerate(files['audio'], 1):
            rel = path.relative_to(root)
            probe = probe_file(path)
            fmt = probe.get('format', {}) if probe else {}
            aus = get_stream_info(probe, 'audio')
            
            duration = format_duration(fmt.get('duration'))
            size = format_size(fmt.get('size') or path.stat().st_size)
            sample_rate = f"{aus.get('sample_rate', '?')} Hz" if aus else 'N/A'
            channels = aus.get('channels', '?') if aus else '?'
            ch_str = 'mono' if channels == 1 else 'stereo' if channels == 2 else f"{channels}ch" if isinstance(channels, int) else str(channels)
            codec = aus.get('codec_name', 'N/A') if aus else 'N/A'
            
            lines.append(f"| {i} | `{rel}` | {duration} | {sample_rate} | {ch_str} | {codec} | {size} |")
        lines.append("")
    
    # Subtitle files
    if files['subtitle']:
        lines.append(f"## 📝 Subtitle Files ({len(files['subtitle'])})\n")
        lines.append("| # | File | Format | Size |")
        lines.append("|---|------|--------|------|")
        fmt_names = {'.srt': 'SubRip', '.ass': 'ASS', '.ssa': 'SSA', '.vtt': 'WebVTT', '.sub': 'MicroDVD', '.idx': 'VobSub'}
        for i, path in enumerate(files['subtitle'], 1):
            rel = path.relative_to(root)
            ext = path.suffix.lower()
            size = format_size(path.stat().st_size)
            lines.append(f"| {i} | `{rel}` | {fmt_names.get(ext, ext)} | {size} |")
        lines.append("")
    
    # Image files
    if files['image']:
        lines.append(f"## 🖼️ Image Files ({len(files['image'])})\n")
        lines.append("| # | File | Dimensions | Format | Size |")
        lines.append("|---|------|------------|--------|------|")
        for i, path in enumerate(files['image'], 1):
            rel = path.relative_to(root)
            probe = probe_file(path)
            vs = get_stream_info(probe, 'video')
            size = format_size(path.stat().st_size)
            
            if vs:
                dims = f"{vs.get('width', '?')}×{vs.get('height', '?')}"
            else:
                dims = "N/A"
            
            fmt_name = path.suffix.upper().lstrip('.')
            lines.append(f"| {i} | `{rel}` | {dims} | {fmt_name} | {size} |")
        lines.append("")
    
    # Footer
    lines.append("---")
    lines.append("*Re-run scan if files change. Tip: organize into `sources/`, `exports/`, `assets/` for cleaner project management.*")
    
    return '\n'.join(lines)


if __name__ == '__main__':
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    depth = 2
    for i, arg in enumerate(sys.argv):
        if arg == '--depth' and i + 1 < len(sys.argv):
            depth = int(sys.argv[i + 1])
    
    inventory = generate_inventory(directory, depth)
    output_path = Path(directory) / 'MEDIA_INVENTORY.md'
    output_path.write_text(inventory, encoding='utf-8')
    print(f"✅ Media inventory written to {output_path}")
    print(inventory)
