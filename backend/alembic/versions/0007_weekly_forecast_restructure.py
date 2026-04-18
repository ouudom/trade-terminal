"""Complete weekly forecast restructure: collapse into JSONB sections, add instrument field, update daily validations

Revision ID: 0007
Revises: 0006
Create Date: 2026-04-18

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "0007"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── weekly_forecasts: add instrument field ─────────────────────────────────
    op.add_column("weekly_forecasts", sa.Column("instrument", sa.String(20), nullable=False, server_default=""))
    op.alter_column("weekly_forecasts", "instrument", server_default=None)

    # ── Drop all old technical/fundamental/sentimental columns ──────────────────
    # Technical columns
    op.drop_column("weekly_forecasts", "technical_bias")
    op.drop_column("weekly_forecasts", "technical_ai_analysis")
    op.drop_column("weekly_forecasts", "technical_invalidation")
    op.drop_column("weekly_forecasts", "weekly_high")
    op.drop_column("weekly_forecasts", "weekly_low")
    op.drop_column("weekly_forecasts", "weekly_structure")
    op.drop_column("weekly_forecasts", "daily_trend_structure")
    op.drop_column("weekly_forecasts", "h4_trend_structure")
    op.drop_column("weekly_forecasts", "supply_demand_zones")
    op.drop_column("weekly_forecasts", "support_resistance_zones")
    op.drop_column("weekly_forecasts", "order_flow")

    # Fundamental columns
    op.drop_column("weekly_forecasts", "fundamental_bias")
    op.drop_column("weekly_forecasts", "fundamental_ai_analysis")
    op.drop_column("weekly_forecasts", "fundamental_key_drivers")
    op.drop_column("weekly_forecasts", "fundamental_invalidation")
    op.drop_column("weekly_forecasts", "fundamental_news")

    # Sentimental columns
    op.drop_column("weekly_forecasts", "sentiment_bias")
    op.drop_column("weekly_forecasts", "sentiment_ai_analysis")
    op.drop_column("weekly_forecasts", "sentiment_invalidation")
    op.drop_column("weekly_forecasts", "retail_long_pct")
    op.drop_column("weekly_forecasts", "retail_short_pct")
    op.drop_column("weekly_forecasts", "cot_net_position")
    op.drop_column("weekly_forecasts", "cot_change_week")

    # ── Add new JSONB columns for sections ──────────────────────────────────────
    op.add_column("weekly_forecasts", sa.Column("technical", JSONB(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("fundamental", JSONB(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("sentimental", JSONB(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("confluence", JSONB(), nullable=True))

    # ── Update overall/confidence columns ───────────────────────────────────────
    # overall_ai_analysis, overall_key_drivers, overall_bias_invalidation_reasons already added in 0006
    op.drop_column("weekly_forecasts", "overall_setup_scenarios")
    op.add_column("weekly_forecasts", sa.Column("correlation_warning", sa.Text(), nullable=True))

    # ── daily_validations: add instrument, restructure columns ──────────────────
    op.add_column("daily_validations", sa.Column("instrument", sa.String(20), nullable=False, server_default=""))
    op.alter_column("daily_validations", "instrument", server_default=None)

    op.add_column("daily_validations", sa.Column("session", sa.String(20), nullable=True))
    op.add_column("daily_validations", sa.Column("price_at_zone", sa.Boolean(), nullable=True))
    op.add_column("daily_validations", sa.Column("weekly_bias_intact", sa.Boolean(), nullable=True))
    op.add_column("daily_validations", sa.Column("overnight_news_invalidation", sa.Boolean(), nullable=True))
    op.add_column("daily_validations", sa.Column("entry_trigger", JSONB(), nullable=True))
    op.add_column("daily_validations", sa.Column("tp_path_clear", sa.Boolean(), nullable=True))
    op.add_column("daily_validations", sa.Column("tp_path_blockers", JSONB(), nullable=True))

    # Drop old status/validation columns
    op.drop_column("daily_validations", "status")
    op.drop_column("daily_validations", "bias_still_intact")
    op.drop_column("daily_validations", "price_respecting_zone")
    op.drop_column("daily_validations", "news_risk")
    op.drop_column("daily_validations", "structural_shift")
    op.drop_column("daily_validations", "notes")
    op.drop_column("daily_validations", "ai_review")
    op.drop_column("daily_validations", "invalidation_triggered")

    # Add new output columns
    op.add_column("daily_validations", sa.Column("output", sa.String(20), nullable=True))
    op.add_column("daily_validations", sa.Column("output_reason", sa.Text(), nullable=True))


def downgrade() -> None:
    # daily_validations restore
    op.drop_column("daily_validations", "output_reason")
    op.drop_column("daily_validations", "output")
    op.add_column("daily_validations", sa.Column("invalidation_triggered", sa.Boolean(), nullable=False, server_default="false"))
    op.add_column("daily_validations", sa.Column("ai_review", sa.Text(), nullable=True))
    op.add_column("daily_validations", sa.Column("notes", sa.Text(), nullable=True))
    op.add_column("daily_validations", sa.Column("structural_shift", sa.Boolean(), nullable=True))
    op.add_column("daily_validations", sa.Column("news_risk", sa.Boolean(), nullable=True))
    op.add_column("daily_validations", sa.Column("price_respecting_zone", sa.Boolean(), nullable=True))
    op.add_column("daily_validations", sa.Column("bias_still_intact", sa.Boolean(), nullable=True))
    op.add_column("daily_validations", sa.Column("status", sa.String(15), nullable=False, server_default="VALID"))
    op.alter_column("daily_validations", "status", server_default=None)
    op.drop_column("daily_validations", "tp_path_blockers")
    op.drop_column("daily_validations", "tp_path_clear")
    op.drop_column("daily_validations", "entry_trigger")
    op.drop_column("daily_validations", "overnight_news_invalidation")
    op.drop_column("daily_validations", "weekly_bias_intact")
    op.drop_column("daily_validations", "price_at_zone")
    op.drop_column("daily_validations", "session")
    op.drop_column("daily_validations", "instrument")

    # weekly_forecasts restore
    op.drop_column("weekly_forecasts", "correlation_warning")
    op.add_column("weekly_forecasts", sa.Column("overall_setup_scenarios", JSONB(), nullable=True))
    # overall_ai_analysis, overall_key_drivers, overall_bias_invalidation_reasons owned by 0006 downgrade
    op.drop_column("weekly_forecasts", "confluence")
    op.drop_column("weekly_forecasts", "sentimental")
    op.drop_column("weekly_forecasts", "fundamental")
    op.drop_column("weekly_forecasts", "technical")
    op.add_column("weekly_forecasts", sa.Column("cot_change_week", sa.Numeric(12, 0), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("cot_net_position", sa.Numeric(12, 0), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("retail_short_pct", sa.Numeric(5, 2), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("retail_long_pct", sa.Numeric(5, 2), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("sentiment_invalidation", sa.Text(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("sentiment_ai_analysis", sa.Text(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("sentiment_bias", sa.String(10), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("fundamental_news", JSONB(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("fundamental_invalidation", sa.Text(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("fundamental_key_drivers", JSONB(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("fundamental_ai_analysis", sa.Text(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("fundamental_bias", sa.String(10), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("order_flow", JSONB(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("support_resistance_zones", JSONB(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("supply_demand_zones", JSONB(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("h4_trend_structure", sa.String(20), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("daily_trend_structure", sa.String(20), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("weekly_structure", sa.String(20), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("weekly_low", sa.Numeric(12, 4), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("weekly_high", sa.Numeric(12, 4), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("technical_invalidation", sa.Text(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("technical_ai_analysis", sa.Text(), nullable=True))
    op.add_column("weekly_forecasts", sa.Column("technical_bias", sa.String(10), nullable=True))
    op.drop_column("weekly_forecasts", "instrument")
