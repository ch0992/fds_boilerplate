"""
WHAT: 로그 서비스 API 라우터
WHY: 중앙집중식 로그 집계 및 관리, 타 서비스에서 비동기/일괄 로그 수집을 위함
"""
from fastapi import APIRouter, Body, Request
import aiofiles
import os
from datetime import datetime

router = APIRouter()
LOG_FILE_PATH = os.getenv(
    "LOG_FILE_PATH",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "total_log/app.log"))
)

def get_daily_log_path():
    """
    WHAT: 오늘 날짜 기준 일자별 로그 파일 경로 반환
    WHY: 로그 파일을 일별로 분리 저장하여 관리/백업/삭제 용이
    EXAMPLE: .../total_log/app-20250513.log
    """
    base_dir = os.path.dirname(LOG_FILE_PATH)
    date_str = datetime.utcnow().strftime('%Y%m%d')
    return os.path.join(base_dir, f"app-{date_str}.log")



@router.post("/event")
async def receive_log_event(request: Request):
    """
    WHAT: 외부 서비스에서 POST로 전달된 로그 이벤트를 일자별 파일에 저장
    WHY: 다양한 서비스의 로그를 중앙에서 집계, 장애/이상탐지/모니터링 용이
    EXAMPLE: POST /event {"level": "INFO", "domain": "gateway", ...}
    """
    try:
        print("LOG_FILE_PATH", LOG_FILE_PATH)
        data = await request.json()
        print("RECEIVED", data)
        # WHAT: 로그 포맷 표준화 (timestamp, level, domain, host, message)
        # WHY: 집계된 로그의 일관성, 검색/분석 용이
        # EXAMPLE: 20250513T12:34:56 [INFO] gateway@localhost - GET /gateway/health 404
        ts = datetime.utcfromtimestamp(data.get("timestamp", datetime.utcnow().timestamp())).isoformat()
        level = data.get("level", "INFO")
        domain = data.get("domain", "unknown")
        host = data.get("host", "-")
        message = data.get("message", "")
        log_line = f"{ts} [{level}] {domain}@{host} - {message}\n"
        try:
            daily_log_path = get_daily_log_path()
            os.makedirs(os.path.dirname(daily_log_path), exist_ok=True)
            async with aiofiles.open(daily_log_path, "a") as f:
                await f.write(log_line)
            print("WRITE SUCCESS", log_line)
        except Exception as file_err:
            print("WRITE FAIL", str(file_err))
            return {"status": "error", "detail": f"File write error: {file_err}"}
        return {"status": "ok"}
    except Exception as e:
        print("RECEIVE FAIL", str(e))
        return {"status": "error", "detail": str(e)}
    data = await request.json()
    # 로그 포맷 표준화 (timestamp, level, domain, host, message)
    ts = datetime.utcfromtimestamp(data.get("timestamp", datetime.utcnow().timestamp())).isoformat()
    level = data.get("level", "INFO")
    domain = data.get("domain", "unknown")
    host = data.get("host", "-")
    message = data.get("message", "")
    log_line = f"{ts} [{level}] {domain}@{host} - {message}\n"
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    async with aiofiles.open(LOG_FILE_PATH, "a") as f:
        await f.write(log_line)
    return {"status": "ok"}

@router.get("/ping", summary="Ping-pong API")
async def ping():
    """헬스 체크 및 테스트용 엔드포인트"""
    return {"message": "pong"}


