"""
/ping 응답 모델
"""
from pydantic import BaseModel

class PingResponse(BaseModel):
    """
    WHAT: /ping 응답 모델
    WHY: 헬스체크 및 연결 상태 확인 목적의 단순 메시지 구조
    """
    message: str
