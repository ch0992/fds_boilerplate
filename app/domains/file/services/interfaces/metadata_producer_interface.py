"""
[📄 metadata_producer_interface.py - File 서비스 인터페이스]

설명:
- 파일 메타데이터를 Kafka로 발행하는 추상 인터페이스 정의
- 실제 구현체(impl/metadata_producer_service.py)에서 상속 및 구현

주요 연동:
- MetadataProducerService (구현체)
"""

from abc import ABC, abstractmethod
from typing import Any

class MetadataProducerInterface(ABC):
    """
    WHAT: 파일 메타데이터 Kafka 발행 인터페이스 (추상)
    WHY: 파일 업로드/변경/삭제 등 이벤트 발생 시 메타데이터를 Kafka로 발행하는 로직을 표준화
    실제 구현체는 MetadataProducerService에서 상속 및 구현
    """
    @abstractmethod
    async def produce_metadata(self, topic: str, metadata: Any) -> dict:
        """
        WHAT: 파일 메타데이터를 Kafka로 발행 (구현체에서 구현)
        WHY: 이벤트 기반 아키텍처에서 파일 메타데이터를 다양한 서비스에 실시간 전달하기 위한 추상화
        Args:
            topic (str): 메타데이터 발행 대상 Kafka 토픽명
            metadata (Any): 발행할 파일 메타데이터(스키마)
        Returns:
            dict: Kafka 발행 결과(상태, 메시지 등)
        """
        pass

    @staticmethod
    def get_service():
        """
        WHAT: 실제 구현체 인스턴스 반환 (factory)
        WHY: DI/테스트/확장성 확보를 위한 추상화
        Returns:
            MetadataProducerService: 실제 구현체 인스턴스
        """
        from app.domains.file.services.impl.metadata_producer_service import MetadataProducerService
        return MetadataProducerService()
