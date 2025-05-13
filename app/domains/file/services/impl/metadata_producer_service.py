"""
[📄 metadata_producer_service.py - File 서비스 구현체]

설명:
- 파일 메타데이터를 Kafka로 발행하는 서비스 구현체
- Kafka 토픽명과 메타데이터를 받아 발행 처리

주요 연동:
- MetadataProducerInterface (인터페이스)
"""

from app.domains.file.services.interfaces.metadata_producer_interface import MetadataProducerInterface
from app.domains.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult
from app.common.kafka.producer_factory import get_kafka_producer
import json
from app.domains.log.services.common.exceptions import capture_and_log

# Initialize Kafka producer instance
kafka_producer = get_kafka_producer()

class MetadataProducerService(MetadataProducerInterface):
    """
    파일 메타데이터 Kafka 발행 서비스 구현체
    WHAT: 파일 메타데이터를 Kafka 토픽으로 발행하는 역할
    WHY: 비동기 처리 및 데이터 파이프라인 연동을 위해 사용
    """
    async def produce_metadata(self, topic: str, body: FileMetadataRequest) -> KafkaProduceResult:
        """
        Kafka로 파일 메타데이터 발행
        Args:
            topic (str): Kafka 토픽명
            body (FileMetadataRequest): 발행할 메타데이터
        Returns:
            KafkaProduceResult: 발행 결과
        """
        try:
            # WHAT: Kafka producer를 통해 메타데이터 발행
            # WHY: 파일 업로드 후 메타데이터를 메시지 큐로 전달하여 비동기 처리 가능
            await kafka_producer.produce(topic, body.dict())
            
            # WHAT: 발행한 메타데이터를 JSON 형식으로 변환
            # WHY: 메시지 내용을 로그 또는 응답에 활용하기 위함
            message = json.dumps(body.dict(), ensure_ascii=False)
            
            # WHAT: 발행 성공 시 결과 반환
            return KafkaProduceResult(
                topic=topic,
                message=message,
                status="queued"
            )
        except Exception as e:
            # WARNING: Kafka 발행 실패 시 예외 캡처 및 장애 추적
            # WHY: 장애 로깅을 통해 시스템 안정성 및 신뢰성 향상
            # WHAT: 예외 정보를 캡처하여 로그에 기록
            capture_and_log(e, None)
            return KafkaProduceResult(
                topic=topic,
                message=str(e),
                status="error"
            )
