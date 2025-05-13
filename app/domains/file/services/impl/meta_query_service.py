from typing import List
"""
[📄 meta_query_service.py - File 서비스 구현체]

설명:
- 파일 메타데이터 조회 서비스 구현체
- S3 파일 키 기반으로 메타데이터 반환

주요 연동:
- MetaQueryInterface (인터페이스)
- MetaInfoSchema (스키마)
"""

from app.domains.file.services.interfaces.meta_query_interface import MetaQueryInterface
from app.domains.file.schemas.sqls import MetaInfoSchema

class MetaQueryService(MetaQueryInterface):
    """
    파일 메타데이터 조회 서비스 구현체
    """
    async def get_file_meta(self, file_key: str):
        raise NotImplementedError("get_file_meta는 아직 구현되지 않았습니다.")

    async def query_metadata(self, query: str) -> List[MetaInfoSchema]:
        """
        메타데이터 조회
        Args:
            query (str): 조회 쿼리
        Returns:
            List[MetaInfoSchema]: 메타데이터 목록
        """
        # WHY: 실제 DB 연동 및 쿼리 실행 로직이 들어가야 함
        # 여기서는 예시로 더미 데이터 반환
        return [
            MetaInfoSchema(id=1, name="meta1", value="value1"),
            MetaInfoSchema(id=2, name="meta2", value="value2")
        ]
