from pydantic import BaseModel
from typing import List

class AuthWorkspaceList(BaseModel):
    """
    WHAT: 인증 workspace 목록 반환 모델
    WHY: 인증된 사용자의 workspace 리스트와 유효성 정보를 일관되게 반환
    """
    workspaces: List[str]
    valid: bool = True
