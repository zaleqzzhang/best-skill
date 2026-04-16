# Core Editing Reference

## Table of Contents
- [Convert — Format & Codec](#convert)
- [Trim — Cut Segments](#trim)
- [Join — Concatenate](#join)
- [Split — Segment into Parts](#split)

---

## Convert

### Container Change (No Re-encoding)
```bash
ffmpeg -i input.mkv -c copy output.mp4
```

### Re-encode to H.264 + AAC (Universal)
```bash
ffmpeg -i input.mov -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4
```

### ProRes for Editing Workflows
```bash
ffmpeg -i input.mp4 -c:v prores_ks -profile:v 3 -c:a pcm_s16le output.mov
```

### WebM for Web
```bash
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus -b:a 128k output.webm
```

### AV1 (Best Compression, Slow)
```bash
ffmpeg -i input.mp4 -c:v libaom-av1 -crf 30 -cpu-used 4 -c:a libopus output.mkv
```

### Audio Format Conversion
```bash
ffmpeg -i input.wav -c:a libmp3lame -q:a 2 output.mp3
ffmpeg -i input.mp3 -c:a aac -b:a 192k output.m4a
ffmpeg -i input.mp3 -c:a flac output.flac
```

### CRF Quality Guide
| Codec | Range | Default | Visually Lossless |
|---|---|---|---|
| H.264 (libx264) | 0–51 | 23 | ~18 |
| H.265 (libx265) | 0–51 | 28 | ~22 |
| VP9 (libvpx-vp9) | 0–63 | 31 | ~15 |
| AV1 (libaom-av1) | 0–63 | — | ~20 |

---

## Trim

### Fast Trim (Keyframe-based, Instant)
```bash
ffmpeg -ss 00:01:30 -i input.mp4 -to 00:00:30 -c copy trimmed.mp4
```
`-ss` before `-i` = fast seek to nearest keyframe. Best with `-c copy`.

### Precise Trim (Frame-accurate, Re-encodes)
```bash
ffmpeg -i input.mp4 -ss 00:01:30 -to 00:02:00 -c:v libx264 -c:a aac trimmed.mp4
```
`-ss` after `-i` = decode from start, cut at exact frame. Slower but pixel-perfect.

### First N Seconds
```bash
ffmpeg -i input.mp4 -t 60 -c copy first_minute.mp4
```

### Last N Seconds
```bash
ffmpeg -sseof -30 -i input.mp4 -c copy last_30s.mp4
```

### Multiple Segments in One Pass
```bash
ffmpeg -i input.mp4 \
  -ss 00:00:10 -to 00:00:20 -c copy seg1.mp4 \
  -ss 00:01:00 -to 00:01:15 -c copy seg2.mp4
```

### When to Choose Fast vs. Precise
- **Fast (`-c copy`)**: instant, no quality loss, but cut point snaps to nearest keyframe (~0.5–2s variance)
- **Precise (re-encode)**: frame-exact, but slower and technically one generation of quality loss (negligible at CRF ≤ 23)

---

## Join

### Method 1 — Concat Demuxer (Same Codec, No Re-encode)
```bash
printf "file '%s'\n" part1.mp4 part2.mp4 part3.mp4 > filelist.txt
ffmpeg -f concat -safe 0 -i filelist.txt -c copy merged.mp4
```
Requires all files to share the same codec, resolution, and frame rate. Clean up `filelist.txt` after.

### Method 2 — Filter Concat (Different Codecs/Resolutions)
```bash
ffmpeg -i part1.mp4 -i part2.mp4 -i part3.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" merged.mp4
```
Re-encodes everything — works with any mix of inputs but slower.

### Method 3 — Concat Protocol (MPEG-TS Only)
```bash
ffmpeg -i "concat:seg1.ts|seg2.ts|seg3.ts" -c copy merged.ts
```

---

## Split

### Fixed-Duration Segments
```bash
ffmpeg -i input.mp4 -c copy -f segment -segment_time 600 -reset_timestamps 1 segment_%03d.mp4
```
Splits every 600 seconds (10 minutes).

### At Specific Timestamps
```bash
ffmpeg -i input.mp4 -t 120 -c copy part1.mp4
ffmpeg -i input.mp4 -ss 120 -t 180 -c copy part2.mp4
ffmpeg -i input.mp4 -ss 300 -c copy part3.mp4
```
