from __future__ import annotations

import uuid
from datetime import date
from typing import Any, Optional

from pydantic import BaseModel


# ── Technical sub-schemas ──────────────────────────────────────────────────────

class PremiumDiscount(BaseModel):
    context: str  # premium | discount | equilibrium
    current_price: float
    note: Optional[str] = None


class TrendStructure(BaseModel):
    weekly: str  # bullish | bearish | ranging
    daily: str
    h4: str
    aligned: bool


class SupplyDemandZone(BaseModel):
    type: str  # supply | demand
    high: float
    low: float
    timeframe: str  # W1 | D1 | H4 | H1 | M15
    freshness: str  # fresh | tested | broken
    tested_count: int = 0
    strength: str  # strong | moderate | weak
    confluence_notes: Optional[str] = None


class SupportResistanceLevel(BaseModel):
    level: float
    type: str  # support | resistance
    strength: str  # strong | moderate | weak
    note: Optional[str] = None


class VolumeProfile(BaseModel):
    timeframe: str
    poc: float  # Point of Control
    vah: float  # Value Area High
    val: float  # Value Area Low
    price_vs_value_area: str  # above_vah | within_va | below_val


class LiquiditySweep(BaseModel):
    side: str  # buy_side | sell_side
    level: float
    swept: bool
    implication: Optional[str] = None


class Imbalance(BaseModel):
    type: str  # buy | sell
    price: float
    timeframe: str


class OrderFlowData(BaseModel):
    volume_profile: Optional[VolumeProfile] = None
    cumulative_delta_4h: Optional[str] = None  # bullish | bearish | neutral
    delta_at_key_zone: Optional[str] = None
    liquidity_sweeps: Optional[list[LiquiditySweep]] = None
    imbalances: Optional[list[Imbalance]] = None
    summary: Optional[str] = None


class TechnicalPayload(BaseModel):
    bias: Optional[str] = None  # bullish | bearish | neutral
    ai_analysis: Optional[str] = None
    invalidation: Optional[str] = None
    weekly_high: Optional[float] = None
    weekly_low: Optional[float] = None
    weekly_midpoint: Optional[float] = None
    premium_discount: Optional[PremiumDiscount] = None
    trend_structure: Optional[TrendStructure] = None
    supply_demand_zones: Optional[list[SupplyDemandZone]] = None
    support_resistance_levels: Optional[list[SupportResistanceLevel]] = None
    order_flow: Optional[OrderFlowData] = None


# ── Fundamental sub-schemas ───────────────────────────────────────────────────

class NewsEvent(BaseModel):
    day: str
    event: str
    currency: str
    impact: str  # high | medium | low
    forecast: Optional[str] = None
    previous: Optional[str] = None
    actual: Optional[str] = None
    bias_impact_if_above: Optional[str] = None
    bias_impact_if_below: Optional[str] = None


class FundamentalPayload(BaseModel):
    bias: Optional[str] = None  # bullish | bearish | neutral
    ai_analysis: Optional[str] = None
    invalidation: Optional[str] = None
    key_drivers: Optional[list[str]] = None
    dxy_bias: Optional[str] = None  # bullish | bearish | neutral
    news: Optional[list[NewsEvent]] = None


# ── Sentimental sub-schemas ───────────────────────────────────────────────────

class SentimentalPayload(BaseModel):
    bias: Optional[str] = None
    ai_analysis: Optional[str] = None
    invalidation: Optional[str] = None
    retail_long_pct: Optional[float] = None
    retail_short_pct: Optional[float] = None
    retail_extreme: Optional[bool] = None
    retail_signal: Optional[str] = None  # contrarian_bullish | contrarian_bearish | aligned
    cot_net_position: Optional[float] = None
    cot_change_week: Optional[float] = None
    cot_trend_direction: Optional[str] = None  # increasing | decreasing
    cot_trend_weeks: Optional[int] = None
    smart_money_vs_retail: Optional[str] = None


