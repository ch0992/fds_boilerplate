from abc import ABC, abstractmethod
from app.services.data.schemas.table import TableRecordRequest, KafkaProduceResult

class TableProducerInterface(ABC):
    """
    WHAT: 테이블 단위 Kafka 발행 추상 인터페이스
    WHY: 테이블별 데이터 변경을 Kafka로 발행하는 일관된 추상화 제공
    """
    @abstractmethod
    async def produce_record(self, table: str, body: TableRecordRequest) -> KafkaProduceResult:
        """
        WHAT: 테이블 단위 Kafka 발행 추상 메서드
        WHY: 실제 발행 로직은 구현체에서 구현, 인터페이스로 일관성 유지
        Args:
            table (str): 테이블명
            body (TableRecordRequest): 발행할 데이터
        Returns:
            KafkaProduceResult: 발행 결과
        """
        pass
