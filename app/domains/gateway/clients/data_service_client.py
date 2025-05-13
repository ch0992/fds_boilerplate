from .base_service_client import BaseServiceClient

"""
[📄 data_service_client.py - Data Service Client]

설명:
- 데이터 관련 서비스와 통신하는 클라이언트
- 데이터 조회, 토픽 등
"""

class DataServiceClient(BaseServiceClient):
    async def health(self):
        return await self._request("GET", "/ping")

    async def get_topics(self):
        return await self._request("GET", "/topics")
