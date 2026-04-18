from __future__ import annotations

from datetime import date

from sqlmodel import Session

from app.core.exceptions import NotFoundError
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


class ForecastService:
    def __init__(self, session: Session) -> None:
        self._repo = ForecastRepository(session)

    def upsert_weekly(self, payload: WeeklyForecastPayload) -> UpsertForecastResponse:
        existing = self._repo.find_weekly(payload.instrument_id, payload.week_of)

        if existing:
            _apply_weekly_fields(existing, payload)
            self._repo.save(existing)
        else:
            row = WeeklyForecast(
                instrument_id=payload.instrument_id,
                instrument=payload.instrument,
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
        return [_to_weekly_response(f) for f in rows]

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
            _apply_validation_fields(existing, payload, forecast)
            self._repo.save(existing)
        else:
            row = DailyValidation(
                forecast_id=forecast.id,
                instrument_id=payload.instrument_id,
                instrument=forecast.instrument,
                validation_date=payload.date,
            )
            _apply_validation_fields(row, payload, forecast)
            self._repo.save(row)

        self._repo.commit()
        return UpsertValidationResponse(upserted=1, date=payload.date)

    def get_daily(self, validation_date: date) -> list[DailyValidationResponse]:
        rows = self._repo.get_daily(validation_date)
        return [_to_validation_response(v) for v in rows]


def _apply_weekly_fields(row: WeeklyForecast, p: WeeklyForecastPayload) -> None:
    row.instrument = p.instrument
    row.technical = p.technical.model_dump() if p.technical else None
    row.fundamental = p.fundamental.model_dump() if p.fundamental else None
    row.sentimental = p.sentimental.model_dump() if p.sentimental else None
    row.confluence = p.confluence.model_dump() if p.confluence else None
    row.overall_bias = p.overall_bias
    row.overall_ai_analysis = p.overall_ai_analysis
    row.overall_key_drivers = p.overall_key_drivers
    row.overall_bias_invalidation_reasons = p.overall_bias_invalidation_reasons
    row.overall_setup_scenarios = p.overall_setup_scenarios.model_dump() if p.overall_setup_scenarios else None
    row.confidence = p.confidence
    row.correlation_warning = p.correlation_warning
    row.high_impact_events = p.high_impact_events


def _apply_validation_fields(
    row: DailyValidation, p: DailyValidationPayload, forecast: WeeklyForecast
) -> None:
    row.session = p.session
    row.price_at_zone = p.price_at_zone
    row.weekly_bias_intact = p.weekly_bias_intact
    row.overnight_news_invalidation = p.overnight_news_invalidation
    row.entry_trigger = p.entry_trigger.model_dump() if p.entry_trigger else None
    row.tp_path_clear = p.tp_path_clear
    row.tp_path_blockers = p.tp_path_blockers
    row.output = p.output
    row.output_reason = p.output_reason


def _to_weekly_response(f: WeeklyForecast) -> WeeklyForecastResponse:
    return WeeklyForecastResponse(
        id=f.id,
        instrument_id=f.instrument_id,
        instrument=f.instrument,
        week_of=f.week_of,
        generated_by=f.generated_by,
        technical=f.technical,
        fundamental=f.fundamental,
        sentimental=f.sentimental,
        confluence=f.confluence,
        overall_bias=f.overall_bias,
        overall_ai_analysis=f.overall_ai_analysis,
        overall_key_drivers=f.overall_key_drivers,
        overall_bias_invalidation_reasons=f.overall_bias_invalidation_reasons,
        overall_setup_scenarios=f.overall_setup_scenarios,
        confidence=f.confidence,
        correlation_warning=f.correlation_warning,
        high_impact_events=f.high_impact_events,
    )


def _to_validation_response(v: DailyValidation) -> DailyValidationResponse:
    return DailyValidationResponse(
        id=v.id,
        forecast_id=v.forecast_id,
        instrument_id=v.instrument_id,
        instrument=v.instrument,
        date=v.validation_date,
        session=v.session,
        price_at_zone=v.price_at_zone,
        weekly_bias_intact=v.weekly_bias_intact,
        overnight_news_invalidation=v.overnight_news_invalidation,
        entry_trigger=v.entry_trigger,
        tp_path_clear=v.tp_path_clear,
        tp_path_blockers=v.tp_path_blockers,
        output=v.output,
        output_reason=v.output_reason,
    )
