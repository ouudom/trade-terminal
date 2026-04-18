from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlmodel import Session

from app.core.exceptions import AppValidationError, NotFoundError
from app.models.weekly_forecast import WeeklyForecast, DailyValidation
from app.repositories.forecast_repository import ForecastRepository
from app.schemas.forecast import (
    DailyValidationPayload,
    DailyValidationResponse,
    UpsertForecastResponse,
    UpsertValidationResponse,
    WeeklyForecastPayload,
    WeeklyForecastResponse,
)


def _to_decimal(v: float | None) -> Decimal | None:
    return Decimal(str(v)) if v is not None else None


class ForecastService:
    def __init__(self, session: Session) -> None:
        self._repo = ForecastRepository(session)

    # ── Weekly forecasts ───────────────────────────────────────────────────────

    def upsert_weekly(self, payload: WeeklyForecastPayload) -> UpsertForecastResponse:
        tech = payload.technical
        sent = payload.sentimental

        existing = self._repo.find_weekly(payload.instrument_id, payload.week_of)

        if existing:
            _apply_weekly_fields(existing, payload)
            self._repo.save(existing)
        else:
            row = WeeklyForecast(
                instrument_id=payload.instrument_id,
                week_of=payload.week_of,
                generated_by="claude",
            )
            _apply_weekly_fields(row, payload)
            self._repo.save(row)

        self._repo.commit()
        return UpsertForecastResponse(upserted=1, week_of=payload.week_of)

    def get_latest_week(self) -> date | None:
        return self._repo.get_latest_week()

    def get_weekly(
        self, week_of: date, instrument_id: int | None = None
    ) -> list[WeeklyForecastResponse]:
        rows = self._repo.get_week(week_of, instrument_id)
        return [_to_weekly_response(f, inst) for f, inst in rows]

    # ── Daily validations ──────────────────────────────────────────────────────

    def upsert_daily_validation(
        self, payload: DailyValidationPayload
    ) -> UpsertValidationResponse:
        forecast = self._repo.find_forecast_for_week(payload.instrument_id, payload.date)
        if forecast is None:
            raise NotFoundError(
                "WeeklyForecast",
                f"instrument_id={payload.instrument_id} week_of={payload.date}",
            )

        existing = self._repo.find_validation(forecast.id, payload.date)

        if existing:
            _apply_validation_fields(existing, payload, forecast.id)
            self._repo.save(existing)
        else:
            row = DailyValidation(
                forecast_id=forecast.id,
                instrument_id=payload.instrument_id,
                validation_date=payload.date,
                status=payload.status,
            )
            _apply_validation_fields(row, payload, forecast.id)
            self._repo.save(row)

        self._repo.commit()
        return UpsertValidationResponse(upserted=1, date=payload.date)

    def get_daily(self, validation_date: date) -> list[DailyValidationResponse]:
        rows = self._repo.get_daily(validation_date)
        return [_to_validation_response(v, inst) for v, inst in rows]


# ── Helpers ────────────────────────────────────────────────────────────────────

def _apply_weekly_fields(row: WeeklyForecast, p: WeeklyForecastPayload) -> None:
    tech = p.technical
    sent = p.sentimental

    if tech:
        row.technical_bias = tech.bias
        row.technical_ai_analysis = tech.ai_analysis
        row.technical_key_drivers = tech.key_drivers
        row.technical_invalidation = tech.invalidation
        row.key_zone_high = _to_decimal(tech.key_zone_high)
        row.key_zone_low = _to_decimal(tech.key_zone_low)
        row.invalidation_level = _to_decimal(tech.invalidation_level)
        row.trend_structure = tech.trend_structure
        row.premium_discount = tech.premium_discount
        row.weekly_high = _to_decimal(tech.weekly_high)
        row.weekly_low = _to_decimal(tech.weekly_low)

    if sent:
        row.sentiment_bias = sent.bias
        row.sentiment_ai_analysis = sent.ai_analysis
        row.sentiment_key_drivers = sent.key_drivers
        row.sentiment_invalidation = sent.invalidation
        row.retail_long_pct = _to_decimal(sent.retail_long_pct)
        row.retail_short_pct = _to_decimal(sent.retail_short_pct)
        row.cot_net_position = _to_decimal(sent.cot_net_position)
        row.cot_change_week = _to_decimal(sent.cot_change_week)

    row.overall_bias = p.overall_bias
    row.confidence = p.confidence
    row.high_impact_events = p.high_impact_events


def _apply_validation_fields(
    row: DailyValidation, p: DailyValidationPayload, forecast_id
) -> None:
    import uuid as _uuid
    row.forecast_id = forecast_id if isinstance(forecast_id, _uuid.UUID) else _uuid.UUID(str(forecast_id))
    row.status = p.status
    row.bias_still_intact = p.bias_still_intact
    row.price_respecting_zone = p.price_respecting_zone
    row.news_risk = p.news_risk
    row.structural_shift = p.structural_shift
    row.notes = p.notes
    row.ai_review = p.ai_review
    row.invalidation_triggered = p.invalidation_triggered


def _to_weekly_response(f: WeeklyForecast, inst) -> WeeklyForecastResponse:
    def _f(v) -> float | None:
        return float(v) if v is not None else None

    return WeeklyForecastResponse(
        id=f.id,
        instrument_id=f.instrument_id,
        symbol=inst.symbol,
        week_of=f.week_of,
        generated_by=f.generated_by,
        technical_bias=f.technical_bias,
        technical_ai_analysis=f.technical_ai_analysis,
        technical_key_drivers=f.technical_key_drivers,
        technical_invalidation=f.technical_invalidation,
        key_zone_high=_f(f.key_zone_high),
        key_zone_low=_f(f.key_zone_low),
        invalidation_level=_f(f.invalidation_level),
        trend_structure=f.trend_structure,
        premium_discount=f.premium_discount,
        weekly_high=_f(f.weekly_high),
        weekly_low=_f(f.weekly_low),
        sentiment_bias=f.sentiment_bias,
        sentiment_ai_analysis=f.sentiment_ai_analysis,
        sentiment_key_drivers=f.sentiment_key_drivers,
        sentiment_invalidation=f.sentiment_invalidation,
        retail_long_pct=_f(f.retail_long_pct),
        retail_short_pct=_f(f.retail_short_pct),
        cot_net_position=_f(f.cot_net_position),
        cot_change_week=_f(f.cot_change_week),
        overall_bias=f.overall_bias,
        confidence=f.confidence,
        high_impact_events=f.high_impact_events,
    )


def _to_validation_response(v: DailyValidation, inst) -> DailyValidationResponse:
    return DailyValidationResponse(
        id=v.id,
        forecast_id=v.forecast_id,
        instrument_id=v.instrument_id,
        symbol=inst.symbol,
        date=v.validation_date,
        status=v.status,
        bias_still_intact=v.bias_still_intact,
        price_respecting_zone=v.price_respecting_zone,
        news_risk=v.news_risk,
        structural_shift=v.structural_shift,
        notes=v.notes,
        ai_review=v.ai_review,
        invalidation_triggered=v.invalidation_triggered,
    )
