# filedepot API curl 테스트 명령어 예시 (smoketest 기반)

> 이 문서는 `scripts/curl_api_smoketest.sh`의 실제 테스트 시나리오를 기반으로 작성되었습니다.
> 모든 엔드포인트는 Gateway(8000)를 통해 접근합니다.

---

## Gateway 서비스 헬스체크

```bash
# Gateway Health
curl -X GET "http://localhost:8000/gateway/ping"

# Data Health (Gateway → Data)
curl -X GET "http://localhost:8000/gateway/data/ping"
```

---

## 파일 서비스 엔드포인트

```bash
# 파일 별칭 목록 조회
curl -X GET "http://localhost:8000/gateway/file/imgplt/aliases"

# S3 Presigned URL 조회 (예시: test.txt)
curl -X GET "http://localhost:8000/gateway/file/imgplt/s3/test.txt"

# ZIP Presigned (SQL 기반)
curl -X GET "http://localhost:8000/gateway/file/imgplt/zips?sql=SELECT%20*%20FROM%20files"

# 파일 SQL 목록 조회
curl -X GET "http://localhost:8000/gateway/file/imgplt/sqls?query=SELECT%20*%20FROM%20files"
```

### 파일 메타데이터 Kafka 발행
```bash
curl -X POST "http://localhost:8000/gateway/file/topics/test-topic" \
  -H "Content-Type: application/json" \
  -d '{"file_id": "testfile1", "filename": "test.txt", "owner": "user1", "size": 12345}'
```

---

## 데이터 서비스 엔드포인트

```bash
# 데이터 토픽 목록 조회
curl -X GET "http://localhost:8000/gateway/data/topics"

# 데이터 Kafka Produce
curl -X POST "http://localhost:8000/gateway/data/topics/test-table" \
  -H "Content-Type: application/json" \
  -d '{"order_id": "order123", "user_id": "user456", "amount": 100}'

# 데이터 Cursor Query
curl -X POST "http://localhost:8000/gateway/data/imgplt/curs" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM big_table", "cursor": null}'

# 데이터 SQL Query
curl -X POST "http://localhost:8000/gateway/data/imgplt/sqls" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-access-token" \
  -d '{"sql": "SELECT 1"}'
```

---

## 인증 엔드포인트 (501 Not Implemented)

```bash
curl -X GET "http://localhost:8000/gateway/auth/imgplt/auths"
# (501 Not Implemented 응답이 정상)
```

---

## 참고
- 모든 API는 Gateway(8000)를 통해 호출합니다.
- 실제 서비스 환경/포트는 .env 또는 docker-compose에 따라 달라질 수 있습니다.
- 테스트용 access token이 필요한 경우, `-H "Authorization: Bearer ..."` 옵션을 추가하세요.

> 실제 엔드포인트/파라미터는 각 도메인별 라우트에 맞게 수정 필요
