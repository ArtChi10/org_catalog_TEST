from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float
from app.models.base import Base


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    organizations = relationship("Organization", back_populates="building", cascade="all, delete")