from uuid import UUID
from typing import List, Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_db
from app.models import Availability, Court
from app.models.availability import AvailabilityStatus
from app.schemas import (
    AvailabilityCreate,
    AvailabilityUpdate,
    AvailabilityResponse,
    AvailabilityWithCourt,
)

router = APIRouter()


@router.get("", response_model=List[AvailabilityWithCourt])
async def list_availability(
    skip: int = 0,
    limit: int = 100,
    court_id: Optional[UUID] = Query(None, description="테니스장 ID로 필터링"),
    date_from: Optional[date] = Query(None, description="시작 날짜"),
    date_to: Optional[date] = Query(None, description="종료 날짜"),
    status: Optional[AvailabilityStatus] = Query(None, description="예약 상태로 필터링"),
    db: AsyncSession = Depends(get_db),
):
    """
    예약 가능 현황 목록 조회
    """
    query = select(Availability).options(selectinload(Availability.court))

    filters = []
    if court_id:
        filters.append(Availability.court_id == court_id)
    if date_from:
        filters.append(Availability.date >= date_from)
    if date_to:
        filters.append(Availability.date <= date_to)
    if status:
        filters.append(Availability.status == status)

    if filters:
        query = query.where(and_(*filters))

    query = query.offset(skip).limit(limit).order_by(
        Availability.date,
        Availability.time_slot
    )

    result = await db.execute(query)
    availabilities = result.scalars().all()

    return availabilities


@router.get("/{availability_id}", response_model=AvailabilityWithCourt)
async def get_availability(
    availability_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    특정 예약 가능 현황 상세 정보 조회
    """
    result = await db.execute(
        select(Availability)
        .options(selectinload(Availability.court))
        .where(Availability.id == availability_id)
    )
    availability = result.scalar_one_or_none()

    if not availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Availability with id {availability_id} not found"
        )

    return availability


@router.post("", response_model=AvailabilityResponse, status_code=status.HTTP_201_CREATED)
async def create_availability(
    availability_in: AvailabilityCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    새 예약 가능 현황 생성
    """
    # Verify court exists
    result = await db.execute(
        select(Court).where(Court.id == availability_in.court_id)
    )
    court = result.scalar_one_or_none()

    if not court:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Court with id {availability_in.court_id} not found"
        )

    # Check for duplicate (court_id, date, time_slot)
    result = await db.execute(
        select(Availability).where(
            and_(
                Availability.court_id == availability_in.court_id,
                Availability.date == availability_in.date,
                Availability.time_slot == availability_in.time_slot
            )
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Availability for court {availability_in.court_id} "
                   f"on {availability_in.date} at {availability_in.time_slot} already exists"
        )

    availability = Availability(**availability_in.model_dump())
    db.add(availability)
    await db.commit()
    await db.refresh(availability)

    return availability


@router.put("/{availability_id}", response_model=AvailabilityResponse)
async def update_availability(
    availability_id: UUID,
    availability_in: AvailabilityUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    예약 가능 현황 수정
    """
    result = await db.execute(
        select(Availability).where(Availability.id == availability_id)
    )
    availability = result.scalar_one_or_none()

    if not availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Availability with id {availability_id} not found"
        )

    update_data = availability_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(availability, field, value)

    await db.commit()
    await db.refresh(availability)

    return availability


@router.delete("/{availability_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_availability(
    availability_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    예약 가능 현황 삭제
    """
    result = await db.execute(
        select(Availability).where(Availability.id == availability_id)
    )
    availability = result.scalar_one_or_none()

    if not availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Availability with id {availability_id} not found"
        )

    await db.delete(availability)
    await db.commit()

    return None
