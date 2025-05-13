"""
[📄 list_query_service.py - File 서비스 구현체]

설명:
- S3(Minio)에서 prefix로 파일 목록을 조회하는 서비스 구현체
- 환경변수(MINIO_BUCKET 등) 체크 및 예외처리
- boto3를 통한 S3 연동, pagination 처리

주요 연동:
- boto3 S3 client
- 환경변수: MINIO_BUCKET, MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY
"""

from app.domains.file.services.interfaces.list_query_interface import ListQueryInterface
from app.domains.file.schemas.listing import S3FileEntry
from app.common.logging import get_tracer, capture_and_log
from app.common.config import settings
import os
import boto3
from typing import List

tracer = get_tracer("file::list_files")

class ListQueryService(ListQueryInterface):
    """
    WHAT: S3 prefix 파일 목록 조회 서비스 구현체
    WHY: S3(Minio)에서 지정된 경로(prefix)로 파일 목록을 효율적으로 조회
    """
    @capture_and_log(tracer)
    async def list_files(self, prefix: str) -> List[S3FileEntry]:
        """
        WHAT: S3에서 prefix로 파일 목록을 조회
        WHY: 대용량 파일 저장소에서 특정 경로 하위 파일만 효율적으로 필터링
        Args:
            prefix (str): S3 prefix 경로
        Returns:
            List[S3FileEntry]: S3 파일 목록
        Raises:
            SystemConfigException: 환경변수 누락 등 시스템 오류
            NotFoundException: 파일 없음
        """
        # WHAT: 환경변수 체크 및 S3 연결 오류 예외처리
        s3 = boto3.client(
            "s3",
            endpoint_url=os.getenv("MINIO_ENDPOINT"),
            aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
        )
        from app.common.utils.exceptions import SystemConfigException, NotFoundException
        bucket = os.getenv("MINIO_BUCKET")
        # WHY: MINIO_BUCKET 환경변수는 필수이므로 체크
        if not bucket:
            # WARNING: 필수 환경변수 누락 시 시스템 예외 발생
            raise SystemConfigException("MINIO_BUCKET 환경변수가 설정되어 있지 않습니다.")
        # WHAT: S3 pagination으로 모든 파일 목록 수집
        # WHY: 파일이 많을 때도 누락 없이 전체 조회 가능
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                key = obj.get("Key")
                size = obj.get("Size")
                last_modified = obj.get("LastModified")
                # WARNING: key/size/last_modified가 없으면 잘못된 S3 객체이므로 skip
                if key is None or size is None or last_modified is None:
                    continue
                result.append({
                    "key": key,
                    "size": size,
                    "last_modified": last_modified.isoformat() if hasattr(last_modified, 'isoformat') else str(last_modified)
                })
        if not result:
            # WARNING: 검색 결과가 없으면 NotFoundException 발생
            raise NotFoundException("지정한 prefix에 파일이 없습니다.")
        # WHAT: 결과를 S3FileEntry 스키마로 변환하여 반환
        return [S3FileEntry(**item) for item in result]
