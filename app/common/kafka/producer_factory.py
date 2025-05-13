# Kafka Producer Factory (싱글턴)
from app.common.kafka.producer import KafkaMessageProducer
from typing import Optional

_kafka_producer_instance: Optional[KafkaMessageProducer] = None

def get_kafka_producer() -> KafkaMessageProducer:
    global _kafka_producer_instance
    if _kafka_producer_instance is None:
        _kafka_producer_instance = KafkaMessageProducer()
    return _kafka_producer_instance
