from fastapi import APIRouter, Request
import aiofiles
import os
from datetime import datetime

router = APIRouter()
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/app.log")

@router.post("/")
async def receive_log(request: Request):
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
