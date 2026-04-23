"""
novel-audiobook 配置模块
通过环境变量 + .env 文件管理所有配置，禁止硬编码。

本地部署模式：
  - LLM: 本地 vLLM 部署 Qwen3-4B-Instruct-2507 GGUF Q4_K_M 量化版，暴露 OpenAI 兼容接口
  - TTS: 本地 qwen-tts 包直接加载 Qwen3-TTS 系列开源模型
"""
import os
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """应用配置，所有值来自环境变量或 .env 文件。"""

    # === LLM 本地 vLLM 服务（GGUF Q4 量化） ===
    llm_base_url: str = Field(
        default="http://localhost:8100/v1",
        description="本地 vLLM 服务的 OpenAI 兼容接口地址",
    )
    llm_api_key: str = Field(
        default="EMPTY",
        description="vLLM API Key（本地部署通常为 EMPTY）",
    )
    llm_model: str = Field(
        default="Qwen3-4B-Instruct-2507",
        description="vLLM 中 served-model-name",
    )
    llm_gguf_repo: str = Field(
        default="bartowski/Qwen_Qwen3-4B-Instruct-2507-GGUF",
        description="GGUF 量化模型的 HuggingFace repo",
    )
    llm_gguf_file: str = Field(
        default="Qwen_Qwen3-4B-Instruct-2507-Q4_K_M.gguf",
        description="GGUF 量化模型文件名",
    )
    llm_tokenizer: str = Field(
        default="Qwen/Qwen3-4B-Instruct-2507",
        description="GGUF 模型对应的 tokenizer（推荐使用原始模型的 tokenizer）",
    )
    llm_max_tokens: int = Field(default=16384, description="LLM 最大输出 token 数")
    llm_temperature: float = Field(default=0.7, description="LLM 温度参数")
    llm_timeout: int = Field(default=300, description="LLM 请求超时秒数（本地推理可能较慢）")
    llm_max_retries: int = Field(default=3, description="LLM 请求最大重试次数")

    # === TTS 本地模型 ===
    tts_custom_voice_model: str = Field(
        default="Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
        description="TTS 自定义音色模型（支持指令控制 + 9种预设音色）",
    )
    tts_voice_design_model: str = Field(
        default="Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
        description="TTS 声音设计模型（根据自然语言描述生成音色）",
    )
    tts_base_model: str = Field(
        default="Qwen/Qwen3-TTS-12Hz-1.7B-Base",
        description="TTS 基础模型（3秒语音克隆）",
    )
    tts_device: str = Field(
        default="auto",
        description="TTS 模型运行设备: auto/cuda/cpu",
    )
    tts_torch_dtype: str = Field(
        default="bfloat16",
        description="TTS 模型精度: bfloat16/float16/float32",
    )
    tts_max_chars: int = Field(
        default=500,
        description="单次 TTS 调用最大字符数",
    )
    tts_sample_rate: int = Field(default=24000, description="音频采样率")

    # === Redis / Celery ===
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis 连接地址",
    )

    # === 文件处理 ===
    max_upload_size_mb: int = Field(default=50, description="最大上传文件 MB")
    output_dir: str = Field(default="./output", description="输出文件目录")

    # === 本地模型路径（可选，覆盖 HuggingFace 自动下载） ===
    llm_model_path: str = Field(
        default="",
        description="LLM GGUF 文件本地路径（留空则 vLLM 使用 repo_id:quant_type 自动下载）",
    )
    tts_model_local_dir: str = Field(
        default="",
        description="TTS 模型本地目录（留空则 qwen-tts 自动从 HF/ModelScope 下载）",
    )

    # === 服务 ===
    host: str = Field(default="0.0.0.0", description="服务监听地址")
    port: int = Field(default=8000, description="服务监听端口")
    debug: bool = Field(default=False, description="调试模式")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }

    @property
    def output_path(self) -> Path:
        """输出目录 Path 对象，自动创建。"""
        p = Path(self.output_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


settings = Settings()
