"""Restructure weekly_forecasts: add fundamental/orderflow/overall fields, drop removed columns

Revision ID: 0006
Revises: 0005
Create Date: 2026-04-18

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "0006"
down_revision: Union[str, None] = "0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Drop removed technical columns ─────────────────────────────────────────
    op.drop_column("weekly_forecasts", "technical_key_drivers")
    op.drop_column("weekly_forecasts", "key_zone_high")
    op.drop_column("weekly_forecasts", "key_zone_low")
    op.drop_column("weekly_forecasts", "invalidation_level")
    op.drop_column("weekly_forecasts", "trend_structure")
    op.drop_column("weekly_forecasts", "premium_discount")

    # ── Drop removed sentimental column ───────────────────────────────────────
    op.drop_column("weekly_forecasts", "sentiment_key_drivers")

    # ── Add new technical columns ──────────────────────────────────────────────
    op.add_column("weekly_forecasts", sa.Column("weekly_structure", sa.String(20), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("daily_trend_structure", sa.String(20), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("h4_trend_structure", sa.String(20), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("supply_demand_zones", JSONB(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("support_resistance_zones", JSONB(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("order_flow", JSONB(), nullable=True))

    # ── Add fundamental section ────────────────────────────────────────────────
    op.add_column("weekly_forecasts", sa.Column("fundamental_bias", sa.String(10), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("fundamental_ai_analysis", sa.Text(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("fundamental_key_drivers", JSONB(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("fundamental_invalidation", sa.Text(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("fundamental_news", JSONB(), nullable=True))

    # ── Add overall fields ─────────────────────────────────────────────────────
    op.add_column("weekly_forecasts", sa.Column("overall_ai_analysis", sa.Text(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("overall_key_drivers", JSONB(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("overall_bias_invalidation_reasons", JSONB(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("overall_setup_scenarios", JSONB(), nullable=True))


def downgrade() -> None:
    # Overall
    op.drop_column("weekly_forecasts", "overall_setup_scenarios")
    op.drop_column("weekly_forecasts", "overall_bias_invalidation_reasons")
    op.drop_column("weekly_forecasts", "overall_key_drivers")
    op.drop_column("weekly_forecasts", "overall_ai_analysis")

    # Fundamental
    op.drop_column("weekly_forecasts", "fundamental_news")
    op.drop_column("weekly_forecasts", "fundamental_invalidation")
    op.drop_column("weekly_forecasts", "fundamental_key_drivers")
    op.drop_column("weekly_forecasts", "fundamental_ai_analysis")
    op.drop_column("weekly_forecasts", "fundamental_bias")

    # Technical additions
    op.drop_column("weekly_forecasts", "order_flow")
    op.drop_column("weekly_forecasts", "support_resistance_zones")
    op.drop_column("weekly_forecasts", "supply_demand_zones")
    op.drop_column("weekly_forecasts", "h4_trend_structure")
    op.drop_column("weekly_forecasts", "daily_trend_structure")
    op.drop_column("weekly_forecasts", "weekly_structure")

    # Restore dropped columns
    op.add_column("weekly_forecasts", sa.Column("sentiment_key_drivers", JSONB(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("premium_discount", sa.String(15), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("trend_structure", sa.String(20), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("invalidation_level", sa.Numeric(12, 4), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("key_zone_low", sa.Numeric(12, 4), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("key_zone_high", sa.Numeric(12, 4), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("technical_key_drivers", JSONB(), nullable=True))
