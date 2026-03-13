# === 构建阶段 ===
FROM python:3.11-slim AS builder

WORKDIR /app

# 安装达梦驱动依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# === 运行阶段 ===
FROM python:3.11-slim

WORKDIR /app

# 从构建阶段复制已安装的包
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 复制项目文件
COPY config.py .
COPY main.py .
COPY core/ core/
COPY middleware/ middleware/
COPY models/ models/
COPY routers/ routers/
COPY services/ services/

# 创建日志目录
RUN mkdir -p logs

# 环境变量（可被 .env 或 docker-compose 覆盖）
ENV DEBUG=False
ENV LOG_LEVEL=INFO
ENV DM_HOST=192.168.1.99
ENV DM_PORT=5236

EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import requests; r=requests.get('http://localhost:8080/health', timeout=5); exit(0 if r.status_code==200 else 1)" || exit 1

# 启动 — 使用 uvicorn 生产模式（关闭 reload，4 worker）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
