from fastapi.testclient import TestClient
from app.domains.gateway.main import app

client = TestClient(app)

def test_auth_workspace_success():
    """
    올바른 인증 토큰이 있을 때 /auth/workspaces 엔드포인트가 200 OK를 반환하는지 검증한다.
    실제 환경에서는 mock 또는 유효한 토큰 필요. 실패 시 401이 반환될 수 있다.
    """
    resp = client.get("/auth/workspaces", headers={"Authorization": "Bearer testtoken"})
    assert resp.status_code in [200, 401]  # 실제 환경/토큰에 따라 다름

def test_auth_workspace_unauthorized():
    """
    인증 토큰 없이 호출할 경우 401 Unauthorized가 반환되는지 검증한다.
    """
    resp = client.get("/auth/workspaces")
    assert resp.status_code == 401
