from abc import ABC, abstractmethod
from app.services.data.schemas.curs import CursorQueryRequest, CursorQueryResult

class CursorQueryInterface(ABC):
    """
    WHAT: 커서 기반 쿼리 추상 인터페이스
    WHY: 대용량 데이터 페이징 처리를 위한 일관된 커서 쿼리 추상화
    """
    @abstractmethod
    async def cursor_query(self, request: CursorQueryRequest) -> CursorQueryResult:
        """
        WHAT: 커서 기반 쿼리 추상 메서드
        WHY: 실제 쿼리 로직은 구현체에서 구현, 인터페이스로 일관성 유지
        Args:
            request (CursorQueryRequest): 쿼리 요청 정보
        Returns:
            CursorQueryResult: 쿼리 결과
        """
        pass
