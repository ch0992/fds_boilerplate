from app.services.data.services.interfaces.table_producer_interface import TableProducerInterface
from app.services.data.schemas.table import TableRecordRequest, KafkaProduceResult

from app.common.kafka.producer_factory import get_kafka_producer
from app.common.logging import logger

class TableProducerService(TableProducerInterface):
    async def produce_record(self, table: str, body: TableRecordRequest) -> KafkaProduceResult:
        try:
            logger.info(f"[Data] Kafka produce 요청: table={table}, body={body}")
            producer = get_kafka_producer()
            result = await producer.produce(table, body.dict())
            logger.info(f"[Data] Kafka produce 성공: result={result}")
            return KafkaProduceResult(topic=table, message=json.dumps(body.dict()), status=result["status"])
        except Exception as e:
            logger.error(f"[Data] Kafka produce 실패: {e}")
            return KafkaProduceResult(topic=table, message=str(e), status="error")

