from fastapi.testclient import TestClient
from app.domains.file.main import app

client = TestClient(app)

def test_imgplt_list_success():
    """
    정상적으로 prefix 파라미터를 전달했을 때 200 OK와 파일 리스트를 반환하는지 검증한다.
    """
    prefix = "uploads/2025/"
    resp = client.get(f"/imgplt/list/{prefix}")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_imgplt_list_missing_prefix():
    """
    prefix 파라미터가 누락된 경우 404 Not Found 또는 422 에러가 반환되는지 검증한다.
    """
    resp = client.get("/imgplt/list/")
    assert resp.status_code in [404, 422]
