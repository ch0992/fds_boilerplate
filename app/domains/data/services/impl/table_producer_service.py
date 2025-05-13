from app.services.data.services.interfaces.table_producer_interface import TableProducerInterface
from app.services.data.schemas.table import TableRecordRequest, KafkaProduceResult

from app.common.kafka.producer_factory import get_kafka_producer

class TableProducerService(TableProducerInterface):
    async def produce_record(self, table: str, body: TableRecordRequest) -> KafkaProduceResult:
        producer = get_kafka_producer()
        result = await producer.produce(table, body.dict())
        return KafkaProduceResult(topic=table, message=json.dumps(body.dict()), status=result["status"])

