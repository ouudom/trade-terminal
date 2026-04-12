"""new bias schema: drop data_snapshots/bias_reports/bias_report_key_levels, add bias_snapshots/bias_macro_context

Revision ID: 0003
Revises: 0002
Create Date: 2026-04-06

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ENUM as PG_ENUM

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop old tables (in dependency order)
    op.drop_index("idx_key_levels_report", table_name="bias_report_key_levels")
    op.drop_index("idx_snapshots_instrument", table_name="data_snapshots")
    op.drop_index("idx_bias_reports_lookup", table_name="bias_reports")

    op.drop_table("bias_report_key_levels")
    op.drop_table("bias_reports")
    op.drop_table("data_snapshots")

    # Drop enum types if they exist (from a previous partial run), then recreate
    op.execute("DROP TYPE IF EXISTS bias_direction")
    op.execute("DROP TYPE IF EXISTS timeframe_type")
    op.execute("DROP TYPE IF EXISTS fed_tone")
    op.execute("DROP TYPE IF EXISTS risk_sentiment")

    op.execute("CREATE TYPE bias_direction AS ENUM ('bullish', 'bearish', 'neutral', 'bullish_bias', 'bearish_bias')")
    op.execute("CREATE TYPE timeframe_type AS ENUM ('weekly', 'daily')")
    op.execute("CREATE TYPE fed_tone AS ENUM ('dovish', 'neutral', 'hawkish', 'unknown')")
    op.execute("CREATE TYPE risk_sentiment AS ENUM ('risk_on', 'risk_off', 'neutral')")

    # Create bias_snapshots table
    op.create_table(
        "bias_snapshots",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("instrument_id", sa.Integer(), sa.ForeignKey("instruments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("timeframe", PG_ENUM("weekly", "daily", name="timeframe_type", create_type=False), nullable=False),
        sa.Column("bias", PG_ENUM("bullish", "bearish", "neutral", "bullish_bias", "bearish_bias", name="bias_direction", create_type=False), nullable=False),
        sa.Column("confidence", sa.SmallInteger(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("key_drivers", sa.Text(), nullable=True),
        sa.Column("invalidation_notes", sa.Text(), nullable=True),
        sa.Column("generated_by", sa.String(50), nullable=False, server_default=sa.text("'claude'")),
        sa.Column("valid_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.CheckConstraint("confidence BETWEEN 1 AND 5", name="ck_bias_snapshots_confidence"),
        sa.UniqueConstraint("instrument_id", "timeframe", "valid_from", name="uq_snapshot_instrument_timeframe_valid_from"),
    )

    op.create_index(
        "idx_snapshots_instrument_timeframe",
        "bias_snapshots",
        ["instrument_id", "timeframe", sa.text("valid_from DESC")],
    )
    op.create_index(
        "idx_snapshots_active",
        "bias_snapshots",
        ["valid_until"],
        postgresql_where=sa.text("valid_until IS NULL"),
    )

    # Create bias_macro_context table
    op.create_table(
        "bias_macro_context",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("snapshot_id", UUID(as_uuid=True), sa.ForeignKey("bias_snapshots.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("dxy_trend", sa.String(10), nullable=True),
        sa.Column("real_yield_10y", sa.Numeric(5, 2), nullable=True),
        sa.Column("vix_level", sa.SmallInteger(), nullable=True),
        sa.Column("fed_tone", PG_ENUM("dovish", "neutral", "hawkish", "unknown", name="fed_tone", create_type=False), nullable=True),
        sa.Column("risk_sentiment", PG_ENUM("risk_on", "risk_off", "neutral", name="risk_sentiment", create_type=False), nullable=True),
        sa.Column("geopolitical_notes", sa.Text(), nullable=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
    )


def downgrade() -> None:
    op.drop_table("bias_macro_context")

    op.drop_index("idx_snapshots_active", table_name="bias_snapshots")
    op.drop_index("idx_snapshots_instrument_timeframe", table_name="bias_snapshots")
    op.drop_table("bias_snapshots")

    op.execute("DROP TYPE IF EXISTS risk_sentiment")
    op.execute("DROP TYPE IF EXISTS fed_tone")
    op.execute("DROP TYPE IF EXISTS timeframe_type")
    op.execute("DROP TYPE IF EXISTS bias_direction")

    # Recreate old tables
    from sqlalchemy.dialects.postgresql import JSONB

    op.create_table(
        "data_snapshots",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("instrument_id", sa.Integer(), sa.ForeignKey("instruments.id"), nullable=False),
        sa.Column("horizon", sa.String(10), nullable=False),
        sa.Column("fundamental", JSONB(), nullable=True),
        sa.Column("sentiment", JSONB(), nullable=True),
        sa.Column("price", JSONB(), nullable=True),
        sa.Column("data_quality", sa.String(10), nullable=False, server_default=sa.text("'complete'")),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.CheckConstraint("horizon IN ('daily','weekly')", name="ck_data_snapshots_horizon"),
        sa.CheckConstraint("data_quality IN ('complete','partial','stale')", name="ck_data_snapshots_data_quality"),
    )

    op.create_table(
        "bias_reports",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("instrument_id", sa.Integer(), sa.ForeignKey("instruments.id"), nullable=False),
        sa.Column("snapshot_id", sa.BigInteger(), sa.ForeignKey("data_snapshots.id"), nullable=True),
        sa.Column("horizon", sa.String(10), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("bias", sa.String(10), nullable=False),
        sa.Column("confidence_pct", sa.Integer(), nullable=False),
        sa.Column("drivers", JSONB(), nullable=True),
        sa.Column("reasoning", sa.Text(), nullable=True),
        sa.Column("llm_model", sa.String(60), nullable=True),
        sa.Column("llm_tokens_used", sa.Integer(), nullable=True),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("invalidated_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("horizon IN ('daily','weekly')", name="ck_bias_reports_horizon"),
        sa.CheckConstraint("bias IN ('bullish','bearish','neutral')", name="ck_bias_reports_bias"),
        sa.CheckConstraint("confidence_pct BETWEEN 0 AND 100", name="ck_bias_reports_confidence_pct"),
        sa.UniqueConstraint("instrument_id", "horizon", "period_start", name="uq_bias_reports_instrument_horizon_period"),
    )

    op.create_table(
        "bias_report_key_levels",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("bias_report_id", sa.BigInteger(), sa.ForeignKey("bias_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("zone_type", sa.String(20), nullable=False),
        sa.Column("price_high", sa.Numeric(12, 4), nullable=False),
        sa.Column("price_low", sa.Numeric(12, 4), nullable=False),
        sa.Column("timeframe", sa.String(5), nullable=True),
        sa.Column("strength", sa.String(10), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.CheckConstraint("zone_type IN ('supply','demand','support','resistance')", name="ck_key_levels_zone_type"),
        sa.CheckConstraint("timeframe IN ('W1','D1','H4','H1')", name="ck_key_levels_timeframe"),
        sa.CheckConstraint("strength IN ('weak','moderate','strong')", name="ck_key_levels_strength"),
    )

    op.create_index("idx_bias_reports_lookup", "bias_reports", ["instrument_id", "horizon", sa.text("period_start DESC")])
    op.create_index("idx_snapshots_instrument", "data_snapshots", ["instrument_id", sa.text("fetched_at DESC")])
    op.create_index("idx_key_levels_report", "bias_report_key_levels", ["bias_report_id"])
