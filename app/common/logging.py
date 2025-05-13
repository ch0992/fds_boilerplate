"""
app/common/logging.py
공통 로깅 설정 모듈
WHAT: loguru 기반의 통합 로깅, Sentry 연동, OpenTelemetry tracer fallback 제공
WHY: 서비스 전역에서 일관된 로그 관리, 장애 추적, 분산 트레이싱 지원 목적
"""

from loguru import logger
from functools import wraps
from opentelemetry import trace
from opentelemetry.trace import Tracer
import sentry_sdk
import sys
import traceback


def setup_logging():
    """
    WHAT: loguru 로깅 기본 설정 함수
    WHY: 콘솔+파일 로그 일괄 관리, 파일 회전/압축/보존 등 정책 일관화
    """
    logger.remove()
    logger.add(sys.stdout, level="INFO", colorize=True, backtrace=True, diagnose=True)
    logger.add("logs/app.log", rotation="10 MB", retention="7 days", compression="zip")
    logger.info("Loguru logging is configured.")


def get_tracer(service_name: str = "default") -> Tracer:
    """
    WHAT: OpenTelemetry tracer 반환 (분산 추적용)
    WHY: 서비스별 trace context 유지, 미지원 환경에서는 DummyTracer 반환
    """
    try:
        # WHAT: OpenTelemetry tracer 객체 반환
        # WHY: 서비스별 trace context 유지 및 분산 추적 지원
        return trace.get_tracer(service_name)
    except Exception:
        logger.warning("OpenTelemetry tracer unavailable, returning dummy tracer.")
        # WHAT: tracer 미지원 환경에서 fallback dummy tracer 제공
        # WHY: 분산 추적 미구현 환경에서도 코드 오류 없이 동작 보장
        class DummySpan:
            def __enter__(self): return self
            def __exit__(self, exc_type, exc_val, exc_tb): pass
            def set_attribute(self, *a, **kw): pass
            def record_exception(self, *a, **kw): pass
        class DummyTracer:
            def start_as_current_span(self, *a, **kw): return DummySpan()
        return DummyTracer()


def capture_and_log(func):
    """
    WHAT: 비동기 함수 예외 자동 로깅+Sentry 전송 데코레이터
    WHY: 장애 발생 시 로그/트레이스/Sentry를 모두 남겨 추적성 강화
    WARNING: 예외 발생 시 로그+Sentry+traceback 모두 기록, 서비스 장애 원인 파악 용이
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # WARNING: 예외 발생 시 loguru 로그+Sentry 전송, 장애 추적 목적
            logger.exception(f"Exception in {func.__name__}: {e}")
            sentry_sdk.capture_exception(e)
            raise
    return wrapper
