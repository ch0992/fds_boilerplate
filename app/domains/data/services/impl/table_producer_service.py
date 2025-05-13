from app.services.data.services.interfaces.table_producer_interface import TableProducerInterface
from app.services.data.schemas.table import TableRecordRequest, KafkaProduceResult

from app.common.kafka.producer_factory import get_kafka_producer
from app.common.logging import logger
import json

class TableProducerService(TableProducerInterface):
    """
    WHAT: 테이블 단위 Kafka 발행 서비스 구현체
    WHY: 테이블별 데이터 변경을 Kafka 토픽으로 발행하여 실시간 파이프라인 구현
    """
    async def produce_record(self, table: str, body: TableRecordRequest) -> KafkaProduceResult:
        """
        WHAT: Kafka에 테이블 단위 데이터 발행
        WHY: 테이블명 기반 토픽으로 데이터 메시지 발행
        Args:
            table (str): 테이블명
            body (TableRecordRequest): 발행할 데이터
        Returns:
            KafkaProduceResult: 발행 결과
        """
        try:
            # WHY: Kafka 발행 요청 로그
            logger.info(f"[Data] Kafka produce 요청: table={table}, body={body}")
            # WHAT: Kafka 프로듀서 인스턴스 생성
            producer = get_kafka_producer()
            # WHAT: Kafka에 데이터 발행
            result = await producer.produce(table, body.dict())
            # WHY: Kafka 발행 성공 로그
            logger.info(f"[Data] Kafka produce 성공: result={result}")
            # WHAT: 발행 결과 반환
            return KafkaProduceResult(topic=table, message=json.dumps(body.dict()), status=result["status"])
        except Exception as e:
            # WARNING: Kafka 발행 실패 시 장애 로그 및 에러 메시지 반환
            logger.error(f"[Data] Kafka produce 실패: {e}")
            # WHAT: 에러 메시지 반환
            return KafkaProduceResult(topic=table, message=str(e), status="error")
