from pydantic import BaseModel
from typing import Optional

class FileMetadataRequest(BaseModel):
    """
    WHAT: 파일 메타데이터 요청/응답 스키마
    WHY: 파일 업로드, 조회, Kafka 발행 등에서 파일의 상세 정보를 구조화
    """
    file_id: str  # WHAT: 파일 고유 식별자
    filename: str  # WHAT: 원본 파일명
    owner: str  # WHAT: 파일 소유자(업로더)
    size: int  # WHAT: 파일 크기(byte)
    user: Optional[str] = None  # WHAT: 추가 사용자 정보(옵션)

    class Config:
        schema_extra = {
            "example": {
                "file_id": "abc123",  # WHAT: 예시 파일 ID
                "filename": "test.png",  # WHAT: 예시 파일명
                "owner": "user1",  # WHAT: 예시 소유자
                "size": 12345  # WHAT: 예시 크기
            }
        }

class KafkaProduceResult(BaseModel):
    """
    WHAT: Kafka 메타데이터 발행 결과 스키마
    WHY: Kafka 메시지 발행 성공/실패, 토픽명, 결과 메시지 등 구조화
    """
    topic: str  # WHAT: 발행 대상 Kafka 토픽명
    message: str  # WHAT: 발행 결과 메시지(상태/오류 등)
    status: str  # WHAT: 발행 상태("success"/"error" 등)
