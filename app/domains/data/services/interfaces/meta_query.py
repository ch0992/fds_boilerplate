"""
IMetaQueryService: 메타 데이터 질의 기능 추상화 인터페이스 정의
"""
from typing import Protocol
from pydantic import BaseModel

class MetaQueryRequest(BaseModel):
    """
    WHAT: 메타 데이터 질의 요청 모델
    WHY: 다양한 질의 조건을 캡슐화하여 서비스 계층에 전달
    """
    query: str

class MetaQueryResponse(BaseModel):
    """
    WHAT: 메타 데이터 질의 응답 모델
    WHY: 질의 결과를 dict 형태로 일관성 있게 반환
    """
    result: dict

class IMetaQueryService(Protocol):
    """
    WHAT: 메타 데이터 질의 추상 서비스 인터페이스
    WHY: 다양한 데이터 소스에 대한 질의 기능 일관성 확보
    """
    def query(self, req: MetaQueryRequest) -> MetaQueryResponse:
        """
        WHAT: 메타 데이터 질의 추상 메서드
        WHY: 실제 질의 로직은 구현체에서 구현
        Args:
            req (MetaQueryRequest): 질의 요청
        Returns:
            MetaQueryResponse: 질의 결과
        """
        ...
