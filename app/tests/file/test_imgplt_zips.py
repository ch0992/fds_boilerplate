from fastapi.testclient import TestClient
from app.domains.file.main import app

client = TestClient(app)

def test_imgplt_zips_success():
    """
    정상적으로 sql 쿼리 파라미터를 전달했을 때 200 OK와 presigned_url을 반환하는지 검증한다.
    """
    resp = client.get("/imgplt/zips?sql=SELECT+1")
    assert resp.status_code == 200
    assert "presigned_url" in resp.json()

def test_imgplt_zips_missing_sql():
    """
    sql 파라미터가 누락된 경우 422 에러가 반환되는지 검증한다.
    """
    resp = client.get("/imgplt/zips")
    assert resp.status_code == 422
