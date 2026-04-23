#!/usr/bin/env bash
# ============================================================
# download_models.sh — 下载本地部署所需的开源模型
# LLM 使用 GGUF Q4_K_M 量化版（~2.3GB，显存 ~3GB）
# ============================================================
set -euo pipefail

MODEL_DIR="${1:-./models}"
mkdir -p "$MODEL_DIR"

echo "========================================"
echo "  novel-audiobook 模型下载脚本"
echo "  目标目录: $MODEL_DIR"
echo "========================================"

# 检查工具
if ! command -v pip &> /dev/null; then
    echo "❌ 未找到 pip，请先安装 Python"
    exit 1
fi

# 确保 huggingface-cli 和 modelscope 已安装
pip install -U "huggingface_hub[cli]" modelscope 2>/dev/null || true

echo ""
echo "========================================"
echo "  [1/4] 下载 LLM: Qwen3-4B-Instruct-2507 GGUF Q4_K_M"
echo "  (~2.3GB, Q4量化, 显存仅需 ~3GB)"
echo "========================================"
GGUF_FILE="$MODEL_DIR/Qwen_Qwen3-4B-Instruct-2507-Q4_K_M.gguf"
if [ -f "$GGUF_FILE" ]; then
    echo "✅ 已存在，跳过"
else
    echo "  从 HuggingFace 下载 GGUF 文件..."
    huggingface-cli download bartowski/Qwen_Qwen3-4B-Instruct-2507-GGUF \
        Qwen_Qwen3-4B-Instruct-2507-Q4_K_M.gguf \
        --local-dir "$MODEL_DIR" 2>/dev/null \
    || {
        echo "  HuggingFace 失败，尝试 wget 直接下载..."
        wget -c "https://huggingface.co/bartowski/Qwen_Qwen3-4B-Instruct-2507-GGUF/resolve/main/Qwen_Qwen3-4B-Instruct-2507-Q4_K_M.gguf" \
            -O "$GGUF_FILE"
    }
    echo "✅ LLM GGUF 下载完成"
fi

echo ""
echo "========================================"
echo "  [2/4] 下载 TTS: Qwen3-TTS-12Hz-1.7B-CustomVoice"
echo "  (~6GB, 预设音色+指令控制)"
echo "========================================"
if [ -d "$MODEL_DIR/Qwen3-TTS-12Hz-1.7B-CustomVoice" ]; then
    echo "✅ 已存在，跳过"
else
    modelscope download --model Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice \
        --local_dir "$MODEL_DIR/Qwen3-TTS-12Hz-1.7B-CustomVoice" 2>/dev/null \
    || huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice \
        --local-dir "$MODEL_DIR/Qwen3-TTS-12Hz-1.7B-CustomVoice"
    echo "✅ TTS CustomVoice 下载完成"
fi

echo ""
echo "========================================"
echo "  [3/4] 下载 TTS: Qwen3-TTS-12Hz-1.7B-VoiceDesign"
echo "  (~6GB, 声音设计)"
echo "========================================"
if [ -d "$MODEL_DIR/Qwen3-TTS-12Hz-1.7B-VoiceDesign" ]; then
    echo "✅ 已存在，跳过"
else
    modelscope download --model Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign \
        --local_dir "$MODEL_DIR/Qwen3-TTS-12Hz-1.7B-VoiceDesign" 2>/dev/null \
    || huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign \
        --local-dir "$MODEL_DIR/Qwen3-TTS-12Hz-1.7B-VoiceDesign"
    echo "✅ TTS VoiceDesign 下载完成"
fi

echo ""
echo "========================================"
echo "  [4/4] 下载 TTS: Qwen3-TTS-12Hz-1.7B-Base"
echo "  (~6GB, 语音克隆)"
echo "========================================"
if [ -d "$MODEL_DIR/Qwen3-TTS-12Hz-1.7B-Base" ]; then
    echo "✅ 已存在，跳过"
else
    modelscope download --model Qwen/Qwen3-TTS-12Hz-1.7B-Base \
        --local_dir "$MODEL_DIR/Qwen3-TTS-12Hz-1.7B-Base" 2>/dev/null \
    || huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-Base \
        --local-dir "$MODEL_DIR/Qwen3-TTS-12Hz-1.7B-Base"
    echo "✅ TTS Base 下载完成"
fi

echo ""
echo "========================================"
echo "  ✅ 所有模型下载完成！"
echo ""
echo "  磁盘占用估算："
echo "    LLM  Qwen3-4B Q4_K_M GGUF    ~2.3GB  ← 大幅缩小！"
echo "    TTS  CustomVoice (1.7B)       ~6GB"
echo "    TTS  VoiceDesign (1.7B)       ~6GB"
echo "    TTS  Base (1.7B)              ~6GB"
echo "    总计                          ~20GB"
echo ""
echo "  GPU 显存需求："
echo "    LLM (vLLM GGUF Q4): ~3GB     ← 大幅降低！"
echo "    TTS (bfloat16):     ~6GB"
echo "    最低需要:           10GB"
echo "    推荐:               16GB (RTX 4060 Ti/3090/4090)"
echo ""
echo "  对比 FP16 原版："
echo "    FP16:  LLM ~8GB + TTS ~6GB = 14GB"
echo "    Q4:    LLM ~3GB + TTS ~6GB =  9GB  (节省 36%)"
echo "========================================"
