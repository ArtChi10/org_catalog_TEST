from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, Integer, ForeignKey
from app.models.base import Base
from app.models.association import organization_activity


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("activities.id"), nullable=True)

    parent = relationship("Activity", remote_side=[id], back_populates="children")
    children = relationship("Activity", back_populates="parent")
    organizations = relationship(
        "Organization",
        secondary=organization_activity,
        back_populates="activities",
    )

    @validates("parent")
    def validate_parent(self, key, parent):
        if parent is None:
            return parent

        depth = 1
        current = parent
        while current is not None:
            depth += 1
            if depth > 3:
                raise ValueError("Activity nesting level cannot exceed 3")
            current = current.parent
        return parent