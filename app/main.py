from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import engine

from app.api.v1 import courts, availability, regions


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    print(f"🚀 Starting {settings.APP_NAME}")
    print(f"📝 Environment: {settings.APP_ENV}")
    print(f"🐛 Debug mode: {settings.DEBUG}")
    print(f"🔌 Database connected")

    yield

    # Shutdown
    print("🔌 Closing database connections...")
    await engine.dispose()
    print(f"👋 {settings.APP_NAME} shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="서울 지역 테니스장 예약 현황을 실시간으로 통합 조회하는 웹 서비스",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
)


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root() -> dict:
    """
    Welcome endpoint.
    """
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check() -> JSONResponse:
    """
    Health check endpoint for monitoring and load balancers.
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "app_name": settings.APP_NAME,
            "environment": settings.APP_ENV,
        },
    )


# Include API routers
app.include_router(
    regions.router,
    prefix=f"{settings.API_V1_PREFIX}/regions",
    tags=["Regions"],
)
app.include_router(
    courts.router,
    prefix=f"{settings.API_V1_PREFIX}/courts",
    tags=["Courts"],
)
app.include_router(
    availability.router,
    prefix=f"{settings.API_V1_PREFIX}/availability",
    tags=["Availability"],
)
