FROM python:3.12-slim
WORKDIR /app

# requirements.txt만 먼저 복사 (캐시 활용)
COPY /requirements.txt /app/requirements.txt
# uv 설치
RUN pip install --no-cache-dir uv
RUN apt-get update && apt-get install -y curl \
    && uv pip install --system -r /app/requirements.txt

# 전체 소스 복사 (이 아래가 자주 invalidate됨)
COPY app /app/app
ENV PYTHONPATH=/app/app

CMD ["sh", "-c", "uvicorn app.domains.file.main:app --host 0.0.0.0 --port 8001 --reload > /app/file.log 2>&1"]
