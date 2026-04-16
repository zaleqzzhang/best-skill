# Power User Reference

## Table of Contents
- [Batch — Process Multiple Files](#batch)
- [HWAccel — Hardware Acceleration](#hwaccel)
- [Reverse — Playback Direction & Loops](#reverse)
- [Chapters — Chapter Management](#chapters)
- [Encoding — Advanced Codec Settings](#encoding)

---

## Batch

### Convert All Files in Directory
```bash
for f in *.avi; do ffmpeg -i "$f" -c:v libx264 -crf 23 -c:a aac "${f%.avi}.mp4"; done
```

### Batch Resize
```bash
for f in *.mp4; do ffmpeg -i "$f" -vf "scale=1280:720" "resized_$f"; done
```

### Batch Extract Audio
```bash
for f in *.mp4; do ffmpeg -i "$f" -vn -c:a libmp3lame -q:a 2 "${f%.mp4}.mp3"; done
```

### Batch Thumbnails
```bash
for f in *.mp4; do ffmpeg -ss 5 -i "$f" -vframes 1 "${f%.mp4}_thumb.jpg"; done
```

### Parallel Processing (4 workers)
```bash
ls *.mp4 | xargs -P 4 -I {} ffmpeg -i {} -c:v libx264 -crf 23 -c:a aac "converted/{}"
```

### GNU Parallel
```bash
parallel ffmpeg -i {} -c:v libx264 -crf 23 -c:a aac {.}.mp4 ::: *.avi
```

### Find + Process (recursive)
```bash
find . -name "*.mov" -exec sh -c 'ffmpeg -i "$1" -c:v libx264 -crf 23 "${1%.mov}.mp4"' _ {} \;
```

---

## HWAccel

### NVIDIA NVENC
```bash
# H.264
ffmpeg -i input.mp4 -c:v h264_nvenc -preset p4 -cq 23 -c:a copy output.mp4

# H.265
ffmpeg -i input.mp4 -c:v hevc_nvenc -preset p4 -cq 28 -c:a copy output.mp4

# Full GPU pipeline (decode + scale + encode)
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input.mp4 \
  -vf "scale_cuda=1280:720" -c:v h264_nvenc -preset p4 output.mp4
```

### Intel QSV
```bash
ffmpeg -i input.mp4 -c:v h264_qsv -preset medium -global_quality 23 -c:a copy output.mp4
```

### Apple VideoToolbox (macOS)
```bash
# H.264
ffmpeg -i input.mp4 -c:v h264_videotoolbox -b:v 5M -c:a copy output.mp4

# H.265 (HEVC)
ffmpeg -i input.mp4 -c:v hevc_videotoolbox -b:v 5M -tag:v hvc1 -c:a copy output.mp4
```

### AMD AMF
```bash
ffmpeg -i input.mp4 -c:v h264_amf -quality quality -c:a copy output.mp4
```

### Detect Available HW Encoders
```bash
ffmpeg -encoders 2>/dev/null | grep -E "nvenc|qsv|videotoolbox|amf|vaapi"
```

### When to Use Hardware Encoding
- **Speed**: 10–30x faster than CPU encoding
- **Quality**: slightly lower than software at same bitrate (use ~20% higher bitrate to compensate)
- **Use cases**: batch processing, real-time streaming, preview renders
- **Avoid when**: maximum quality matters more than speed (use software + two-pass instead)

---

## Reverse

### Reverse Entire Video
```bash
ffmpeg -i input.mp4 -vf reverse -af areverse reversed.mp4
```
Warning: loads entire video into RAM. Only use on short clips (< 30s recommended).

### Reverse a Short Clip
```bash
ffmpeg -ss 0 -t 5 -i input.mp4 -vf reverse -af areverse reversed_clip.mp4
```

### Loop Video N Times
```bash
ffmpeg -stream_loop 3 -i input.mp4 -c copy looped.mp4
```

### Seamless Loop (Forward + Reverse = Boomerang)
```bash
ffmpeg -i input.mp4 -filter_complex "[0:v]split[fwd][cpy];[cpy]reverse[rev];[fwd][rev]concat=n=2:v=1" -an loop.mp4
```

---

## Chapters

### Extract Chapter Info
```bash
ffprobe -v quiet -print_format json -show_chapters input.mkv
```

### Add Chapters via Metadata File
Create `chapters.txt`:
```
;FFMETADATA1
[CHAPTER]
TIMEBASE=1/1000
START=0
END=60000
title=Intro

[CHAPTER]
TIMEBASE=1/1000
START=60000
END=180000
title=Main Content

[CHAPTER]
TIMEBASE=1/1000
START=180000
END=300000
title=Conclusion
```

Apply:
```bash
ffmpeg -i input.mp4 -i chapters.txt -map_metadata 1 -c copy output.mp4
```

---

## Encoding

### H.264 Presets (Speed vs. Compression)
| Preset | Speed | File Size | Use Case |
|---|---|---|---|
| ultrafast | Fastest | Largest | Preview, screen recording |
| veryfast | Very fast | Large | Streaming |
| medium | Balanced | Balanced | **Default** |
| slow | Slow | Smaller | Final render |
| veryslow | Slowest | Smallest | Archival |

### H.265 / HEVC
```bash
ffmpeg -i input.mp4 -c:v libx265 -crf 28 -preset medium -c:a aac output.mp4
```
~50% smaller files than H.264 at equivalent quality, but slower to encode.

### AV1
```bash
ffmpeg -i input.mp4 -c:v libaom-av1 -crf 30 -cpu-used 4 -row-mt 1 -c:a libopus output.mkv
```
Best compression but very slow. `-cpu-used` (0–8): higher = faster but lower quality.

### ProRes (Editing Friendly)
```bash
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 3 -c:a pcm_s16le output.mov
```
Profiles: 0=Proxy, 1=LT, 2=Standard, **3=HQ**, 4=4444, 5=4444XQ

### VP9 / WebM
```bash
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus output.webm
```

### Two-Pass Encoding (Target Bitrate)
```bash
ffmpeg -i input.mp4 -c:v libx264 -b:v 4M -pass 1 -an -f null /dev/null
ffmpeg -i input.mp4 -c:v libx264 -b:v 4M -pass 2 -c:a aac output.mp4
```
