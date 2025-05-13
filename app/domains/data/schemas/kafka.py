from pydantic import BaseModel

class KafkaProduceResult(BaseModel):
    """
    WHAT: Kafka 발행 결과 응답 모델
    WHY: 토픽명, 상태, 메시지를 일관성 있게 반환
    """
    topic: str
    status: str
    message: str
