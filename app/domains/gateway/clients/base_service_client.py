import httpx
from abc import ABC, abstractmethod
from typing import Any, Dict
from fastapi import HTTPException
import asyncio

"""
[📄 base_service_client.py - BaseServiceClient]

설명:
- 모든 서비스 클라이언트의 공통 기능을 제공하는 베이스 클래스
- 서비스 간 통신, 인증, 예외처리 등의 기본 메서드를 정의
- WHY: 서비스 클라이언트의 공통 기능을 추상화하여 코드 중복을 줄이고 유지보수를 용이하게 함
- WHAT: BaseServiceClient는 서비스 클라이언트의 기본 동작을 정의하며, 하위 클래스에서 구체적인 서비스 클라이언트를 구현할 수 있도록 함
- WARNING: BaseServiceClient를 상속받아 구현하는 서비스 클라이언트는 반드시 health 메서드를 구현해야 함
"""

class BaseServiceClient(ABC):
    """
    BaseServiceClient는 모든 서비스 클라이언트의 공통 기능을 제공하는 베이스 클래스입니다.
    
    Attributes:
    - base_url (str): 서비스 클라이언트의 기본 URL
    - timeout (float): 서비스 클라이언트의 타임아웃 시간 (기본값: 5.0초)
    - max_retries (int): 서비스 클라이언트의 최대 재시도 횟수 (기본값: 2회)
    
    WHY: 서비스 클라이언트의 기본 속성을 정의하여 하위 클래스에서 공통 속성을 사용할 수 있도록 함
    WHAT: BaseServiceClient의 속성은 서비스 클라이언트의 동작을 제어하는 데 사용됨
    WARNING: BaseServiceClient의 속성은 하위 클래스에서 재정의할 수 있으므로 주의가 필요함
    """

    def __init__(self, base_url: str, timeout: float = 5.0, max_retries: int = 2):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        """
        서비스 클라이언트의 요청을 처리하는 메서드
        
        Args:
        - method (str): 요청 메서드 (e.g. GET, POST, PUT, DELETE)
        - path (str): 요청 경로
        - **kwargs: 추가 요청 파라미터
        
        Returns:
        - Any: 요청 결과
        
        WHY: 서비스 클라이언트의 요청을 처리하는 메서드를 추상화하여 하위 클래스에서 재사용할 수 있도록 함
        WHAT: _request 메서드는 서비스 클라이언트의 요청을 처리하고 결과를 반환함
        WARNING: _request 메서드는 하위 클래스에서 재정의할 수 있으므로 주의가 필요함
        """
        url = self.base_url + path
        print(f"[ServiceClient] Request: {method} {url} | kwargs={kwargs}")
        for attempt in range(self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                print(f"[ServiceClient] Response: {response.status_code} {response.text}")
                return response.json()
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                """
                서비스 클라이언트의 요청 처리 중 발생하는 예외
                
                WHY: 서비스 클라이언트의 요청 처리 중 발생하는 예외를 처리하여 안정적인 동작을 보장함
                WHAT: 예외 처리는 서비스 클라이언트의 요청 처리 중 발생하는 오류를 처리함
                WARNING: 예외 처리는 서비스 클라이언트의 동작을 중단할 수 있으므로 주의가 필요함
                """
                print(f"[ServiceClient][ERROR] Attempt {attempt+1}/{self.max_retries+1}: {e} | type={type(e)}")
                if attempt < self.max_retries:
                    await asyncio.sleep(0.2 * (attempt + 1))
                    continue
                print(f"[ServiceClient][FAIL] Final failure for {method} {url}")
                raise HTTPException(status_code=502, detail=f"Service call failed: {e}")

    @abstractmethod
    async def health(self) -> Dict[str, Any]:
        """
        서비스 클라이언트의 헬스 체크 메서드
        
        Returns:
        - Dict[str, Any]: 헬스 체크 결과
        
        WHY: 서비스 클라이언트의 헬스 체크를 추상화하여 하위 클래스에서 구현할 수 있도록 함
        WHAT: health 메서드는 서비스 클라이언트의 헬스 체크를 수행함
        WARNING: health 메서드는 하위 클래스에서 구현해야 함
        """
        pass
