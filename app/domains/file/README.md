# File 도메인

이 디렉토리는 **filedepot** 프로젝트의 파일 서비스(8001포트) 구현체입니다. 파일 업로드, presigned URL, S3/MinIO 연동, Kafka 메타데이터 발행 등을 담당합니다.

---

## 1. 주요 역할
- **파일 업로드/다운로드**: REST API로 파일 업로드 및 presigned URL 제공
- **S3/MinIO 연동**: 실제 파일 저장소와 연동 (운영/개발 환경 분기)
- **Kafka 발행**: 파일 메타데이터를 Kafka로 produce
- **파일 목록/검색**: SQL 기반 파일 목록 제공

---

## 2. 디렉토리 구조 및 설명

```
file/
├── services/   # 업로더/다운로더, S3/MinIO 클라이언트, presigned 등
├── schemas/    # 파일 요청/응답 모델
├── kafka/      # Kafka producer (파일 이벤트)
└── ...         # 기타 유틸, 인터페이스, 테스트 등
```

- **services/**: 업로드/다운로드, presigned, S3/MinIO 연동 등 핵심 로직
- **schemas/**: 파일 관련 요청/응답 모델 (FastAPI 문서 자동화)
- **kafka/**: 파일 이벤트용 Kafka producer

---

## 3. 실행 방법 (로컬)

### 1) 의존성 설치
```bash
pip install -r requirements.txt
```

### 2) 환경설정
- 프로젝트 루트에 `.env` 파일 준비 (예: `ENV=development`)

### 3) 파일 서비스 단독 실행
```bash
uvicorn app.domains.file.main:app --host 0.0.0.0 --port 8001 --reload
```
- FastAPI 문서: [http://localhost:8001/docs](http://localhost:8001/docs)

#### 로그 파일 생성
- **Docker 환경 실행 시:** `/app/file.log` 파일로 로그가 저장됩니다. (Dockerfile에서 리다이렉트)
- **직접 실행(uvicorn) 시:** 별도의 로그 파일이 자동 생성되지 않으므로, 로그 파일로 저장하려면 아래처럼 실행하세요:
  ```bash
  uvicorn app.domains.file.main:app --host 0.0.0.0 --port 8001 --reload > file.log 2>&1
  ```
- 로그 파일 저장을 위한 logging 설정을 main.py에 추가할 수도 있습니다.

### 4) 기타
- FastAPI 앱 엔트리포인트는 `app/domains/file/main.py`
- 여러 서비스 동시 기동 시, 각 서비스별로 uvicorn을 별도 포트로 실행

---

## 4. API 테스트 방법

- smoke test 전체 실행:
```bash
sh scripts/curl_api_smoketest.sh
```
- 개별 엔드포인트 테스트 예시:
```bash
# presigned URL 조회
curl -X GET "http://localhost:8000/gateway/file/imgplt/s3/test.txt"

# 파일 메타데이터 Kafka 발행
curl -X POST "http://localhost:8000/gateway/file/topics/test-topic" \
  -H "Content-Type: application/json" \
  -d '{"file_id": "testfile1", "filename": "test.txt", "owner": "user1", "size": 12345}'
```
- 자세한 테스트 명령어는 `curl_tests.md` 참고

---

## 5. 참고/확장
- S3/MinIO, Kafka 등 인프라 연동 설정은 `.env` 및 `app/common/config.py`에서 제어
- 예외처리, 인증 등은 `app/common` 모듈 활용
- 마이크로서비스 분리/확장 가능

---

이 디렉토리는 **파일 서비스만 분리/확장**하거나, 파일 저장소/메타데이터 관리 관점에서 독립 배포할 때도 활용할 수 있습니다.
