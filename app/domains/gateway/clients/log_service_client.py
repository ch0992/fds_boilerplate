from .base_service_client import BaseServiceClient

"""
[📄 log_service_client.py - Log Service Client]

설명:
- 로그 관련 서비스와 통신하는 클라이언트
- 로그 수집, 이벤트 전송 등
- WHY: 로그 서비스와 통신하여 로그 수집 및 이벤트 전송을 위한 클라이언트 제공
- WHAT: 로그 서비스와 통신하여 로그 수집 및 이벤트 전송을 위한 기능 제공
- WARNING: 로그 서비스와 통신 시 발생할 수 있는 예외 처리에 주의
"""

class LogServiceClient(BaseServiceClient):
    """
    로그 서비스 클라이언트
    - 로그 서비스와 통신하여 로그 수집 및 이벤트 전송을 위한 기능 제공
    - WHY: 로그 서비스와 통신하여 로그 수집 및 이벤트 전송을 위한 클라이언트 제공
    - WHAT: 로그 서비스와 통신하여 로그 수집 및 이벤트 전송을 위한 기능 제공
    - WARNING: 로그 서비스와 통신 시 발생할 수 있는 예외 처리에 주의
    """
    async def health(self):
        """
        로그 서비스의 헬스 체크
        - 로그 서비스의 상태를 확인
        - WHY: 로그 서비스의 상태를 확인하여 정상 동작 여부를 확인
        - WHAT: 로그 서비스의 헬스 체크를 위한 GET 요청
        - WARNING: 로그 서비스의 상태가 비정상일 경우 예외 처리
        """
        return await self._request("GET", "/ping")

    async def log_event(self, event: dict):
        """
        로그 이벤트 전송
        - 로그 이벤트를 전송
        - WHY: 로그 이벤트를 전송하여 로그 수집
        - WHAT: 로그 이벤트를 전송하기 위한 POST 요청
        - WARNING: 로그 이벤트 전송 시 발생할 수 있는 예외 처리에 주의
        """
        return await self._request("POST", "/event", json=event)
