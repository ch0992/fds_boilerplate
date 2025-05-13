from app.common.config import settings

"""
[📄 auth_mode.py - Auth Mode Utility]

설명:
- 인증 모드(예: 개발, 운영 등)를 반환하는 유틸리티 함수
- 환경 변수 또는 기본값 활용
"""

def get_auth_mode() -> str:
    """
    WHAT: 현재 인증 모드(AUTH_MODE) 반환 함수
    WHY: 환경별(로컬/운영 등) 인증 정책 분기, 예외/미설정 시 안전하게 'local' fallback
    """
    try:
        # WHAT: settings 객체에서 AUTH_MODE를 안전하게 추출
        # WHY: 환경변수 미설정/오류 시에도 항상 'local'로 동작 보장
        return getattr(settings, "AUTH_MODE", "local") or "local"
    except Exception:
        # WARNING: settings 객체 접근 오류 등 비정상 상황에서도 무조건 'local' 반환
        return "local"
