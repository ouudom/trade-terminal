"""
Central registry of FastAPI dependency factories.

Routers import dependency functions from here — never import service
classes directly. This keeps the dependency graph explicit and testable.
"""
from __future__ import annotations

from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.services.instrument_service import InstrumentService
from app.services.forecast_service import ForecastService


def get_instrument_service(session: Session = Depends(get_session)) -> InstrumentService:
    return InstrumentService(session)


def get_forecast_service(session: Session = Depends(get_session)) -> ForecastService:
    return ForecastService(session)
