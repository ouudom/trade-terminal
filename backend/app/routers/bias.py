from datetime import datetime
from decimal import Decimal
from typing import Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from sqlalchemy import text

from app.core.database import get_session
from app.models.bias_snapshot import BiasSnapshot, BiasDirection, Timeframe
from app.models.bias_macro_context import BiasMacroContext, FedTone, RiskSentiment
from app.models.instrument import Instrument

router = APIRouter(prefix="/bias", tags=["bias"])


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


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/snapshots", response_model=list[BiasSnapshotResponse])
def get_latest_snapshots(
    timeframe: Optional[Timeframe] = None,
    session: Session = Depends(get_session),
):
    """
    Return the latest active snapshot per instrument (optionally filtered by timeframe).
    "Latest" = highest valid_from. Active = valid_until IS NULL or valid_until > now.
    """
    now = datetime.utcnow()

    # Subquery: max valid_from per (instrument_id, timeframe)
    from sqlalchemy import func
    subq = (
        select(
            BiasSnapshot.instrument_id,
            BiasSnapshot.timeframe,
            func.max(BiasSnapshot.valid_from).label("max_valid_from"),
        )
        .where(
            (BiasSnapshot.valid_until == None) | (BiasSnapshot.valid_until > now)
        )
    )
    if timeframe:
        subq = subq.where(BiasSnapshot.timeframe == timeframe)
    subq = subq.group_by(BiasSnapshot.instrument_id, BiasSnapshot.timeframe).subquery()

    stmt = (
        select(BiasSnapshot, Instrument)
        .join(Instrument, Instrument.id == BiasSnapshot.instrument_id)
        .join(
            subq,
            (BiasSnapshot.instrument_id == subq.c.instrument_id)
            & (BiasSnapshot.timeframe == subq.c.timeframe)
            & (BiasSnapshot.valid_from == subq.c.max_valid_from),
        )
    )

    rows = session.exec(stmt).all()

    results = []
    for snapshot, instrument in rows:
        macro_ctx = session.exec(
            select(BiasMacroContext).where(BiasMacroContext.snapshot_id == snapshot.id)
        ).first()

        macro_resp = None
        if macro_ctx:
            macro_resp = MacroResponse(
                dxy_trend=macro_ctx.dxy_trend,
                real_yield_10y=float(macro_ctx.real_yield_10y) if macro_ctx.real_yield_10y is not None else None,
                vix_level=macro_ctx.vix_level,
                fed_tone=macro_ctx.fed_tone.value if macro_ctx.fed_tone else None,
                risk_sentiment=macro_ctx.risk_sentiment.value if macro_ctx.risk_sentiment else None,
                geopolitical_notes=macro_ctx.geopolitical_notes,
            )

        results.append(BiasSnapshotResponse(
            snapshot_id=snapshot.id,
            instrument_id=snapshot.instrument_id,
            symbol=instrument.symbol,
            name=instrument.name,
            timeframe=snapshot.timeframe.value,
            bias=snapshot.bias.value,
            confidence=snapshot.confidence,
            summary=snapshot.summary,
            key_drivers=snapshot.key_drivers,
            invalidation_notes=snapshot.invalidation_notes,
            valid_from=snapshot.valid_from,
            valid_until=snapshot.valid_until,
            macro=macro_resp,
        ))

    return results


@router.post("/insert-bias", response_model=InsertBiasResponse)
def insert_bias(
    payloads: list[BiasPayload],
    session: Session = Depends(get_session),
):
    """
    Upsert a batch of bias snapshots (and optional macro context).
    Idempotent on (instrument_id, timeframe, valid_from).
    """
    if not payloads:
        raise HTTPException(status_code=422, detail="Payload list is empty.")

    results: list[BiasInsertResult] = []

    for p in payloads:
        # Check for existing snapshot to determine insert vs update
        existing = session.exec(
            select(BiasSnapshot).where(
                BiasSnapshot.instrument_id == p.instrument_id,
                BiasSnapshot.timeframe == p.timeframe,
                BiasSnapshot.valid_from == p.valid_from,
            )
        ).first()

        if existing:
            # Update in place
            existing.bias = p.bias
            existing.confidence = p.confidence
            existing.summary = p.summary
            existing.key_drivers = p.key_drivers
            existing.invalidation_notes = p.invalidation_notes
            existing.valid_until = p.valid_until
            session.add(existing)
            session.flush()
            snapshot = existing
            action = "updated"
        else:
            snapshot = BiasSnapshot(
                instrument_id=p.instrument_id,
                timeframe=p.timeframe,
                bias=p.bias,
                confidence=p.confidence,
                summary=p.summary,
                key_drivers=p.key_drivers,
                invalidation_notes=p.invalidation_notes,
                generated_by="claude",
                valid_from=p.valid_from,
                valid_until=p.valid_until,
            )
            session.add(snapshot)
            session.flush()  # populate snapshot.id
            action = "inserted"

        # Upsert macro context
        if p.macro:
            existing_macro = session.exec(
                select(BiasMacroContext).where(
                    BiasMacroContext.snapshot_id == snapshot.id
                )
            ).first()

            macro_data = p.macro
            if existing_macro:
                existing_macro.dxy_trend = macro_data.dxy_trend
                existing_macro.real_yield_10y = (
                    Decimal(str(macro_data.real_yield_10y))
                    if macro_data.real_yield_10y is not None
                    else None
                )
                existing_macro.vix_level = macro_data.vix_level
                existing_macro.fed_tone = macro_data.fed_tone
                existing_macro.risk_sentiment = macro_data.risk_sentiment
                existing_macro.geopolitical_notes = macro_data.geopolitical_notes
                session.add(existing_macro)
            else:
                macro_ctx = BiasMacroContext(
                    snapshot_id=snapshot.id,
                    dxy_trend=macro_data.dxy_trend,
                    real_yield_10y=(
                        Decimal(str(macro_data.real_yield_10y))
                        if macro_data.real_yield_10y is not None
                        else None
                    ),
                    vix_level=macro_data.vix_level,
                    fed_tone=macro_data.fed_tone,
                    risk_sentiment=macro_data.risk_sentiment,
                    geopolitical_notes=macro_data.geopolitical_notes,
                )
                session.add(macro_ctx)

        results.append(
            BiasInsertResult(
                snapshot_id=snapshot.id,
                instrument_id=p.instrument_id,
                action=action,
            )
        )

    session.commit()
    return InsertBiasResponse(inserted=len(results), results=results)
