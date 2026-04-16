# Capture & Streaming Reference

## Table of Contents
- [Screen — Desktop Recording](#screen)
- [Webcam — Camera Capture](#webcam)
- [RTMP — Push to Streaming Platforms](#rtmp)
- [HLS — HTTP Live Streaming](#hls)
- [Pull — Record Remote Streams](#pull)

---

## Screen

### macOS (AVFoundation)
```bash
# List available devices
ffmpeg -f avfoundation -list_devices true -i ""

# Record screen + audio
ffmpeg -f avfoundation -framerate 30 -i "1:0" -c:v libx264 -preset ultrafast -crf 18 screen.mp4

# Record specific area
ffmpeg -f avfoundation -framerate 30 -video_size 1280x720 -i "1:0" screen.mp4
```

### Linux (x11grab)
```bash
# Full screen
ffmpeg -f x11grab -framerate 30 -video_size 1920x1080 -i :0.0 -c:v libx264 -preset ultrafast screen.mp4

# With PulseAudio
ffmpeg -f x11grab -framerate 30 -video_size 1920x1080 -i :0.0 -f pulse -i default -c:v libx264 -preset ultrafast screen.mp4

# Specific region (offset 100,200)
ffmpeg -f x11grab -framerate 30 -video_size 800x600 -i :0.0+100,200 -c:v libx264 screen.mp4
```

### Windows (gdigrab)
```bash
# Full desktop
ffmpeg -f gdigrab -framerate 30 -i desktop -c:v libx264 -preset ultrafast screen.mp4

# Specific window
ffmpeg -f gdigrab -framerate 30 -i title="Notepad" window.mp4
```

---

## Webcam

```bash
# macOS
ffmpeg -f avfoundation -framerate 30 -i "0" webcam.mp4

# Linux
ffmpeg -f v4l2 -framerate 30 -video_size 1280x720 -i /dev/video0 webcam.mp4

# Windows
ffmpeg -f dshow -i video="Integrated Camera" webcam.mp4

# Webcam + screen side-by-side (macOS)
ffmpeg -f avfoundation -framerate 30 -i "1" -f avfoundation -framerate 30 -video_size 320x240 -i "0" \
  -filter_complex "[1:v]scale=320:-1[cam];[0:v][cam]overlay=W-w-10:H-h-10" output.mp4
```

---

## RTMP

### Push File to Streaming Platform
```bash
ffmpeg -re -i input.mp4 \
  -c:v libx264 -preset veryfast -b:v 3000k -maxrate 3000k -bufsize 6000k \
  -c:a aac -b:a 128k -f flv \
  "rtmp://live.twitch.tv/app/YOUR_STREAM_KEY"
```

### Screen Capture → Live Stream
```bash
ffmpeg -f avfoundation -framerate 30 -i "1:0" \
  -c:v libx264 -preset ultrafast -tune zerolatency -b:v 2500k \
  -c:a aac -b:a 128k -f flv \
  "rtmp://your-server/live/stream"
```

### Platform-Specific Settings
| Platform | Recommended Video Bitrate | Audio | Max Resolution |
|---|---|---|---|
| Twitch | 3000–6000 kbps | 128k AAC | 1080p60 |
| YouTube Live | 4500–9000 kbps | 128k AAC | 4K60 |
| Bilibili | 2000–6000 kbps | 128k AAC | 1080p60 |
| Facebook Live | 3000–6000 kbps | 128k AAC | 1080p30 |

### RTMP with Audio Input (macOS)
```bash
ffmpeg -f avfoundation -framerate 30 -i "1:0" \
  -c:v libx264 -preset ultrafast -tune zerolatency -b:v 4500k \
  -g 60 -keyint_min 60 \
  -c:a aac -b:a 160k -ar 44100 \
  -f flv "rtmp://your-server/live/stream"
```

---

## HLS

### Basic HLS
```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -f hls \
  -hls_time 6 -hls_list_size 0 -hls_segment_filename "segment_%03d.ts" playlist.m3u8
```

### Adaptive Bitrate HLS (Multi-Quality)
```bash
ffmpeg -i input.mp4 \
  -filter_complex "[v:0]split=3[v1][v2][v3]; \
    [v1]scale=1920:1080[v1out];[v2]scale=1280:720[v2out];[v3]scale=640:360[v3out]" \
  -map "[v1out]" -c:v:0 libx264 -b:v:0 5M \
  -map "[v2out]" -c:v:1 libx264 -b:v:1 3M \
  -map "[v3out]" -c:v:2 libx264 -b:v:2 1M \
  -map a:0 -c:a aac -b:a 128k \
  -f hls -hls_time 6 -hls_list_size 0 \
  -master_pl_name master.m3u8 \
  -var_stream_map "v:0,a:0 v:1,a:0 v:2,a:0" stream_%v.m3u8
```

### DASH Output
```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -f dash -min_seg_duration 4000000 output.mpd
```

---

## Pull

### Record RTSP Stream
```bash
ffmpeg -rtsp_transport tcp -i "rtsp://camera-ip:554/stream" -c copy -t 3600 recording.mp4
```

### Record HTTP Stream
```bash
ffmpeg -i "https://stream-url/live.m3u8" -c copy recording.mp4
```

### Record with Duration Limit
```bash
ffmpeg -rtsp_transport tcp -i "rtsp://camera-ip:554/stream" -c copy -t 7200 -f segment -segment_time 3600 recording_%03d.mp4
```
