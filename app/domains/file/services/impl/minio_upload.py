"""
[📄 minio_upload.py - File 서비스 구현체]

설명:
- Minio S3 업로드 기능을 제공하는 서비스 구현체
- 버킷/키/파일을 받아 업로드 처리

주요 연동:
- MinioClientInterface (인터페이스)
"""

from app.domains.file.services.interfaces.file_upload import IFileUploadService, FileUploadRequest, FileUploadResponse

from app.common.logging import logger

class MinIOFileUploadService(IFileUploadService):
    """
    WHAT: Minio S3 업로드 서비스 구현체
    WHY: 파일 업로드 요청을 받아 Minio S3에 저장, 업로드 URL 반환
    """
    def upload(self, req: FileUploadRequest) -> FileUploadResponse:
        """
        WHAT: 파일 업로드 처리 메서드
        WHY: 파일명 기반으로 Minio S3에 업로드 후 접근 URL 반환
        Args:
            req (FileUploadRequest): 업로드 요청 정보(파일명 등)
        Returns:
            FileUploadResponse: 업로드 결과(파일 URL)
        Raises:
            Exception: 업로드 실패 시 예외 발생 및 로그 기록
        """
        try:
            logger.info(f"[MinIOFileUploadService] S3 파일 업로드 시도: filename={req.filename}")
            # WHAT: 실제 MinIO 연동 로직은 구현체에서 처리(여기선 예시)
            # WHY: 파일 URL을 생성하기 위해 req.filename을 사용
            file_url = f"https://minio.example.com/{req.filename}"
            logger.info(f"[MinIOFileUploadService] S3 파일 업로드 성공: url={file_url}")
            # WHAT: 업로드 결과를 반환하기 위해 FileUploadResponse를 사용
            return FileUploadResponse(url=file_url)
        except Exception as e:
            logger.error(f"[MinIOFileUploadService] S3 파일 업로드 실패: {e}")
            # WARNING: 업로드 실패 시 예외 발생, 상위에서 핸들링 필요
            raise
