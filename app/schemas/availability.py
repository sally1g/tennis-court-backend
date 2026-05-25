from datetime import datetime
from datetime import date as date_type
from uuid import UUID
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, Field, ConfigDict

from app.models.availability import AvailabilityStatus

if TYPE_CHECKING:
    from app.schemas.court import CourtResponse


class AvailabilityBase(BaseModel):
    """예약 가능 현황 기본 스키마"""
    court_id: UUID = Field(..., description="테니스장 ID")
    date: date_type = Field(..., description="날짜")
    time_slot: str = Field(..., max_length=20, description="시간대 (예: '09:00-10:00')")
    status: AvailabilityStatus = Field(..., description="예약 상태")
    price: Optional[int] = Field(None, ge=0, description="가격 (원)")


class AvailabilityCreate(AvailabilityBase):
    """예약 가능 현황 생성 스키마"""
    pass


class AvailabilityUpdate(BaseModel):
    """예약 가능 현황 수정 스키마"""
    date: Optional[date_type] = None
    time_slot: Optional[str] = Field(None, max_length=20)
    status: Optional[AvailabilityStatus] = None
    price: Optional[int] = Field(None, ge=0)


class AvailabilityResponse(AvailabilityBase):
    """예약 가능 현황 응답 스키마"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AvailabilityWithCourt(AvailabilityResponse):
    """테니스장 정보를 포함한 예약 가능 현황 응답 스키마"""
    court: "CourtResponse"

    model_config = ConfigDict(from_attributes=True)


class AvailabilityQuery(BaseModel):
    """예약 가능 현황 조회 파라미터"""
    region_id: Optional[UUID] = Field(None, description="지역 ID 필터")
    date_from: Optional[date_type] = Field(None, description="시작 날짜")
    date_to: Optional[date_type] = Field(None, description="종료 날짜")
    status: Optional[AvailabilityStatus] = Field(None, description="예약 상태 필터")
    court_id: Optional[UUID] = Field(None, description="테니스장 ID 필터")
