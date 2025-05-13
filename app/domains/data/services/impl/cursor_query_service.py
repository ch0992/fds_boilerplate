from app.services.data.services.interfaces.cursor_query_interface import CursorQueryInterface
from app.services.data.schemas.curs import CursorQueryRequest, CursorQueryResult

class CursorQueryService(CursorQueryInterface):
    """
    WHAT: 커서 기반 쿼리 서비스 구현체
    WHY: 대용량 데이터 페이징 처리를 위해 커서 기반 쿼리 방식 제공
    """
    async def cursor_query(self, request: CursorQueryRequest) -> CursorQueryResult:
        """
        WHAT: 커서 기반 쿼리 처리 메서드
        WHY: SQL 실행 및 커서 기반 페이징 처리(여기서는 더미 데이터)
        Args:
            request (CursorQueryRequest): 쿼리 요청 정보
        Returns:
            CursorQueryResult: 쿼리 결과 및 next_cursor
        """
        # WHAT: 실제 구현에서는 DB에서 SQL 실행 및 커서 기반 페이징 처리 필요
        # WHY: 더미 데이터 예시 반환
        records = [
            {"id": 101, "value": "foo"},
            {"id": 102, "value": "bar"}
        ]
        next_cursor = "eyJpZCI6MTAz..." if records else None
        # WHAT: 쿼리 결과 및 next_cursor 반환
        # WHY: 페이징 처리를 위한 next_cursor 제공
        return CursorQueryResult(records=records, next_cursor=next_cursor)
