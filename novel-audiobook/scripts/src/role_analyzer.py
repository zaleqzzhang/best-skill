"""
角色分析模块
调用 Qwen3-4B-Instruct-2507 对小说文本进行角色划分。
输出：旁白 + 各角色 + 每段演绎风格的结构化 JSON。
"""
import json
import re
from typing import Any, Optional

from loguru import logger
from openai import AsyncOpenAI

from src.config import settings


# ============================================================
# 数据结构定义
# ============================================================

from pydantic import BaseModel, Field


class RoleInfo(BaseModel):
    """角色信息。"""
    role_id: str = Field(description="角色唯一标识，如 narrator / role_1 / role_2")
    name: str = Field(description="角色名称，旁白为 '旁白'")
    gender: Optional[str] = Field(default=None, description="性别: 男/女/未知")
    age_range: Optional[str] = Field(default=None, description="年龄段: 少年/青年/中年/老年")
    personality: Optional[str] = Field(default=None, description="性格特征简述")
    voice_description: str = Field(description="音色描述，用于 TTS 声音设计")


class Segment(BaseModel):
    """文本段落。"""
    segment_id: int = Field(description="段落序号，从 0 开始")
    role_id: str = Field(description="说话角色 ID")
    text: str = Field(description="段落文本内容")
    style: str = Field(description="演绎风格指令，如 '低沉沙哑、缓慢而有力'")
    emotion: Optional[str] = Field(default=None, description="情绪: 平静/激动/悲伤/愤怒/喜悦等")


class RoleAnalysisResult(BaseModel):
    """角色分析完整结果。"""
    title: str = Field(default="未知", description="小说标题（尝试推断）")
    roles: list[RoleInfo] = Field(description="所有角色列表（含旁白）")
    segments: list[Segment] = Field(description="分段列表")
    total_chars: int = Field(description="总字符数")
    total_segments: int = Field(description="总段落数")


# ============================================================
# Prompt 模板
# ============================================================

SYSTEM_PROMPT = """你是一位专业的小说有声书导演。你的任务是分析小说文本，完成以下工作：

1. **角色识别**：识别出所有说话角色（包括旁白），为每个角色提供：
   - 唯一 ID（旁白固定为 "narrator"，其他角色为 "role_1", "role_2" ...）
   - 名称
   - 性别、年龄段
   - 性格特征
   - 音色描述（用自然语言描述，如"沉稳的中年男性，低沉浑厚，富有磁性"）

2. **段落划分**：将文本切分为段落，每段标注：
   - 说话角色 ID
   - 演绎风格（TTS 指令，如"语速较慢，声音低沉，带有忧伤的情绪"）
   - 情绪标签

重要规则：
- 旁白（叙述性文字）的 role_id 固定为 "narrator"
- 对话内容必须标注为对应角色
- 演绎风格要具体、可执行，适合 TTS 指令控制
- 每个段落的 text 必须完整，不能遗漏任何原文内容
- 所有原文必须出现在某个段落中，不可丢失

请严格按以下 JSON 格式输出，不要输出任何额外文字："""

OUTPUT_FORMAT = """{
  "title": "小说标题",
  "roles": [
    {
      "role_id": "narrator",
      "name": "旁白",
      "gender": null,
      "age_range": null,
      "personality": "客观冷静",
      "voice_description": "沉稳的中性播音员声音，语速适中，吐字清晰"
    },
    {
      "role_id": "role_1",
      "name": "角色名",
      "gender": "男",
      "age_range": "青年",
      "personality": "热情开朗",
      "voice_description": "年轻有活力的男性声音，语调明快"
    }
  ],
  "segments": [
    {
      "segment_id": 0,
      "role_id": "narrator",
      "text": "旁白文本...",
      "style": "语速平稳，声音舒缓，像在讲述一个悠远的故事",
      "emotion": "平静"
    },
    {
      "segment_id": 1,
      "role_id": "role_1",
      "text": "对话文本...",
      "style": "语速较快，声音洪亮，带着兴奋的语调",
      "emotion": "喜悦"
    }
  ]
}"""


# ============================================================
# 核心逻辑
# ============================================================

def _build_llm_client() -> AsyncOpenAI:
    """构建 OpenAI 兼容客户端，默认连接本地 vLLM 服务。"""
    return AsyncOpenAI(
        base_url=settings.llm_base_url,  # 默认 http://localhost:8100/v1
        api_key=settings.llm_api_key,    # 本地部署通常为 "EMPTY"
        timeout=settings.llm_timeout,
        max_retries=settings.llm_max_retries,
    )


