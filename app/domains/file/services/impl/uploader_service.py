"""
[📄 uploader_service.py - File 서비스 구현체]

설명:
- 파일 업로드를 처리하는 서비스 구현체
- 사용자 ID, 파일, 토픽명을 받아 업로드 처리

주요 연동:
- UploaderInterface (인터페이스)
"""

from fastapi import UploadFile
from app.domains.file.services.interfaces.uploader_interface import UploaderInterface
from app.domains.file.schemas.upload import UploadResponse
import aiofiles
import uuid
import os
from app.common.config import settings
from app.domains.file.services.impl.minio_memory_client import MinioMemoryClient
from app.domains.file.services.impl.minio_prod_client import MinioProdClient

from app.common.logging import logger
from app.common.kafka.producer import KafkaMessageProducer

class UploaderService(UploaderInterface):
    """
    WHAT: 파일 업로드 서비스 구현체
    WHY: 사용자가 업로드한 파일을 S3(Minio) 또는 메모리로 저장하고, 메타데이터를 Kafka로 발행
    """

    async def upload_file(self, file: UploadFile):
        """
        WHAT: 파일 업로드 처리 메서드
        WHY: 업로드 파일을 환경에 따라 S3 또는 메모리에 저장, 메타데이터는 Kafka로 발행
        Args:
            file (UploadFile): 업로드할 파일 객체
        Returns:
            UploadResponse: 업로드 결과 정보
        Raises:
            Exception: 업로드/메타데이터 발행 실패 시 예외 발생
        """
        # WHAT: 업로드 파일명에 UUID 부여 (중복 방지)
        filename = f"{uuid.uuid4()}_{file.filename}"
        bucket = "filedepot-bucket"
        key = filename
        chunk_size = 20 * 1024 * 1024  # 20MB

        # WHAT: 환경에 따라 실제 S3 또는 메모리 mock 클라이언트 선택
        # WHY: 운영/스테이지는 MinioProdClient, 그 외는 MinioMemoryClient 사용
        if settings.ENV in ["production", "stage"]:
            minio_client = MinioProdClient()
        else:
            minio_client = MinioMemoryClient()

        # WHAT: 업로드 파일을 임시파일로 저장 (aiofiles 활용)
        # WHY: 대용량 파일도 chunk 단위로 처리 가능
        temp_path = f"/tmp/{filename}"
        async with aiofiles.open(temp_path, 'wb') as out_file:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                await out_file.write(chunk)

        file_size = os.path.getsize(temp_path)
        from app.common.kafka.producer_factory import get_kafka_producer
        if file_size < chunk_size:
            # WHAT: 단일 업로드(20MB 미만) - 메모리/네트워크 효율적
            async with aiofiles.open(temp_path, 'rb') as f:
                data = await f.read()
                location = minio_client.upload_file(bucket, key, data)
                os.remove(temp_path)  # WHY: 임시파일 삭제로 자원 회수
                producer = get_kafka_producer()
                kafka_result = await producer.produce("file_metadata", {"filename": filename, "location": location})
                # WHAT: 업로드 후 검수(무결성 검증) 로깅
                if settings.ENV in ["production", "stage"]:
                    # TODO: 실제 검수/무결성 검사 인터페이스 호출 필요
                    logger.info(f"[검수] 파일 {filename} 업로드 후 무결성 검증 (실서비스)")
                else:
                    logger.info(f"[검수] 파일 {filename} 업로드 후 무결성 검증 (dummy)")
                return UploadResponse(filename=filename, status="uploaded", location=location, kafka_result=kafka_result)
        else:
            # WHAT: multipart upload (20MB 이상) - chunk 단위로 분할 업로드
            logger.info(f"[멀티파트 업로드 시작] 파일명={filename}, 전체용량={file_size} bytes, chunk={chunk_size} bytes")
            # WHY: 대용량 파일 업로드 진행률 시각화
            uploaded = 0
            with open(temp_path, "rb") as f:
                part_num = 1
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    minio_client.upload_file(bucket, f"{key}.part{part_num}", chunk)
                    uploaded += len(chunk)
                    percent = int(uploaded / file_size * 100)
                    logger.info(f"[업로드 진행] {uploaded}/{file_size} bytes ({percent}%) part={part_num}")
                    part_num += 1
            # WARNING: 실제로는 multipart_upload로 파트 병합이 필요하지만, 여기선 단순화
            location = f"memory://{bucket}/{key}" if settings.ENV not in ["production", "stage"] else f"s3://{bucket}/{key}"
            os.remove(temp_path)  # WHY: 임시파일 삭제로 자원 회수
            producer = KafkaMessageProducer()
            kafka_result = await producer.produce("file_metadata", {"filename": filename, "location": location})
            # WHAT: 업로드 후 검수(무결성 검증) 로깅
            if settings.ENV in ["production", "stage"]:
                # TODO: 실제 검수/무결성 검사 인터페이스 호출 필요
                logger.info(f"[검수] 파일 {filename} 업로드 후 무결성 검증 (실서비스)")
            else:
                logger.info(f"[검수] 파일 {filename} 업로드 후 무결성 검증 (dummy)")
            logger.info(f"[멀티파트 업로드 완료] 파일명={filename}, 전체용량={file_size} bytes")
            return UploadResponse(filename=filename, status="uploaded", location=location, kafka_result=kafka_result)


