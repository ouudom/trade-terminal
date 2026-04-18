from __future__ import annotations

import uuid
from datetime import date
from typing import Any, Optional

from pydantic import BaseModel


# ── Request sub-schemas ────────────────────────────────────────────────────────

class TechnicalPayload(BaseModel):
    bias: Optional[str] = None                       # bullish | bearish | neutral
    ai_analysis: Optional[str] = None
    key_drivers: Optional[list[str]] = None
    invalidation: Optional[str] = None
    key_zone_high: Optional[float] = None
    key_zone_low: Optional[float] = None
    invalidation_level: Optional[float] = None
    trend_structure: Optional[str] = None            # HH_HL | LH_LL | RANGING
    premium_discount: Optional[str] = None           # PREMIUM | DISCOUNT | EQUILIBRIUM
    weekly_high: Optional[float] = None
    weekly_low: Optional[float] = None


class SentimentalPayload(BaseModel):
    bias: Optional[str] = None
    ai_analysis: Optional[str] = None
    key_drivers: Optional[list[str]] = None
    invalidation: Optional[str] = None
    retail_long_pct: Optional[float] = None
    retail_short_pct: Optional[float] = None
    cot_net_position: Optional[float] = None
    cot_change_week: Optional[float] = None


# ── Request schemas ────────────────────────────────────────────────────────────

class WeeklyForecastPayload(BaseModel):
    instrument_id: int
    week_of: date
    technical: Optional[TechnicalPayload] = None
    sentimental: Optional[SentimentalPayload] = None
    overall_bias: Optional[str] = None
    confidence: Optional[str] = None                 # HIGH | MEDIUM | LOW
    high_impact_events: Optional[list[dict[str, Any]]] = None


class DailyValidationPayload(BaseModel):
    instrument_id: int
    date: date
    status: str                                      # VALID | WATCH | INVALIDATED
    bias_still_intact: Optional[bool] = None
    price_respecting_zone: Optional[bool] = None
    news_risk: Optional[bool] = None
    structural_shift: Optional[bool] = None
    invalidation_triggered: bool = False
    notes: Optional[str] = None
    ai_review: Optional[str] = None


# ── Response schemas ───────────────────────────────────────────────────────────

class LatestWeekResponse(BaseModel):
    week_of: Optional[date]


class UpsertForecastResponse(BaseModel):
    upserted: int
    week_of: date


class UpsertValidationResponse(BaseModel):
    upserted: int
    date: date


class WeeklyForecastResponse(BaseModel):
    id: uuid.UUID
    instrument_id: int
    symbol: str
    week_of: date
    generated_by: str
    technical_bias: Optional[str]
    technical_ai_analysis: Optional[str]
    technical_key_drivers: Optional[Any]
    technical_invalidation: Optional[str]
    key_zone_high: Optional[float]
    key_zone_low: Optional[float]
    invalidation_level: Optional[float]
    trend_structure: Optional[str]
    premium_discount: Optional[str]
    weekly_high: Optional[float]
    weekly_low: Optional[float]
    sentiment_bias: Optional[str]
    sentiment_ai_analysis: Optional[str]
    sentiment_key_drivers: Optional[Any]
    sentiment_invalidation: Optional[str]
    retail_long_pct: Optional[float]
    retail_short_pct: Optional[float]
    cot_net_position: Optional[float]
    cot_change_week: Optional[float]
    overall_bias: Optional[str]
    confidence: Optional[str]
    high_impact_events: Optional[Any]


class DailyValidationResponse(BaseModel):
    id: uuid.UUID
    forecast_id: uuid.UUID
    instrument_id: int
    symbol: str
    date: date
    status: str
    bias_still_intact: Optional[bool]
    price_respecting_zone: Optional[bool]
    news_risk: Optional[bool]
    structural_shift: Optional[bool]
    notes: Optional[str]
    ai_review: Optional[str]
    invalidation_triggered: bool
