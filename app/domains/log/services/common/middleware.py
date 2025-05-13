"""
WHAT: 로그 서비스 공통 미들웨어/예외처리 모듈
WHY: HTTP 트레이스, 예외 상황 로깅, 장애 추적, Sentry/OTEL 연동 등 일원화
EXAMPLE: app.add_middleware(TraceLoggingMiddleware)
"""
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from .exceptions import AppException, capture_and_log
from .tracing import get_tracer, inject_trace_context
from app.common.logging import logger
import traceback
import os

ENABLE_HTTP_EXCEPTION_TRACE = os.getenv("ENABLE_HTTP_EXCEPTION_TRACE", "true").lower() == "true"
CUSTOM_HTTP_EXCEPTION_HANDLER = os.getenv("CUSTOM_HTTP_EXCEPTION_HANDLER", "true").lower() == "true"
SENTRY_CAPTURE_HTTP_EXCEPTION = os.getenv("SENTRY_CAPTURE_HTTP_EXCEPTION", "false").lower() == "true"

class TraceLoggingMiddleware(BaseHTTPMiddleware):
    """
    WHAT: HTTP 요청/응답 트레이스 및 로그 미들웨어
    WHY: 모든 요청/응답, 트랜잭션, trace_id, span_id 자동 로깅
    EXAMPLE: app.add_middleware(TraceLoggingMiddleware)
    """
    async def dispatch(self, request: Request, call_next):
        tracer = get_tracer()
        with tracer.start_as_current_span(f"HTTP {request.method} {request.url.path}") as span:
            _logger = inject_trace_context(logger, span)
            trace_ctx = span.get_span_context()
            _logger.info(f"[access] {request.method} {request.url.path} | path={str(request.url)} | trace_id={format(trace_ctx.trace_id, 'x') if trace_ctx and trace_ctx.is_valid else '-'} | span_id={format(trace_ctx.span_id, 'x') if trace_ctx and trace_ctx.is_valid else '-'}")
            try:
                response = await call_next(request)
                return response
            except Exception as exc:
                capture_and_log(exc, logger, extra={"path": str(request.url)})
                raise

def install_exception_handlers(app: FastAPI):
    """
    WHAT: FastAPI 예외 핸들러 등록 함수
    WHY: HTTP/커스텀 예외를 통합 처리, 트레이스/Sentry 연동, 일관된 에러 응답 제공
    EXAMPLE: install_exception_handlers(app)
    """
    if CUSTOM_HTTP_EXCEPTION_HANDLER:
        @app.exception_handler(HTTPException)
        async def custom_http_exception_handler(request: Request, exc: HTTPException):
            # OpenTelemetry trace 연동
            if ENABLE_HTTP_EXCEPTION_TRACE:
                try:
                    from opentelemetry import trace
                    span = trace.get_current_span()
                    if span is not None:
                        span.set_attribute("http.status_code", exc.status_code)
                        span.set_attribute("http.exception.detail", str(exc.detail))
                        span.set_status(trace.status.Status(trace.status.StatusCode.ERROR, str(exc.detail)))
                except Exception:
                    pass
            # Sentry 연동
            if SENTRY_CAPTURE_HTTP_EXCEPTION:
                try:
                    import sentry_sdk
                    sentry_sdk.capture_exception(exc)
                except Exception:
                    pass
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(AppException)
    async def custom_app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.code,
            content={
                "error": exc.message,
                "detail": exc.detail,
                "trace_id": exc.trace_id
            }
        )