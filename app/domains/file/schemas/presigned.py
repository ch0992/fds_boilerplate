from pydantic import BaseModel

class PresignedURLResponse(BaseModel):
    """
    WHAT: S3 presigned URL 응답 스키마
    WHY: presigned URL 및 만료시간을 구조화하여 반환
    """
    url: str  # WHAT: S3 presigned URL(임시 접근용)
    expires_in: int  # WHAT: presigned URL 만료 시간(초)
