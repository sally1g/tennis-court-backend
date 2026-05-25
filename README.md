# Tennis Court Finder - Backend

서울 지역 테니스장 예약 현황을 실시간으로 통합 조회하는 웹 서비스의 백엔드 API입니다.

## 기술 스택

- **Python**: 3.11+
- **Framework**: FastAPI
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy 2.0
- **Migration**: Alembic
- **Crawling**: BeautifulSoup4, Selenium, httpx
- **Scheduling**: APScheduler

## 프로젝트 구조

```
tennis-court-backend/
├── app/
│   ├── api/v1/          # API 엔드포인트
│   ├── core/            # 설정 및 데이터베이스
│   ├── models/          # SQLAlchemy 모델
│   ├── schemas/         # Pydantic 스키마
│   ├── crawlers/        # 크롤러 모듈
│   ├── services/        # 비즈니스 로직
│   ├── tasks/           # 스케줄링 작업
│   └── utils/           # 유틸리티
├── alembic/             # 데이터베이스 마이그레이션
├── requirements.txt     # 프로덕션 의존성
└── requirements-dev.txt # 개발 의존성
```

## 설치 방법

### 1. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 개발 환경
```

### 3. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일을 편집하여 실제 데이터베이스 정보 입력
```

### 4. 데이터베이스 마이그레이션

```bash
alembic upgrade head
```

## 실행 방법

### 개발 서버 실행

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API 문서는 다음 주소에서 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 테스트 실행

```bash
pytest
pytest --cov=app  # 커버리지 포함
```

### 코드 포맷팅 및 린팅

```bash
black app/
flake8 app/
mypy app/
```

## API 엔드포인트

- `GET /api/v1/courts` - 테니스장 목록 조회
- `GET /api/v1/courts/{court_id}` - 테니스장 상세 정보
- `GET /api/v1/availability` - 예약 가능 현황 조회
- `GET /api/v1/regions` - 지역 목록 조회

## 개발 가이드

자세한 개발 가이드는 `CLAUDE.md` 파일을 참고하세요.

## 라이선스

MIT
