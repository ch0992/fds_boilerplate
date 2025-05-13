from fastapi.testclient import TestClient
from app.domains.gateway.main import app

client = TestClient(app)

def test_log_ping_success():
    """
    정상적으로 /log/ping 엔드포인트 호출 시 200 OK가 반환되는지 검증한다.
    """
    resp = client.get("/log/ping")
    assert resp.status_code == 200

def test_log_ping_not_found():
    """
    존재하지 않는 엔드포인트(/log/ping-not-exist) 호출 시 404 Not Found가 반환되는지 검증한다.
    """
    resp = client.get("/log/ping-not-exist")
    assert resp.status_code == 404
