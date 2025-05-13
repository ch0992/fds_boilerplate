"""
실행 가능한 FastAPI 앱 엔트리포인트
Swagger UI(/docs) 활성화, 환경설정 연동 예시 포함
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.common.logging import logger, setup_logging
from app.common.utils.log_sender import send_log_async
from fastapi import Request

# loguru 기반 로깅 설정
setup_logging()

from app.domains.log.services.common.tracing import init_tracer, patch_global_logging_format
from app.domains.log.services.common.sentry import init_sentry
from app.domains.log.services.common.middleware import install_exception_handlers, TraceLoggingMiddleware
from app.domains.gateway.api.routes import router as gateway_router
from app.common.config import settings

# 글로벌 로그 포맷터 패치(최상단에 적용)
patch_global_logging_format()

# .env 파일 로드 (상위 루트 기준)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(ENV_PATH, override=True)

tags_metadata = [
    {"name": "Auth", "description": "인증 관련 API"},
    {"name": "Data", "description": "데이터 관련 API"},
    {"name": "File", "description": "파일 관련 API"},
    {"name": "Log", "description": "로그 관련 API"},
    {"name": "Health", "description": "헬스 체크 API"}
]

app = FastAPI(
    title="Gateway Service",
    description="Auth/JWT gateway microservice",
    openapi_tags=tags_metadata,
    openapi_url="/gateway/openapi.json",
    docs_url="/gateway/docs",
    redoc_url="/gateway/redoc"
)

# 모든 HTTP 요청마다 log 전송 미들웨어 추가


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
    init_tracer("stdout")

# 예외 핸들러 및 미들웨어 등록
install_exception_handlers(app)
app.add_middleware(TraceLoggingMiddleware)

# 라우터 등록
app.include_router(gateway_router, prefix="/gateway")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    SENTRY_ENABLED = os.environ.get("SENTRY", "false").lower() == "true"
    SENTRY_DSN = os.environ.get("SENTRY_DSN") or None
    if SENTRY_ENABLED and SENTRY_DSN:
        try:
            import sentry_sdk
            sentry_sdk.capture_exception(exc)
        except Exception as sentry_exc:
            logger.error(f"[Sentry] 연동 실패: {sentry_exc}")
    logger.error(f"[Global Exception Handler] {request.method} {request.url} - {exc}")
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "예상치 못한 오류가 발생했습니다.", "error": str(exc)},
    )

from app.common.logging import logger

@app.on_event("startup")
async def on_startup():
    mode = os.environ.get("AUTH_MODE")
    local_token = os.environ.get("AUTH_LOCAL_TOKEN")
    remote_url = os.environ.get("AUTH_SERVER_URL")
    logger.info("Gateway service started.")
    logger.info(f"[gateway] AUTH_MODE={mode}")
    if mode == "local" and local_token:
        logger.info(f"[gateway] AUTH_LOCAL_TOKEN={local_token}")
    elif mode == "remote":
        logger.info(f"[gateway] AUTH_SERVER_URL={remote_url}")

# 진단용: 실제 등록된 모든 라우트 경로와 메서드 출력
for route in app.routes:
    print(route.path, route.methods)

from fastapi.responses import JSONResponse
from fastapi.requests import Request
