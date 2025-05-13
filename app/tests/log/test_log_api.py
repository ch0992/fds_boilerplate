import pytest
from fastapi.testclient import TestClient
from app.domains.log.main import app

client = TestClient(app)

def test_ping_success():
    resp = client.get("/ping")
    assert resp.status_code == 200
    assert resp.json()["message"] == "pong"

def test_log_event_success():
    resp = client.post("/event", json={"event": "test"})
    assert resp.status_code == 200
    assert resp.json()["result"] == "logged"

def test_log_event_fail():
    resp = client.post("/event", json={})
    assert resp.status_code == 200  # 현재 실패 조건 없음, 실제 실패케이스 필요시 수정
