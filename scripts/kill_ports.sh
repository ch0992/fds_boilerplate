#!/bin/bash
# 사용 중인 주요 포트 강제 종료 (filedepot 서비스)
PORTS=(8000 8001 8002 8003)
for PORT in "${PORTS[@]}"; do
  PID=$(lsof -t -i tcp:$PORT)
  if [ -n "$PID" ]; then
    echo "[filedepot] Killing process on port $PORT (PID: $PID)"
    kill -9 $PID
  fi
done