def _split_text_chunks(text: str, max_chars: int = 12000) -> list[str]:
    """
    将长文本按自然段落边界切分为多个 chunk。
    每个 chunk 不超过 max_chars 字符，保证段落完整性。
    """
    paragraphs = re.split(r"\n\s*\n|\n", text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    chunks: list[str] = []
    current_chunk: list[str] = []
    current_len = 0

    for para in paragraphs:
        if current_len + len(para) + 1 > max_chars and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = []
            current_len = 0
        current_chunk.append(para)
        current_len += len(para) + 1

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


def _extract_json(text: str) -> dict[str, Any]:
    """从 LLM 输出中提取 JSON，容错处理 markdown 代码块。"""
    # 尝试直接解析
    text = text.strip()

    # 移除 markdown 代码块包裹
    json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if json_match:
        text = json_match.group(1).strip()

    # 尝试找到 JSON 对象边界
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start : end + 1]

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error(f"JSON 解析失败: {e}\n原始文本前500字: {text[:500]}")
        raise ValueError(f"LLM 输出的 JSON 格式无效: {e}")


async def analyze_roles_single_chunk(
    client: AsyncOpenAI,
    text_chunk: str,
    chunk_index: int,
    total_chunks: int,
) -> dict[str, Any]:
    """对单个文本块执行角色分析。"""
    user_content = f"""以下是小说的第 {chunk_index + 1}/{total_chunks} 部分，请分析角色和段落：

---小说文本开始---
{text_chunk}
---小说文本结束---

请按指定 JSON 格式输出分析结果。"""

    logger.info(
        f"LLM 角色分析: chunk {chunk_index + 1}/{total_chunks}, "
        f"文本长度 {len(text_chunk)} 字符"
    )

    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT + "\n\n" + OUTPUT_FORMAT},
            {"role": "user", "content": user_content},
        ],
        max_tokens=settings.llm_max_tokens,
        temperature=settings.llm_temperature,
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("LLM 返回空内容")

    return _extract_json(content)


def _merge_chunk_results(chunk_results: list[dict[str, Any]]) -> dict[str, Any]:
    """合并多个 chunk 的分析结果。"""
    if len(chunk_results) == 1:
        return chunk_results[0]

    # 合并角色列表（去重）
    all_roles: dict[str, dict] = {}
    all_segments: list[dict] = []
    title = "未知"
    segment_counter = 0

    for result in chunk_results:
        if result.get("title") and result["title"] != "未知":
            title = result["title"]

        for role in result.get("roles", []):
            rid = role.get("role_id", "")
            if rid and rid not in all_roles:
                all_roles[rid] = role

        for seg in result.get("segments", []):
            seg["segment_id"] = segment_counter
            all_segments.append(seg)
            segment_counter += 1

    return {
        "title": title,
        "roles": list(all_roles.values()),
        "segments": all_segments,
    }


async def analyze_roles(text: str) -> RoleAnalysisResult:
    """
    对小说文本执行完整的角色分析。
    长文本自动切分为多个 chunk 分别处理后合并。

    Args:
        text: 完整的小说纯文本

    Returns:
        RoleAnalysisResult: 结构化的角色分析结果
    """
    client = _build_llm_client()
    chunks = _split_text_chunks(text)
    logger.info(f"文本切分为 {len(chunks)} 个 chunk，总长 {len(text)} 字符")

    chunk_results: list[dict[str, Any]] = []
    for i, chunk in enumerate(chunks):
        result = await analyze_roles_single_chunk(client, chunk, i, len(chunks))
        chunk_results.append(result)

    merged = _merge_chunk_results(chunk_results)

    # 构建并验证结果
    analysis = RoleAnalysisResult(
        title=merged.get("title", "未知"),
        roles=[RoleInfo(**r) for r in merged.get("roles", [])],
        segments=[Segment(**s) for s in merged.get("segments", [])],
        total_chars=len(text),
        total_segments=len(merged.get("segments", [])),
    )

    logger.info(
        f"角色分析完成: {analysis.title}, "
        f"{len(analysis.roles)} 个角色, {analysis.total_segments} 个段落"
    )
    return analysis
