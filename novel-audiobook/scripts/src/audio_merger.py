"""
音频合并模块
将多个音频片段按顺序合并为完整的 MP3 有声书。
依赖 pydub + FFmpeg。
"""
import os
from pathlib import Path
from typing import Optional

from loguru import logger
from pydub import AudioSegment


class AudioMergeError(Exception):
    """音频合并异常。"""

    def __init__(self, message: str, detail: Optional[str] = None):
        self.message = message
        self.detail = detail
        super().__init__(message)


def _load_audio(path: str) -> AudioSegment:
    """加载单个音频文件，自动识别格式。"""
    ext = Path(path).suffix.lower().lstrip(".")
    if ext in ("wav", "mp3", "ogg", "flac", "m4a"):
        return AudioSegment.from_file(path, format=ext)
    return AudioSegment.from_file(path)


def merge_audio_files(
    audio_paths: list[str],
    output_path: str,
    silence_between_ms: int = 500,
    silence_between_chapters_ms: int = 2000,
    chapter_boundaries: Optional[list[int]] = None,
    export_format: str = "mp3",
    bitrate: str = "192k",
) -> str:
    """
    将多个音频文件合并为单个 MP3。

    Args:
        audio_paths: 音频文件路径列表（按顺序）
        output_path: 输出 MP3 文件路径
        silence_between_ms: 段落间静音时长（毫秒）
        silence_between_chapters_ms: 章节间静音时长（毫秒）
        chapter_boundaries: 章节边界的段落索引列表
        export_format: 输出格式（mp3/wav/ogg）
        bitrate: MP3 比特率

    Returns:
        output_path: 输出文件路径
    """
    if not audio_paths:
        raise AudioMergeError("没有可合并的音频文件")

    chapter_set = set(chapter_boundaries or [])
    silence_gap = AudioSegment.silent(duration=silence_between_ms)
    chapter_gap = AudioSegment.silent(duration=silence_between_chapters_ms)

    logger.info(f"开始合并 {len(audio_paths)} 个音频文件...")

    combined = AudioSegment.empty()
    skipped = 0

    for i, path in enumerate(audio_paths):
        if not os.path.exists(path):
            logger.warning(f"音频文件不存在，跳过: {path}")
            skipped += 1
            continue

        try:
            segment = _load_audio(path)
            combined += segment

            # 添加间隔静音
            if i < len(audio_paths) - 1:
                if i + 1 in chapter_set:
                    combined += chapter_gap
                else:
                    combined += silence_gap

        except Exception as e:
            logger.error(f"加载音频失败: {path} — {e}")
            skipped += 1
            continue

    if len(combined) == 0:
        raise AudioMergeError("合并后音频为空，所有片段均加载失败")

    # 确保输出目录存在
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # 导出
    logger.info(
        f"导出 {export_format.upper()}: "
        f"时长 {len(combined) / 1000:.1f}s, "
        f"比特率 {bitrate}, "
        f"跳过 {skipped} 个文件"
    )
    combined.export(output_path, format=export_format, bitrate=bitrate)

    file_size = os.path.getsize(output_path)
    logger.info(
        f"合并完成: {output_path} "
        f"({file_size / 1024 / 1024:.1f} MB, "
        f"{len(combined) / 1000 / 60:.1f} 分钟)"
    )
    return output_path
