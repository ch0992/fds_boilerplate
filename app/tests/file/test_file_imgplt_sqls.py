from fastapi.testclient import TestClient
from app.domains.file.main import app

client = TestClient(app)

def test_imgplt_sqls_success():
    resp = client.get("/imgplt/sqls?query=SELECT+1")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_imgplt_sqls_fail():
    resp = client.get("/imgplt/sqls")
    assert resp.status_code in [400, 422]
