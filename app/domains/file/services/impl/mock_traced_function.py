import asyncio
from app.domains.log.services.common.tracing import get_tracer

tracer = get_tracer("file")

async def mock_traced_function():
    """
    WHAT: 트레이싱 테스트용 mock 비동기 함수
    WHY: OpenTelemetry tracer 연동/동작 검증, 실제 서비스 로직 없이 트레이스만 확인
    Returns:
        str: 트레이싱 성공 메시지
    """
    with tracer.start_as_current_span("file::mock_process"):
        await asyncio.sleep(1)
        return "trace OK"
