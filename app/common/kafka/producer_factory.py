# Kafka Producer Factory (싱글턴)
# WHAT: KafkaMessageProducer 인스턴스 싱글턴 패턴으로 제공
# WHY: 매번 새로 생성하지 않고, 프로세스 내에서 재사용해 리소스 절약 및 연결 효율화
from app.common.kafka.producer import KafkaMessageProducer
from typing import Optional

_kafka_producer_instance: Optional[KafkaMessageProducer] = None  # WHAT: 싱글턴 인스턴스 저장용 글로벌 변수

def get_kafka_producer() -> KafkaMessageProducer:
    """
    WHAT: KafkaMessageProducer 싱글턴 반환 함수
    WHY: 여러 모듈/서비스에서 동일 인스턴스 재사용, 불필요한 중복 연결 방지
    Returns:
        KafkaMessageProducer: 싱글턴 인스턴스
    """
    global _kafka_producer_instance
    if _kafka_producer_instance is None:
        _kafka_producer_instance = KafkaMessageProducer()
    return _kafka_producer_instance
