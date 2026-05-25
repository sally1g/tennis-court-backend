from uuid import UUID
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_db
from app.models import Court, Region
from app.schemas import (
    CourtCreate,
    CourtUpdate,
    CourtResponse,
    CourtWithRegion,
    CourtWithAvailability,
)

router = APIRouter()


@router.get("", response_model=List[CourtWithRegion])
async def list_courts(
    skip: int = 0,
    limit: int = 100,
    region_id: Optional[UUID] = Query(None, description="지역 ID로 필터링"),
    db: AsyncSession = Depends(get_db),
):
    """
    테니스장 목록 조회 (지역 정보 포함)
    """
    query = select(Court).options(selectinload(Court.region))

    if region_id:
        query = query.where(Court.region_id == region_id)

    query = query.offset(skip).limit(limit).order_by(Court.name)

    result = await db.execute(query)
    courts = result.scalars().all()

    return courts


@router.get("/{court_id}", response_model=CourtWithAvailability)
async def get_court(
    court_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    특정 테니스장 상세 정보 조회 (예약 가능 현황 포함)
    """
    result = await db.execute(
        select(Court)
        .options(
            selectinload(Court.region),
            selectinload(Court.availabilities)
        )
        .where(Court.id == court_id)
    )
    court = result.scalar_one_or_none()

    if not court:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Court with id {court_id} not found"
        )

    return court


@router.post("", response_model=CourtResponse, status_code=status.HTTP_201_CREATED)
async def create_court(
    court_in: CourtCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    새 테니스장 생성
    """
    # Verify region exists
    result = await db.execute(
        select(Region).where(Region.id == court_in.region_id)
    )
    region = result.scalar_one_or_none()

    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Region with id {court_in.region_id} not found"
        )

    court = Court(**court_in.model_dump())
    db.add(court)
    await db.commit()
    await db.refresh(court)

    return court


@router.put("/{court_id}", response_model=CourtResponse)
async def update_court(
    court_id: UUID,
    court_in: CourtUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    테니스장 정보 수정
    """
    result = await db.execute(
        select(Court).where(Court.id == court_id)
    )
    court = result.scalar_one_or_none()

    if not court:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Court with id {court_id} not found"
        )

    # If updating region_id, verify new region exists
    update_data = court_in.model_dump(exclude_unset=True)
    if "region_id" in update_data:
        result = await db.execute(
            select(Region).where(Region.id == update_data["region_id"])
        )
        region = result.scalar_one_or_none()
        if not region:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Region with id {update_data['region_id']} not found"
            )

    for field, value in update_data.items():
        setattr(court, field, value)

    await db.commit()
    await db.refresh(court)

    return court


@router.delete("/{court_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_court(
    court_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    테니스장 삭제 (CASCADE로 관련 예약 현황도 함께 삭제됨)
    """
    result = await db.execute(
        select(Court).where(Court.id == court_id)
    )
    court = result.scalar_one_or_none()

    if not court:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Court with id {court_id} not found"
        )

    await db.delete(court)
    await db.commit()

    return None
