from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum
import uuid

from sqlmodel import SQLModel, Field, Column
import sqlalchemy as sa
from sqlalchemy import Text, SmallInteger, Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class FedTone(str, Enum):
    dovish = "dovish"
    neutral = "neutral"
    hawkish = "hawkish"
    unknown = "unknown"


class RiskSentiment(str, Enum):
    risk_on = "risk_on"
    risk_off = "risk_off"
    neutral = "neutral"


class BiasMacroContext(SQLModel, table=True):
    __tablename__ = "bias_macro_context"

    id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"),
    )
    snapshot_id: uuid.UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            sa.ForeignKey("bias_snapshots.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        )
    )
    dxy_trend: Optional[str] = Field(default=None, max_length=10, nullable=True)
    real_yield_10y: Optional[Decimal] = Field(
        default=None, sa_column=Column(Numeric(5, 2), nullable=True)
    )
    vix_level: Optional[int] = Field(
        default=None, sa_column=Column(SmallInteger, nullable=True)
    )
    fed_tone: Optional[FedTone] = Field(default=None, nullable=True)
    risk_sentiment: Optional[RiskSentiment] = Field(default=None, nullable=True)
    geopolitical_notes: Optional[str] = Field(
        default=None, sa_column=Column(Text, nullable=True)
    )
    captured_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
