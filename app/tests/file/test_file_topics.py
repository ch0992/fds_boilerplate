from fastapi.testclient import TestClient
from app.domains.file.main import app

client = TestClient(app)

def test_topics_success():
    """
    정상적으로 모든 필수 파라미터를 전달했을 때 200 OK와 status가 반환되는지 검증한다.
    """
    topic = "test-topic"
    payload = {"file_id": "abc", "filename": "test.png", "owner": "user1", "size": 12345}
    resp = client.post(f"/topics/{topic}", json=payload)
    assert resp.status_code == 200
    assert "status" in resp.json()

def test_topics_missing_payload():
    """
    필수 파라미터(payload)가 누락된 경우 422 에러가 반환되는지 검증한다.
    """
    topic = "test-topic"
    resp = client.post(f"/topics/{topic}", json={})
    assert resp.status_code == 422

def test_topics_invalid_topic():
    """
    존재하지 않는 토픽명으로 호출해도 실제 서비스에서는 200 OK가 반환된다.
    """
    topic = "not_exist_topic"
    payload = {"file_id": "abc", "filename": "test.png", "owner": "user1", "size": 12345}
    resp = client.post(f"/topics/{topic}", json=payload)
    assert resp.status_code == 200
