"""
[📄 uploader_interface.py - File 서비스 인터페이스]

설명:
- 파일 업로드를 위한 추상 인터페이스 정의
- 실제 구현체(impl/uploader_service.py)에서 상속 및 구현

주요 연동:
- UploaderService (구현체)
"""

from abc import ABC, abstractmethod
from fastapi import UploadFile
from typing import Any

class UploaderInterface(ABC):
    """
    WHAT: 파일 업로드 추상 인터페이스
    WHY: 서비스 계층에서 파일 업로드 구현체(UploaderService)와의 결합도 최소화, 확장성 확보 목적
    실제 구현체는 UploaderService에서 상속 및 구현
    """
    @abstractmethod
    async def upload_file(self, file: UploadFile) -> Any:
        """
        WHAT: 파일 업로드 추상 메서드
        WHY: 실제 업로드 로직은 구현체에서 구현, 인터페이스로 일관성 유지
        Args:
            file (UploadFile): 업로드할 파일
        Returns:
            Any: 업로드 결과
        """
        pass

    @staticmethod
    def get_service():
        """
        WHAT: 실제 구현체 인스턴스 반환 (factory 메서드)
        WHY: 외부에서 인터페이스만 의존하도록 하여 구현체 교체 유연성 확보
        Returns:
            UploaderService: 실제 구현체 인스턴스
        """
        from app.domains.file.services.impl.uploader_service import UploaderService
        return UploaderService()
