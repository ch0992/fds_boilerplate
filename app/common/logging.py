"""
app/common/logging.py
공통 로깅 설정 (core에서 이동)
"""

import logging
from functools import wraps
from opentelemetry import trace
from opentelemetry.trace import Tracer
import sentry_sdk
import sys
import traceback


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logging.info("Logging is configured.")

def get_tracer(service_name: str = "default") -> Tracer:
    try:
        return trace.get_tracer(service_name)
    except Exception:
        logging.warning("OpenTelemetry tracer unavailable, returning dummy tracer.")
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
            logging.error(f"Exception in {func.__name__}: {e}")
            traceback.print_exc()
            sentry_sdk.capture_exception(e)
            raise
    return wrapper
