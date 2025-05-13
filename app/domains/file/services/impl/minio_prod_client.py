"""
[📄 minio_prod_client.py - File 서비스 구현체]

설명:
- Minio S3 연동을 위한 실제 운영 클라이언트 구현체
- S3 버킷/키/파일을 받아 실제 업로드 수행

주요 연동:
- MinioClientInterface (인터페이스)
"""

from app.domains.file.services.interfaces.minio_client_interface import MinioClientInterface
# 실제 환경에서는 minio/minio-py, boto3 등으로 구현

from app.common.logging import logger

class MinioProdClient(MinioClientInterface):
    """
    Minio S3 연동 운영 클라이언트 구현체
    """
    def upload_file(self, bucket: str, key: str, data: bytes) -> str:
        try:
            logger.info(f"[MinioProdClient] S3 파일 업로드 시도: bucket={bucket}, key={key}, data_size={len(data)}")
            # 실제 S3 업로드 로직은 운영 환경에서만 사용
            # TODO: 실제 MinIO/S3 연동 코드 구현
            raise NotImplementedError("Production MinioClient not implemented.")
        except Exception as e:
            logger.error(f"[MinioProdClient] S3 파일 업로드 실패: {e}")
            raise

    def multipart_upload(self, file_path: str, bucket: str, key: str, chunk_size: int = 20*1024*1024) -> str:
        try:
            logger.info(f"[MinioProdClient] S3 멀티파트 업로드 시도: file_path={file_path}, bucket={bucket}, key={key}, chunk_size={chunk_size}")
            # 실제 S3 멀티파트 업로드 로직은 운영 환경에서만 사용
            # TODO: 실제 MinIO/S3 멀티파트 업로드 구현
            raise NotImplementedError("Production MinioClient multipart not implemented.")
        except Exception as e:
            logger.error(f"[MinioProdClient] S3 멀티파트 업로드 실패: {e}")
            raise

