from __future__ import annotations

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends

from app.core.dependencies import get_forecast_service
from app.schemas.forecast import (
    DailyValidationPayload,
    DailyValidationResponse,
    LatestWeekResponse,
    UpsertForecastResponse,
    UpsertValidationResponse,
    WeeklyForecastPayload,
    WeeklyForecastResponse,
)
from app.services.forecast_service import ForecastService

router = APIRouter(prefix="/forecast", tags=["forecast"])


@router.post("/weekly", response_model=UpsertForecastResponse)
def upsert_weekly_forecast(
    payload: WeeklyForecastPayload,
    svc: ForecastService = Depends(get_forecast_service),
):
    return svc.upsert_weekly(payload)


@router.post("/daily-validation", response_model=UpsertValidationResponse)
def upsert_daily_validation(
    payload: DailyValidationPayload,
    svc: ForecastService = Depends(get_forecast_service),
):
    return svc.upsert_daily_validation(payload)


@router.get("/latest-week", response_model=LatestWeekResponse)
def get_latest_week(svc: ForecastService = Depends(get_forecast_service)):
    return LatestWeekResponse(week_of=svc.get_latest_week())


@router.get("/weekly", response_model=list[WeeklyForecastResponse])
def get_weekly_forecasts(
    week: date,
    instrument_id: Optional[int] = None,
    svc: ForecastService = Depends(get_forecast_service),
):
    return svc.get_weekly(week, instrument_id)


@router.get("/daily", response_model=list[DailyValidationResponse])
def get_daily_validations(
    date: date,
    svc: ForecastService = Depends(get_forecast_service),
):
    return svc.get_daily(date)
