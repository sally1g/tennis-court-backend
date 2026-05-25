from datetime import datetime
from uuid import UUID
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, Field, ConfigDict

if TYPE_CHECKING:
    from app.schemas.court import CourtResponse


class RegionBase(BaseModel):
    """지역 기본 스키마"""
    name: str = Field(..., max_length=100, description="지역 식별자 (예: 'gangnam')")
    display_name: str = Field(..., max_length=100, description="지역 표시명 (예: '강남구')")


class RegionCreate(RegionBase):
    """지역 생성 스키마"""
    pass


class RegionUpdate(BaseModel):
    """지역 수정 스키마"""
    name: Optional[str] = Field(None, max_length=100)
    display_name: Optional[str] = Field(None, max_length=100)


class RegionResponse(RegionBase):
    """지역 응답 스키마"""
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RegionWithCourts(RegionResponse):
    """테니스장 정보를 포함한 지역 응답 스키마"""
    courts: list["CourtResponse"] = []

    model_config = ConfigDict(from_attributes=True)
