"""
[📄 zip_presigned_service.py - File 서비스 구현체]

설명:
- S3 zip presigned URL 생성을 위한 서비스 구현체
- 버킷/키/만료시간을 받아 zip presigned URL 반환

주요 연동:
- ZipPresignedInterface (인터페이스)
"""

from app.domains.file.services.interfaces.zip_presigned_interface import ZipPresignedInterface
from app.domains.file.schemas.zips import ZipPresignedResponse

from app.common.logging import logger

class ZipPresignedService(ZipPresignedInterface):
    """
    Zip Presigned URL 생성 서비스 구현체
    WHAT: 여러 S3 객체를 zip으로 묶어 presigned URL(임시 접근 링크) 생성
    WHY: 다수 파일을 한 번에 다운로드할 때 사용
    """
    async def create_zip_presigned_url(self, sql: str) -> ZipPresignedResponse:
        try:
            logger.info(f"[ZipPresignedService] zip presigned URL 생성 시도: sql={sql}")
            # WHAT: 실제 SQL 처리 및 presigned URL 생성 로직은 시뮬레이션
            # WHY: 실제 구현에서는 SQL을 기반으로 파일 리스트를 조회해야 함
            # 예시: sql 조건에 맞는 파일 리스트를 조회했다고 가정
            files = [
                "file1.txt",
                "file2.txt",
                "file3.txt"
            ]
            # WARNING: 환경 분기 (예시: 개발/운영 환경에 따라 presigned URL 생성 로직이 다를 수 있음)
            # TODO: 환경 분기 로직 추가 필요
            presigned_url = f"https://dummy-presigned-url.com/download/zip?sql={sql}"
            logger.info(f"[ZipPresignedService] zip presigned URL 생성 성공: url={presigned_url}")
            # WHAT: 반환 구조 (presigned URL, 파일 리스트, SQL)
            # WHY: 클라이언트에서 presigned URL을 사용하여 파일 다운로드 및 SQL을 기반으로 파일 리스트를 처리할 수 있도록 지원
            return ZipPresignedResponse(
                presigned_url=presigned_url,
                files=files,
                sql=sql
            )
        except Exception as e:
            # WARNING: zip presigned URL 생성 실패 시 장애 로그 기록 및 예외 전파
            logger.error(f"[ZipPresignedService] zip presigned URL 생성 실패: {e}")
            raise
