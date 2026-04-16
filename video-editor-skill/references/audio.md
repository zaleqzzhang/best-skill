# Audio Reference

## Table of Contents
- [Extract — Pull Audio from Video](#extract)
- [Replace — Swap Audio Track](#replace)
- [Mix — Layer Multiple Audio Sources](#mix)
- [Volume — Adjust Levels & Normalize](#volume)
- [Effects — Fade, Denoise, EQ, Silence](#effects)

---

## Extract

```bash
# Copy original codec (fastest)
ffmpeg -i video.mp4 -vn -c:a copy audio.aac

# Convert to MP3
ffmpeg -i video.mp4 -vn -c:a libmp3lame -q:a 2 audio.mp3

# Uncompressed WAV
ffmpeg -i video.mp4 -vn -c:a pcm_s16le audio.wav

# Lossless FLAC
ffmpeg -i video.mp4 -vn -c:a flac audio.flac
```

## Replace

```bash
# Replace audio track, keep video untouched
ffmpeg -i video.mp4 -i new_audio.mp3 -c:v copy -map 0:v:0 -map 1:a:0 output.mp4

# Replace audio and trim to shorter of the two
ffmpeg -i video.mp4 -i new_audio.mp3 -c:v copy -map 0:v:0 -map 1:a:0 -shortest output.mp4

# Remove audio entirely (mute)
ffmpeg -i video.mp4 -an -c:v copy silent.mp4
```

## Mix

```bash
# Background music under voice (music at 30% volume)
ffmpeg -i voice.mp4 -i bgm.mp3 \
  -filter_complex "[1:a]volume=0.3[bg];[0:a][bg]amix=inputs=2:duration=first[outa]" \
  -map 0:v -map "[outa]" -c:v copy output.mp4

# Mix two audio files with equal weight
ffmpeg -i audio1.mp3 -i audio2.mp3 -filter_complex "amix=inputs=2:duration=longest" mixed.mp3

# Delay second audio by 5 seconds before mixing
ffmpeg -i main.mp4 -i sfx.mp3 \
  -filter_complex "[1:a]adelay=5000|5000[delayed];[0:a][delayed]amix=inputs=2:duration=first[out]" \
  -map 0:v -map "[out]" -c:v copy output.mp4
```

## Volume

```bash
# Increase volume to 150%
ffmpeg -i input.mp4 -af "volume=1.5" -c:v copy louder.mp4

# Reduce by 5 dB
ffmpeg -i input.mp4 -af "volume=-5dB" -c:v copy quieter.mp4

# EBU R128 loudness normalization (broadcast standard)
ffmpeg -i input.mp4 -af loudnorm=I=-16:TP=-1.5:LR=11 -c:v copy normalized.mp4

# Detect current volume levels
ffmpeg -i input.mp4 -af volumedetect -f null - 2>&1 | grep -E "mean_volume|max_volume"

# Dynamic audio normalization (auto-adjusts throughout)
ffmpeg -i input.mp4 -af dynaudnorm -c:v copy normalized.mp4
```

### Platform Loudness Targets
| Platform | Target LUFS |
|---|---|
| YouTube | -14 |
| Spotify | -14 |
| Apple Music | -16 |
| Broadcast (EBU R128) | -23 |
| Podcast | -16 to -19 |

## Effects

### Fade In / Out
```bash
# Audio fade in (3s) and fade out (3s from second 57)
ffmpeg -i input.mp3 -af "afade=t=in:ss=0:d=3,afade=t=out:st=57:d=3" output.mp3
```

### Noise Reduction
```bash
# FFT-based denoise (nf = noise floor in dB)
ffmpeg -i noisy.mp4 -af "afftdn=nf=-25" -c:v copy cleaned.mp4

# RNN-based denoise (requires model file)
ffmpeg -i noisy.mp4 -af "arnndn=m=rnnoise-model.rnnn" -c:v copy cleaned.mp4

# Remove clicks and pops
ffmpeg -i vinyl.mp3 -af "adeclick" cleaned.mp3
```

### Equalizer
```bash
# Boost bass, cut harsh highs
ffmpeg -i input.mp3 -af "equalizer=f=100:t=h:w=200:g=5,equalizer=f=8000:t=h:w=2000:g=-3" output.mp3

# Telephone voice effect (bandpass)
ffmpeg -i input.mp3 -af "highpass=f=300,lowpass=f=3400" telephone.mp3
```

### Silence Detection & Splitting
```bash
# Detect silent parts (useful before auto-splitting)
ffmpeg -i input.mp4 -af silencedetect=noise=-30dB:d=2 -f null -

# Find silence timestamps for chapter splitting
ffmpeg -i podcast.mp3 -af silencedetect=noise=-35dB:d=1.5 -f null - 2>&1 | grep silence_end
```

### Audio Channel Manipulation
```bash
# Stereo to mono
ffmpeg -i stereo.mp3 -ac 1 mono.mp3

# Mono to stereo (duplicate channel)
ffmpeg -i mono.mp3 -ac 2 stereo.mp3

# Extract left/right channel
ffmpeg -i stereo.mp3 -af "pan=mono|c0=FL" left.mp3
ffmpeg -i stereo.mp3 -af "pan=mono|c0=FR" right.mp3

# 5.1 surround to stereo downmix
ffmpeg -i surround.ac3 -ac 2 stereo.mp3
```
