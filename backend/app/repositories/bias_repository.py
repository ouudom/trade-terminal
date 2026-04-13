from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.bias_snapshot import BiasSnapshot, BiasDirection, Timeframe
from app.models.bias_macro_context import BiasMacroContext
from app.models.instrument import Instrument


class BiasRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_latest_active_snapshots(
        self, timeframe: Timeframe | None = None
    ) -> list[tuple[BiasSnapshot, Instrument]]:
        """Return the latest active snapshot per (instrument, timeframe)."""
        now = datetime.utcnow()

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
        subq = subq.group_by(
            BiasSnapshot.instrument_id, BiasSnapshot.timeframe
        ).subquery()

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
        return self._session.exec(stmt).all()

    def get_macro_contexts(
        self, snapshot_ids: list[uuid.UUID]
    ) -> dict[uuid.UUID, BiasMacroContext]:
        """Batch-load macro contexts for multiple snapshots (avoids N+1)."""
        if not snapshot_ids:
            return {}
        rows = self._session.exec(
            select(BiasMacroContext).where(
                BiasMacroContext.snapshot_id.in_(snapshot_ids)
            )
        ).all()
        return {row.snapshot_id: row for row in rows}

    def find_snapshot(
        self, instrument_id: int, timeframe: Timeframe, valid_from: datetime
    ) -> BiasSnapshot | None:
        return self._session.exec(
            select(BiasSnapshot).where(
                BiasSnapshot.instrument_id == instrument_id,
                BiasSnapshot.timeframe == timeframe,
                BiasSnapshot.valid_from == valid_from,
            )
        ).first()

    def find_macro(self, snapshot_id: uuid.UUID) -> BiasMacroContext | None:
        return self._session.exec(
            select(BiasMacroContext).where(
                BiasMacroContext.snapshot_id == snapshot_id
            )
        ).first()

    def save(self, obj: BiasSnapshot | BiasMacroContext) -> None:
        self._session.add(obj)
        self._session.flush()

    def commit(self) -> None:
        self._session.commit()
