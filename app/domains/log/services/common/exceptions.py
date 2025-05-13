"""
WHAT: 로그 서비스 공통 예외/추적 유틸리티
WHY: 커스텀 예외, trace_id 기반 추적, Sentry/OTEL 연동 등 일원화
EXAMPLE: raise AppException(400, "잘못된 요청", detail)
"""
from typing import Any, Optional
from .sentry import capture_exception
from app.common.logging import logger
from opentelemetry import trace

class AppException(Exception):
    """
    WHAT: 커스텀 예외 클래스 (trace_id 포함)
    WHY: 예외 발생 시 trace_id 자동 추적, 장애 원인 분석 용이
    EXAMPLE: raise AppException(400, "잘못된 요청", detail)
    """
    def __init__(self, code: int, message: str, detail: Any = None, trace_id: Optional[str] = None):
        self.code = code
        self.message = message
        self.detail = detail
        self.trace_id = trace_id or self._get_trace_id()
        super().__init__(message)

    def _get_trace_id(self):
        ctx = trace.get_current_span()
        if ctx and ctx.get_span_context().is_valid:
            return hex(ctx.get_span_context().trace_id)
        return None

def capture_and_log(exc: Exception, span, logger_instance=None, extra: dict = None):
    """
    WHAT: 예외 발생 시 trace_id와 함께 로깅 및 Sentry 전송
    WHY: 장애 상황 통합 추적, 로그/트레이스/대시보드 연동
    EXAMPLE: capture_and_log(Exception("error"), span, logger)
    """
    try:
        trace_id = None
        try:
            ctx = trace.get_current_span()
            if ctx and ctx.get_span_context().is_valid:
                trace_id = hex(ctx.get_span_context().trace_id)
        except Exception as e:
            if logger_instance:
                logger_instance.warning(f"[capture_and_log] trace context unavailable: {e}")
        log_extra = extra or {}
        if trace_id:
            log_extra["trace_id"] = trace_id
        if logger_instance:
            try:
                logger_instance.error(f"Exception captured: {exc} | {log_extra}")
            except Exception as e:
                print(f"[capture_and_log] logger error: {e}")
        try:
            capture_exception(exc)
        except Exception as e:
            if logger_instance:
                logger_instance.warning(f"[capture_and_log] sentry capture failed: {e}")
        if span is not None:
            if RECORD_EXCEPTION_EVENT:
                span.record_exception(exc)
            if SET_SPAN_ERROR_STATUS:
                span.set_status(StatusCode.ERROR)
    except Exception as e:
        print(f"[capture_and_log] fallback error: {e}")
