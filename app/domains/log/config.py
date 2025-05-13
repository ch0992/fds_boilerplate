"""
WHAT: 로그 서비스 환경설정 모듈
WHY: .env 및 서비스별 환경설정 통합 관리, 로그 경로/스토리지 등 확장 가능
EXAMPLE: LOG_STORAGE_PATH=/data/logs
"""
from app.common.config import settings

# 예시: 서비스별 설정
# WHAT: 로그 파일/스토리지 경로 환경변수
# WHY: 로그 저장 위치를 환경별로 유연하게 지정
LOG_STORAGE_PATH = getattr(settings, "LOG_STORAGE_PATH", "/data/logs")
