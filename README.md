# filedepot Boilerplate

---

## 아키텍처 및 구조

- **모놀리식처럼 개발, 마이크로서비스처럼 배포**
- 주요 도메인(`gateway`, `file`, `data`, `log`)은 각각 독립적으로 FastAPI 서비스로 동작
- 공통 모듈(`app/common`)과 도메인별 서비스(`app/domains/<domain>`)로 계층화
- 환경설정은 `.env`와 `app/common/config.py`에서 일괄 관리


## 📁 전체 디렉토리 구조 개요

```
📦 fds_boilerplate
├── app
│   ├── common
│   ├── domains
│   │   ├── gateway
│   │   ├── file
│   │   ├── data
│   │   └── log
│   └── tests
│       ├── gateway
│       ├── file
│       ├── data
│       └── log
├── infra
├── scripts
├── .env
└── requirements.txt
```

## ✅ 핵심 구성 요소 설명

| 디렉토리             | 설명                                                                 |
|----------------------|----------------------------------------------------------------------|
| app/common           | 설정, 예외 처리, 인증, 공통 모델 등 모든 도메인에서 공통 사용하는 코드들 |
| app/domains/{도메인} | gateway, file, data, log 등 도메인별 독립 서비스로 분리된 FastAPI 앱    |
| infra                | Helm chart, Kubernetes manifest 등 실제 배포 인프라 구성 관리 영역      |
| scripts              | 개발 및 실행을 돕는 로컬 실행 스크립트들 포함 (예: run_all_fastapi_local.sh) |
| app/tests            | 테스트 코드 모음 (TDD 방식으로 도메인별로 작성, CI/CD Test Stage에서 필요)                |
| .env                 | 환경별 실행 변수를 정의하는 파일로, 서비스 간 통일된 포트 및 설정 공유   |
| requirements.txt     | 전체 서비스에서 사용하는 Python 패키지 의존성 목록                      |



## 🚀 로컬 개발 환경 준비

```bash
# 1. Python 3.12+ 설치 (권장: pyenv, conda 등 사용)
# 2. 패키지 설치 (uv 빠른 설치 권장)
pip install uv
uv pip install --system -r requirements.txt
# 또는
pip install -r requirements.txt
```
- `.env` 파일을 복사/수정하여 환경변수 설정

## 🛠️ VSCode 추천 확장 프로그램

| 확장 프로그램          | 설명                                 | 필수/권장 |
|-----------------------|--------------------------------------|----------|
| Python                | Python 개발 및 디버깅                | 필수     |
| Pylance               | 빠른 타입체크, 코드 완성             | 필수     |
| REST Client           | HTTP API 테스트 자동화                | 권장     |
| dotenv                | .env 파일 문법 하이라이트             | 권장     |
| Docker                | Dockerfile, Compose 관리              | 권장     |
| YAML                  | yaml 파일 작성 지원                   | 권장     |
| GitLens               | git 변경 이력, blame 시각화           | 권장     |

- VSCode 좌측 Extensions(확장) 탭에서 검색/설치

## 실행 방법 (로컬)

```bash
# 모든 서비스(8000~8003) 로컬 실행
cd scripts
sh run_all_fastapi_local.sh
```

- 서비스별 로그는 `scripts/*.log`에서 확인
- 환경별 설정은 `.env` 파일로 제어

## VSCode 디버깅 가이드 (FastAPI 마이크로서비스)

### 1. 필수 VSCode 확장 프로그램
- **Python** (by Microsoft)
- **Pylance** (by Microsoft)
- (권장) **REST Client**: HTTP API 테스트 자동화

### 2. 디버깅 환경 및 launch.json 구조
- `.vscode/launch.json`에 각 도메인(Gateway, File, Data, Log)별 디버깅 환경과 복합 실행(compound) 환경이 미리 정의되어 있습니다.
- **복합 실행(모든 서비스 동시 디버깅)**:
    - 좌측 Run & Debug 패널 상단 드롭다운에서 `All FDS Services` 선택 → F5
    - 4개 서비스가 각각 8000~8003 포트에서 동시에 디버깅 모드로 실행
- **개별 서비스 디버깅**:
    - 원하는 도메인 환경(`Python: Gateway (FastAPI)` 등) 선택 → F5

#### launch.json 예시 (실제 구조와 동일)
```jsonc
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Gateway (FastAPI)",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.domains.gateway.main:app",
                "--host", "0.0.0.0",
                "--port", "8000"
            ],
            "console": "integratedTerminal",
            "envFile": "${workspaceFolder}/.env",
            "env": { "PYTHONPATH": "${workspaceFolder}" },
            "justMyCode": false
        },
        // ... (File, Data, Log도 동일 구조, 포트만 다름)
    ],
    "compounds": [
        {
            "name": "All FDS Services",
            "configurations": [
                "Python: Gateway (FastAPI)",
                "Python: File (FastAPI)",
                "Python: Data (FastAPI)",
                "Python: Log (FastAPI)"
            ]
        }
    ]
}
```

### 3. 디버깅 사용법 (브레이크포인트 활용)
1. **Run & Debug 패널(좌측 ▶️) 진입**
2. 드롭다운에서 `All FDS Services` 또는 원하는 도메인 선택
3. F5(또는 Start Debugging) 클릭 → 서비스별 터미널이 여러 개 뜸
4. 디버깅하고 싶은 Python 코드 라인(예: main.py, 라우터, 서비스 함수 등)에 **브레이크포인트(빨간 점)** 클릭
5. 클라이언트(예: curl, REST Client, Swagger UI 등)로 해당 API 호출
6. 브레이크포인트에서 코드 실행이 멈추면, 변수/스택/콜스택/step-in/out 등 표준 Python 디버깅 기능 사용

### 4. 자주 발생하는 문제 및 해결법
- **복합 실행이 안 보임**: launch.json에 `compounds`가 있는지, VSCode를 재시작했는지 확인
- **포트 충돌/이미 사용 중**: scripts/kill_ports.sh로 포트 강제 종료 후 재실행
- **모듈 임포트 에러**: PYTHONPATH 설정 확인 (launch.json의 env에 `${workspaceFolder}` 포함)
- **중단점이 안 걸림**: uvicorn 핫리로드(`--reload`) 옵션은 디버깅에 비권장
- **환경변수 적용 안 됨**: `.env` 파일 위치와 launch.json의 envFile 경로 확인

### 5. 참고
- VSCode의 [Python 디버깅 공식 문서](https://code.visualstudio.com/docs/python/debugging) 참고
- 복합 실행 환경은 대규모 마이크로서비스 개발 및 통합 테스트에 매우 유용
- launch.json은 자유롭게 커스텀 가능 (포트, 환경변수, 인자 등)

---

## 테스트 방법

### 1. Python 단위 테스트 (pytest)

- 모든 테스트는 `app/tests/` 하위에 위치
- `pytest.ini` 파일로 테스트 경로, 옵션, PYTHONPATH 등이 자동 설정됨

```bash
# 전체 테스트 실행
pytest

# 상세 결과 출력
pytest -v

# 특정 파일/테스트만 실행
pytest app/tests/gateway/test_auth.py
```

- pytest가 없으면 `pip install pytest`로 설치
- 테스트 환경에서 `.env` 파일 및 의존성 설치 필요

### 2. Smoke Test (API 헬스체크)

```bash
sh scripts/curl_api_smoketest.sh
```

- 상세 curl 예시는 `curl_tests.md` 참고

## 기타
- 각 도메인별 구조, 공통 모듈, 예외처리, 인증 등은 하위 README.md 참고
