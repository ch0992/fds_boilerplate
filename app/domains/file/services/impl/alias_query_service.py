"""
[📄 alias_query_service.py - File 서비스 구현체]

설명:
- 파일 alias 목록 조회 서비스 구현체
- 인증된 사용자 ID 기반 alias 목록 반환

주요 연동:
- AliasQueryInterface (인터페이스)
- AliasEntry (스키마)
"""

from app.domains.file.services.interfaces.alias_query_interface import AliasQueryInterface
from app.domains.file.schemas.aliases import AliasEntry
from typing import List, Any

from app.domains.log.services.common.tracing import get_tracer
# WHY: 성능/장애 추적을 위한 트레이싱 모듈

from app.domains.log.services.common.exceptions import capture_and_log
# WHY: 예외 발생 시 장애 추적 및 로깅을 위한 예외 처리 모듈

class AliasQueryService(AliasQueryInterface):
    """
    WHAT: 파일 alias 목록 조회 서비스 구현체
    WHY: 인증된 사용자별 접근 가능한 파일 alias(경로/권한 등) 목록을 반환
    """
    async def get_aliases(self, user_info: Any) -> List[AliasEntry]:
        """
        WHAT: 인증된 사용자 ID로 접근 가능한 alias 목록 반환
        WHY: 권한 제어 및 사용자별 데이터 분리를 위해 설계
        Args:
            user_info (Any): 사용자 정보
        Returns:
            List[AliasEntry]: alias 목록
        """
        # WHAT: 트레이싱(trace) 시작 (성능/장애 추적 목적)
        tracer = get_tracer("file")
        with tracer.start_as_current_span("file::get_aliases_for_user"):
            try:
                # WHAT: 실제 환경에서는 DB 조회 필요, 현재는 mock 데이터 반환
                # WHY: user_info['user'] 등으로 사용자별 분기 로직 추가 가능
                return [
                    AliasEntry(alias="project-a", description="프로젝트 A 적재 경로"),
                    AliasEntry(alias="project-b", description="프로젝트 B 적재 경로")
                ]
            except Exception as e:
                # WARNING: 예외 발생 시 장애 추적 및 로깅
                # WHY: 예외 발생 시 로깅 및 추적을 위해 capture_and_log 호출
                capture_and_log(e)
                raise
