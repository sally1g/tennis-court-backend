from datetime import datetime
from uuid import UUID
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.availability import Availability


class Court(Base):
    """테니스장 정보 모델"""

    __tablename__ = "courts"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
    )
    address: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    # Foreign Key
    region_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("regions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
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
    region: Mapped["Region"] = relationship(
        "Region",
        back_populates="courts",
        lazy="selectin",
    )
    availabilities: Mapped[list["Availability"]] = relationship(
        "Availability",
        back_populates="court",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Court(id={self.id}, name={self.name}, region_id={self.region_id})>"
