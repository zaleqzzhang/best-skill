# ====== 构建阶段 ======
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04 AS base

# 安装系统依赖（FFmpeg + Python）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    python3.12 \
    python3.12-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 设置 Python 别名
RUN ln -sf /usr/bin/python3.12 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.12 /usr/bin/python

WORKDIR /app

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝源码
COPY src/ ./src/
COPY .env.example ./.env.example

# 创建输出和模型目录
RUN mkdir -p /app/output /app/models

# 非 root 用户运行
RUN useradd --create-home appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# 启动 API 服务
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
