from pydantic import BaseModel
from typing import Any, Dict

class InsertPayload(BaseModel):
    """
    WHAT: dict 기반 데이터 삽입 페이로드 모델
    WHY: 다양한 테이블 구조에 유연하게 대응하기 위한 래퍼
    """
    __root__: Dict[str, Any]

    def dict(self, *args, **kwargs):
        return self.__root__
