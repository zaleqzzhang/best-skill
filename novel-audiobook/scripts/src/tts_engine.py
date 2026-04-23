"""
TTS 语音合成引擎 — 本地开源模型版
使用 qwen-tts Python 包直接加载 Qwen3-TTS 系列开源模型，无需调用远程 API。

三种能力：
  1. 声音设计（VoiceDesign 模型：根据自然语言描述生成全新音色）
  2. 语音克隆（Base 模型：3 秒参考音频克隆音色）
  3. 自定义音色 + 指令控制（CustomVoice 模型：9种预设音色 + 情感/风格控制）
"""
import os
import re
import threading
from pathlib import Path
from typing import Optional

import torch
import numpy as np
import soundfile as sf
from loguru import logger

from src.config import settings


class TTSError(Exception):
    """TTS 相关异常。"""

    def __init__(self, message: str, detail: Optional[str] = None):
        self.message = message
        self.detail = detail
        super().__init__(message)


# ============================================================
# 模型单例管理（懒加载，首次调用时初始化）
# ============================================================

_model_cache: dict[str, object] = {}
_model_lock = threading.Lock()


def _get_torch_dtype():
    """根据配置返回 torch dtype。"""
    dtype_map = {
        "bfloat16": torch.bfloat16,
        "float16": torch.float16,
        "float32": torch.float32,
    }
    return dtype_map.get(settings.tts_torch_dtype, torch.bfloat16)


def _unwrap_wav(wav) -> np.ndarray:
    """
    qwen-tts 的 generate_* 返回 (list[np.ndarray], sr)，
    需要取 list 中第一个元素作为实际音频数据。
    """
    if isinstance(wav, list):
        wav = wav[0]
    if hasattr(wav, 'cpu'):
        wav = wav.cpu().numpy()
    if isinstance(wav, np.ndarray) and wav.ndim == 0:
        raise ValueError("TTS 返回空音频 (scalar)")
    return wav


def _load_tts_model(model_name: str):
    """加载 TTS 模型（线程安全、懒加载、单例）。"""
    if model_name in _model_cache:
        return _model_cache[model_name]

    with _model_lock:
        if model_name in _model_cache:
            return _model_cache[model_name]

        from qwen_tts import Qwen3TTSModel

        # 如果配置了本地路径，优先使用
        model_path = model_name
        if settings.tts_model_local_dir:
            local_path = Path(settings.tts_model_local_dir) / Path(model_name).name
            if local_path.exists():
                model_path = str(local_path)

        logger.info(f"加载 TTS 模型: {model_path} (dtype={settings.tts_torch_dtype})")

        model = Qwen3TTSModel.from_pretrained(
            model_path,
            dtype=_get_torch_dtype(),
            device_map=settings.tts_device,
        )

        _model_cache[model_name] = model
        logger.info(f"TTS 模型加载完成: {model_name}")
        return model


# ============================================================
# 声音设计：根据文字描述生成新音色
# ============================================================

async def design_voice(
    voice_description: str,
    preview_text: str = "你好，我是你的有声书朗读者。",
    preferred_name: str = "novel_voice",
) -> dict:
    """
    通过 VoiceDesign 模型根据自然语言描述生成音色。

    Args:
        voice_description: 音色描述，如 "沉稳的中年男性播音员，音色低沉浑厚"
        preview_text: 预览文本（用于生成预览音频）
        preferred_name: 音色名称标识

    Returns:
        voice_config: 包含模型类型和描述信息的 dict，后续合成时使用
    """
    logger.info(f"声音设计: {preferred_name} — {voice_description[:50]}...")

    try:
        model = _load_tts_model(settings.tts_voice_design_model)

        # 生成预览音频，验证描述有效
        wav, sr = model.generate_voice_design(
            text=preview_text,
            language="Chinese",
            instruct=voice_description,
        )
        wav = _unwrap_wav(wav)

        # 保存预览音频
        preview_dir = settings.output_path / "voice_previews"
        preview_dir.mkdir(parents=True, exist_ok=True)
        preview_path = preview_dir / f"{preferred_name}_preview.wav"
        sf.write(str(preview_path), wav, sr)

        voice_config = {
            "type": "voice_design",
            "description": voice_description,
            "preview_path": str(preview_path),
        }
        logger.info(f"声音设计成功: {preferred_name}")
        return voice_config

    except Exception as e:
        raise TTSError(f"声音设计失败: {type(e).__name__}", detail=str(e))


# ============================================================
# 语音克隆：从参考音频克隆音色
# ============================================================

async def clone_voice(
    audio_path: str,
    ref_text: str = "",
    preferred_name: str = "cloned_voice",
) -> dict:
    """
    通过 Base 模型从参考音频克隆音色（3 秒即可）。

    Args:
        audio_path: 参考音频文件路径
        ref_text: 参考音频对应的文本（有则效果更好）
        preferred_name: 音色名称标识

    Returns:
        voice_config: 包含克隆 prompt 信息的 dict
    """
    audio_file = Path(audio_path)
    if not audio_file.exists():
        raise TTSError(f"参考音频文件不存在: {audio_path}")

    logger.info(f"语音克隆: {preferred_name} ← {audio_path}")

    try:
        model = _load_tts_model(settings.tts_base_model)

        # 创建可复用的克隆 prompt
        clone_prompt = model.create_voice_clone_prompt(
            ref_audio=str(audio_file),
            ref_text=ref_text,
            x_vector_only_mode=False,
        )

        voice_config = {
            "type": "voice_clone",
            "clone_prompt": clone_prompt,
            "ref_audio": str(audio_file),
        }
        logger.info(f"语音克隆成功: {preferred_name}")
        return voice_config

    except Exception as e:
        raise TTSError(f"语音克隆失败: {type(e).__name__}", detail=str(e))


