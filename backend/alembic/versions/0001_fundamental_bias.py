"""fundamental bias: instruments, data_snapshots, bias_reports, bias_report_key_levels

Revision ID: 0001
Revises:
Create Date: 2026-03-31

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table(
        "instruments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("symbol", sa.String(20), nullable=False, unique=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("asset_class", sa.String(20), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("TRUE")),
        sa.CheckConstraint(
            "asset_class IN ('commodity','forex','stock','crypto')",
            name="ck_instruments_asset_class",
        ),
    )

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
        sa.CheckConstraint(
            "horizon IN ('daily','weekly')",
            name="ck_data_snapshots_horizon",
        ),
        sa.CheckConstraint(
            "data_quality IN ('complete','partial','stale')",
            name="ck_data_snapshots_data_quality",
        ),
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
        sa.CheckConstraint(
            "horizon IN ('daily','weekly')",
            name="ck_bias_reports_horizon",
        ),
        sa.CheckConstraint(
            "bias IN ('bullish','bearish','neutral')",
            name="ck_bias_reports_bias",
        ),
        sa.CheckConstraint(
            "confidence_pct BETWEEN 0 AND 100",
            name="ck_bias_reports_confidence_pct",
        ),
        sa.UniqueConstraint("instrument_id", "horizon", "period_start", name="uq_bias_reports_instrument_horizon_period"),
    )

    op.create_table(
        "bias_report_key_levels",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "bias_report_id",
            sa.BigInteger(),
            sa.ForeignKey("bias_reports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("zone_type", sa.String(20), nullable=False),
        sa.Column("price_high", sa.Numeric(12, 4), nullable=False),
        sa.Column("price_low", sa.Numeric(12, 4), nullable=False),
        sa.Column("timeframe", sa.String(5), nullable=True),
        sa.Column("strength", sa.String(10), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "zone_type IN ('supply','demand','support','resistance')",
            name="ck_key_levels_zone_type",
        ),
        sa.CheckConstraint(
            "timeframe IN ('W1','D1','H4','H1')",
            name="ck_key_levels_timeframe",
        ),
        sa.CheckConstraint(
            "strength IN ('weak','moderate','strong')",
            name="ck_key_levels_strength",
        ),
    )

    op.create_index("idx_bias_reports_lookup", "bias_reports", ["instrument_id", "horizon", sa.text("period_start DESC")])
    op.create_index("idx_snapshots_instrument", "data_snapshots", ["instrument_id", sa.text("fetched_at DESC")])
    op.create_index("idx_key_levels_report", "bias_report_key_levels", ["bias_report_id"])


def downgrade() -> None:
    op.drop_index("idx_key_levels_report", table_name="bias_report_key_levels")
    op.drop_index("idx_snapshots_instrument", table_name="data_snapshots")
    op.drop_index("idx_bias_reports_lookup", table_name="bias_reports")

    op.drop_table("bias_report_key_levels")
    op.drop_table("bias_reports")
    op.drop_table("data_snapshots")
    op.drop_table("instruments")

    op.execute("DROP EXTENSION IF EXISTS pgcrypto")
