"""
Pydantic request/response schemas for the bias endpoints.
Extracted from app/routers/bias.py.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.bias_snapshot import BiasDirection, Timeframe
from app.models.bias_macro_context import FedTone, RiskSentiment


# ── Request schemas ────────────────────────────────────────────────────────────

class MacroPayload(BaseModel):
    dxy_trend: Optional[str] = None
    real_yield_10y: Optional[float] = None
    vix_level: Optional[int] = None
    fed_tone: Optional[FedTone] = None
    risk_sentiment: Optional[RiskSentiment] = None
    geopolitical_notes: Optional[str] = None


class BiasPayload(BaseModel):
    instrument_id: int
    timeframe: Timeframe
    bias: BiasDirection
    confidence: int  # 1–5
    summary: str
    key_drivers: Optional[str] = None
    invalidation_notes: Optional[str] = None
    valid_from: datetime
    valid_until: Optional[datetime] = None
    macro: Optional[MacroPayload] = None


# ── Response schemas ───────────────────────────────────────────────────────────

class BiasInsertResult(BaseModel):
    snapshot_id: uuid.UUID
    instrument_id: int
    action: str  # "inserted" | "updated"


class InsertBiasResponse(BaseModel):
    inserted: int
    results: list[BiasInsertResult]


class MacroResponse(BaseModel):
    dxy_trend: Optional[str]
    real_yield_10y: Optional[float]
    vix_level: Optional[int]
    fed_tone: Optional[str]
    risk_sentiment: Optional[str]
    geopolitical_notes: Optional[str]


class BiasSnapshotResponse(BaseModel):
    snapshot_id: uuid.UUID
    instrument_id: int
    symbol: str
    name: str
    timeframe: str
    bias: str
    confidence: int
    summary: str
    key_drivers: Optional[str]
    invalidation_notes: Optional[str]
    valid_from: datetime
    valid_until: Optional[datetime]
    macro: Optional[MacroResponse]
