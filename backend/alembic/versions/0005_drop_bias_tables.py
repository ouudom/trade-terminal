"""Drop bias_snapshots and bias_macro_context tables

Revision ID: 0005
Revises: 0004
Create Date: 2026-04-18

"""
from typing import Sequence, Union
from alembic import op

revision: str = "0005"
down_revision: Union[str, None] = "0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("idx_snapshots_active", table_name="bias_snapshots")
    op.drop_index("idx_snapshots_instrument_timeframe", table_name="bias_snapshots")
    op.drop_table("bias_macro_context")
    op.drop_table("bias_snapshots")
    op.execute("DROP TYPE IF EXISTS bias_direction")
    op.execute("DROP TYPE IF EXISTS timeframe_type")
    op.execute("DROP TYPE IF EXISTS fed_tone")
    op.execute("DROP TYPE IF EXISTS risk_sentiment")


def downgrade() -> None:
    raise NotImplementedError("Downgrade not supported — bias feature was permanently removed")