# ── Confluence section ─────────────────────────────────────────────────────────

class ConfluenceData(BaseModel):
    factors_aligned: Optional[list[str]] = None
    factor_count: int = 0
    score: str  # HIGH | MEDIUM | LOW


# ── Setup scenarios ────────────────────────────────────────────────────────────

class SetupScenario(BaseModel):
    entry_zone: Optional[list[float]] = None
    stop: Optional[float] = None
    target_1r2: Optional[float] = None
    target_1r3: Optional[float] = None
    sl_pips: Optional[int] = None
    lot_size: Optional[float] = None
    r_ratio_min: Optional[float] = None
    narrative: Optional[str] = None
    valid_if: Optional[str] = None


class SetupScenarios(BaseModel):
    primary: Optional[str] = None  # buy | sell
    buy: Optional[SetupScenario] = None
    sell: Optional[SetupScenario] = None


# ── Request schemas ────────────────────────────────────────────────────────────

class WeeklyForecastPayload(BaseModel):
    instrument_id: int
    instrument: str
    week_of: date
    technical: Optional[TechnicalPayload] = None
    fundamental: Optional[FundamentalPayload] = None
    sentimental: Optional[SentimentalPayload] = None
    confluence: Optional[ConfluenceData] = None
    overall_bias: Optional[str] = None
    overall_ai_analysis: Optional[str] = None
    overall_key_drivers: Optional[list[str]] = None
    overall_bias_invalidation_reasons: Optional[list[str]] = None
    overall_setup_scenarios: Optional[SetupScenarios] = None
    confidence: Optional[str] = None  # HIGH | MEDIUM | LOW
    correlation_warning: Optional[str] = None
    high_impact_events: Optional[list[dict[str, Any]]] = None


# ── Daily validation ───────────────────────────────────────────────────────────

class EntryTrigger(BaseModel):
    liquidity_sweep: Optional[bool] = None
    sweep_level: Optional[float] = None
    sweep_side: Optional[str] = None
    adds_strength: Optional[bool] = None
    engulfing_15m: Optional[bool] = None
    bos_choch_15m: Optional[str] = None  # BOS | CHoCH
    bos_choch_level: Optional[float] = None
    pullback_entry: Optional[dict[str, Any]] = None


class DailyValidationPayload(BaseModel):
    instrument_id: int
    date: date
    session: Optional[str] = None  # london_open | ny_open | asia_open
    price_at_zone: Optional[bool] = None
    weekly_bias_intact: Optional[bool] = None
    overnight_news_invalidation: Optional[bool] = None
    entry_trigger: Optional[EntryTrigger] = None
    tp_path_clear: Optional[bool] = None
    tp_path_blockers: Optional[list[str]] = None
    output: Optional[str] = None  # SETUP | WAIT | INVALIDATED
    output_reason: Optional[str] = None


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
    instrument: str
    week_of: date
    generated_by: str
    technical: Optional[Any]
    fundamental: Optional[Any]
    sentimental: Optional[Any]
    confluence: Optional[Any]
    overall_bias: Optional[str]
    overall_ai_analysis: Optional[str]
    overall_key_drivers: Optional[Any]
    overall_bias_invalidation_reasons: Optional[Any]
    overall_setup_scenarios: Optional[Any]
    confidence: Optional[str]
    correlation_warning: Optional[str]
    high_impact_events: Optional[Any]


class DailyValidationResponse(BaseModel):
    id: uuid.UUID
    forecast_id: uuid.UUID
    instrument_id: int
    instrument: str
    date: date
    session: Optional[str]
    price_at_zone: Optional[bool]
    weekly_bias_intact: Optional[bool]
    overnight_news_invalidation: Optional[bool]
    entry_trigger: Optional[Any]
    tp_path_clear: Optional[bool]
    tp_path_blockers: Optional[Any]
    output: Optional[str]
    output_reason: Optional[str]
