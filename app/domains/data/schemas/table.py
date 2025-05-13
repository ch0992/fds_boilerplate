from pydantic import BaseModel

class TableRecordRequest(BaseModel):
    """
    WHAT: 테이블 레코드 요청 모델
    WHY: 실제 테이블 구조에 맞춰 주문/사용자/금액 등 필드 전달
    """
    # 예시 필드, 실제 Mart 테이블 구조에 따라 변경
    order_id: str
    user_id: str
    amount: int
    # 기타 컬럼은 Dict 등으로 확장 가능
    # extra: Dict[str, Any] = {}

class KafkaProduceResult(BaseModel):
    """
    WHAT: Kafka 발행 결과 응답 모델
    WHY: 토픽명, 메시지, 상태를 일관성 있게 반환
    """
    topic: str
    message: str
    status: str
