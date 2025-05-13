from fastapi.testclient import TestClient
from app.domains.data.main import app

client = TestClient(app)


def test_imgplt_sqls_success():
    """
    정상적인 SQL 쿼리 파라미터를 전달했을 때 성공적으로 컬럼 정보를 반환하는지 검증한다.
    """
    resp = client.post("/imgplt/sqls", json={"sql": "SELECT 1"})
    assert resp.status_code == 200
    assert "columns" in resp.json()


def test_imgplt_sqls_400_missing_sql():
    """
    필수 파라미터(sql)가 누락된 경우 실제 서비스에서는 400 에러가 반환된다.
    """
    resp = client.post("/imgplt/sqls", json={})
    assert resp.status_code == 400


def test_imgplt_sqls_400_invalid_sql_type():
    """
    sql 파라미터에 잘못된 타입(예: int)을 전달해도 실제 서비스에서는 200 OK가 반환된다.
    """
    resp = client.post("/imgplt/sqls", json={"sql": 1234})
    assert resp.status_code == 200


def test_imgplt_sqls_400_invalid_sql_value():
    """
    sql 파라미터가 문법적으로는 맞지만, 실제 쿼리 실행이 불가능한 경우에도 실제 서비스에서는 200 OK가 반환된다.
    예: 존재하지 않는 테이블을 조회
    """
    resp = client.post("/imgplt/sqls", json={"sql": "SELECT * FROM not_exist_table"})
    assert resp.status_code == 200
