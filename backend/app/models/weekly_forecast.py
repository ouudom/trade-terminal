from typing import Any, Optional
from datetime import date as Date, datetime
import uuid

import sqlalchemy as sa
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Date as SADate, Text, UniqueConstraint, text
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
    instrument: str = Field(max_length=20, nullable=False)
    week_of: Optional[Date] = Field(default=None, sa_column=Column(SADate, nullable=False))
    generated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    generated_by: str = Field(max_length=50, default="claude", nullable=False)

    # Stored as JSONB for complex nested structures
    technical: Optional[Any] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    fundamental: Optional[Any] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    sentimental: Optional[Any] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    confluence: Optional[Any] = Field(default=None, sa_column=Column(JSONB, nullable=True))

    # Overall
    overall_bias: Optional[str] = Field(default=None, max_length=10)
    overall_ai_analysis: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
    overall_key_drivers: Optional[Any] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    overall_bias_invalidation_reasons: Optional[Any] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    overall_setup_scenarios: Optional[Any] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    confidence: Optional[str] = Field(default=None, max_length=10)
    correlation_warning: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
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
    instrument: str = Field(max_length=20, nullable=False)
    validation_date: Optional[Date] = Field(
        default=None,
        sa_column=Column("date", SADate, nullable=False),
    )
    validated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    session: Optional[str] = Field(default=None, max_length=20)
    price_at_zone: Optional[bool] = Field(default=None)
    weekly_bias_intact: Optional[bool] = Field(default=None)
    overnight_news_invalidation: Optional[bool] = Field(default=None)
    entry_trigger: Optional[Any] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    tp_path_clear: Optional[bool] = Field(default=None)
    tp_path_blockers: Optional[Any] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    output: Optional[str] = Field(default=None, max_length=20)
    output_reason: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
