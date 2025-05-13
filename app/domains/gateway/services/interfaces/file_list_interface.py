from abc import ABC, abstractmethod
from typing import List
from app.domains.file.schemas.listing import S3FileEntry

class FileListInterface(ABC):
    """
    WHAT: 파일 목록 조회 추상 인터페이스
    WHY: 다양한 파일 서비스 구현에 대한 일관된 목록 조회 추상화 제공
    """
    @abstractmethod
    async def list_files(self, prefix: str) -> List[S3FileEntry]:
        """
        WHAT: 파일 목록 조회 추상 메서드
        WHY: 실제 파일 조회 로직은 구현체에서 구현, 인터페이스로 일관성 유지
        Args:
            prefix (str): S3 prefix 경로
        Returns:
            List[S3FileEntry]: 파일 목록
        """
        pass

    @staticmethod
    def get_service():
        """
        WHAT: 파일 목록 서비스 구현체 반환 정적 메서드
        WHY: 인터페이스 기반 DI/테스트 용이성 확보
        Returns:
            FileListService: 구현체 인스턴스
        """
        from app.domains.gateway.services.impl.file_list_service import FileListService
        return FileListService()
