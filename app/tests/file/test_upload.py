from fastapi.testclient import TestClient
from app.domains.file.main import app
import io

client = TestClient(app)

def test_upload_success_with_metadata_json():
    """
    파일과 metadata_json만 올바르게 전달했을 때 200 OK를 반환하는지 검증한다.
    """
    files = {"file": ("test.txt", io.BytesIO(b"data"), "text/plain")}
    data = {"metadata_json": '{"file_id": "abc", "filename": "test.txt", "owner": "u", "size": 1}'}
    resp = client.post("/upload", files=files, data=data)
    assert resp.status_code == 200

def test_upload_fail_missing_file():
    """
    파일 없이 metadata_json만 전달할 경우 422 에러가 발생하는지 검증한다.
    """
    data = {"metadata_json": '{"file_id": "abc", "filename": "test.txt", "owner": "u", "size": 1}'}
    resp = client.post("/upload", data=data)
    assert resp.status_code == 422

def test_upload_fail_both_metadata():
    """
    file, metadata_file, metadata_json을 모두 전달할 경우 잘못된 요청으로 400 또는 422 에러가 발생하는지 검증한다.
    """
    files = {"file": ("test.txt", io.BytesIO(b"data"), "text/plain"), "metadata_file": ("meta.json", io.BytesIO(b"{}"), "application/json")}
    data = {"metadata_json": '{"file_id": "abc", "filename": "test.txt", "owner": "u", "size": 1}'}
    resp = client.post("/upload", files=files, data=data)
    assert resp.status_code in [400, 422]
