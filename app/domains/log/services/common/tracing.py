"""
WHAT: 로그 서비스 트레이싱/분산추적 유틸리티
WHY: OTEL, Jaeger, Tempo 등 다양한 트레이싱 백엔드 연동 및 초기화
EXAMPLE: init_tracer("jaeger"), get_tracer("log-service")
"""
import os
import logging
from app.common.logging import logger
from typing import Optional
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
try:
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
except ImportError:
    JaegerExporter = None
# Jaeger, Zipkin 등 확장 가능

_otel_exporter = os.getenv("OTEL_EXPORTER", "stdout")
_service_name = os.getenv("SERVICE_NAME", "filedepot-service")

_tracer_provider = None

def init_tracer(exporter_type: Optional[str] = None):
    """
    WHAT: 서비스별 트레이싱(OTEL 등) 초기화
    WHY: Jaeger/Tempo/콘솔 등 다양한 백엔드 지원, trace_id/분산추적 활성화
    EXAMPLE: init_tracer("jaeger")
    """
    global _tracer_provider
    try:
        exporter_type = (exporter_type or _otel_exporter or "stdout").lower()
        if exporter_type == "none":
            # 익스포터 등록하지 않음 (테스트 환경 등)
            return
        _tracer_provider = TracerProvider(resource=Resource.create({"service.name": _service_name}))
        exporter = None
        if exporter_type in ("console", "stdout"):
            exporter = ConsoleSpanExporter()
        elif exporter_type == "jaeger":
            if not JaegerExporter:
                raise ImportError("opentelemetry-exporter-jaeger-thrift not installed")
            jaeger_host = os.getenv("JAEGER_HOST", "localhost")
            jaeger_port = int(os.getenv("JAEGER_PORT", 6831))
            exporter = JaegerExporter(agent_host_name=jaeger_host, agent_port=jaeger_port)
        elif exporter_type in ("tempo", "otlp"):
            otlp_endpoint = os.getenv("OTLP_ENDPOINT", "http://tempo:4318/v1/traces")
            exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        else:
            exporter = ConsoleSpanExporter()
        _tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(_tracer_provider)
    except Exception as e:
        logger.warning(f"[Tracing fallback] tracer init failed: {e}")
        _tracer_provider = None

# 서비스 main.py 등에서 init_tracer() 호출 필요
try:
    init_tracer()
except Exception as e:
    logger.warning(f"[Tracing fallback] global tracer init failed: {e}")

def get_tracer(service_name: Optional[str] = None):
    """
    WHAT: 현재 서비스용 tracer 객체 반환
    WHY: trace_id/ span_id 추적, 로그/미들웨어와 연동
    EXAMPLE: tracer = get_tracer("log-service")
    """
    try:
        tracer_provider = trace.get_tracer_provider()
        tracer = tracer_provider.get_tracer(service_name or _service_name)
        if tracer is None:
            raise RuntimeError("Tracer is None")
        return tracer
    except Exception as e:
        return trace.get_tracer("default")

# --- 글로벌 로그 포맷터 패치: 모든 로그에 trace_id/ span_id 자동 포함 ---
class TraceIdFormatter(logging.Formatter):
    def format(self, record):
        record.trace_id = self._get_trace_id()
        record.span_id = self._get_span_id()
        return super().format(record)
    def _get_trace_id(self):
        ctx = trace.get_current_span()
        if ctx and ctx.get_span_context().is_valid:
            return hex(ctx.get_span_context().trace_id)
        return "-"
    def _get_span_id(self):
        ctx = trace.get_current_span()
        if ctx and ctx.get_span_context().is_valid:
            return hex(ctx.get_span_context().span_id)
        return "-"
def patch_global_logging_format():
    handler = logging.StreamHandler()
    handler.setFormatter(TraceIdFormatter("%(asctime)s %(levelname)s %(message)s [trace_id=%(trace_id)s span_id=%(span_id)s]"))
    logging.root.handlers = [handler]
patch_global_logging_format()

def inject_trace_context(logger, span=None):
    # ... (생략)
    return logger
