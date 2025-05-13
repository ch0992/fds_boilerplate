from .base_service_client import BaseServiceClient

"""
[📄 file_service_client.py - File Service Client]

설명:
- 파일 관련 서비스와 통신하는 클라이언트
- 파일 업로드, 다운로드, 리스트, alias 등
"""

class FileServiceClient(BaseServiceClient):
    async def health(self):
        return await self._request("GET", "/ping")

    async def get_aliases(self, user_id: str):
        return await self._request("GET", f"/aliases?user_id={user_id}")

    async def list_files(self, prefix: str):
        return await self._request("GET", f"/imgplt/list/{prefix}")
