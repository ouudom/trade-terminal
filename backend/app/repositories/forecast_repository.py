from __future__ import annotations

import uuid
from datetime import date, datetime, timedelta

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.weekly_forecast import WeeklyForecast, DailyValidation
from app.models.instrument import Instrument


def _monday_of_week(d: date) -> date:
    return d - timedelta(days=d.weekday())


class ForecastRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    # ── Weekly forecasts ───────────────────────────────────────────────────────

    def get_latest_week(self) -> date | None:
        result = self._session.exec(
            select(func.max(WeeklyForecast.week_of))
        ).first()
        return result

    def find_weekly(self, instrument_id: int, week_of: date) -> WeeklyForecast | None:
        return self._session.exec(
            select(WeeklyForecast).where(
                WeeklyForecast.instrument_id == instrument_id,
                WeeklyForecast.week_of == week_of,
            )
        ).first()

    def get_week(
        self, week_of: date, instrument_id: int | None = None
    ) -> list[WeeklyForecast]:
        stmt = (
            select(WeeklyForecast)
            .where(WeeklyForecast.week_of == week_of)
            .order_by(WeeklyForecast.instrument)
        )
        if instrument_id is not None:
            stmt = stmt.where(WeeklyForecast.instrument_id == instrument_id)
        return self._session.exec(stmt).all()

    # ── Daily validations ──────────────────────────────────────────────────────

    def find_validation(
        self, forecast_id: uuid.UUID, validation_date: date
    ) -> DailyValidation | None:
        return self._session.exec(
            select(DailyValidation).where(
                DailyValidation.forecast_id == forecast_id,
                DailyValidation.validation_date == validation_date,
            )
        ).first()

    def find_forecast_for_week(
        self, instrument_id: int, validation_date: date
    ) -> WeeklyForecast | None:
        week_of = _monday_of_week(validation_date)
        return self.find_weekly(instrument_id, week_of)

    def get_daily(
        self, validation_date: date
    ) -> list[DailyValidation]:
        return self._session.exec(
            select(DailyValidation)
            .where(DailyValidation.validation_date == validation_date)
            .order_by(DailyValidation.instrument)
        ).all()

    # ── Persistence ────────────────────────────────────────────────────────────

    def save(self, obj: WeeklyForecast | DailyValidation) -> None:
        self._session.add(obj)
        self._session.flush()

    def commit(self) -> None:
        self._session.commit()
