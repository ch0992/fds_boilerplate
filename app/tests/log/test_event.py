from fastapi.testclient import TestClient
from app.domains.log.main import app

client = TestClient(app)

def test_event_success():
    """
    정상적으로 event 파라미터를 전달했을 때 200 OK와 result=logged를 반환하는지 검증한다.
    """
    resp = client.post("/event", json={"event": "test"})
    assert resp.status_code == 200
    assert resp.json().get("result") == "logged"

def test_event_missing_param():
    """
    필수 파라미터(event)가 누락된 경우 422 에러가 반환되는지 검증한다.
    """
    resp = client.post("/event", json={})
    assert resp.status_code == 422
