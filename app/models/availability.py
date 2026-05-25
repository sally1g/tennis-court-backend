from datetime import datetime, date
from uuid import UUID
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey, Date, Integer, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import enum

from app.core.database import Base


class AvailabilityStatus(str, enum.Enum):
    """예약 가능 상태"""
    AVAILABLE = "available"  # 예약 가능
    RESERVED = "reserved"    # 예약됨
    UNAVAILABLE = "unavailable"  # 이용 불가


class Availability(Base):
    """테니스장 예약 가능 현황 모델"""

    __tablename__ = "availability"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    # Foreign Key
    court_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("courts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Availability Info
    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    time_slot: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="예: '09:00-10:00', '10:00-11:00'",
    )
    status: Mapped[AvailabilityStatus] = mapped_column(
        SQLEnum(AvailabilityStatus, name="availability_status"),
        nullable=False,
        default=AvailabilityStatus.AVAILABLE,
    )
    price: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="가격 (원 단위)",
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    court: Mapped["Court"] = relationship(
        "Court",
        back_populates="availabilities",
        lazy="selectin",
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "court_id",
            "date",
            "time_slot",
            name="uq_court_date_time",
        ),
        {"comment": "테니스장 예약 가능 현황"},
    )

    def __repr__(self) -> str:
        return (
            f"<Availability(id={self.id}, court_id={self.court_id}, "
            f"date={self.date}, time_slot={self.time_slot}, status={self.status})>"
        )
