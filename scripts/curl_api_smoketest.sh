#!/bin/bash
set -e

# .env의 ENV 값에 따라 API_BASE 자동 설정 (boilerplate 기준)
ENV=$(grep '^ENV=' "$(dirname "$0")/../.env" | cut -d '=' -f2 | tr -d '\r')
if [[ "$ENV" == "development" ]]; then
  API_BASE="http://localhost:8000/gateway"
else
  API_BASE="http://gateway:8000/gateway"
fi
TOKEN="test-access-token"

function assert_http_200() {
  local code=$1
  local desc=$2
  if [[ "$code" != "200" ]]; then
    echo "[FAIL] $desc (HTTP $code)" >&2
    exit 1
  else
    echo "[OK] $desc (HTTP 200)"
  fi
}

function api_get() {
  local path="$1"
  local desc="$2"
  echo -e "\n### GET $path"
  code=$(curl -s -o /dev/null -w '%{http_code}' "$API_BASE$path")
  assert_http_200 "$code" "$desc"
}

function api_post() {
  local path="$1"
  local data="$2"
  local desc="$3"
  echo -e "\n### POST $path"
  code=$(curl -s -o /dev/null -w '%{http_code}' -X POST -H "Content-Type: application/json" -d "$data" "$API_BASE$path")
  assert_http_200 "$code" "$desc"
}

# Gateway 서비스 헬스체크
api_get "/ping" "Gateway Health"
api_get "/data/ping" "Data Health (Gateway)"

# 파일 서비스 엔드포인트
api_get "/file/imgplt/aliases" "File Aliases"
api_get "/file/imgplt/s3/test.txt" "File S3 Presigned"
api_get "/file/imgplt/zips?sql=SELECT%20*%20FROM%20files" "File ZIP Presigned"
api_get "/file/imgplt/sqls?query=SELECT%20*%20FROM%20files" "File SQLs"

# 파일 메타데이터 Kafka 발행
api_post "/file/topics/test-topic" '{"file_id": "testfile1", "filename": "test.txt", "owner": "user1", "size": 12345}' "File Metadata Kafka Produce"

# 데이터 서비스 엔드포인트
api_get "/data/topics" "Data Topics"
api_post "/data/topics/test-table" '{"order_id": "order123", "user_id": "user456", "amount": 100}' "Data Kafka Produce"
api_post "/data/imgplt/curs" '{"query": "SELECT * FROM big_table", "cursor": null}' "Data Cursor Query"
echo -e "\n### POST /data/imgplt/sqls"
code=$(curl -s -o /dev/null -w '%{http_code}' -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"sql": "SELECT 1"}' \
  "$API_BASE/data/imgplt/sqls")
assert_http_200 "$code" "Data SQL Query"

# 인증 (501 Not Implemented 예상)
code=$(curl -s -o /dev/null -w '%{http_code}' "$API_BASE/auth/imgplt/auths")
if [[ "$code" == "501" ]]; then
  echo "[OK] Auth endpoint (501 Not Implemented as expected)"
else
  assert_http_200 "$code" "Auth endpoint"
fi

# 로그 서비스 엔드포인트 (Log)
# 실제 log 서비스는 별도 포트일 수 있으니 필요시 아래 주석 해제 후 PORT 수정
# LOG_API_BASE="http://localhost:8003"
# code=$(curl -s -o /dev/null -w '%{http_code}' "$LOG_API_BASE/ping")
# assert_http_200 "$code" "Log Health"

# 종료
echo -e "\n[ALL TESTS PASSED]"
