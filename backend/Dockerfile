FROM python:3.13-slim
WORKDIR /app
COPY pdm.lock pyproject.toml ./
RUN pip install pdm && pdm install --prod --no-editable
COPY src ./src
RUN mkdir -p data logs
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["pdm", "run", "uvicorn", "main:APP", "--host", "0.0.0.0", "--port", "8000"]
