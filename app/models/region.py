from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.court import Court


class Region(Base):
    """지역 정보 모델 (서울 구/동)"""

    __tablename__ = "regions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    courts: Mapped[list["Court"]] = relationship(
        "Court",
        back_populates="region",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Region(id={self.id}, name={self.name})>"
