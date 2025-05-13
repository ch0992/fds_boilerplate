from fastapi.testclient import TestClient
from app.domains.file.main import app

client = TestClient(app)

def test_aliases_success():
    """
    정상적으로 user_id 쿼리 파라미터를 전달했을 때 200 OK와 alias 리스트를 반환하는지 검증한다.
    """
    resp = client.get("/aliases?user_id=test")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_aliases_missing_user_id():
    """
    user_id 파라미터가 누락된 경우 422 에러가 반환되는지 검증한다.
    """
    resp = client.get("/aliases")
    assert resp.status_code == 422
