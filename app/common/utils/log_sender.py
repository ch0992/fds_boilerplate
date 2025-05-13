"""
WHAT: 외부 로그 집계 서버로 fire-and-forget 방식 비동기 로그 전송 유틸리티
WHY: 비즈니스 로직과 무관하게 로그를 신속/안정적으로 중앙 서버에 전송, 실패해도 서비스 영향 없음
EXAMPLE: send_log_async("gateway health check fail", level="ERROR", extra={"domain": "gateway"})
"""
import threading
import time
import requests
import traceback
import os
from dotenv import load_dotenv

load_dotenv()

LOG_EVENT_URL = os.getenv("LOG_EVENT_URL", "http://localhost:8003/event")


def send_log_async(message, level="INFO", extra=None, url=None):
    """
    WHAT: 비동기(fire-and-forget) 방식으로 로그를 외부 집계 서버에 전송
    WHY: 로그 전송 실패 시에도 비즈니스 로직 영향 없이 안전하게 처리
    EXAMPLE: send_log_async("file upload fail", level="ERROR", extra={"domain": "file"})
    message: str (필수)
    level: str (기본 INFO)
    extra: dict (옵션, 필요시 추가 정보)
    url: str (옵션, override)
    """
    target_url = url or LOG_EVENT_URL

    log_payload = {
        "timestamp": time.time(),
        "level": level,
        "message": message,
    }
    if extra:
        log_payload.update(extra)

    def _send():
        try:
            requests.post(
                target_url,
                json=log_payload,
                timeout=1,
            )
        except Exception:
            print("[send_log_async] LOG SEND FAIL", traceback.format_exc())

    threading.Thread(target=_send, daemon=True).start()

