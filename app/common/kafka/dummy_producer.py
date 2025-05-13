# DummyKafkaProducer (개발/테스트용)
class DummyKafkaProducer:
    """
    WHAT: Kafka Dummy Producer (테스트/개발용)
    WHY: 실제 Kafka 브로커에 메시지를 발행하지 않고, 로그만 출력하여 로컬 테스트/CI 환경에서 안전하게 사용
    """
    async def produce(self, topic: str, value: dict):
        """
        WHAT: Kafka 메시지 발행 시도(실제 전송 없음)
        WHY: 개발/테스트 환경에서 side effect 없이 인터페이스만 검증
        Args:
            topic (str): 발행 대상 Kafka 토픽명
            value (dict): 발행 메시지(딕셔너리)
        Returns:
            dict: dummy 발행 결과 (토픽명, 상태)
        """
        print(f"[DummyKafkaProducer] topic={topic}, value={value}")
        return {"topic": topic, "status": "dummy"}
