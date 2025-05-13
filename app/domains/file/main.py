"""
실행 가능한 FastAPI 앱 엔트리포인트
Swagger UI(/docs) 활성화, 환경설정 연동 예시 포함
"""
import os
from app.common.logging import logger, setup_logging
from dotenv import load_dotenv
from fastapi import FastAPI
from app.domains.log.services.common.tracing import init_tracer
from app.domains.log.services.common.sentry import init_sentry
from app.domains.log.services.common.middleware import install_exception_handlers, TraceLoggingMiddleware
from app.common.remote_log_handler import RemoteLogHandler
from app.domains.file.api.routes import router as file_router
from app.common.config import settings
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# loguru 기반 로깅 설정
setup_logging()

# .env 파일 로드 (상위 루트 기준)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(ENV_PATH, override=True)

app = FastAPI(title="File Service", description="File upload/download microservice")

from fastapi import Request
from app.common.utils.log_sender import send_log_async

@app.middleware("http")
async def log_http_requests(request: Request, call_next):
    response = await call_next(request)
    try:
        host = request.url.hostname or "unknown"
        domain = request.url.path.strip("/").split("/")[0] if request.url.path.strip("/") else "unknown"
        send_log_async(
            message=f"{request.method} {request.url.path} {response.status_code}",
            level="INFO",
            extra={"domain": domain, "host": host}
        )
    except Exception:
        pass
    return response


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

# OpenTelemetry FastAPI 미들웨어 적용
FastAPIInstrumentor().instrument_app(app)

# 예외 핸들러 및 미들웨어 등록
install_exception_handlers(app)
app.add_middleware(TraceLoggingMiddleware)

# 라우터 등록
app.include_router(file_router)
