from typing import Any, Optional
from datetime import date as Date, datetime
from decimal import Decimal
import uuid

import sqlalchemy as sa
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Date as SADate, Numeric, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB


class WeeklyForecast(SQLModel, table=True):
    __tablename__ = "weekly_forecasts"
    __table_args__ = (
        UniqueConstraint("instrument_id", "week_of", name="uq_weekly_forecast"),
    )

    id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")),
    )
    instrument_id: int = Field(
        sa_column=Column(sa.Integer, sa.ForeignKey("instruments.id", ondelete="CASCADE"), nullable=False)
    )
    week_of: Optional[Date] = Field(default=None, sa_column=Column(SADate, nullable=False))
    generated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    generated_by: str = Field(max_length=50, default="claude", nullable=False)

    # Technical
    technical_bias: Optional[str] = Field(default=None, max_length=10)
    technical_ai_analysis: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
    technical_key_drivers: Optional[Any] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    technical_invalidation: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
    key_zone_high: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 4), nullable=True))
    key_zone_low: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 4), nullable=True))
    invalidation_level: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 4), nullable=True))
    trend_structure: Optional[str] = Field(default=None, max_length=20)
    premium_discount: Optional[str] = Field(default=None, max_length=15)
    weekly_high: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 4), nullable=True))
    weekly_low: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 4), nullable=True))

    # Sentimental
    sentiment_bias: Optional[str] = Field(default=None, max_length=10)
    sentiment_ai_analysis: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
    sentiment_key_drivers: Optional[Any] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    sentiment_invalidation: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
    retail_long_pct: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(5, 2), nullable=True))
    retail_short_pct: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(5, 2), nullable=True))
    cot_net_position: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 0), nullable=True))
    cot_change_week: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 0), nullable=True))

    # Composite
    overall_bias: Optional[str] = Field(default=None, max_length=10)
    confidence: Optional[str] = Field(default=None, max_length=10)
    high_impact_events: Optional[Any] = Field(default=None, sa_column=Column(JSONB, nullable=True))


class DailyValidation(SQLModel, table=True):
    __tablename__ = "daily_validations"
    __table_args__ = (
        UniqueConstraint("forecast_id", "date", name="uq_daily_validation"),
    )

    id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")),
    )
    forecast_id: Optional[uuid.UUID] = Field(
        default=None,
        sa_column=Column(
            PG_UUID(as_uuid=True),
            sa.ForeignKey("weekly_forecasts.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    instrument_id: int = Field(
        sa_column=Column(sa.Integer, sa.ForeignKey("instruments.id", ondelete="CASCADE"), nullable=False)
    )
    validation_date: Optional[Date] = Field(
        default=None,
        sa_column=Column("date", SADate, nullable=False),
    )
    validated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    status: str = Field(max_length=15, nullable=False)
    bias_still_intact: Optional[bool] = Field(default=None)
    price_respecting_zone: Optional[bool] = Field(default=None)
    news_risk: Optional[bool] = Field(default=None)
    structural_shift: Optional[bool] = Field(default=None)
    notes: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
    ai_review: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
    invalidation_triggered: bool = Field(default=False, nullable=False)
