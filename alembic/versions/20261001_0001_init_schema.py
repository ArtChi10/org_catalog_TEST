"""init schema

Revision ID: 20261001_0001
Revises:
Create Date: 2026-10-01 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20261001_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["parent_id"], ["activities.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_activities_id"), "activities", ["id"], unique=False)

    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("address"),
    )
    op.create_index(op.f("ix_buildings_id"), "buildings", ["id"], unique=False)

    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["building_id"], ["buildings.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_organizations_id"), "organizations", ["id"], unique=False)
    op.create_index(op.f("ix_organizations_name"), "organizations", ["name"], unique=False)

    op.create_table(
        "organization_activity",
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["activity_id"], ["activities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("organization_id", "activity_id"),
    )

    op.create_table(
        "phones",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("number", sa.String(length=50), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("phones")
    op.drop_table("organization_activity")
    op.drop_index(op.f("ix_organizations_name"), table_name="organizations")
    op.drop_index(op.f("ix_organizations_id"), table_name="organizations")
    op.drop_table("organizations")
    op.drop_index(op.f("ix_buildings_id"), table_name="buildings")
    op.drop_table("buildings")
    op.drop_index(op.f("ix_activities_id"), table_name="activities")
    op.drop_table("activities")