#!/bin/bash
# filedepot: gateway, file, data, log 모든 FastAPI 앱을 로컬에서 포트별로 실행
# (8000: gateway, 8001: file, 8002: data, 8003: log)
# 기존 kill_ports.sh와 연계 사용

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_ROOT="$SCRIPT_DIR/.."

# 1. 포트 강제 종료
bash "$SCRIPT_DIR/kill_ports.sh"

# 2. 각 서비스별 FastAPI 앱 실행 (백그라운드)
echo "[filedepot] Starting FastAPI services on ports 8000~8003..."

# gateway
PYTHONPATH="$PROJECT_ROOT" nohup uvicorn app.domains.gateway.main:app --host 0.0.0.0 --port 8000 > $SCRIPT_DIR/gateway.log 2>&1 &
# file
PYTHONPATH="$PROJECT_ROOT" nohup uvicorn app.domains.file.main:app --host 0.0.0.0 --port 8001 > $SCRIPT_DIR/file.log 2>&1 &
# data
PYTHONPATH="$PROJECT_ROOT" nohup uvicorn app.domains.data.main:app --host 0.0.0.0 --port 8002 > $SCRIPT_DIR/data.log 2>&1 &
# log
PYTHONPATH="$PROJECT_ROOT" nohup uvicorn app.domains.log.main:app --host 0.0.0.0 --port 8003 > $SCRIPT_DIR/log.log 2>&1 &

echo "[filedepot] All FastAPI services started. (Check *.log logs in scripts/)"
