from .base_service_client import BaseServiceClient

"""
[📄 data_service_client.py - Data Service Client]

설명:
- 데이터 관련 서비스와 통신하는 클라이언트
- 데이터 조회, 토픽 등
"""

class DataServiceClient(BaseServiceClient):
    """
    WHY: 데이터 서비스와 통신하기 위한 클라이언트 클래스
    WHAT: 데이터 조회, 토픽 등 데이터 관련 서비스와 통신하는 메서드 제공
    WARNING: 데이터 서비스와 통신 시 발생할 수 있는 예외 처리에 주의
    """
    async def health(self):
        """
        WHY: 데이터 서비스의 상태를 확인하기 위한 메서드
        WHAT: GET /ping 요청을 보내 데이터 서비스의 상태를 확인
        WARNING: 데이터 서비스가 응답하지 않을 경우 예외 발생
        """
        try:
            return await self._request("GET", "/ping")
        except Exception as e:
            # 예외 처리: 데이터 서비스가 응답하지 않을 경우
            print(f"데이터 서비스 상태 확인 실패: {e}")

    async def get_topics(self):
        """
        WHY: 데이터 서비스의 토픽 목록을 조회하기 위한 메서드
        WHAT: GET /topics 요청을 보내 데이터 서비스의 토픽 목록을 조회
        WARNING: 데이터 서비스가 응답하지 않을 경우 예외 발생
        """
        try:
            return await self._request("GET", "/topics")
        except Exception as e:
            # 예외 처리: 데이터 서비스가 응답하지 않을 경우
            print(f"데이터 서비스 토픽 목록 조회 실패: {e}")
