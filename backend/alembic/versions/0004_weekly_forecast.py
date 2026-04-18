"""Add weekly_forecasts and daily_validations tables

Revision ID: 0004
Revises: 0003
Create Date: 2026-04-18

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "weekly_forecasts",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("instrument_id", sa.Integer(), sa.ForeignKey("instruments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("week_of", sa.Date(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("generated_by", sa.String(50), nullable=False, server_default=sa.text("'claude'")),
        # Technical
        sa.Column("technical_bias", sa.String(10), nullable=True),
        sa.Column("technical_ai_analysis", sa.Text(), nullable=True),
        sa.Column("technical_key_drivers", JSONB(), nullable=True),
        sa.Column("technical_invalidation", sa.Text(), nullable=True),
        sa.Column("key_zone_high", sa.Numeric(12, 4), nullable=True),
        sa.Column("key_zone_low", sa.Numeric(12, 4), nullable=True),
        sa.Column("invalidation_level", sa.Numeric(12, 4), nullable=True),
        sa.Column("trend_structure", sa.String(20), nullable=True),
        sa.Column("premium_discount", sa.String(15), nullable=True),
        sa.Column("weekly_high", sa.Numeric(12, 4), nullable=True),
        sa.Column("weekly_low", sa.Numeric(12, 4), nullable=True),
        # Sentimental
        sa.Column("sentiment_bias", sa.String(10), nullable=True),
        sa.Column("sentiment_ai_analysis", sa.Text(), nullable=True),
        sa.Column("sentiment_key_drivers", JSONB(), nullable=True),
        sa.Column("sentiment_invalidation", sa.Text(), nullable=True),
        sa.Column("retail_long_pct", sa.Numeric(5, 2), nullable=True),
        sa.Column("retail_short_pct", sa.Numeric(5, 2), nullable=True),
        sa.Column("cot_net_position", sa.Numeric(12, 0), nullable=True),
        sa.Column("cot_change_week", sa.Numeric(12, 0), nullable=True),
        # Composite
        sa.Column("overall_bias", sa.String(10), nullable=True),
        sa.Column("confidence", sa.String(10), nullable=True),
        sa.Column("high_impact_events", JSONB(), nullable=True),
        sa.UniqueConstraint("instrument_id", "week_of", name="uq_weekly_forecast"),
    )

    op.create_index("idx_weekly_forecasts_week", "weekly_forecasts", ["week_of", "instrument_id"])

    op.create_table(
        "daily_validations",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("forecast_id", UUID(as_uuid=True), sa.ForeignKey("weekly_forecasts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("instrument_id", sa.Integer(), sa.ForeignKey("instruments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("validated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("status", sa.String(15), nullable=False),
        sa.Column("bias_still_intact", sa.Boolean(), nullable=True),
        sa.Column("price_respecting_zone", sa.Boolean(), nullable=True),
        sa.Column("news_risk", sa.Boolean(), nullable=True),
        sa.Column("structural_shift", sa.Boolean(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("ai_review", sa.Text(), nullable=True),
        sa.Column("invalidation_triggered", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.UniqueConstraint("forecast_id", "date", name="uq_daily_validation"),
        # note: SQLModel maps validation_date → "date" column via sa_column
    )

    op.create_index("idx_daily_validations_date", "daily_validations", ["date", "instrument_id"])


def downgrade() -> None:
    op.drop_index("idx_daily_validations_date", table_name="daily_validations")
    op.drop_table("daily_validations")
    op.drop_index("idx_weekly_forecasts_week", table_name="weekly_forecasts")
    op.drop_table("weekly_forecasts")
