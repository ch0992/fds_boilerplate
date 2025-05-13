from abc import ABC, abstractmethod
from typing import Dict, Any

class DataInsertInterface(ABC):
    """
    WHAT: 데이터 삽입 추상 인터페이스
    WHY: 다양한 데이터 소스/서비스에 대한 일관된 삽입 추상화 제공
    """
    @abstractmethod
    async def insert(self, table: str, payload: Dict[str, Any]) -> Dict[str, str]:
        """
        WHAT: 데이터 삽입 추상 메서드
        WHY: 실제 삽입 로직은 구현체에서 구현, 인터페이스로 일관성 유지
        Args:
            table (str): 테이블명
            payload (Dict[str, Any]): 삽입할 데이터
        Returns:
            Dict[str, str]: 결과 정보
        """
        pass
