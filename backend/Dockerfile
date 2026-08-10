# 后端运行时镜像
FROM python:3.13-slim

WORKDIR /app

# uv 安装
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 先装依赖（利用层缓存）
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# 复制源码
COPY src ./src
COPY main.py ./main.py

RUN mkdir -p data logs

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]
