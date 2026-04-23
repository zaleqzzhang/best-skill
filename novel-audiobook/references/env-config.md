# 环境变量配置说明

## LLM: 本地 vLLM 服务 (GGUF Q4_K_M 量化版)

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `LLM_BASE_URL` | vLLM 服务的 OpenAI 兼容接口地址 | `http://localhost:8100/v1` |
| `LLM_API_KEY` | vLLM API Key（本地部署通常为 EMPTY） | `EMPTY` |
| `LLM_MODEL` | vLLM 中 served-model-name | `Qwen3-4B-Instruct-2507` |
| `LLM_GGUF_REPO` | GGUF 模型 HF repo | `bartowski/Qwen_Qwen3-4B-Instruct-2507-GGUF` |
| `LLM_GGUF_FILE` | GGUF 文件名 | `Qwen_Qwen3-4B-Instruct-2507-Q4_K_M.gguf` |
| `LLM_TOKENIZER` | GGUF 模型 tokenizer | `Qwen/Qwen3-4B-Instruct-2507` |
| `LLM_MODEL_PATH` | LLM GGUF 本地文件路径 | `./models/...Q4_K_M.gguf` |

## TTS: 本地 Qwen3-TTS 开源模型

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `TTS_CUSTOM_VOICE_MODEL` | CustomVoice 模型 | `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` |
| `TTS_VOICE_DESIGN_MODEL` | VoiceDesign 模型 | `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` |
| `TTS_BASE_MODEL` | Base 模型 | `Qwen/Qwen3-TTS-12Hz-1.7B-Base` |
| `TTS_DEVICE` | 运行设备 (auto/cuda/cpu) | `auto` |
| `TTS_TORCH_DTYPE` | 模型精度 | `bfloat16` |
| `TTS_MODEL_LOCAL_DIR` | TTS 模型本地目录 | `./models` |

## 服务配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `REDIS_URL` | Redis 连接地址 | `redis://localhost:6379/0` |
| `MAX_UPLOAD_SIZE_MB` | 最大上传文件大小 | `50` |
| `OUTPUT_DIR` | 输出文件目录 | `./output` |

## .env 示例

```env
LLM_BASE_URL=http://localhost:8100/v1
LLM_API_KEY=EMPTY
LLM_MODEL=Qwen3-4B-Instruct-2507
LLM_GGUF_REPO=bartowski/Qwen_Qwen3-4B-Instruct-2507-GGUF
LLM_GGUF_FILE=Qwen_Qwen3-4B-Instruct-2507-Q4_K_M.gguf
LLM_TOKENIZER=Qwen/Qwen3-4B-Instruct-2507
LLM_MODEL_PATH=./models/Qwen_Qwen3-4B-Instruct-2507-Q4_K_M.gguf

TTS_CUSTOM_VOICE_MODEL=Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice
TTS_VOICE_DESIGN_MODEL=Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign
TTS_BASE_MODEL=Qwen/Qwen3-TTS-12Hz-1.7B-Base
TTS_DEVICE=auto
TTS_TORCH_DTYPE=bfloat16
TTS_MODEL_LOCAL_DIR=./models

REDIS_URL=redis://localhost:6379/0
MAX_UPLOAD_SIZE_MB=50
OUTPUT_DIR=./output
```
