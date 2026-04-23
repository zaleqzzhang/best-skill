"""
novel-audiobook FastAPI 应用主入口
"""
import base64
import json
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger

from src.config import settings
from src.file_parser import ALLOWED_EXTENSIONS, FileParseError
from src.tasks import celery_app, generate_audiobook_task, get_task_status


# ============================================================
# FastAPI 应用
# ============================================================

app = FastAPI(
    title="novel-audiobook",
    description="小说有声书全自动生成服务 — 角色划分 + TTS 音色克隆 + MP3 输出",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ============================================================
# 响应格式
# ============================================================

def success_response(data=None, message: str = "success"):
    return JSONResponse(content={
        "code": 0,
        "message": message,
        "data": data,
    })


def error_response(code: int, message: str, status_code: int = 400, detail=None):
    content = {"code": code, "message": message}
    if detail:
        content["detail"] = detail
    return JSONResponse(content=content, status_code=status_code)


# ============================================================
# 健康检查
# ============================================================

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "novel-audiobook"}


# ============================================================
# 上传小说，启动生成任务
# ============================================================

@app.post("/api/v1/audiobook/generate")
async def generate_audiobook(
    file: UploadFile = File(..., description="小说文件 (txt/pdf/epub/docx)"),
    voice_config: str = Form(default=None, description="可选的音色配置 JSON"),
):
    """上传小说文件，启动有声书生成任务。"""

    # 验证文件扩展名
    if not file.filename:
        return error_response(40001, "未提供文件名")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return error_response(
            40001,
            f"不支持的文件格式: {ext}",
            detail=f"支持的格式: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    # 读取文件内容
    content = await file.read()
    if len(content) > settings.max_upload_bytes:
        return error_response(
            40002,
            f"文件过大: {len(content) / 1024 / 1024:.1f} MB",
            detail=f"最大允许: {settings.max_upload_size_mb} MB",
        )

    if len(content) == 0:
        return error_response(40003, "文件为空")

    # 解析 voice_config
    vc = None
    if voice_config:
        try:
            vc = json.loads(voice_config)
        except json.JSONDecodeError:
            return error_response(40004, "voice_config JSON 格式无效")

    # 生成任务 ID
    task_id = str(uuid.uuid4())[:12]

    # 将文件内容 base64 编码传给 Celery
    content_b64 = base64.b64encode(content).decode("ascii")

    # 提交异步任务
    generate_audiobook_task.delay(
        task_id=task_id,
        filename=file.filename,
        file_content_b64=content_b64,
        voice_config=vc,
    )

    logger.info(f"任务已创建: {task_id}, 文件: {file.filename}, 大小: {len(content)} bytes")

    return success_response(
        data={"task_id": task_id, "status": "pending"},
        message="任务已创建，正在后台处理",
    )


# ============================================================
# 查询任务状态
# ============================================================

@app.get("/api/v1/audiobook/status/{task_id}")
async def get_audiobook_status(task_id: str):
    """查询有声书生成任务的状态和进度。"""
    status = get_task_status(task_id)
    if not status:
        return error_response(40404, "任务不存在", status_code=404)
    return success_response(data=status)


# ============================================================
# 获取角色划分结果
# ============================================================

@app.get("/api/v1/audiobook/roles/{task_id}")
async def get_role_analysis(task_id: str):
    """获取角色划分的 JSON 结果。"""
    analysis_path = settings.output_path / task_id / "role_analysis.json"
    if not analysis_path.exists():
        # 检查任务是否存在
        status = get_task_status(task_id)
        if not status:
            return error_response(40404, "任务不存在", status_code=404)
        if status.get("status") == "processing":
            return error_response(40405, "角色分析尚未完成，请稍后重试")
        return error_response(50001, "角色分析结果文件不存在")

    data = json.loads(analysis_path.read_text(encoding="utf-8"))
    return success_response(data=data)


# ============================================================
# 下载 MP3
# ============================================================

@app.get("/api/v1/audiobook/download/{task_id}")
async def download_audiobook(task_id: str):
    """下载生成的有声书 MP3 文件。"""
    task_dir = settings.output_path / task_id

    # 查找 MP3 文件
    mp3_files = list(task_dir.glob("*.mp3")) if task_dir.exists() else []
    if not mp3_files:
        status = get_task_status(task_id)
        if not status:
            return error_response(40404, "任务不存在", status_code=404)
        if status.get("status") == "processing":
            return error_response(40405, "有声书尚未生成完毕，请稍后下载")
        return error_response(50003, "MP3 文件不存在")

    mp3_path = mp3_files[0]
    return FileResponse(
        path=str(mp3_path),
        filename=mp3_path.name,
        media_type="audio/mpeg",
    )


# ============================================================
# 直接调用模式（不通过 Celery，小文件同步处理）
# ============================================================

@app.post("/api/v1/audiobook/generate-sync")
async def generate_audiobook_sync(
    file: UploadFile = File(..., description="小说文件"),
    voice_config: str = Form(default=None, description="可选的音色配置 JSON"),
):
    """
    同步模式生成有声书（适用于小文件测试）。
    注意：大文件请使用异步接口 /generate。
    """
    if not file.filename:
        return error_response(40001, "未提供文件名")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return error_response(40001, f"不支持的文件格式: {ext}")

    content = await file.read()
    if len(content) > 5 * 1024 * 1024:  # 同步模式限制 5MB
        return error_response(40002, "同步模式仅支持 5MB 以内文件，请使用异步接口")

    vc = None
    if voice_config:
        try:
            vc = json.loads(voice_config)
        except json.JSONDecodeError:
            return error_response(40004, "voice_config JSON 格式无效")

    task_id = str(uuid.uuid4())[:12]

    try:
        from src.pipeline import generate_audiobook as run_pipeline

        result = await run_pipeline(
            filename=file.filename,
            file_content=content,
            task_id=task_id,
            voice_config=vc,
        )
        return success_response(data=result, message="有声书生成完成")
    except FileParseError as e:
        return error_response(40003, e.message, detail=e.detail)
    except Exception as e:
        logger.error(f"同步生成失败: {e}")
        return error_response(50000, f"生成失败: {str(e)}", status_code=500)
