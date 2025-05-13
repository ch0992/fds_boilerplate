from abc import ABC, abstractmethod
from typing import Dict, Any

class InsertProducerInterface(ABC):
    """
    WHAT: 데이터 삽입/발행 추상 인터페이스
    WHY: 다양한 데이터 소스/브로커에 대한 삽입/발행 일관성 확보
    """
    @abstractmethod
    async def insert(self, table: str, payload: Dict[str, Any]) -> Dict[str, str]:
        """
        WHAT: 데이터 삽입/발행 추상 메서드
        WHY: 실제 삽입/발행 로직은 구현체에서 구현, 인터페이스로 일관성 유지
        Args:
            table (str): 테이블명
            payload (Dict[str, Any]): 삽입할 데이터
        Returns:
            Dict[str, str]: 결과 정보
        """
        pass
