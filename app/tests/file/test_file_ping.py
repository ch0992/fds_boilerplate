from fastapi.testclient import TestClient
from app.domains.file.main import app

client = TestClient(app)

def test_ping_success():
    """
    정상적으로 /ping 엔드포인트 호출 시 200 OK와 pong 메시지를 반환하는지 검증한다.
    """
    resp = client.get("/ping")
    assert resp.status_code == 200
    assert resp.json()["message"] == "pong"

def test_ping_not_found():
    """
    존재하지 않는 엔드포인트 호출 시 404 Not Found가 반환되는지 검증한다.
    """
    resp = client.get("/ping-not-exist")
    assert resp.status_code == 404
