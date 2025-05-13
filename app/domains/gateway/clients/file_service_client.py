from .base_service_client import BaseServiceClient

"""
[📄 file_service_client.py - File Service Client]

설명:
- 파일 관련 서비스와 통신하는 클라이언트
- 파일 업로드, 다운로드, 리스트, alias 등
"""

class FileServiceClient(BaseServiceClient):
    """
    WHY: 파일 서비스와 통신하기 위한 클라이언트 클래스
    WHAT: 파일 업로드, 다운로드, 리스트, alias 등 파일 관련 서비스와 통신하는 메서드 제공
    WARNING: 파일 서비스와 통신 시 발생할 수 있는 예외 처리에 주의
    """
    async def health(self):
        """
        WHY: 파일 서비스의 상태를 확인하기 위한 메서드
        WHAT: 파일 서비스의 상태를 확인하여 응답 반환
        WARNING: 파일 서비스가 비정상 상태일 경우 예외 발생
        """
        return await self._request("GET", "/ping")

    async def get_aliases(self, user_id: str):
        """
        WHY: 사용자 별 alias 목록을 가져오기 위한 메서드
        WHAT: 사용자 별 alias 목록을 가져와 반환
        WARNING: 사용자 ID가 잘못된 경우 예외 발생
        """
        return await self._request("GET", f"/aliases?user_id={user_id}")

    async def list_files(self, prefix: str):
        """
        WHY: 파일 목록을 가져오기 위한 메서드
        WHAT: 파일 목록을 가져와 반환
        WARNING: prefix가 잘못된 경우 예외 발생
        """
        return await self._request("GET", f"/imgplt/list/{prefix}")
