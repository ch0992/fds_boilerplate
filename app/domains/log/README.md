# Log 도메인

이 디렉토리는 **filedepot** 프로젝트의 로그 서비스(8003포트) 구현체입니다. 서비스별 로그 집계/조회, 향후 모니터링/분석 확장 등을 담당합니다.

---

## 1. 주요 역할
- **로그 집계/저장**: 각 서비스에서 발생하는 로그를 수집/저장
- **로그 조회 API**: REST API로 로그 검색/필터링 제공
- **모니터링/분석**: (추후 확장) 서비스 상태 모니터링, 대시보드 연동 등

---

## 2. 디렉토리 구조 및 설명

```
log/
├── services/   # 로그 집계/조회 서비스
├── schemas/    # 로그 요청/응답 모델
└── ...         # 기타 유틸, 인터페이스, 테스트 등
```

- **services/**: 로그 집계/저장/조회 등 핵심 로직
- **schemas/**: 로그 관련 요청/응답 모델 (FastAPI 문서 자동화)

---

## 3. 실행 방법 (로컬)

### 1) 의존성 설치
```bash
pip install -r requirements.txt
```

### 2) 환경설정
- 프로젝트 루트에 `.env` 파일 준비 (예: `ENV=development`)

### 3) 로그 서비스 단독 실행
```bash
uvicorn app.domains.log.main:app --host 0.0.0.0 --port 8003 --reload
```
- FastAPI 문서: [http://localhost:8003/docs](http://localhost:8003/docs)

#### 로그 파일 생성
- **Docker 환경 실행 시:** `/app/log.log` 파일로 로그가 저장됩니다. (Dockerfile에서 리다이렉트)
- **직접 실행(uvicorn) 시:** 별도의 로그 파일이 자동 생성되지 않으므로, 로그 파일로 저장하려면 아래처럼 실행하세요:
  ```bash
  uvicorn app.domains.log.main:app --host 0.0.0.0 --port 8003 --reload > log.log 2>&1
  ```
- 로그 파일 저장을 위한 logging 설정을 main.py에 추가할 수도 있습니다.

### 4) 기타
- FastAPI 앱 엔트리포인트는 `app/domains/log/main.py`
- 여러 서비스 동시 기동 시, 각 서비스별로 uvicorn을 별도 포트로 실행

---

## 4. API 테스트 방법

- smoke test 전체 실행:
```bash
sh scripts/curl_api_smoketest.sh
```
- 개별 엔드포인트 테스트 예시:
```bash
# 로그 서비스 health check (예시, 실제 엔드포인트는 구현에 따라 다름)
curl -X GET "http://localhost:8003/ping"
```
- 자세한 테스트 명령어는 `curl_tests.md` 참고

---

## 5. 참고/확장
- 로그 저장소, 모니터링 연동 등은 환경에 따라 `.env` 및 `app/common/config.py`에서 제어
- 예외처리, 인증 등은 `app/common` 모듈 활용
- 마이크로서비스 분리/확장 가능

---

이 디렉토리는 **로그 서비스만 분리/확장**하거나, 모니터링/분석 관점에서 독립 배포할 때도 활용할 수 있습니다.
