---
name: anime-video-generator
description: 动漫风格短视频一键生成器。当用户需要以下功能时使用：(1) 输入提示词或角色名自动生成 15-30 秒动漫短视频，如"唐三成神"、"陆雪琪舞剑"等；(2) 自动从网络搜索高清素材图片并进行 AI 超分辨率放大和智能裁剪；(3) 使用 librosa 节拍检测实现音乐卡点转场；(4) 支持 Ken Burns 运镜、粒子特效、字幕叠加等专业后期效果；(5) 设置每日定时任务从 30 个国漫角色库中随机生成视频；(6) 自动生成社交平台文案并发布到小红书或抖音。核心亮点：AI 节拍卡点 + 高清素材自动采集 + 专业级后期特效 + 全自动流水线。
---

# 动漫短视频生成器

根据用户的文字描述或每日自动随机选取国漫角色，生成动漫风格的短视频（15-30 秒），支持 AI 节拍卡点、高清素材自动采集、专业后期特效和社交平台自动发布。

## 核心功能

1. **手动生成** - 输入提示词/角色名，一键生成动漫短视频
2. **AI 节拍卡点** - librosa 检测 BGM 节拍，转场精确对齐强拍
3. **高清素材采集** - 自动搜索下载高清图片 + AI 超分辨率放大至 1080p
4. **智能图片裁剪** - 竖屏图片模糊背景合成，确保人物至少露出一半身体
5. **专业后期特效** - Ken Burns 运镜、粒子光效、渐变字幕
6. **每日自动生成** - 从 30 个国漫角色库随机选角色，定时自动生成
7. **社交平台发布** - 自动生成文案并发布到小红书/抖音

## 工作流程

### 模式一：手动生成（用户指定角色/提示词）

1. 获取太湖平台 Token（调用 `get_taihu_token` MCP 工具）
2. 搜索下载高清素材图片（网络搜索 + AI 超分辨率放大）
3. 下载/生成 BGM 音乐
4. 运行节拍卡点视频生成脚本

```bash
# 使用节拍卡点引擎生成视频（推荐）
python3 scripts/create_anime_video_v8.py

# 在代码中调用：
from create_anime_video_v8 import create_beat_synced_video
create_beat_synced_video(
    image_paths=["img1.jpg", "img2.jpg", ...],  # 高清素材图片路径列表
    output_path="output.mp4",                     # 输出视频路径
    bgm_wav_path="bgm.wav",                       # BGM 音频文件路径
    clip_descs=["描述1", "描述2", ...],            # 每个片段的字幕描述
    duration=30,                                   # 视频总时长（秒）
)
```

### 模式二：AI 视频生成（混元 API）

```bash
# 单片段生成（5秒，混元视频 AI）
python3 scripts/generate_video.py --prompt "用户提示词" --token <TOKEN>

# 多片段拼接
python3 scripts/concat_videos.py --inputs clip_*.mp4 --output final.mp4 --duration 30
```

### 模式三：每日自动生成（定时任务）

```bash
# 随机选角色，生成 30 秒视频
python3 scripts/daily_auto_generate.py --token <TOKEN>

# 生成并发布到社交平台
python3 scripts/daily_auto_generate.py --token <TOKEN> \
  --publish-xiaohongshu --xhs-token <XHS_TOKEN> \
  --publish-douyin --dy-token <DY_TOKEN> --dy-openid <DY_OPENID>
```

### 设置每日定时任务

使用 Knot 的 `cron` 工具，设置每天 10:00 自动执行：

> 请执行每日国漫短视频自动生成任务：
> 1. 调用 get_taihu_token 获取 Token
> 2. 运行 `python3 scripts/daily_auto_generate.py --token <TOKEN> --duration 30`
> 3. 将生成的视频文件通过 display_download_links 提供下载
>
> You must use the notify tool to proactively inform me of the results.

## 脚本说明

| 脚本 | 功能 | 说明 |
|------|------|------|
| `create_anime_video_v8.py` | 节拍卡点视频引擎 | 核心引擎：librosa 节拍检测 + Ken Burns 运镜 + 粒子特效 + 字幕 |
| `generate_video.py` | 混元 AI 视频生成 | 调用混元视频 API 生成单片段 |
| `daily_auto_generate.py` | 每日自动流水线 | 随机选角色 → AI 分镜 → 生成 → 拼接 → 发布 |
| `concat_videos.py` | 视频拼接 | ffmpeg 多片段拼接为完整视频 |
| `bgm_generator.py` | BGM 生成 | 程序化生成古风/电子风 BGM |
| `smart_frame_extractor.py` | 智能帧提取 | 从视频中提取关键帧作为素材 |

## 技术亮点

### AI 节拍卡点（create_anime_video_v8.py）
- 使用 **librosa** 进行节拍检测，精确到毫秒级
- 转场自动对齐音乐强拍，节拍稳定性评分 ≥ 0.95
- 支持任意 BPM 的音乐自适应

### 高清素材处理
- 网络自动搜索下载（Bing/百度/Pixabay 多源）
- **OpenCV INTER_CUBIC** 超分辨率放大 + **UnsharpMask** 锐化
- 竖屏图片**模糊背景合成**：保留完整人物构图
- 统一输出 **1920×1080** 高清分辨率

### 专业后期特效
- **Ken Burns 效果**：缩放+平移模拟电影运镜
- **粒子光效**：随机粒子飘动增强氛围
- **渐变字幕**：底部半透明字幕条 + 淡入淡出
- **转场特效**：交叉溶解过渡

## 角色库

内置 30 个腾讯视频热门国漫角色，覆盖 10 部动漫。完整数据见 [character_database.md](references/character_database.md)。
提示词模板见 [prompt_templates.md](references/prompt_templates.md)。

## 前置依赖

- Python 3.8+、ffmpeg
- `pip install requests librosa numpy pillow opencv-python-headless soundfile`
- 太湖平台 API Token（通过 `get_taihu_token` MCP 工具获取）
