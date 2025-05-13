from pydantic import BaseModel

class S3FileEntry(BaseModel):
    """
    WHAT: S3 파일 엔트리(단일 파일 정보) 스키마
    WHY: S3 prefix 하위 파일 목록 조회 결과의 각 파일 정보를 구조화
    """
    key: str  # WHAT: S3 객체 키(파일 경로)
    size: int  # WHAT: 파일 크기(byte)
    last_modified: str  # WHAT: 마지막 수정일(ISO8601)

    class Config:
        schema_extra = {
            "example": {
                "key": "uploads/2025/file1.png",  # WHAT: 예시 S3 경로
                "size": 123456,  # WHAT: 예시 파일 크기
                "last_modified": "2025-05-06T10:00:00"  # WHAT: 예시 수정일
            }
        }
