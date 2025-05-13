"""
WHAT: 파일 서비스 API 라우터
WHY: presigned URL, zip, 메타데이터, kafka 등 파일 관련 서비스 엔드포인트 일괄 제공
"""
from app.common.logging import logger
from fastapi import APIRouter, Query, Path, Body, File, UploadFile, HTTPException
from app.domains.file.schemas.aliases import AliasEntry
from typing import List

from app.domains.file.services.impl.presigned_service import PresignedService
from app.domains.file.schemas.presigned import PresignedURLResponse
from app.domains.file.services.impl.zip_presigned_service import ZipPresignedService
from app.domains.file.schemas.zips import ZipPresignedResponse
from app.domains.file.services.impl.meta_query_service import MetaQueryService
from app.domains.file.schemas.sqls import MetaInfoSchema
from app.domains.file.services.impl.metadata_producer_service import MetadataProducerService
from app.domains.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult

router = APIRouter()

@router.get("/ping", summary="Health check", tags=["Health"])
async def ping():
    """
    WHAT: 파일 서비스 헬스체크 엔드포인트
    WHY: 서비스 정상 동작 확인 용도
    """
    import logging
    logger.info("[file] /ping called")
    return {"message": "pong"}

@router.post(
    "/upload",
    summary="파일 및 메타데이터 업로드 (파일 + 메타데이터: JSON 파일 or 직접입력)",
    description="파일(file, 필수)과 메타데이터(metadata_file: JSON 파일 업로드, 또는 metadata_json: JSON 직접입력) 중 하나만 입력. metadata_file과 metadata_json 둘 다 입력/미입력 시 에러.",
)
async def upload(
    file: UploadFile = File(..., description="업로드할 파일 (예: 이미지, 문서 등)"),
    metadata_file: UploadFile = File(None, description="JSON 메타데이터 파일 업로드 (application/json)"),
    metadata_json: FileMetadataRequest = Body(None, description="직접 입력할 JSON 메타데이터 (application/json)")
):
    '''
    WHAT: 파일 및 메타데이터 업로드 API
    WHY: 파일(file)은 필수, 메타데이터는 metadata_file(.json 파일) 또는 metadata_json(직접 입력) 중 하나만 허용
    WARNING: metadata_file과 metadata_json 둘 다 입력/미입력 시 400 에러 반환 (명확한 입력 분기)
    '''
    if metadata_file and metadata_json:
        raise HTTPException(400, "metadata_file(파일) 또는 metadata_json(body) 중 하나만 입력하세요.")
    if not metadata_file and not metadata_json:
        raise HTTPException(400, "metadata_file(파일) 또는 metadata_json(body) 중 하나는 반드시 입력해야 합니다.")
    if metadata_file:
        contents = await metadata_file.read()
        import json
        try:
            data = json.loads(contents)
            metadata_obj = FileMetadataRequest(**data)
        except Exception:
            raise HTTPException(400, "metadata_file의 JSON 파싱 실패 또는 필드 누락")
    else:
        metadata_obj = metadata_json
    return {
        "uploaded_filename": file.filename,
        "metadata": metadata_obj.dict(),
    }

presigned_service = PresignedService()
zip_presigned_service = ZipPresignedService()
meta_query_service = MetaQueryService()
metadata_producer_service = MetadataProducerService()

from app.domains.file.services.impl.list_query_service import ListQueryService
from app.domains.file.schemas.listing import S3FileEntry
from fastapi import status

@router.get(
    "/imgplt/list/{prefix}",
    response_model=List[S3FileEntry],
    summary="S3 prefix 기반 파일 리스트 조회",
    description="S3 버킷 내 지정된 prefix 하위의 파일 목록을 조회합니다.",
    tags=["File"]
)
async def list_files_by_prefix(prefix: str = Path(..., description="S3 prefix 경로 (예: uploads/2025/)")):
    '''
    WHAT: 지정된 prefix 하위의 S3 파일 목록 반환 API
    WHY: S3 내 특정 경로(폴더) 기준으로 파일 리스트 제공, 파일 없으면 404로 명확히 안내
    '''
    service = ListQueryService()
    files = await service.list_files(prefix)
    if not files:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="지정한 prefix에 파일이 없습니다.")
    return files

@router.get("/ping", summary="Ping-pong API")
async def ping():
    """
    WHAT: 단순 ping-pong API (테스트/헬스체크용)
    WHY: 서비스 alive 체크, 배포/모니터링/로드밸런서 등에서 활용
    """
    return {"message": "pong"}

@router.get("/aliases", response_model=List[AliasEntry], summary="사용자별 적재 alias 목록 조회")
async def aliases(user_id: str = Query(...)):
    """
    WHAT: 사용자별 파일 적재 alias 목록 반환 API
    WHY: 각 사용자/조직별로 사전 정의된 S3 경로 alias를 제공, 실제로는 DB 등에서 동적 조회
    """
    # 실제로는 DB 등에서 user_id별 alias 조회
    return [
        AliasEntry(alias="project-a", description="프로젝트 A 적재 경로"),
        AliasEntry(alias="project-b", description="프로젝트 B 적재 경로")
    ]

@router.get("/imgplt/s3/{file_path}", response_model=PresignedURLResponse, summary="Presigned S3 다운로드 링크 생성")
async def get_presigned_url(file_path: str = Path(...)):
    """
    WHAT: presigned S3 다운로드 링크 생성 API
    WHY: S3 파일에 대한 임시 접근 URL 발급, 인증/권한 체크 후 안전하게 제공
    """
    print("[FILE] /imgplt/s3/{file_path} called")
    return await presigned_service.create_presigned_url(file_path)

@router.get("/imgplt/zips", response_model=ZipPresignedResponse, summary="Presigned ZIP 다운로드 링크 생성")
async def get_zip_presigned_url(sql: str = Query(..., description="SQL 조건")):
    """
    WHAT: presigned ZIP 다운로드 링크 생성 API
    WHY: SQL 조건에 맞는 여러 파일을 zip으로 묶어 임시 접근 URL 제공
    """
    print("[FILE] /imgplt/zips called")
    return await zip_presigned_service.create_zip_presigned_url(sql)

@router.get("/imgplt/sqls", response_model=List[MetaInfoSchema], summary="SQL 기반 메타데이터 조회")
async def get_meta_sqls(query: str = Query(..., description="실행할 SQL 쿼리")):
    """
    WHAT: SQL 기반 메타데이터 조회 API
    WHY: SQL 쿼리로 파일/메타데이터 등 다양한 정보 동적 조회 지원
    """
    print("[FILE] /imgplt/sqls called")
    return await meta_query_service.query_metadata(query)

@router.post("/topics/{topic}", response_model=KafkaProduceResult, summary="Kafka 메타데이터 적재")
async def produce_metadata_to_kafka(
    topic: str = Path(..., description="Kafka topic명"),
    body: FileMetadataRequest = Body(...)
):
    """
    WHAT: Kafka 메타데이터 적재 API
    WHY: 파일/업로드 메타데이터를 Kafka 토픽에 발행, 비동기 처리/이벤트 기반 확장성 확보
    WARNING: 발행 결과 및 입력 데이터 모두 로그로 남겨 장애 추적성 강화
    """
    from app.common.logging import logger
    logger.info(f"[FILE] /topics/{topic} called with metadata: {body.dict()}")
    result = await metadata_producer_service.produce_metadata(topic, body)
    logger.info(f"[FILE] Kafka produce result: {result}")
    return result
