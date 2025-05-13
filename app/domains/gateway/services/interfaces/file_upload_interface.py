from abc import ABC, abstractmethod
from fastapi import UploadFile
from typing import Any

class FileUploadInterface(ABC):
    """
    WHAT: 파일 업로드 추상 인터페이스
    WHY: 다양한 파일 업로드 구현에 대한 일관된 추상화 제공
    """
    @abstractmethod
    async def upload_file_and_metadata(self, topic: str, file: UploadFile, metadata: str) -> Any:
        """
        WHAT: 파일 업로드 및 메타데이터 저장 추상 메서드
        WHY: 실제 업로드/저장 로직은 구현체에서 구현, 인터페이스로 일관성 유지
        Args:
            topic (str): Kafka 토픽명 등 업로드 목적지
            file (UploadFile): 업로드할 파일
            metadata (str): 파일 메타데이터(JSON 등)
        Returns:
            Any: 업로드 결과
        """
        pass

    @staticmethod
    def get_service():
        """
        WHAT: 파일 업로드 서비스 구현체 반환 정적 메서드
        WHY: 인터페이스 기반 DI/테스트 용이성 확보
        Returns:
            FileUploadService: 구현체 인스턴스
        """
        from app.domains.gateway.services.impl.file_upload_service import FileUploadService
        return FileUploadService()
