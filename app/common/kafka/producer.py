# KafkaMessageProducer (통합 구현체)
import json
import os
from faststream.kafka import KafkaBroker
from app.common.config import settings
from app.common.kafka.dummy_producer import DummyKafkaProducer

class KafkaMessageProducer:
    """
    Kafka Message Producer (환경별 Dummy 자동 분기)
    """
    def __init__(self):
        if getattr(settings, "ENV", "development") in ["production", "stage"]:
            self._broker = KafkaBroker(os.getenv("KAFKA_BROKER_URL", "localhost:9092"))
            self._dummy = False
        else:
            self._dummy = True
            self._dummy_producer = DummyKafkaProducer()

    async def produce(self, topic: str, value: dict):
        if self._dummy:
            return await self._dummy_producer.produce(topic, value)
        try:
            message = json.dumps(value, ensure_ascii=False)
            await self._broker.connect()
            await self._broker.publish(message, topic)
            await self._broker.disconnect()
            return {"topic": topic, "status": "queued"}
        except Exception as e:
            # 필요시 예외 로깅 추가
            raise
