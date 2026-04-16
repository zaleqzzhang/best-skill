# Compositing & Effects Reference

## Table of Contents
- [Watermark — Image & Text Overlays](#watermark)
- [Subtitles — Burn-in & Embed](#subtitles)
- [PiP — Picture-in-Picture](#pip)
- [Layout — Side-by-Side & Grid](#layout)
- [ChromaKey — Green Screen](#chromakey)
- [Transitions — Crossfades & Wipes](#transitions)
- [Effects — Blur, Pixelate, Vintage, and More](#effects)

---

## Watermark

### Image Watermark — Positioning
```bash
# Top-left
ffmpeg -i video.mp4 -i logo.png -filter_complex "overlay=10:10" output.mp4
# Top-right
ffmpeg -i video.mp4 -i logo.png -filter_complex "overlay=W-w-10:10" output.mp4
# Bottom-left
ffmpeg -i video.mp4 -i logo.png -filter_complex "overlay=10:H-h-10" output.mp4
# Bottom-right
ffmpeg -i video.mp4 -i logo.png -filter_complex "overlay=W-w-10:H-h-10" output.mp4
# Center
ffmpeg -i video.mp4 -i logo.png -filter_complex "overlay=(W-w)/2:(H-h)/2" output.mp4
```

### Watermark with Opacity & Scale
```bash
# 30% opacity
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]format=rgba,colorchannelmixer=aa=0.3[wm];[0:v][wm]overlay=W-w-10:H-h-10" output.mp4

# Resize watermark to 80px wide
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]scale=80:-1[wm];[0:v][wm]overlay=W-w-10:H-h-10" output.mp4
```

### Text Watermark
```bash
ffmpeg -i video.mp4 \
  -vf "drawtext=text='© 2026 MyBrand':fontsize=20:fontcolor=white@0.6:x=W-tw-10:y=H-th-10:shadowcolor=black@0.4:shadowx=1:shadowy=1" \
  output.mp4
```

### Timecode Overlay
```bash
ffmpeg -i video.mp4 -vf "drawtext=text='%{pts\\:hms}':fontsize=16:fontcolor=yellow:x=10:y=10" output.mp4
```

### Scrolling Watermark
```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]scale=60:-1[wm];[0:v][wm]overlay='mod(t*50,W):10'" output.mp4
```

---

## Subtitles

### Hard Subtitles (Burned In)
```bash
# SRT
ffmpeg -i video.mp4 -vf "subtitles=subs.srt" output.mp4

# ASS/SSA (preserves styling)
ffmpeg -i video.mp4 -vf "ass=subs.ass" output.mp4

# With custom style
ffmpeg -i video.mp4 -vf "subtitles=subs.srt:force_style='FontSize=28,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2'" output.mp4
```

### Soft Subtitles (Toggleable Track)
```bash
# MP4
ffmpeg -i video.mp4 -i subs.srt -c copy -c:s mov_text output.mp4

# MKV
ffmpeg -i video.mp4 -i subs.srt -c copy -c:s srt output.mkv
ffmpeg -i video.mp4 -i subs.ass -c copy -c:s ass output.mkv
```

### Extract / Convert Subtitles
```bash
# Extract subtitle track
ffmpeg -i video.mkv -map 0:s:0 -c:s srt output.srt

# Convert format
ffmpeg -i subs.vtt -c:s srt output.srt
```

### Multiple Language Tracks
```bash
ffmpeg -i video.mp4 -i en.srt -i zh.srt \
  -map 0:v -map 0:a -map 1 -map 2 \
  -c copy -c:s mov_text \
  -metadata:s:s:0 language=eng -metadata:s:s:1 language=chi \
  output.mp4
```

When the user mentions subtitles, scan their directory for `.srt`, `.ass`, `.ssa`, `.vtt`, `.sub` files.

---

## PiP

### Basic Picture-in-Picture
```bash
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "[1:v]scale=320:-1[pip];[0:v][pip]overlay=W-w-20:H-h-20" output.mp4
```

### PiP with Border
```bash
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "[1:v]scale=320:-1,drawbox=0:0:iw:ih:white:t=3[pip];[0:v][pip]overlay=W-w-20:H-h-20" output.mp4
```

### PiP with Rounded Corners (using geq)
```bash
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "[1:v]scale=320:-1,format=yuva420p,geq='lum=lum(X,Y):a=if(gt(abs(W/2-X),W/2-10)*gt(abs(H/2-Y),H/2-10),0,255)'[pip];[0:v][pip]overlay=W-w-20:H-h-20" output.mp4
```

---

## Layout

### Side-by-Side
```bash
ffmpeg -i left.mp4 -i right.mp4 \
  -filter_complex "[0:v]scale=960:540[l];[1:v]scale=960:540[r];[l][r]hstack" output.mp4
```

### Top / Bottom Stack
```bash
ffmpeg -i top.mp4 -i bottom.mp4 \
  -filter_complex "[0:v]scale=1920:540[t];[1:v]scale=1920:540[b];[t][b]vstack" output.mp4
```

### 2×2 Grid
```bash
ffmpeg -i v1.mp4 -i v2.mp4 -i v3.mp4 -i v4.mp4 \
  -filter_complex "[0:v]scale=960:540[a];[1:v]scale=960:540[b];[2:v]scale=960:540[c];[3:v]scale=960:540[d];[a][b][c][d]xstack=inputs=4:layout=0_0|960_0|0_540|960_540" \
  output.mp4
```

### 3×2 Grid
```bash
ffmpeg -i v1.mp4 -i v2.mp4 -i v3.mp4 -i v4.mp4 -i v5.mp4 -i v6.mp4 \
  -filter_complex "[0:v]scale=640:360[a];[1:v]scale=640:360[b];[2:v]scale=640:360[c];[3:v]scale=640:360[d];[4:v]scale=640:360[e];[5:v]scale=640:360[f];[a][b][c][d][e][f]xstack=inputs=6:layout=0_0|640_0|1280_0|0_360|640_360|1280_360" \
  output.mp4
```

---

## ChromaKey

### Remove Green → Transparent
```bash
ffmpeg -i greenscreen.mp4 -vf "chromakey=0x00FF00:0.3:0.1" -c:v png output.mov
```
Output must support alpha (WebM, ProRes 4444 MOV, PNG sequence).

### Replace Background with Video/Image
```bash
ffmpeg -i greenscreen.mp4 -i background.mp4 \
  -filter_complex "[0:v]chromakey=0x00FF00:0.3:0.1[fg];[1:v][fg]overlay[out]" \
  -map "[out]" -map 1:a output.mp4
```

### Blue Screen
```bash
ffmpeg -i bluescreen.mp4 -i bg.jpg \
  -filter_complex "[0:v]chromakey=0x0000FF:0.3:0.1[fg];[1:v]scale=1920:1080[bg];[bg][fg]overlay[out]" \
  -map "[out]" output.mp4
```

### Fine-Tuned Colorkey
```bash
ffmpeg -i greenscreen.mp4 -i bg.mp4 \
  -filter_complex "[0:v]colorkey=0x00FF00:0.4:0.15[fg];[1:v][fg]overlay[out]" \
  -map "[out]" -map 0:a output.mp4
```

**Tuning**: `similarity` (0.01–1.0, higher = more aggressive keying), `blend` (0.0–1.0, higher = softer edges).

---

## Transitions

### Crossfade (xfade)
```bash
# Fade (offset = first clip duration minus transition duration)
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "xfade=transition=fade:duration=1:offset=4" output.mp4
```

### Available Transitions
`fade`, `wipeleft`, `wiperight`, `wipeup`, `wipedown`, `slideleft`, `slideright`, `slideup`, `slidedown`, `circlecrop`, `rectcrop`, `distance`, `fadeblack`, `fadewhite`, `radial`, `smoothleft`, `smoothright`, `smoothup`, `smoothdown`, `circleopen`, `circleclose`, `vertopen`, `vertclose`, `horzopen`, `horzclose`, `dissolve`, `pixelize`, `diagtl`, `diagtr`, `diagbl`, `diagbr`, `hlslice`, `hrslice`, `vuslice`, `vdslice`, `hblur`, `fadegrays`, `squeezev`, `squeezeh`, `zoomin`, `coverleft`, `coverright`, `coverup`, `coverdown`, `revealleft`, `revealright`, `revealup`, `revealdown`

### Audio + Video Crossfade
```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v];[0:a][1:a]acrossfade=d=1[a]" \
  -map "[v]" -map "[a]" output.mp4
```

### Fade In / Fade Out
```bash
# Fade in from black (first 2 seconds)
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=2" -af "afade=t=in:st=0:d=2" output.mp4

# Fade out to black (last 2 seconds — need duration from ffprobe)
ffmpeg -i input.mp4 -vf "fade=t=out:st=28:d=2" -af "afade=t=out:st=28:d=2" output.mp4
```

---

## Effects

### Blur
```bash
# Box blur
ffmpeg -i input.mp4 -vf "boxblur=10:5" blurred.mp4

# Gaussian blur
ffmpeg -i input.mp4 -vf "gblur=sigma=10" blurred.mp4

# Blur specific region (privacy mask)
ffmpeg -i input.mp4 -vf "split[main][mask];[mask]crop=200:200:300:100,gblur=sigma=20[b];[main][b]overlay=300:100" output.mp4
```

### Pixelate Region
```bash
ffmpeg -i input.mp4 -vf "split[main][mask];[mask]crop=200:200:300:100,scale=20:20:flags=neighbor,scale=200:200:flags=neighbor[pix];[main][pix]overlay=300:100" output.mp4
```

### Vintage Film Look
```bash
ffmpeg -i input.mp4 -vf "curves=preset=vintage,noise=alls=20:allf=t+u,vignette=PI/4,hue=s=0.7" vintage.mp4
```

### Mirror Effect
```bash
ffmpeg -i input.mp4 -vf "split[l][r];[l]crop=iw/2:ih:0:0,hflip[lf];[r]crop=iw/2:ih:0:0[rf];[lf][rf]hstack" mirror.mp4
```

### Edge Detection
```bash
ffmpeg -i input.mp4 -vf "edgedetect=low=0.1:high=0.3" edges.mp4
```

### Emboss
```bash
ffmpeg -i input.mp4 -vf "convolution='0 -1 0 -1 5 -1 0 -1 0:0 -1 0 -1 5 -1 0 -1 0:0 -1 0 -1 5 -1 0 -1 0:0 -1 0 -1 5 -1 0 -1 0'" emboss.mp4
```

### Invert Colors
```bash
ffmpeg -i input.mp4 -vf "negate" inverted.mp4
```

### Draw Shapes
```bash
ffmpeg -i input.mp4 -vf "drawbox=x=100:y=100:w=300:h=200:color=red@0.5:t=fill" box.mp4
```

### Remove Logo / Watermark
```bash
ffmpeg -i input.mp4 -vf "delogo=x=10:y=10:w=100:h=30" cleaned.mp4
```

### Audio Visualization
```bash
# Waveform image
ffmpeg -i audio.mp3 -filter_complex "showwavespic=s=1920x200:colors=0x00AAFF" waveform.png

# Spectrum video
ffmpeg -i audio.mp3 -filter_complex "showspectrum=s=1920x1080:slide=scroll:mode=combined" spectrum.mp4

# Waveform monitor (for color grading)
ffmpeg -i input.mp4 -vf "waveform=m=column:e=1" -pix_fmt yuv420p waveform.mp4
```
