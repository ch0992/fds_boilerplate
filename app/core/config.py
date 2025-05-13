"""
app/core/config.py
공통 환경설정 관리 (예: 환경 변수 로딩)
"""

import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        # boilerplate 환경에서는 .env 경로를 boilerplate/.env로 강제 지정
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        env_path = os.path.join(base_dir, '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path, override=True)
        self.ENV = os.getenv("ENV") or "development_k8s"
        # 서비스 엔드포인트 분기 (LOCAL/REMOTE URL 분리)
        if self.ENV == "development":
            self.GATEWAY_SERVICE_URL = os.getenv("GATEWAY_SERVICE_LOCAL_URL", "http://localhost:8000")
            self.FILE_SERVICE_URL = os.getenv("FILE_SERVICE_LOCAL_URL", "http://localhost:8001")
            self.DATA_SERVICE_URL = os.getenv("DATA_SERVICE_LOCAL_URL", "http://localhost:8002")
            self.LOG_SERVICE_URL = os.getenv("LOG_SERVICE_LOCAL_URL", "http://localhost:8003")
        else:  # development_k8s, stage, production 등 쿠버네티스 기본
            self.GATEWAY_SERVICE_URL = os.getenv("GATEWAY_SERVICE_REMOTE_URL", "http://gateway:8000")
            self.FILE_SERVICE_URL = os.getenv("FILE_SERVICE_REMOTE_URL", "http://file:8001")
            self.DATA_SERVICE_URL = os.getenv("DATA_SERVICE_REMOTE_URL", "http://data:8002")
            self.LOG_SERVICE_URL = os.getenv("LOG_SERVICE_REMOTE_URL", "http://log:8003")

        # Sentry DSN, OTEL Exporter, Kafka, MinIO 등 환경별 분기 예시
        if self.ENV == "production":
            self.SENTRY_DSN = os.getenv("SENTRY_DSN", "")
            self.OTEL_EXPORTER = os.getenv("OTEL_EXPORTER", "jaeger")
            self.KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka-prod:9092")
            self.MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio-prod:9000")
        elif self.ENV == "stage":
            self.SENTRY_DSN = os.getenv("SENTRY_DSN", "")
            self.OTEL_EXPORTER = os.getenv("OTEL_EXPORTER", "jaeger")
            self.KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka-stage:9092")
            self.MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio-stage:9000")
        else:  # development, development_k8s 등
            self.SENTRY_DSN = os.getenv("SENTRY_DSN", "")
            self.OTEL_EXPORTER = os.getenv("OTEL_EXPORTER", "stdout")
            self.KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
            self.MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")

        # 로그 레벨, 인증 모드 등 추가 환경변수
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.AUTH_MODE = os.getenv("AUTH_MODE", "local")
        self.USE_SENTRY = os.getenv("USE_SENTRY", "false").lower() == "true"

settings = Settings()
