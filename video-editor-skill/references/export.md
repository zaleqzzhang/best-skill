# Export & Delivery Reference

## Table of Contents
- [GIF — Animated GIF Creation](#gif)
- [Thumbnails — Frame Extraction](#thumbnails)
- [Slideshow — Images to Video](#slideshow)
- [Quality — Bitrate & File Size Control](#quality)
- [FrameRate — FPS Conversion](#framerate)
- [Metadata — Tags & Container Settings](#metadata)

---

## GIF

### Quick GIF
```bash
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1" output.gif
```

### High-Quality with Palette (Recommended)
```bash
ffmpeg -i input.mp4 \
  -vf "fps=12,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  output.gif
```

### GIF from Time Range
```bash
ffmpeg -ss 5 -t 3 -i input.mp4 \
  -vf "fps=15,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5" \
  output.gif
```

### Boomerang GIF (Forward + Reverse)
```bash
ffmpeg -ss 2 -t 2 -i input.mp4 \
  -vf "fps=12,scale=320:-1,split[fwd][rev];[rev]reverse[r];[fwd][r]concat=n=2:v=1,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  boomerang.gif
```

### GIF Size Tips
- Width 320px = small (< 2MB typical)
- Width 480px = medium (2–5MB)
- Width 640px = large (5–15MB)
- Lower fps = smaller file (10 fps is usually fine for GIFs)

---

## Thumbnails

### Single Frame
```bash
ffmpeg -ss 00:00:10 -i input.mp4 -vframes 1 thumb.jpg
ffmpeg -ss 00:00:10 -i input.mp4 -vframes 1 thumb.png   # lossless
```

### Periodic Thumbnails
```bash
ffmpeg -i input.mp4 -vf "fps=1/10" thumb_%04d.jpg       # every 10 seconds
```

### Sized Thumbnail
```bash
ffmpeg -ss 5 -i input.mp4 -vframes 1 -vf "scale=320:180" thumb.jpg
```

### Contact Sheet / Tile Grid
```bash
ffmpeg -i input.mp4 -vf "fps=1/30,scale=240:135,tile=4x5" contact_sheet.jpg
```

### Animated Preview (Like YouTube Hover)
```bash
ffmpeg -ss 10 -t 5 -i input.mp4 -vf "fps=8,scale=320:-1" -an preview.webm
```

---

## Slideshow

### Basic Image Slideshow
```bash
ffmpeg -framerate 1/3 -i img_%03d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p slideshow.mp4
```
Each image shown for 3 seconds (`1/3` = one frame per 3 seconds).

### Slideshow with Crossfade
```bash
ffmpeg -loop 1 -t 3 -i img1.jpg -loop 1 -t 3 -i img2.jpg \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=2,format=yuv420p" slideshow.mp4
```

### Ken Burns Effect (Pan + Zoom)
```bash
ffmpeg -loop 1 -i photo.jpg \
  -vf "scale=8000:-1,zoompan=z='min(zoom+0.001,1.5)':d=300:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080" \
  -t 10 -c:v libx264 kenburns.mp4
```

### Video to Image Sequence
```bash
ffmpeg -i input.mp4 -r 1 frames/frame_%04d.png          # 1 frame per second
ffmpeg -i input.mp4 frames/frame_%04d.png                # all frames
```

### Image Sequence to Video
```bash
ffmpeg -framerate 24 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p video.mp4
```

### Slideshow with Background Music
```bash
ffmpeg -framerate 1/4 -i img_%03d.jpg -i music.mp3 \
  -c:v libx264 -r 30 -pix_fmt yuv420p -shortest slideshow.mp4
```

---

## Quality

### CRF Mode (Quality-Based, Variable Size)
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -c:a aac output.mp4
```

### CBR (Constant Bitrate)
```bash
ffmpeg -i input.mp4 -c:v libx264 -b:v 5M -maxrate 5M -bufsize 10M output.mp4
```

### VBR with Cap
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -maxrate 8M -bufsize 16M output.mp4
```

### Two-Pass (Best for Target File Size)
```bash
ffmpeg -i input.mp4 -c:v libx264 -b:v 4M -pass 1 -an -f null /dev/null
ffmpeg -i input.mp4 -c:v libx264 -b:v 4M -pass 2 -c:a aac output.mp4
```

### Target File Size Formula
```
bitrate (kbps) = target_size_KB × 8 / duration_seconds
```
Example: 50MB for 5 min video → `50×1024×8/300 ≈ 1365 kbps` total (video + audio).

---

## FrameRate

```bash
# Simple fps change
ffmpeg -i input.mp4 -r 30 output.mp4

# Filter-based (more control)
ffmpeg -i input.mp4 -vf "fps=24" output.mp4

# Motion-interpolated 60fps (smooth)
ffmpeg -i input.mp4 -vf "minterpolate=fps=60" smooth60.mp4
```

---

## Metadata

### Set Tags
```bash
ffmpeg -i input.mp4 -metadata title="My Video" -metadata artist="Author" -metadata year="2026" -c copy output.mp4
```

### Strip All Metadata
```bash
ffmpeg -i input.mp4 -map_metadata -1 -c copy stripped.mp4
```

### Copy Metadata Between Files
```bash
ffmpeg -i source.mp4 -i target.mp4 -map 1 -map_metadata 0 -c copy output.mp4
```

### Enable Fast Start (Web Playback)
```bash
ffmpeg -i input.mp4 -c copy -movflags +faststart output.mp4
```

### Check Fast Start
```bash
ffmpeg -v trace -i input.mp4 2>&1 | grep -i moov
```
