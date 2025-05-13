"""
[📄 presigned_service.py - File 서비스 구현체]

설명:
- S3 presigned URL 생성을 위한 서비스 구현체
- 버킷/키/만료시간을 받아 presigned URL 반환

주요 연동:
- PresignedInterface (인터페이스)
"""

from app.domains.file.services.interfaces.presigned_interface import PresignedInterface
from app.domains.file.schemas.presigned import PresignedURLResponse

from app.common.logging import logger

class PresignedService(PresignedInterface):
    """
    S3 presigned URL 생성 서비스 구현체
    WHAT: S3 객체에 대한 presigned URL(임시 접근 링크) 생성
    WHY: 인증 없이 제한 시간 동안 파일 다운로드/업로드 허용
    """
    async def create_presigned_url(self, file_path: str) -> PresignedURLResponse:
        try:
            logger.info(f"[PresignedService] presigned URL 생성 시도: file_path={file_path}")
            # WHAT: presigned URL 생성 로직은 구현체에서 처리
            # WHY: 실제로는 MinIO 또는 AWS S3 SDK 활용
            # 여기서는 더미 presigned URL 반환
            url = f"https://minio.local/bucket/{file_path}?presigned=1"
            logger.info(f"[PresignedService] presigned URL 생성 성공: url={url}")
            # WHAT: presigned URL 반환 구조
            # WHY: URL과 만료 시간 반환
            return PresignedURLResponse(url=url, expires_in=3600)
        except Exception as e:
            # WARNING: presigned URL 생성 실패 시 장애 로그 기록 및 예외 전파
            logger.error(f"[PresignedService] presigned URL 생성 실패: {e}")
            raise
