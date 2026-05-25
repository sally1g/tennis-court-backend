# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Tennis Court Finder** - 서울 지역 테니스장 예약 현황을 실시간으로 통합 조회하는 웹 서비스의 백엔드 API

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy 2.0
- **Crawling**: BeautifulSoup4, Selenium, httpx
- **Scheduling**: APScheduler

## Development Commands

### Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
alembic upgrade head
```

### Running the Application
```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API Documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest app/tests/test_courts.py

# Run specific test
pytest app/tests/test_courts.py::test_get_court
```

### Code Quality
```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## Architecture

### Directory Structure

- **`app/api/v1/`** - API endpoints (courts, availability, regions)
- **`app/core/`** - Core configuration (config.py, database.py)
- **`app/models/`** - SQLAlchemy database models
- **`app/schemas/`** - Pydantic schemas for request/response validation
- **`app/crawlers/`** - Web crawlers for tennis court data
  - `base.py` - Base crawler class
  - `seoul_public.py` - Seoul public facility crawler
- **`app/services/`** - Business logic layer
- **`app/tasks/`** - Scheduled background tasks (APScheduler)
- **`app/utils/`** - Utility functions (logging, helpers)
- **`alembic/`** - Database migration files

### Data Flow

1. **Scheduled Crawlers** (APScheduler) → scrape court availability from various sources
2. **Crawlers** → parse and normalize data → **Services**
3. **Services** → save to **Database** (SQLAlchemy models)
4. **API Endpoints** → query **Services** → return **Pydantic schemas**

### Key Design Patterns

- **Repository Pattern**: Services layer abstracts database operations
- **Dependency Injection**: FastAPI's `Depends()` for database sessions and config
- **Schema Separation**: Pydantic schemas separate from SQLAlchemy models for clean API contracts
- **Base Crawler**: Inheritance-based crawler design for different court sources

### Database Schema

Core entities:
- **Region** - 지역 정보 (서울 구/동)
- **Court** - 테니스장 기본 정보 (이름, 주소, 연락처)
- **Availability** - 예약 가능 현황 (날짜, 시간, 상태)

Relations:
- Region 1:N Court
- Court 1:N Availability

### Environment Variables

Key configuration in `.env`:
- `DATABASE_URL` - PostgreSQL connection string
- `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY` - Supabase credentials
- `API_V1_PREFIX` - API versioning prefix (default: `/api/v1`)
- `BACKEND_CORS_ORIGINS` - Allowed CORS origins for frontend
- `CRAWL_DELAY_SECONDS` - Rate limiting for web crawlers
- `LOG_LEVEL` - Logging level (INFO, DEBUG, ERROR)

