# KafkaMessageProducer (통합 구현체)
import json
import os
from faststream.kafka import KafkaBroker
from app.common.config import settings
from app.common.kafka.dummy_producer import DummyKafkaProducer

class KafkaMessageProducer:
    """
    WHAT: Kafka Message Producer (환경별 Dummy 자동 분기)
    WHY: 운영/스테이지 환경만 실제 Kafka 브로커 사용, 개발/테스트 환경은 side effect 방지 위해 DummyProducer 사용
    """
    def __init__(self):
        # WHAT: 운영/스테이지 환경에서는 실제 Kafka 브로커 연결
        # WHY: 실서비스 데이터만 실제 큐에 적재, 그 외 환경은 안전하게 더미 사용
        if getattr(settings, "ENV", "development") in ["production", "stage"]:
            self._broker = KafkaBroker(os.getenv("KAFKA_BROKER_URL", "localhost:9092"))
            self._dummy = False
        else:
            # WHAT: 개발/테스트 환경에서는 DummyKafkaProducer 사용
            # WHY: 실제 메시지 발행 side effect 없이 인터페이스만 검증
            self._dummy = True
            self._dummy_producer = DummyKafkaProducer()

    async def produce(self, topic: str, value: dict):
        """
        WHAT: Kafka 메시지 발행 (환경에 따라 실제/더미 분기)
        WHY: 운영/스테이지만 실제 큐, 그 외는 안전하게 로그만 남김
        Args:
            topic (str): 발행 대상 Kafka 토픽명
            value (dict): 발행 메시지(딕셔너리)
        Returns:
            dict: 발행 결과 (토픽명, 상태)
        """
        if self._dummy:
            return await self._dummy_producer.produce(topic, value)
        try:
            message = json.dumps(value, ensure_ascii=False)
            await self._broker.connect()
            await self._broker.publish(message, topic)
            await self._broker.disconnect()
            return {"topic": topic, "status": "queued"}
        except Exception as e:
            # WARNING: 실제 브로커 발행 실패 시 예외 발생 (필요시 로깅/모니터링)
            raise
