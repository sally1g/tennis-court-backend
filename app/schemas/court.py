from datetime import datetime
from uuid import UUID
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, Field, HttpUrl, ConfigDict

if TYPE_CHECKING:
    from app.schemas.region import RegionResponse
    from app.schemas.availability import AvailabilityResponse


class CourtBase(BaseModel):
    """테니스장 기본 스키마"""
    name: str = Field(..., max_length=200, description="테니스장 이름")
    address: str = Field(..., max_length=300, description="주소")
    phone: Optional[str] = Field(None, max_length=20, description="전화번호")
    description: Optional[str] = Field(None, description="설명")
    url: Optional[str] = Field(None, max_length=500, description="웹사이트 URL")
    region_id: UUID = Field(..., description="지역 ID")


class CourtCreate(CourtBase):
    """테니스장 생성 스키마"""
    pass


class CourtUpdate(BaseModel):
    """테니스장 수정 스키마"""
    name: Optional[str] = Field(None, max_length=200)
    address: Optional[str] = Field(None, max_length=300)
    phone: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    url: Optional[str] = Field(None, max_length=500)
    region_id: Optional[UUID] = None


class CourtResponse(CourtBase):
    """테니스장 응답 스키마"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CourtWithRegion(CourtResponse):
    """지역 정보를 포함한 테니스장 응답 스키마"""
    region: "RegionResponse"

    model_config = ConfigDict(from_attributes=True)


class CourtWithAvailability(CourtResponse):
    """예약 가능 현황을 포함한 테니스장 응답 스키마"""
    availabilities: list["AvailabilityResponse"] = []

    model_config = ConfigDict(from_attributes=True)
