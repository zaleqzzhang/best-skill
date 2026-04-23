#!/usr/bin/env bash
# ============================================================
# start_vllm.sh — 启动本地 vLLM 服务
# Qwen3-4B-Instruct-2507 GGUF Q4_K_M 量化版（~2.3GB，显存 ~3GB）
# ============================================================
set -euo pipefail

MODEL_PATH="${1:-}"
PORT="${2:-8100}"
GPU_UTIL="${3:-0.25}"

# GGUF 模型的 HuggingFace 配置
GGUF_REPO="bartowski/Qwen_Qwen3-4B-Instruct-2507-GGUF"
GGUF_QUANT="Q4_K_M"
GGUF_FILE="Qwen_Qwen3-4B-Instruct-2507-Q4_K_M.gguf"
TOKENIZER="Qwen/Qwen3-4B-Instruct-2507"
SERVED_NAME="Qwen3-4B-Instruct-2507"

echo "========================================"
echo "  启动 vLLM 服务 (GGUF Q4_K_M 量化版)"
echo "  端口: $PORT"
echo "  GPU 利用率: $GPU_UTIL"
echo "========================================"

if [ -n "$MODEL_PATH" ] && [ -f "$MODEL_PATH" ]; then
    # 使用本地 GGUF 文件
    echo "  模式: 本地文件 $MODEL_PATH"
    vllm serve "$MODEL_PATH" \
        --tokenizer "$TOKENIZER" \
        --served-model-name "$SERVED_NAME" \
        --gpu-memory-utilization "$GPU_UTIL" \
        --max-model-len 32768 \
        --tensor-parallel-size 1 \
        --host 0.0.0.0 \
        --port "$PORT"
elif [ -n "$MODEL_PATH" ] && [ -d "$MODEL_PATH" ]; then
    # 兼容旧版：如果传入的是目录，检查目录下是否有 GGUF 文件
    GGUF_IN_DIR=$(find "$MODEL_PATH" -name "*.gguf" -type f | head -1)
    if [ -n "$GGUF_IN_DIR" ]; then
        echo "  模式: 目录中的 GGUF 文件 $GGUF_IN_DIR"
        vllm serve "$GGUF_IN_DIR" \
            --tokenizer "$TOKENIZER" \
            --served-model-name "$SERVED_NAME" \
            --gpu-memory-utilization "$GPU_UTIL" \
            --max-model-len 32768 \
            --tensor-parallel-size 1 \
            --host 0.0.0.0 \
            --port "$PORT"
    else
        echo "❌ 目录中未找到 .gguf 文件: $MODEL_PATH"
        echo "请下载 GGUF 模型: bash scripts/download_models.sh"
        exit 1
    fi
else
    # 直接从 HuggingFace 加载（vLLM 支持 repo_id:quant_type 格式）
    echo "  模式: HuggingFace 自动下载 ${GGUF_REPO}:${GGUF_QUANT}"
    vllm serve "${GGUF_REPO}:${GGUF_QUANT}" \
        --tokenizer "$TOKENIZER" \
        --served-model-name "$SERVED_NAME" \
        --gpu-memory-utilization "$GPU_UTIL" \
        --max-model-len 32768 \
        --tensor-parallel-size 1 \
        --host 0.0.0.0 \
        --port "$PORT"
fi
