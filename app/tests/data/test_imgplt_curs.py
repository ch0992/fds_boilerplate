from fastapi.testclient import TestClient
from app.domains.data.main import app

client = TestClient(app)

def test_imgplt_curs_success():
    """
    정상적으로 cursor 파라미터를 전달했을 때 200 OK와 rows 키가 포함된 응답을 검증한다.
    """
    resp = client.post("/imgplt/curs", json={"cursor": None})
    assert resp.status_code == 200
    assert "rows" in resp.json()

def test_imgplt_curs_missing_param():
    """
    필수 파라미터(cursor)가 누락된 경우에도 실제 서비스에서는 200 OK가 반환된다.
    """
    resp = client.post("/imgplt/curs", json={})
    assert resp.status_code == 200
