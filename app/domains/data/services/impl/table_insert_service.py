from app.services.data.services.interfaces.table_insert_service_interface import TableInsertServiceInterface
from app.common.broker.interfaces.message_producer_interface import MessageProducerInterface
from opentelemetry import trace
from app.services.log.exceptions import capture_and_log
from typing import Dict, Any

tracer = trace.get_tracer("data")

class TableInsertService(TableInsertServiceInterface):
    """
    WHAT: 테이블 데이터 삽입 서비스 구현체
    WHY: Kafka 토픽에 데이터 삽입 요청을 발행하여 비동기 데이터 파이프라인 구축
    """
    def __init__(self, producer: MessageProducerInterface):
        """
        WHAT: 메시지 프로듀서 의존성 주입
        WHY: Kafka 등 외부 브로커 연동 유연성 확보
        """
        self._producer = producer

    async def insert(self, table: str, payload: Dict[str, Any]) -> Dict[str, str]:
        """
        WHAT: 테이블 데이터 삽입 요청 처리
        WHY: Kafka 토픽명 규칙에 따라 데이터 발행(iceberg-insert-<table>)
        Args:
            table (str): 테이블명
            payload (Dict[str, Any]): 삽입할 데이터
        Returns:
            Dict[str, str]: 발행 결과(status, topic)
        Raises:
            Exception: 장애 발생 시 예외 및 트레이스 기록
        """
        topic = f"iceberg-insert-{table}"
        try:
            with tracer.start_as_current_span("data.table_insert") as span:
                await self._producer.produce(topic, payload)
                span.set_attribute("kafka.topic", topic)
                return {"status": "queued", "topic": topic}
        except Exception as e:
            # WARNING: 장애 발생 시 트레이스 및 로그 기록
            capture_and_log(e, trace.get_current_span())
            raise
