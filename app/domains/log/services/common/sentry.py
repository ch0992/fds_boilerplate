"""
WHAT: 로그 서비스 Sentry 연동 유틸리티
WHY: 장애/예외 상황 실시간 모니터링, 외부 Sentry 대시보드 연동
EXAMPLE: init_sentry(dsn, environment), capture_exception(exc)
"""
import os
import sentry_sdk

_sentry_dsn = os.getenv("SENTRY_DSN", None)
_sentry_env = os.getenv("ENV", "development")

_sentry_inited = False

from app.common.logging import logger

def init_sentry(dsn: str = None, environment: str = None):
    """
    WHAT: Sentry SDK 초기화
    WHY: DSN/환경별로 Sentry 연동, 장애/예외 실시간 추적
    EXAMPLE: init_sentry(dsn, environment)
    """
    global _sentry_inited
    dsn = dsn or _sentry_dsn
    environment = environment or _sentry_env
    if not dsn:
        logger.warning("[Sentry fallback] SENTRY_DSN 미설정, Sentry 비활성화")
        return
    if not _sentry_inited:
        try:
            sentry_sdk.init(
                dsn=dsn,
                traces_sample_rate=1.0,
                environment=environment,
            )
            _sentry_inited = True
        except Exception as e:
            logger.warning(f"[Sentry fallback] sentry init failed: {e}")

def capture_exception(exc: Exception):
    """
    WHAT: Sentry로 예외 전송
    WHY: 장애/예외 상황 대시보드 집계, 실시간 알림
    EXAMPLE: capture_exception(Exception("test"))
    """
    if not _sentry_dsn:
        logger.warning(f"[Sentry fallback] SENTRY_DSN 미설정, 예외만 출력: {exc}")
        return
    try:
        sentry_sdk.capture_exception(exc)
    except Exception as e:
        logger.warning(f"[Sentry fallback] sentry capture_exception failed: {e}")
