from typing import Optional
from datetime import datetime
from enum import Enum
import uuid

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Text, SmallInteger, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class BiasDirection(str, Enum):
    bullish = "bullish"
    bearish = "bearish"
    neutral = "neutral"
    bullish_bias = "bullish_bias"
    bearish_bias = "bearish_bias"


class Timeframe(str, Enum):
    weekly = "weekly"
    daily = "daily"


class BiasSnapshot(SQLModel, table=True):
    __tablename__ = "bias_snapshots"
    __table_args__ = (
        UniqueConstraint("instrument_id", "timeframe", "valid_from", name="uq_snapshot_instrument_timeframe_valid_from"),
    )

    id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")),
    )
    instrument_id: int = Field(foreign_key="instruments.id", nullable=False)
    timeframe: Timeframe = Field(nullable=False)
    bias: BiasDirection = Field(nullable=False)
    confidence: int = Field(sa_column=Column(SmallInteger, nullable=False))  # 1–5
    summary: str = Field(sa_column=Column(Text, nullable=False))
    key_drivers: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
    invalidation_notes: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
    generated_by: str = Field(max_length=50, default="claude", nullable=False)
    valid_from: datetime = Field(nullable=False)
    valid_until: Optional[datetime] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
