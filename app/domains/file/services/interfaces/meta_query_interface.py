"""
[📄 meta_query_interface.py - File 서비스 인터페이스]

설명:
- 파일 메타데이터 조회를 위한 추상 인터페이스 정의
- 실제 구현체(impl/meta_query_service.py)에서 상속 및 구현

주요 연동:
- FileMeta 스키마
- MetaQueryService (구현체)
"""

from abc import ABC, abstractmethod
from typing import List
from app.domains.file.schemas.metadata import FileMetadataRequest

class MetaQueryInterface(ABC):
    """
    WHAT: 파일 메타데이터 조회 인터페이스 (추상)
    WHY: 파일의 상세 메타데이터(사이즈, 생성일, 커스텀 속성 등)를 표준화된 방식으로 조회하기 위한 인터페이스
    실제 구현체는 MetaQueryService에서 상속 및 구현
    """
    @abstractmethod
    async def get_file_meta(self, file_key: str) -> FileMetadataRequest:
        """
        WHAT: 파일 메타데이터를 조회 (구현체에서 구현)
        WHY: 파일별 상세 정보(메타데이터) 접근을 추상화하여 다양한 저장소/구현체에 대응
        Args:
            file_key (str): 메타데이터를 조회할 파일의 고유 키
        Returns:
            FileMetadataRequest: 파일 메타데이터(스키마)
        """
        pass

    @staticmethod
    def get_service():
        """
        WHAT: 실제 구현체 인스턴스 반환 (factory)
        WHY: DI/테스트/확장성 확보를 위한 추상화
        Returns:
            MetaQueryService: 실제 구현체 인스턴스
        """
        from app.domains.file.services.impl.meta_query_service import MetaQueryService
        return MetaQueryService()
