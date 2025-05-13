"""
[📄 minio_memory_client.py - File 서비스 구현체]

설명:
- Minio S3 연동을 위한 메모리 기반 클라이언트 구현체 (테스트/로컬용)
- 실제 S3 업로드 대신 메모리 내 객체 저장

주요 연동:
- MinioClientInterface (인터페이스)
"""

from app.domains.file.services.interfaces.minio_client_interface import MinioClientInterface
from typing import Any

class MinioMemoryClient(MinioClientInterface):
    """
    Minio S3 연동 메모리 클라이언트 구현체 (테스트/로컬)

    WHAT: 실제 S3 대신 메모리 내에 객체를 저장하는 mock 클라이언트
    WHY: 테스트/로컬/개발 환경에서 외부 S3 연동 없이 파일 업로드 로직 검증 가능
    """

    def __init__(self):
        """
        MinioMemoryClient 초기화

        WHAT: 메모리 내 객체 저장소 생성
        WHY: 실제 S3가 없으므로 dict로 버킷/파일 관리
        """
        # WHY: 메모리 내 객체 저장을 위한 초기화
        self.storage = {}

    def upload_file(self, bucket: str, key: str, data: bytes) -> str:
        """
        메모리 내에 파일 업로드 (테스트/로컬)

        Args:
            bucket (str): S3 버킷명
            key (str): S3 오브젝트 키
            data (bytes): 업로드할 파일 데이터

        Returns:
            str: 업로드 결과 (메모리 내 객체 경로)
        """
        # WHAT: 버킷이 없으면 새로 생성 (dict)
        # WHY: S3와 동일하게 버킷 단위로 객체 관리
        if bucket not in self.storage:
            self.storage[bucket] = {}
        # WHAT: 파일 데이터를 메모리 내 객체로 저장
        self.storage[bucket][key] = data
        # WHAT: 업로드 결과를 S3 URI와 유사하게 반환
        return f"memory://{bucket}/{key}"

    def multipart_upload(self, file_path: str, bucket: str, key: str, chunk_size: int = 20*1024*1024) -> str:
        # WHAT: 멀티파트 업로드 시뮬레이션 (실제 S3 multipart upload와 인터페이스만 동일)
        # WHY: 대용량 파일 업로드 테스트용 (실제 S3 연동 X)
        # WARNING: 파일을 chunk 단위로 메모리에 저장하므로 대용량 파일은 메모리 사용량 주의
        return self.upload_file(bucket, key, open(file_path, 'rb').read())
        with open(file_path, "rb") as f:
            data = f.read()
        return self.upload_file(bucket, key, data)
