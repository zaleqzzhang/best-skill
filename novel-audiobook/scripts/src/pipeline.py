"""
有声书生成流水线
编排完整的生成流程：文件解析 → 角色分析 → 声音设计 → TTS 合成 → MP3 合并
"""
import asyncio
import json
import os
import time
from pathlib import Path
from typing import Any, Callable, Optional

from loguru import logger

from src.config import settings
from src.file_parser import parse_file
from src.role_analyzer import analyze_roles, RoleAnalysisResult, RoleInfo
from src.tts_engine import design_voice, synthesize_segment
from src.audio_merger import merge_audio_files


# ============================================================
# 进度回调类型
# ============================================================

ProgressCallback = Optional[Callable[[str, float, str], None]]
"""进度回调: (step_name, progress_ratio, message)"""


# ============================================================
# 默认系统音色映射（当声音设计不可用时的 fallback）
# ============================================================

# Qwen3-TTS CustomVoice 模型内置的 9 种预设音色
# 当声音设计失败时，回退到这些预设音色（通过 CustomVoice 模型使用）
FALLBACK_VOICES: dict[str, dict] = {
    "narrator": {"type": "custom_voice", "speaker": "Cherry"},        # 旁白：沉稳女声
    "male_young": {"type": "custom_voice", "speaker": "Ethan"},       # 青年男性
    "male_middle": {"type": "custom_voice", "speaker": "Chengfeng"},  # 中年男性
    "male_old": {"type": "custom_voice", "speaker": "Uncle_Fu"},      # 老年男性
    "female_young": {"type": "custom_voice", "speaker": "Bella"},     # 青年女性
    "female_middle": {"type": "custom_voice", "speaker": "Vivian"},   # 中年女性
    "female_old": {"type": "custom_voice", "speaker": "Serena"},      # 老年女性
    "default": {"type": "custom_voice", "speaker": "Cherry"},         # 默认
}


def _select_fallback_voice(role: RoleInfo) -> dict:
    """根据角色信息选择 fallback 预设音色（返回 voice_config dict）。"""
    if role.role_id == "narrator":
        return FALLBACK_VOICES["narrator"]

    gender = (role.gender or "").lower()
    age = (role.age_range or "").lower()

    if "男" in gender or "male" in gender:
        if "老" in age or "old" in age:
            return FALLBACK_VOICES["male_old"]
        elif "中" in age or "middle" in age:
            return FALLBACK_VOICES["male_middle"]
        return FALLBACK_VOICES["male_young"]
    elif "女" in gender or "female" in gender:
        if "老" in age or "old" in age:
            return FALLBACK_VOICES["female_old"]
        elif "中" in age or "middle" in age:
            return FALLBACK_VOICES["female_middle"]
        return FALLBACK_VOICES["female_young"]

    return FALLBACK_VOICES["default"]


# ============================================================
# 流水线核心
# ============================================================

