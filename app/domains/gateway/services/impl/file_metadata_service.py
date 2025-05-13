from app.domains.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult
from app.domains.gateway.clients.file_service_client import FileServiceClient
from app.common.config import settings

file_client = FileServiceClient(settings.FILE_SERVICE_URL)

class FileMetadataService:
    """
    WHAT: 파일 메타데이터 Kafka 발행 서비스 구현체
    WHY: gateway 계층에서 파일 서비스 연동 및 메타데이터 발행 처리
    """
    async def produce_metadata(self, topic: str, body: FileMetadataRequest) -> KafkaProduceResult:
        """
        WHAT: 파일 메타데이터 Kafka 발행 메서드
        WHY: 외부 파일 서비스에 POST 요청으로 메타데이터를 Kafka로 발행
        Args:
            topic (str): Kafka 토픽명
            body (FileMetadataRequest): 발행할 메타데이터
        Returns:
            KafkaProduceResult: 발행 결과
        """
        result = await file_client._request(
            "POST", f"/topics/{topic}",
            json=body.dict(),
        )
        return KafkaProduceResult(**result)