# ============================================================
# 语音合成：文本 → 音频
# ============================================================

# Qwen3-TTS CustomVoice 内置 9 种预设音色
PRESET_SPEAKERS = [
    "Cherry", "Serena", "Ethan", "Chengfeng",
    "Vivian", "Bella", "Ryan", "Dylan", "Uncle_Fu",
]


async def synthesize_speech(
    text: str,
    voice: dict | str,
    output_path: str,
    instructions: Optional[str] = None,
    language: str = "Chinese",
) -> str:
    """
    将文本合成为语音音频文件。

    Args:
        text: 要合成的文本
        voice: 音色配置（dict 或预设音色名称字符串）
        output_path: 输出音频文件路径
        instructions: TTS 指令控制（情感、语速、风格等）
        language: 语言 Chinese/English/Auto

    Returns:
        output_path: 生成的音频文件路径
    """
    # 文本长度限制检查
    if len(text) > settings.tts_max_chars:
        raise TTSError(
            f"文本超长: {len(text)} > {settings.tts_max_chars}",
            detail="请切分文本后分别合成",
        )

    # 确保输出目录存在
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    try:
        wav = None
        sr = settings.tts_sample_rate

        if isinstance(voice, dict):
            voice_type = voice.get("type", "")

            if voice_type == "voice_design":
                # 使用 VoiceDesign 模型
                model = _load_tts_model(settings.tts_voice_design_model)
                wav, sr = model.generate_voice_design(
                    text=text,
                    language=language,
                    instruct=voice["description"],
                )
                wav = _unwrap_wav(wav)

            elif voice_type == "voice_clone":
                # 使用 Base 模型克隆音色
                model = _load_tts_model(settings.tts_base_model)
                wav, sr = model.generate_voice_clone(
                    text=text,
                    language=language,
                    voice_clone_prompt=voice["clone_prompt"],
                )
                wav = _unwrap_wav(wav)

            elif voice_type == "custom_voice":
                # 使用 CustomVoice 模型 + 预设音色 + 指令控制
                model = _load_tts_model(settings.tts_custom_voice_model)
                kwargs = {
                    "text": text,
                    "language": language,
                    "speaker": voice.get("speaker", "Cherry"),
                }
                if instructions:
                    kwargs["instruct"] = instructions
                wav, sr = model.generate_custom_voice(**kwargs)
                wav = _unwrap_wav(wav)

            else:
                raise TTSError(f"未知的 voice 类型: {voice_type}")

        elif isinstance(voice, str):
            # 字符串 → 预设音色名称，使用 CustomVoice 模型
            model = _load_tts_model(settings.tts_custom_voice_model)
            kwargs = {
                "text": text,
                "language": language,
                "speaker": voice if voice in PRESET_SPEAKERS else "Cherry",
            }
            if instructions:
                kwargs["instruct"] = instructions
            wav, sr = model.generate_custom_voice(**kwargs)
            wav = _unwrap_wav(wav)

        else:
            raise TTSError(f"无效的 voice 参数类型: {type(voice)}")

        if wav is None:
            raise TTSError("TTS 合成返回空音频")

        # 写入音频文件
        sf.write(output_path, wav, sr)
        logger.debug(f"TTS 合成完成: {output_path} ({len(wav) / sr:.1f}s)")
        return output_path

    except TTSError:
        raise
    except Exception as e:
        raise TTSError(f"TTS 合成异常: {type(e).__name__}", detail=str(e))


# ============================================================
# 文本切分工具
# ============================================================

def _split_text_for_tts(text: str, max_chars: int) -> list[str]:
    """
    将文本按标点符号边界切分为不超过 max_chars 的片段。
    """
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    current = ""

    # 按句子切分
    sentences = re.split(r"([。！？.!?\n])", text)

    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else "")
        if len(current) + len(sentence) > max_chars and current:
            chunks.append(current)
            current = ""
        current += sentence

    # 处理最后可能的奇数元素
    if len(sentences) % 2 == 1:
        last = sentences[-1]
        if len(current) + len(last) > max_chars and current:
            chunks.append(current)
            current = ""
        current += last

    if current:
        chunks.append(current)

    return chunks


async def synthesize_segment(
    text: str,
    voice: dict | str,
    output_dir: str,
    segment_id: int,
    instructions: Optional[str] = None,
) -> list[str]:
    """
    合成一个段落的语音，自动处理长文本切分。

    Args:
        text: 段落文本
        voice: 音色配置（dict 或预设音色名称）
        output_dir: 输出目录
        segment_id: 段落序号
        instructions: TTS 指令

    Returns:
        生成的音频文件路径列表
    """
    chunks = _split_text_for_tts(text, settings.tts_max_chars)
    audio_files: list[str] = []

    for i, chunk in enumerate(chunks):
        if not chunk.strip():
            continue
        suffix = f"_{i}" if len(chunks) > 1 else ""
        out_path = os.path.join(output_dir, f"seg_{segment_id:05d}{suffix}.wav")
        await synthesize_speech(
            text=chunk,
            voice=voice,
            output_path=out_path,
            instructions=instructions,
        )
        audio_files.append(out_path)

    return audio_files