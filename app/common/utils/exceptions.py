from fastapi import HTTPException, status

class BadRequestException(HTTPException):
    """
    WHAT: 400 Bad Request 예외
    WHY: 잘못된 요청 파라미터, 데이터 형식 오류 등 클라이언트 입력 문제 시 사용
    """
    def __init__(self, detail="잘못된 요청입니다."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedException(HTTPException):
    """
    WHAT: 401 Unauthorized 예외
    WHY: 인증 토큰 누락/만료/유효하지 않은 경우 인증 요구
    """
    def __init__(self, detail="인증이 필요합니다."):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenException(HTTPException):
    """
    WHAT: 403 Forbidden 예외
    WHY: 인증은 되었으나 권한이 부족한 경우
    """
    def __init__(self, detail="권한이 없습니다."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class NotFoundException(HTTPException):
    """
    WHAT: 404 Not Found 예외
    WHY: 요청한 리소스(파일/엔티티 등)가 존재하지 않을 때 사용
    """
    def __init__(self, detail="리소스를 찾을 수 없습니다."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ConflictException(HTTPException):
    """
    WHAT: 409 Conflict 예외
    WHY: 중복 데이터, 리소스 충돌 등 상태 불일치 시 사용
    """
    def __init__(self, detail="이미 존재합니다."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class UnprocessableEntityException(HTTPException):
    """
    WHAT: 422 Unprocessable Entity 예외
    WHY: 구문은 맞지만 의미상 처리가 불가능한 요청(비즈니스 검증 실패 등)
    """
    def __init__(self, detail="요청을 처리할 수 없습니다."):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class SystemConfigException(HTTPException):
    """
    WHAT: 500 Internal Server Error (시스템 환경설정 예외)
    WHY: 환경변수 누락/설정 오류 등 운영자 개입이 필요한 시스템 내부 장애
    """
    def __init__(self, detail="시스템 환경설정 오류입니다. 운영자에게 문의하세요."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class ServiceUnavailableException(HTTPException):
    """
    WHAT: 503 Service Unavailable 예외
    WHY: 외부 시스템 장애, 의존 서비스 불가 등 일시적 서비스 중단 상황
    """
    def __init__(self, detail="서비스를 사용할 수 없습니다."):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)
