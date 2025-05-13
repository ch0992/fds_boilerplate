from app.domains.gateway.services.interfaces.file_list_interface import FileListInterface
from app.domains.file.services.interfaces.list_query_interface import ListQueryInterface
from app.common.config import settings
from app.common.logging import get_tracer, capture_and_log

tracer = get_tracer("gateway::list_files")

class FileListService(FileListInterface):
    """
    WHAT: 파일 목록 조회 서비스 구현체
    WHY: gateway 계층에서 파일 서비스 연동 및 트레이싱 처리
    """
    @capture_and_log(tracer)
    async def list_files(self, prefix: str):
        """
        WHAT: 파일 목록 조회 메서드
        WHY: 파일 서비스 계층의 list_files를 호출하여 결과 반환
        Args:
            prefix (str): S3 prefix 경로
        Returns:
            List[S3FileEntry]: 파일 목록
        """
        service = ListQueryInterface.get_service()
        return await service.list_files(prefix)
