from fastapi.testclient import TestClient
from app.domains.data.main import app

client = TestClient(app)

def test_topics_success():
    """
    정상적으로 /topics 엔드포인트 호출 시 200 OK와 리스트 반환을 검증한다.
    """
    resp = client.get("/topics")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_topics_not_found():
    """
    존재하지 않는 엔드포인트(/topics-invalid) 호출 시 404 Not Found가 반환되는지 검증한다.
    """
    resp = client.get("/topics-invalid")
    assert resp.status_code == 404
