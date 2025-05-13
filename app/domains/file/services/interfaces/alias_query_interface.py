"""
[📄 alias_query_interface.py - File 서비스 인터페이스]

설명:
- 파일 alias 목록 조회를 위한 추상 인터페이스 정의
- 실제 구현체(impl/alias_query_service.py)에서 상속 및 구현

주요 연동:
- AliasEntry 스키마
- AliasQueryService (구현체)
"""

from abc import ABC, abstractmethod
from typing import List
from app.domains.file.schemas.aliases import AliasEntry

class AliasQueryInterface(ABC):
    """
    WHAT: 파일 alias 목록 조회 인터페이스 (추상)
    WHY: 사용자별 접근 가능한 파일 alias(경로/권한 등)를 표준화된 방식으로 조회하기 위한 인터페이스
    실제 구현체는 AliasQueryService에서 상속 및 구현
    """
    @abstractmethod
    async def get_aliases(self, user_id: str) -> List[AliasEntry]:
        """
        WHAT: 파일 alias 목록을 조회 (구현체에서 구현)
        WHY: 사용자별 권한/경로 분리를 위해 추상화
        Args:
            user_id (str): alias 목록을 조회할 사용자 ID
        Returns:
            List[AliasEntry]: alias 목록(스키마)
        """
        pass

    @staticmethod
    def get_service():
        """
        WHAT: 실제 구현체 인스턴스 반환 (factory)
        WHY: DI/테스트/확장성 확보를 위한 추상화
        Returns:
            AliasQueryService: 실제 구현체 인스턴스
        """
        from app.domains.file.services.impl.alias_query_service import AliasQueryService
        return AliasQueryService()
