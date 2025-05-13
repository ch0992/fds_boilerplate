from pydantic import BaseModel
from typing import List

class AliasEntry(BaseModel):
    """
    WHAT: 파일 alias(별칭) 정보 스키마
    WHY: 파일 업로드/조회 시 사용자가 선택할 수 있는 논리적 경로/권한 구분자 역할
    """
    alias: str  # WHAT: alias명(논리 경로/권한 구분자)
    description: str  # WHAT: alias 설명(사용자 안내용)

class AliasListResponse(BaseModel):
    """
    WHAT: 파일 alias 목록 응답 스키마
    WHY: 여러 alias를 한 번에 반환할 때 사용
    """
    aliases: List[AliasEntry]  # WHAT: alias 엔트리 리스트
