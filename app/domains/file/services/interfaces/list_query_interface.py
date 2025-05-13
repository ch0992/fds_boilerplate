"""
[📄 list_query_interface.py - File 서비스 인터페이스]

설명:
- S3 prefix 기반 파일 목록 조회를 위한 추상 인터페이스 정의
- 실제 구현체(impl/list_query_service.py)에서 상속 및 구현

주요 연동:
- S3FileEntry 스키마
- ListQueryService (구현체)
"""

from abc import ABC, abstractmethod
from typing import List
from app.domains.file.schemas.listing import S3FileEntry

class ListQueryInterface(ABC):
    """
    WHAT: S3 prefix 파일 목록 조회 인터페이스 (추상)
    WHY: S3(Minio)에서 특정 prefix 하위 파일 목록을 표준화된 방식으로 조회하기 위한 인터페이스
    실제 구현체는 ListQueryService에서 상속 및 구현
    """
    @abstractmethod
    async def list_files(self, prefix: str) -> List[S3FileEntry]:
        """
        WHAT: S3 prefix로 파일 목록을 조회 (구현체에서 구현)
        WHY: 대용량 저장소에서 특정 경로 하위 파일만 효율적으로 필터링하기 위한 추상화
        Args:
            prefix (str): 파일 목록 조회 대상 S3 prefix 경로
        Returns:
            List[S3FileEntry]: S3 파일 목록(스키마)
        """
        pass

    @staticmethod
    def get_service():
        """
        WHAT: 실제 구현체 인스턴스 반환 (factory)
        WHY: DI/테스트/확장성 확보를 위한 추상화
        Returns:
            ListQueryService: 실제 구현체 인스턴스
        """
        from app.domains.file.services.impl.list_query_service import ListQueryService
        return ListQueryService()
