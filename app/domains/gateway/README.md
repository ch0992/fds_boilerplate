# Gateway 도메인

이 디렉토리는 **filedepot** 프로젝트의 게이트웨이 서비스(8000포트) 구현체입니다. 외부 API 엔트리포인트, 인증/라우팅, 내부 서비스 연동을 담당합니다.

---

## 1. 주요 역할
- **API Gateway**: 모든 외부 요청의 진입점 역할
- **인증/권한**: (추후 확장) 인증, 권한 체크, 토큰 관리
- **내부 서비스 연동**: 파일/데이터/로그 등 내부 FastAPI 서비스와 연동
- **라우팅/통합**: 각 도메인별 엔드포인트로 요청 분배

---

## 2. 디렉토리 구조 및 설명

```
gateway/
├── api/routes/   # FastAPI 라우트 (엔드포인트별 분리)
├── services/     # 비즈니스 로직 (업로드, 메타데이터 등)
├── clients/      # 내부 서비스 클라이언트 (file/data/log 등)
├── schemas/      # 요청/응답 모델
└── ...           # 기타 유틸, 인터페이스, 테스트 등
```

- **api/routes/**: 실제 API 엔드포인트 정의. 예) `file.py`, `data.py`, `health.py`
- **services/**: 업로드, 메타데이터 처리 등 핵심 로직
- **clients/**: 내부 서비스 호출용 클라이언트
- **schemas/**: FastAPI용 요청/응답 모델

---

## 3. 실행 방법 (로컬)

### 1) 의존성 설치
```bash
pip install -r requirements.txt
```

### 2) 환경설정
- 프로젝트 루트에 `.env` 파일 준비 (예: `ENV=development`)

### 3) Gateway 서비스 단독 실행
```bash
uvicorn app.domains.gateway.main:app --host 0.0.0.0 --port 8000 --reload
```
- FastAPI 문서: [http://localhost:8000/docs](http://localhost:8000/docs)

#### 로그 파일 생성
- **Docker 환경 실행 시:** `/app/gateway.log` 파일로 로그가 저장됩니다. (Dockerfile에서 리다이렉트)
- **직접 실행(uvicorn) 시:** `app/domains/gateway/gateway.log` 파일이 자동 생성되어 로그가 저장됩니다. (main.py에 설정)
- 로그 파일이 아닌 터미널로만 보고 싶다면 `logging.StreamHandler()`만 사용하거나, 로그 파일 경로를 변경하고 싶으면 main.py의 logging 설정을 참고하세요.
- 로그 파일을 별도로 생성하려면 아래처럼 실행하세요:
  ```bash
  uvicorn app.domains.gateway.main:app --host 0.0.0.0 --port 8000 --reload > gateway.log 2>&1
  ```
  로그 파일 저장을 위한 logging 설정을 main.py에 추가할 수도 있습니다.

### 4) 기타
- FastAPI 앱 엔트리포인트는 `app/domains/gateway/main.py`
- 여러 서비스 동시 기동 시, 각 서비스별로 uvicorn을 별도 포트로 실행

---

## 4. API 테스트 방법

- smoke test 전체 실행:
```bash
sh scripts/curl_api_smoketest.sh
```
- 개별 엔드포인트 테스트 예시:
```bash
# Gateway Health
curl -X GET "http://localhost:8000/gateway/ping"

# 파일 서비스 연동
curl -X GET "http://localhost:8000/gateway/file/imgplt/aliases"
```
- 자세한 테스트 명령어는 `curl_tests.md` 참고

---

## 5. 참고/확장
- 인증/권한, 로깅, 예외처리 등은 `app/common` 모듈 활용
- 내부 서비스 연동 구조, 라우팅 패턴 등은 소스코드와 FastAPI 문서 참고
- 마이크로서비스 분리/확장 가능

---

이 디렉토리는 **API Gateway만 분리/확장**하거나, 인증/통합 관점에서 독립 배포할 때도 활용할 수 있습니다.
