from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from app.models.base import Base
from app.models.association import organization_activity


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=False)

    building = relationship("Building", back_populates="organizations")
    phones = relationship("Phone", back_populates="organization", cascade="all, delete-orphan")
    activities = relationship(
        "Activity",
        secondary=organization_activity,
        back_populates="organizations",
    )