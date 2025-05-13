from pydantic import BaseModel, StrictStr
from typing import List, Optional, Any

class CursorQueryRequest(BaseModel):
    """
    WHAT: 커서 기반 쿼리 요청 모델
    WHY: 쿼리문과 커서 정보를 함께 전달하여 페이징 질의 지원
    """
    query: StrictStr
    cursor: Optional[str] = None

class CursorQueryResult(BaseModel):
    """
    WHAT: 커서 기반 쿼리 응답 모델
    WHY: 쿼리 결과와 다음 커서 정보를 함께 반환하여 연속 페이징 지원
    """
    records: List[Any]
    next_cursor: Optional[str] = None
