---
name: novel-audiobook
description: >
  小说有声书全自动生成技能 — 100% 本地部署，不调用任何远程 API。
  当用户需要以下操作时使用：(1) 将小说文件（txt/pdf/epub/docx）转换为有声书 MP3，
  (2) 对小说进行角色识别和对话划分，(3) 使用 AI 语音合成（TTS）朗读小说，
  (4) 为小说角色设计不同音色，(5) 部署或启动有声书生成服务。
  触发关键词：有声书、audiobook、小说朗读、TTS、语音合成、角色配音、
  小说转语音、文字转语音、novel to speech、text to audiobook。
---

# 小说有声书全自动生成

将小说文件上传后自动完成：文本解析 → LLM 角色划分 → TTS 声音设计 → 语音合成 → MP3 输出。

## 技术架构

| 组件 | 技术 |
|------|------|
| LLM 角色分析 | Qwen3-4B-Instruct-2507 GGUF Q4_K_M（本地 vLLM，~3GB 显存） |
| TTS 语音合成 | Qwen3-TTS-12Hz-1.7B 系列开源模型（qwen-tts Python 包） |
| Web 框架 | FastAPI + Celery + Redis |
| 音频处理 | pydub + FFmpeg |
| 文件解析 | PyPDF2 / ebooklib / python-docx / chardet |

## 硬件要求

- **GPU**: 最低 10GB VRAM（LLM ~3GB + TTS ~6GB）
- **内存**: 16GB+ RAM
- **磁盘**: 22GB+（模型存储）

## 部署流程

### 1. 环境准备

```bash
apt-get install -y ffmpeg
conda create -n novel-audiobook python=3.12 -y
conda activate novel-audiobook
pip install -r requirements.txt
pip install vllm>=0.8.5
```

requirements.txt 位于 `scripts/requirements.txt`。

### 2. 下载模型（~20GB）

运行 `scripts/download_models.sh ./models`，或手动下载：

- **LLM GGUF**: `bartowski/Qwen_Qwen3-4B-Instruct-2507-GGUF` → `Qwen_Qwen3-4B-Instruct-2507-Q4_K_M.gguf`（~2.3GB）
- **TTS CustomVoice**: `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`（~6GB，预设音色+指令控制）
- **TTS VoiceDesign**: `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`（~6GB，声音设计）
- **TTS Base**: `Qwen/Qwen3-TTS-12Hz-1.7B-Base`（~6GB，语音克隆）

### 3. 启动服务

```bash
cp .env.example .env
redis-server &
bash scripts/start_vllm.sh ./models/Qwen_Qwen3-4B-Instruct-2507-Q4_K_M.gguf 8100 &
sleep 60
celery -A src.tasks.celery_app worker --loglevel=info --concurrency=1 &
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### 4. Docker 一键部署（推荐）

```bash
bash scripts/download_models.sh ./models
cp .env.example .env
docker-compose up -d
```

Docker 配置文件见 `references/docker-compose.yml` 和 `references/Dockerfile`。

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/api/v1/audiobook/generate` | 异步上传+生成 |
| `POST` | `/api/v1/audiobook/generate-sync` | 同步生成（≤5MB） |
| `GET` | `/api/v1/audiobook/status/{task_id}` | 查询进度 |
| `GET` | `/api/v1/audiobook/roles/{task_id}` | 获取角色划分 JSON |
| `GET` | `/api/v1/audiobook/download/{task_id}` | 下载 MP3 |
| `GET` | `/health` | 健康检查 |

使用示例：

```bash
# 上传小说
curl -X POST http://localhost:8000/api/v1/audiobook/generate -F "file=@novel.txt"
# 查询状态
curl http://localhost:8000/api/v1/audiobook/status/{task_id}
# 下载 MP3
curl -O http://localhost:8000/api/v1/audiobook/download/{task_id}
```

## 预设音色

| 音色 | 特点 | 适合角色 |
|------|------|---------|
| Cherry | 沉稳女声 | 旁白、成熟女性 |
| Serena | 温柔女声 | 温柔女性 |
| Bella | 甜美女声 | 年轻女性 |
| Vivian | 活力女声 | 活泼女性 |
| Ethan | 年轻男声 | 青年男性 |
| Chengfeng | 成熟男声 | 中年男性 |
| Ryan | 沉稳男声 | 稳重男性 |
| Dylan | 低沉男声 | 沉默寡言型 |
| Uncle_Fu | 老年男声 | 老年男性 |

## 环境变量

完整配置见 `references/env-config.md`。关键变量：

- `LLM_BASE_URL` — vLLM 服务地址（默认 `http://localhost:8100/v1`）
- `TTS_MODEL_LOCAL_DIR` — TTS 模型本地目录
- `REDIS_URL` — Redis 连接地址
- `OUTPUT_DIR` — 输出文件目录

## 源码结构

```
src/
├── config.py          — 配置管理（pydantic-settings）
├── file_parser.py     — 多格式文件解析（txt/pdf/epub/docx）
├── role_analyzer.py   — LLM 角色分析（调用本地 vLLM）
├── tts_engine.py      — TTS 引擎（声音设计/克隆/预设音色）
├── audio_merger.py    — 音频合并（pydub → MP3）
├── pipeline.py        — 五阶段流水线编排
├── tasks.py           — Celery 异步任务
└── main.py            — FastAPI 路由
```

完整源码位于 `scripts/src/` 目录下，可直接部署运行。

## 故障排除

- **显存不足**：TTS 换 0.6B 版本或设 `TTS_DEVICE=cpu`
- **Q4 量化精度**：Q4_K_M 保持原始模型 95-98% 精度，角色划分任务影响可忽略
- **TTS 加载慢**：首次调用 ~30s 加载模型，后续毫秒级响应
