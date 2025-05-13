from app.domains.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult
from app.domains.gateway.clients.file_service_client import FileServiceClient
from app.common.config import settings

file_client = FileServiceClient(settings.FILE_SERVICE_URL)

class FileMetadataService:
    async def produce_metadata(self, topic: str, body: FileMetadataRequest) -> KafkaProduceResult:
        result = await file_client._request(
            "POST", f"/topics/{topic}",
            json=body.dict(),
        )
        return KafkaProduceResult(**result)
