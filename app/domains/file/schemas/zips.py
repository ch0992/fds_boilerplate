from pydantic import BaseModel
from typing import List

class ZipPresignedResponse(BaseModel):
    """
    WHAT: presigned zip URL 응답 스키마
    WHY: 여러 파일을 zip으로 묶어 presigned URL, 포함 파일 목록, 쿼리 조건(SQL)까지 구조화 반환
    """
    presigned_url: str  # WHAT: zip 파일에 대한 presigned URL(임시 접근용)
    files: List[str]  # WHAT: zip에 포함된 파일 리스트
    sql: str  # WHAT: presigned zip 생성에 사용된 SQL 쿼리문
