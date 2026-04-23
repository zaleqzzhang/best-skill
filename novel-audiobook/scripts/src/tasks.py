"""
Celery 异步任务定义
大文件有声书生成通过后台任务队列处理。
"""
import asyncio
import json
from pathlib import Path

from celery import Celery
from loguru import logger

from src.config import settings

# ============================================================
# Celery 应用初始化
# ============================================================

celery_app = Celery(
    "novel-audiobook",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Shanghai",
    enable_utc=False,
    task_track_started=True,
    task_time_limit=3600,       # 单任务最大 1 小时
    task_soft_time_limit=3000,  # 软超时 50 分钟
    worker_prefetch_multiplier=1,
    worker_concurrency=2,
)


# ============================================================
# 任务状态存储（基于 Redis）
# ============================================================

def _update_task_status(task_id: str, status: dict):
    """更新任务状态到 Redis。"""
    import redis
    r = redis.from_url(settings.redis_url)
    r.set(f"task:{task_id}:status", json.dumps(status, ensure_ascii=False), ex=86400)


def get_task_status(task_id: str) -> dict | None:
    """从 Redis 获取任务状态。"""
    import redis
    r = redis.from_url(settings.redis_url)
    data = r.get(f"task:{task_id}:status")
    if data:
        return json.loads(data)
    return None


# ============================================================
# Celery 任务
# ============================================================

@celery_app.task(bind=True, name="generate_audiobook_task")
def generate_audiobook_task(
    self,
    task_id: str,
    filename: str,
    file_content_b64: str,
    voice_config: dict | None = None,
):
    """
    异步有声书生成任务。

    Args:
        task_id: 任务唯一 ID
        filename: 原始文件名
        file_content_b64: Base64 编码的文件内容
        voice_config: 可选的音色配置
    """
    import base64

    logger.info(f"任务开始: {task_id}, 文件: {filename}")

    def progress_callback(step: str, progress: float, message: str):
        status = {
            "task_id": task_id,
            "status": "processing",
            "current_step": step,
            "progress": round(progress, 4),
            "message": message,
            "error": None,
        }
        _update_task_status(task_id, status)

    try:
        # 初始化状态
        _update_task_status(task_id, {
            "task_id": task_id,
            "status": "processing",
            "current_step": "init",
            "progress": 0.0,
            "message": "任务已启动",
            "error": None,
        })

        # 解码文件内容
        file_content = base64.b64decode(file_content_b64)

        # 运行异步流水线
        from src.pipeline import generate_audiobook

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                generate_audiobook(
                    filename=filename,
                    file_content=file_content,
                    task_id=task_id,
                    progress_cb=progress_callback,
                    voice_config=voice_config,
                )
            )
        finally:
            loop.close()

        # 更新完成状态
        final_status = {
            "task_id": task_id,
            "status": "completed",
            "current_step": "done",
            "progress": 1.0,
            "message": "有声书生成完成",
            "error": None,
            "result": result,
        }
        _update_task_status(task_id, final_status)

        logger.info(f"任务完成: {task_id}")
        return result

    except Exception as e:
        logger.error(f"任务失败: {task_id} — {e}")
        error_status = {
            "task_id": task_id,
            "status": "failed",
            "current_step": "error",
            "progress": 0.0,
            "message": f"任务失败: {str(e)}",
            "error": str(e),
        }
        _update_task_status(task_id, error_status)
        raise
