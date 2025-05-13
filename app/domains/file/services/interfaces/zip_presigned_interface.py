"""
[📄 zip_presigned_interface.py - File 서비스 인터페이스]

설명:
- S3 zip presigned URL 생성을 위한 추상 인터페이스 정의
- 실제 구현체(impl/zip_presigned_service.py)에서 상속 및 구현

주요 연동:
- ZipPresignedService (구현체)
"""

from abc import ABC, abstractmethod
from app.domains.file.schemas.zips import ZipPresignedResponse

class ZipPresignedInterface(ABC):
    """
    WHAT: S3 zip presigned URL 생성 인터페이스 (추상)
    WHY: 여러 파일을 zip으로 묶어 presigned URL을 생성하는 서비스의 표준화된 인터페이스 제공
    실제 구현체는 ZipPresignedService에서 상속 및 구현
    """
    @abstractmethod
    async def create_zip_presigned_url(self, sql: str) -> ZipPresignedResponse:
        """
        WHAT: SQL 쿼리 기반으로 S3 zip presigned URL 생성 (구현체에서 구현)
        WHY: 다양한 파일 조건을 SQL로 지정해 presigned URL을 생성할 수 있도록 추상화
        Args:
            sql (str): presigned URL 생성을 위한 쿼리 조건(SQL)
        Returns:
            ZipPresignedResponse: presigned URL, 파일 리스트 등 zip 다운로드 응답 구조
        """
        pass
