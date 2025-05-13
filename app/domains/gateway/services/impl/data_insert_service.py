from app.domains.gateway.services.interfaces.data_insert_interface import DataInsertInterface
from app.domains.data.client import DataServiceClient
from typing import Dict, Any

class DataInsertService(DataInsertInterface):
    """
    WHAT: 데이터 삽입 서비스 구현체
    WHY: gRPC/HTTP 등 다양한 방식으로 데이터 서비스에 삽입 요청 처리
    """
    async def insert(self, table: str, payload: Dict[str, Any]) -> Dict[str, str]:
        """
        WHAT: 데이터 삽입 처리 메서드
        WHY: 실제 환경에서는 gRPC/HTTP 등 외부 데이터 서비스 연동, 여기선 HTTP 비동기 예시
        Args:
            table (str): 테이블명
            payload (Dict[str, Any]): 삽입할 데이터
        Returns:
            Dict[str, str]: 삽입 결과 정보
        """
        # WHAT: 실제로는 gRPC/HTTP 등으로 data 서비스에 요청
        # WHY: 다양한 서비스 연동을 지원하기 위한 구조
        return await DataServiceClient().insert(table, payload)
