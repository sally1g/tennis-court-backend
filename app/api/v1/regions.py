from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_db
from app.models import Region
from app.schemas import (
    RegionCreate,
    RegionUpdate,
    RegionResponse,
    RegionWithCourts,
)

router = APIRouter()


@router.get("", response_model=List[RegionResponse])
async def list_regions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """
    모든 지역 목록 조회
    """
    result = await db.execute(
        select(Region).offset(skip).limit(limit).order_by(Region.name)
    )
    regions = result.scalars().all()
    return regions


@router.get("/{region_id}", response_model=RegionWithCourts)
async def get_region(
    region_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    특정 지역 상세 정보 조회 (테니스장 목록 포함)
    """
    result = await db.execute(
        select(Region)
        .options(selectinload(Region.courts))
        .where(Region.id == region_id)
    )
    region = result.scalar_one_or_none()

    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Region with id {region_id} not found"
        )

    return region


@router.post("", response_model=RegionResponse, status_code=status.HTTP_201_CREATED)
async def create_region(
    region_in: RegionCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    새 지역 생성
    """
    # Check if region with same name already exists
    result = await db.execute(
        select(Region).where(Region.name == region_in.name)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Region with name '{region_in.name}' already exists"
        )

    region = Region(**region_in.model_dump())
    db.add(region)
    await db.commit()
    await db.refresh(region)

    return region


@router.put("/{region_id}", response_model=RegionResponse)
async def update_region(
    region_id: UUID,
    region_in: RegionUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    지역 정보 수정
    """
    result = await db.execute(
        select(Region).where(Region.id == region_id)
    )
    region = result.scalar_one_or_none()

    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Region with id {region_id} not found"
        )

    # Update only provided fields
    update_data = region_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(region, field, value)

    await db.commit()
    await db.refresh(region)

    return region


@router.delete("/{region_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_region(
    region_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    지역 삭제 (CASCADE로 관련 테니스장도 함께 삭제됨)
    """
    result = await db.execute(
        select(Region).where(Region.id == region_id)
    )
    region = result.scalar_one_or_none()

    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Region with id {region_id} not found"
        )

    await db.delete(region)
    await db.commit()

    return None
