from fastapi.testclient import TestClient
from app.domains.file.main import app

client = TestClient(app)

def test_imgplt_s3_success():
    """
    정상적으로 file_path 파라미터를 전달했을 때 200 OK와 presigned url을 반환하는지 검증한다.
    """
    resp = client.get("/imgplt/s3/test.txt")
    assert resp.status_code == 200
    assert "url" in resp.json()

def test_imgplt_s3_missing_file_path():
    """
    file_path 파라미터가 누락된 경우 404 Not Found 또는 422 에러가 반환되는지 검증한다.
    """
    resp = client.get("/imgplt/s3/")
    assert resp.status_code in [404, 422]
