"""
app/common/logging.py
공통 로깅 설정
"""

from loguru import logger
from functools import wraps
from opentelemetry import trace
from opentelemetry.trace import Tracer
import sentry_sdk
import sys
import traceback


def setup_logging():
    logger.remove()
    logger.add(sys.stdout, level="INFO", colorize=True, backtrace=True, diagnose=True)
    logger.add("logs/app.log", rotation="10 MB", retention="7 days", compression="zip")
    logger.info("Loguru logging is configured.")

def get_tracer(service_name: str = "default") -> Tracer:
    try:
        return trace.get_tracer(service_name)
    except Exception:
        logger.warning("OpenTelemetry tracer unavailable, returning dummy tracer.")
        class DummySpan:
            def __enter__(self): return self
            def __exit__(self, exc_type, exc_val, exc_tb): pass
            def set_attribute(self, *a, **kw): pass
            def record_exception(self, *a, **kw): pass
        class DummyTracer:
            def start_as_current_span(self, *a, **kw): return DummySpan()
        return DummyTracer()

def capture_and_log(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Exception in {func.__name__}: {e}")
            sentry_sdk.capture_exception(e)
            raise
    return wrapper
