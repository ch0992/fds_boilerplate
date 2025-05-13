"""
데이터 서비스 API 라우터
"""
import json
from fastapi import APIRouter, Path, Body, HTTPException
from app.domains.data.schemas.ping import PingResponse
from app.domains.data.schemas.kafka import KafkaProduceResult


router = APIRouter()

@router.get("/ping", response_model=PingResponse, summary="Ping-pong API")
async def ping():
    print("[DATA] /ping called")
    """헬스 체크 및 테스트용 엔드포인트"""
    return {"message": "pong"}

@router.get("/topics", summary="토픽 목록 조회")
async def get_topics():
    print("[DATA] /topics called")
    # 실제로는 DB 등에서 토픽 목록 조회
    return ["topic-a", "topic-b"]

@router.post("/imgplt/curs", summary="Cursor 기반 대용량 레코드 조회")
async def cursor_query_endpoint(body: dict = Body(...)):
    # 실제로는 DB에서 커서 기반 쿼리 처리
    # 예시 응답
    return {
        "rows": [
            {"id": 1, "value": "row1"},
            {"id": 2, "value": "row2"}
        ],
        "next_cursor": None
    }

@router.post("/topics/{table}", summary="토픽 데이터 적재", response_model=KafkaProduceResult)
async def produce_table_record_to_kafka(
    table: str = Path(..., description="Kafka 토픽명"),
    body: dict = Body(...)
):
    print(f"[DATA] /topics/{{table}} called")
    # 실제로는 DB/Kafka 등에 데이터 적재
    return {"topic": table, "status": "success", "message": json.dumps(body)}


@router.post("/imgplt/sqls", summary="임의 SQL 실행 결과 조회")
async def execute_sql(body: dict = Body(...)):
    # body: {"sql": "SELECT ..."}
    sql = body.get("sql")
    print(f"[DATA] /imgplt/sqls called | sql={sql}")
    # 실제로는 DB에 쿼리 실행 후 결과 반환
    # 여기서는 mock 응답
    if not sql:
        raise HTTPException(status_code=400, detail="SQL query required")
    return {
        "columns": ["id", "value"],
        "rows": [
            [1, "row1"],
            [2, "row2"]
        ],
        "row_count": 2
    }
