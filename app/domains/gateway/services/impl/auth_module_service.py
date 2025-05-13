class AuthService:
    """
    WHAT: 인증 모듈 서비스 클래스
    WHY: JWT 토큰 검증 및 사용자 workspace 정보 제공
    """
    async def verify_token_and_get_workspaces(self, access_token: str):
        """
        WHAT: 액세스 토큰 검증 및 workspace 목록 반환
        WHY: 실제 환경에서는 JWT 검증 및 사용자 권한 체크, 현재는 더미 처리
        Args:
            access_token (str): JWT 액세스 토큰
        Returns:
            List[str]: 유효한 경우 workspace 목록
        Raises:
            Exception: 토큰이 유효하지 않을 때 예외 발생
        """
        # WHAT: 실제 구현에서는 JWT 검증 및 workspace 정보 반환
        # WARNING: 더미 검증(토큰이 'valid' 아니면 예외)
        if not access_token or access_token == "invalid":
            raise Exception("Invalid access token")
        return ["default_workspace"]

auth_service = AuthService()

async def verify_access_token_dependency(authorization: str):
    """
    WHAT: FastAPI Depends용 액세스 토큰 검증 함수
    WHY: API 엔드포인트에서 인증 의존성 주입을 위해 사용
    Args:
        authorization (str): Authorization 헤더
    Returns:
        List[str]: workspace 목록
    Raises:
        Exception: 헤더 누락/형식 오류/토큰 불일치 시 예외 발생
    """
    # WHAT: Bearer 토큰 형식 체크 및 추출
    if not authorization or not authorization.startswith("Bearer "):
        raise Exception("Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    return await auth_service.verify_token_and_get_workspaces(access_token)
