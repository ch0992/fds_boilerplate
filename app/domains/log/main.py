"""
WHAT: 로그 서비스 FastAPI 앱 엔트리포인트
WHY: 중앙집중식 로그 집계 및 API 제공, 서비스간 연동 및 모니터링을 위함
EXAMPLE: uvicorn app.domains.log.main:app --reload
"""
import os
from app.common.logging import setup_logging
from dotenv import load_dotenv
from fastapi import FastAPI

from app.common.config import settings
from app.domains.log.services.common.middleware import install_exception_handlers, TraceLoggingMiddleware
from app.domains.log.services.common.tracing import init_tracer
from app.domains.log.services.common.sentry import init_sentry

# loguru 기반 로깅 설정
setup_logging()

# .env 파일 로드 (상위 루트 기준)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(ENV_PATH, override=True)

# WHAT: 로그 서비스용 FastAPI 인스턴스 생성
# WHY: API 기반 로그 집계, 모니터링, 헬스체크 등 제공
app = FastAPI(title="Log Service", description="API log microservice")

# 로그 라우터 등록 (중앙 로그 집계 API)
# WHAT: 로그 수집/조회 라우터 등록
# WHY: 외부 서비스에서 로그 집계 및 API 접근 지원
from app.domains.log.api.routes.routes import router as log_router
app.include_router(log_router)

# OpenTelemetry 및 Sentry 초기화 (ENV에 따라 분기)
if settings.ENV in ["production", "stage"]:
    if settings.OTEL_EXPORTER:
        init_tracer(settings.OTEL_EXPORTER)
    if settings.USE_SENTRY and settings.SENTRY_DSN:
        init_sentry(dsn=settings.SENTRY_DSN, environment=settings.ENV)
else:
    # 개발/테스트 환경: OTEL, Sentry는 stdout 또는 mock
    init_tracer("stdout")
    # Sentry 미연동 또는 dummy

# WHAT: 예외 핸들러/트레이스 미들웨어 등록
# WHY: 장애 추적, 트랜잭션/트레이스 연동, 예외 상황 로깅 일원화
install_exception_handlers(app)
app.add_middleware(TraceLoggingMiddleware)