async def generate_audiobook(
    filename: str,
    file_content: bytes,
    task_id: str,
    progress_cb: ProgressCallback = None,
    voice_config: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """
    完整的有声书生成流水线。

    Args:
        filename: 原始文件名
        file_content: 文件二进制内容
        task_id: 任务 ID
        progress_cb: 进度回调
        voice_config: 可选的音色配置覆盖

    Returns:
        dict: {
            "task_id": str,
            "role_analysis": RoleAnalysisResult (dict),
            "mp3_path": str,
            "duration_seconds": float,
            "stats": {...}
        }
    """

    def _report(step: str, progress: float, msg: str):
        if progress_cb:
            progress_cb(step, progress, msg)
        logger.info(f"[{task_id}] [{step}] {progress:.0%} — {msg}")

    start_time = time.time()
    task_dir = settings.output_path / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    audio_dir = task_dir / "audio_segments"
    audio_dir.mkdir(exist_ok=True)

    # =====================================================
    # Phase 1: 文件解析
    # =====================================================
    _report("file_parse", 0.0, f"解析文件: {filename}")
    text = parse_file(filename, file_content)
    _report("file_parse", 1.0, f"解析完成: {len(text)} 字符")

    # =====================================================
    # Phase 2: LLM 角色分析
    # =====================================================
    _report("role_analysis", 0.0, "开始角色分析...")
    analysis = await analyze_roles(text)

    # 保存角色分析结果
    analysis_path = task_dir / "role_analysis.json"
    analysis_path.write_text(
        analysis.model_dump_json(indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    _report(
        "role_analysis",
        1.0,
        f"角色分析完成: {len(analysis.roles)} 个角色, {analysis.total_segments} 个段落",
    )

    # =====================================================
    # Phase 3: 声音设计（为每个角色生成专属音色）
    # =====================================================
    _report("voice_design", 0.0, "为角色设计音色...")
    voice_map: dict[str, dict | str] = {}

    for i, role in enumerate(analysis.roles):
        progress = (i + 1) / len(analysis.roles)
        try:
            voice = await design_voice(
                voice_description=role.voice_description,
                preview_text=f"你好，我是{role.name}。",
                preferred_name=f"{task_id}_{role.role_id}",
            )
            voice_map[role.role_id] = voice
            _report("voice_design", progress, f"音色就绪: {role.name}")
        except Exception as e:
            # 降级到系统音色
            fallback = _select_fallback_voice(role)
            voice_map[role.role_id] = fallback
            logger.warning(
                f"声音设计失败，降级到系统音色: {role.name} → {fallback} (原因: {e})"
            )
            _report("voice_design", progress, f"音色降级: {role.name} → {fallback}")

    # 保存音色映射
    voice_map_path = task_dir / "voice_map.json"
    voice_map_path.write_text(
        json.dumps(voice_map, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # =====================================================
    # Phase 4: TTS 语音合成
    # =====================================================
    _report("tts_synthesis", 0.0, f"开始语音合成: {analysis.total_segments} 个段落")
    all_audio_files: list[str] = []
    failed_segments = 0

    for i, seg in enumerate(analysis.segments):
        progress = (i + 1) / len(analysis.segments)
        voice = voice_map.get(seg.role_id, FALLBACK_VOICES["default"])

        try:
            audio_files = await synthesize_segment(
                text=seg.text,
                voice=voice,
                output_dir=str(audio_dir),
                segment_id=seg.segment_id,
                instructions=seg.style,
            )
            all_audio_files.extend(audio_files)
        except Exception as e:
            logger.error(f"段落 {seg.segment_id} TTS 失败: {e}")
            failed_segments += 1

        if (i + 1) % 10 == 0 or i == len(analysis.segments) - 1:
            _report(
                "tts_synthesis",
                progress,
                f"已合成 {i + 1}/{analysis.total_segments} 段, "
                f"失败 {failed_segments}",
            )

    if not all_audio_files:
        raise RuntimeError("所有段落 TTS 合成均失败，无法生成有声书")

    # =====================================================
    # Phase 5: 音频合并
    # =====================================================
    _report("audio_merge", 0.0, f"合并 {len(all_audio_files)} 个音频片段...")
    mp3_path = str(task_dir / f"{analysis.title or task_id}.mp3")

    merge_audio_files(
        audio_paths=all_audio_files,
        output_path=mp3_path,
        silence_between_ms=500,
    )
    _report("audio_merge", 1.0, "合并完成")

    # =====================================================
    # 统计
    # =====================================================
    elapsed = time.time() - start_time
    mp3_size = os.path.getsize(mp3_path)

    result = {
        "task_id": task_id,
        "title": analysis.title,
        "role_analysis": json.loads(analysis.model_dump_json()),
        "mp3_path": mp3_path,
        "mp3_size_mb": round(mp3_size / 1024 / 1024, 2),
        "stats": {
            "total_chars": analysis.total_chars,
            "total_segments": analysis.total_segments,
            "total_roles": len(analysis.roles),
            "failed_segments": failed_segments,
            "total_audio_files": len(all_audio_files),
            "elapsed_seconds": round(elapsed, 1),
        },
    }

    # 保存完整结果
    result_path = task_dir / "result.json"
    result_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    _report("done", 1.0, f"有声书生成完成! 耗时 {elapsed:.0f}s")
    return result
