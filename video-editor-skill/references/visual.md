# Visual Adjustments Reference

## Table of Contents
- [Scale — Resize Video](#scale)
- [Crop — Extract Region / Remove Borders](#crop)
- [Rotate — Rotation & Flipping](#rotate)
- [Speed — Playback Rate Changes](#speed)
- [Color — Grading & Correction](#color)
- [Stabilize — Remove Camera Shake](#stabilize)
- [Denoise — Noise Reduction & Sharpening](#denoise)
- [Deinterlace — Progressive Conversion](#deinterlace)

---

## Scale

```bash
# Resize to specific dimensions
ffmpeg -i input.mp4 -vf "scale=1280:720" resized.mp4

# Maintain aspect ratio (auto-calculate height)
ffmpeg -i input.mp4 -vf "scale=1280:-1" resized.mp4

# Auto-even width (avoids "not divisible by 2" errors)
ffmpeg -i input.mp4 -vf "scale=-2:720" resized.mp4

# Fit inside box without stretching
ffmpeg -i input.mp4 -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" boxed.mp4

# Downscale 4K to 1080p
ffmpeg -i 4k.mp4 -vf "scale=1920:1080" -c:v libx264 -crf 20 1080p.mp4
```

## Crop

```bash
# Crop to region (width:height:x:y)
ffmpeg -i input.mp4 -vf "crop=640:480:100:50" cropped.mp4

# Auto-detect and remove black bars
ffmpeg -i input.mp4 -vf cropdetect -f null - 2>&1 | tail -5    # detect
ffmpeg -i input.mp4 -vf "crop=1920:800:0:140" cropped.mp4      # apply

# Crop to square (center)
ffmpeg -i input.mp4 -vf "crop=min(iw\,ih):min(iw\,ih)" square.mp4

# Add letterbox padding
ffmpeg -i input.mp4 -vf "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" padded.mp4

# Vertical (9:16) to horizontal (16:9) with blurred background
ffmpeg -i vertical.mp4 -filter_complex \
  "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=20:5[bg]; \
   [0:v]scale=-2:1080:force_original_aspect_ratio=decrease[fg]; \
   [bg][fg]overlay=(W-w)/2:(H-h)/2[out]" \
  -map "[out]" -map 0:a -c:a copy horizontal.mp4
```

## Rotate

```bash
# 90° clockwise
ffmpeg -i input.mp4 -vf "transpose=1" rotated.mp4

# 90° counter-clockwise
ffmpeg -i input.mp4 -vf "transpose=2" rotated.mp4

# 180°
ffmpeg -i input.mp4 -vf "transpose=1,transpose=1" rotated180.mp4

# Arbitrary angle (30°)
ffmpeg -i input.mp4 -vf "rotate=PI/6:fillcolor=black" rotated_30.mp4

# Horizontal mirror
ffmpeg -i input.mp4 -vf "hflip" mirrored.mp4

# Vertical flip
ffmpeg -i input.mp4 -vf "vflip" flipped.mp4

# Aspect ratio change
ffmpeg -i input.mp4 -vf "scale=1920:1080,setsar=1" stretched.mp4
```

## Speed

```bash
# 2x (video + audio synced)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" fast.mp4

# 0.5x slow motion
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" -map "[v]" -map "[a]" slow.mp4

# 4x (chain atempo — max 2.0 per filter)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.25*PTS[v];[0:a]atempo=2.0,atempo=2.0[a]" -map "[v]" -map "[a]" 4x.mp4

# Video only (drop audio)
ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" -an fast_silent.mp4

# Smooth slow-mo with motion interpolation
ffmpeg -i input.mp4 -vf "setpts=2.0*PTS,minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" -an smooth_slow.mp4
```

**Formula**: video `setpts=1/FACTOR*PTS`, audio `atempo=FACTOR` (range 0.5–2.0; chain for larger factors).

## Color

```bash
# Brightness / contrast / saturation
ffmpeg -i input.mp4 -vf "eq=brightness=0.06:contrast=1.2:saturation=1.3" output.mp4

# Color temperature
ffmpeg -i input.mp4 -vf "colortemperature=temperature=6500" warm.mp4

# Color balance (tweak shadows)
ffmpeg -i input.mp4 -vf "colorbalance=rs=0.1:gs=-0.05:bs=-0.1" output.mp4

# Curves presets
ffmpeg -i input.mp4 -vf "curves=preset=lighter" output.mp4
ffmpeg -i input.mp4 -vf "curves=preset=increase_contrast" output.mp4
ffmpeg -i input.mp4 -vf "curves=preset=vintage" vintage.mp4

# LUT file (cinematic color grading)
ffmpeg -i input.mp4 -vf "lut3d=cinematic.cube" graded.mp4

# Black & white
ffmpeg -i input.mp4 -vf "hue=s=0" bw.mp4

# Sepia tone
ffmpeg -i input.mp4 -vf "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131" sepia.mp4

# Vignette
ffmpeg -i input.mp4 -vf "vignette=PI/4" vignette.mp4

# HDR → SDR tone mapping
ffmpeg -i hdr.mkv -vf "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable,zscale=t=bt709:m=bt709:r=tv,format=yuv420p" sdr.mp4
```

### Quick Looks
| Look | Filter Chain |
|---|---|
| Cinematic warm | `eq=contrast=1.1:saturation=0.9,colorbalance=rs=0.1:bs=-0.1,vignette=PI/4` |
| Cold/thriller | `eq=contrast=1.2:saturation=0.7,colorbalance=rs=-0.1:bs=0.15` |
| Vintage film | `curves=preset=vintage,noise=alls=20:allf=t+u,vignette=PI/4,hue=s=0.7` |
| High-key bright | `curves=preset=lighter,eq=brightness=0.05:saturation=1.1` |
| Bleach bypass | `eq=contrast=1.4:saturation=0.5,curves=preset=increase_contrast` |

## Stabilize

```bash
# Two-pass stabilization (best quality)
# Pass 1: Analyze
ffmpeg -i shaky.mp4 -vf vidstabdetect=shakiness=5:accuracy=15:result=transforms.trf -f null -

# Pass 2: Apply
ffmpeg -i shaky.mp4 -vf vidstabtransform=input=transforms.trf:smoothing=10:zoom=1 -c:a copy stabilized.mp4

# Single-pass (faster, less effective)
ffmpeg -i shaky.mp4 -vf deshake stabilized.mp4
```

**Parameters**:
- `shakiness` (1–10): how shaky the source is (higher = more aggressive detection)
- `smoothing` (1–30): how smooth the result should be (higher = smoother but more zoom)
- `zoom`: compensating zoom to hide edge artifacts

## Denoise

```bash
# NLMeans (balanced quality/speed)
ffmpeg -i noisy.mp4 -vf "nlmeans=s=6:p=7:r=15" denoised.mp4

# FFT-based (faster)
ffmpeg -i noisy.mp4 -vf "fftdnoiz=sigma=8" denoised.mp4

# BM3D (highest quality, slowest)
ffmpeg -i noisy.mp4 -vf "bm3d=sigma=10" denoised.mp4

# Sharpen
ffmpeg -i soft.mp4 -vf "unsharp=5:5:1.0" sharp.mp4

# Denoise + light sharpen (film grain removal)
ffmpeg -i grainy.mp4 -vf "nlmeans=s=3:p=5:r=11,unsharp=3:3:0.5" clean.mp4
```

## Deinterlace

```bash
# Yadif (standard)
ffmpeg -i interlaced.mp4 -vf "yadif=mode=1" progressive.mp4

# Bwdif (better quality)
ffmpeg -i interlaced.mp4 -vf "bwdif" progressive.mp4
```
