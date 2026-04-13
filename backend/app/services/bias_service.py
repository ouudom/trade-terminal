from __future__ import annotations

from decimal import Decimal

from sqlmodel import Session

from app.core.exceptions import AppValidationError
from app.models.bias_snapshot import BiasSnapshot
from app.models.bias_macro_context import BiasMacroContext
from app.repositories.bias_repository import BiasRepository
from app.schemas.bias import (
    BiasPayload,
    BiasInsertResult,
    BiasSnapshotResponse,
    InsertBiasResponse,
    MacroResponse,
)


class BiasService:
    def __init__(self, session: Session) -> None:
        self._repo = BiasRepository(session)

    def get_snapshots(self, timeframe=None) -> list[BiasSnapshotResponse]:
        rows = self._repo.get_latest_active_snapshots(timeframe)

        snapshot_ids = [s.id for s, _ in rows]
        macro_map = self._repo.get_macro_contexts(snapshot_ids)

        results = []
        for snapshot, instrument in rows:
            macro_ctx = macro_map.get(snapshot.id)
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

    def insert_bias(self, payloads: list[BiasPayload]) -> InsertBiasResponse:
        if not payloads:
            raise AppValidationError("Payload list is empty.")

        results: list[BiasInsertResult] = []

        for p in payloads:
            existing = self._repo.find_snapshot(p.instrument_id, p.timeframe, p.valid_from)

            if existing:
                existing.bias = p.bias
                existing.confidence = p.confidence
                existing.summary = p.summary
                existing.key_drivers = p.key_drivers
                existing.invalidation_notes = p.invalidation_notes
                existing.valid_until = p.valid_until
                self._repo.save(existing)
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
                self._repo.save(snapshot)
                action = "inserted"

            if p.macro:
                existing_macro = self._repo.find_macro(snapshot.id)
                macro_data = p.macro
                if existing_macro:
                    existing_macro.dxy_trend = macro_data.dxy_trend
                    existing_macro.real_yield_10y = (
                        Decimal(str(macro_data.real_yield_10y))
                        if macro_data.real_yield_10y is not None else None
                    )
                    existing_macro.vix_level = macro_data.vix_level
                    existing_macro.fed_tone = macro_data.fed_tone
                    existing_macro.risk_sentiment = macro_data.risk_sentiment
                    existing_macro.geopolitical_notes = macro_data.geopolitical_notes
                    self._repo.save(existing_macro)
                else:
                    macro_ctx = BiasMacroContext(
                        snapshot_id=snapshot.id,
                        dxy_trend=macro_data.dxy_trend,
                        real_yield_10y=(
                            Decimal(str(macro_data.real_yield_10y))
                            if macro_data.real_yield_10y is not None else None
                        ),
                        vix_level=macro_data.vix_level,
                        fed_tone=macro_data.fed_tone,
                        risk_sentiment=macro_data.risk_sentiment,
                        geopolitical_notes=macro_data.geopolitical_notes,
                    )
                    self._repo.save(macro_ctx)

            results.append(BiasInsertResult(
                snapshot_id=snapshot.id,
                instrument_id=p.instrument_id,
                action=action,
            ))

        self._repo.commit()
        return InsertBiasResponse(inserted=len(results), results=results)
