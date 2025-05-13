"""
[📄 presigned_interface.py - File 서비스 인터페이스]

설명:
- S3 presigned URL 생성을 위한 추상 인터페이스 정의
- 실제 구현체(impl/presigned_service.py)에서 상속 및 구현

주요 연동:
- PresignedService (구현체)
"""

from typing import Protocol
from app.domains.file.schemas.presigned import PresignedURLResponse

class PresignedInterface(Protocol):
    """
    WHAT: S3 presigned URL 생성 인터페이스 (추상)
    WHY: S3 객체에 대한 임시 접근 URL을 표준화된 방식으로 생성하기 위한 인터페이스
    실제 구현체는 PresignedService에서 상속 및 구현
    """
    async def create_presigned_url(self, file_path: str) -> PresignedURLResponse:
        """
        WHAT: S3 presigned URL을 생성 (구현체에서 구현)
        WHY: 인증 없이 임시로 S3 객체에 접근할 수 있도록 presigned URL을 생성하는 로직 추상화
        Args:
            file_path (str): presigned URL을 생성할 S3 파일 경로
        Returns:
            PresignedURLResponse: presigned URL, 만료시간 등 응답 스키마
        """
        ...
