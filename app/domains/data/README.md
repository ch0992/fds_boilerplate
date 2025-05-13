# Data 도메인

이 디렉토리는 **filedepot** 프로젝트의 데이터 서비스(8002포트) 구현체입니다. 데이터 테이블 관리, Kafka 연동, SQL/커서 기반 데이터 제공을 담당합니다.

---

## 1. 주요 역할
- **데이터 업로드/삽입**: REST API로 데이터 행(row) 업로드
- **Kafka Produce**: 데이터 변경 이벤트를 Kafka로 발행
- **SQL/커서 기반 쿼리**: 대용량 데이터 조회, 페이징 지원
- **토픽/테이블 관리**: 동적 토픽 생성, 메타데이터 관리

---

## 2. 디렉토리 구조 및 설명

```
data/
├── services/   # 실제 데이터 처리 로직 (업로드, 쿼리, Kafka 발행)
├── schemas/    # Pydantic 기반 요청/응답 모델
└── ...         # 기타 유틸, 인터페이스, 테스트 등
```

- **services/**: 핵심 비즈니스 로직. 예) `insert_service.py`, `kafka_service.py`, `query_service.py`
- **schemas/**: API 요청/응답 데이터 타입 정의. FastAPI 자동 문서화에 활용

---

## 3. 실행 방법 (로컬)

### 1) 의존성 설치

```bash
pip install -r requirements.txt
```

### 2) 환경설정

- 프로젝트 루트에 `.env` 파일을 준비합니다.
- 예시: `ENV=development` 등 환경별 변수 지정

### 3) 데이터 서비스 단독 실행

아래 명령어로 **uvicorn**을 직접 실행하여 데이터 서비스만 기동할 수 있습니다.

```bash
uvicorn app.domains.data.main:app --host 0.0.0.0 --port 8002 --reload
```

- `--reload` 옵션은 개발환경에서 코드 변경 시 자동 재시작을 의미합니다.
- 서비스가 정상 실행되면 [http://localhost:8002/docs](http://localhost:8002/docs)에서 OpenAPI 문서를 확인할 수 있습니다.

#### 로그 파일 생성
- **Docker 환경 실행 시:** `/app/data.log` 파일로 로그가 저장됩니다. (Dockerfile에서 리다이렉트)
- **직접 실행(uvicorn) 시:** 별도의 로그 파일이 자동 생성되지 않으므로, 로그 파일로 저장하려면 아래처럼 실행하세요:
  ```bash
  uvicorn app.domains.data.main:app --host 0.0.0.0 --port 8002 --reload > data.log 2>&1
  ```
- 로그 파일 저장을 위한 logging 설정을 main.py에 추가할 수도 있습니다.

### 4) 기타
- FastAPI 앱 엔트리포인트는 `app/domains/data/main.py`입니다.
- 여러 서비스(파일/게이트웨이 등)와 동시에 띄우려면 각 서비스별로 uvicorn을 별도 포트로 실행하세요.

---

## 4. API 테스트 방법

- smoke test 전체 실행:

```bash
sh scripts/curl_api_smoketest.sh
```

- 개별 엔드포인트 테스트 예시:

```bash
# 데이터 토픽 목록 조회
curl -X GET "http://localhost:8000/gateway/data/topics"

# 데이터 Kafka Produce
curl -X POST "http://localhost:8000/gateway/data/topics/test-table" \
  -H "Content-Type: application/json" \
  -d '{"order_id": "order123", "user_id": "user456", "amount": 100}'

# SQL Query
curl -X POST "http://localhost:8000/gateway/data/imgplt/sqls" \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT 1"}'
```

자세한 테스트 명령어는 프로젝트 루트의 `curl_tests.md` 참고.

---

## 5. 참고/확장
- 실제 데이터베이스 연동, Kafka 브로커 설정, 커스텀 쿼리 등은 환경에 따라 `.env` 및 `app/common/config.py`에서 제어
- 예외처리, 인증, 공통 유틸 등은 `app/common` 모듈 활용
- FastAPI 자동 문서: `http://localhost:8002/docs` 접속

---

이 디렉토리의 코드는 **데이터 서비스만 분리/확장**하거나, 마이크로서비스로 독립 배포할 때도 활용할 수 있습니다.
