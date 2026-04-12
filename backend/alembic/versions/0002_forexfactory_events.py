"""forexfactory_events table

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-02

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "forexfactory_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("currency", sa.String(10), nullable=False),
        sa.Column("event_name", sa.String(200), nullable=False),
        sa.Column("date", sa.String(50), nullable=True),
        sa.Column("time", sa.String(20), nullable=True),
        sa.Column("impact", sa.String(20), nullable=False),
        sa.Column("actual", sa.String(50), nullable=True),
        sa.Column("forecast", sa.String(50), nullable=True),
        sa.Column("previous", sa.String(50), nullable=True),
        sa.Column(
            "fetched_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.UniqueConstraint("currency", "event_name", "date", name="uq_ff_event"),
    )


def downgrade() -> None:
    op.drop_table("forexfactory_events")
