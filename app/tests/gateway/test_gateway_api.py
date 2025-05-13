import pytest
from fastapi.testclient import TestClient
from app.domains.gateway.main import app

client = TestClient(app)

def test_ping_success():
    resp = client.get("/ping")
    assert resp.status_code == 200
    assert resp.json()["message"] == "pong"

def test_file_ping_success():
    resp = client.get("/file/ping")
    assert resp.status_code == 200

def test_data_ping_success():
    resp = client.get("/data/ping")
    assert resp.status_code == 200

def test_log_ping_success():
    resp = client.get("/log/ping")
    assert resp.status_code == 200
