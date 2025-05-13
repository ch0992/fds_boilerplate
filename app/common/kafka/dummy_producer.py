# DummyKafkaProducer (개발/테스트용)
class DummyKafkaProducer:
    """
    Kafka Dummy Producer
    실제 Kafka로 메시지를 보내지 않고, 로그로만 출력
    """
    async def produce(self, topic: str, value: dict):
        print(f"[DummyKafkaProducer] topic={topic}, value={value}")
        return {"topic": topic, "status": "dummy"}
