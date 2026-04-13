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
from app.services.bias_service import BiasService
from app.services.forexfactory_service import ForexFactoryService
from app.services.news_service import NewsService
from app.services.forex_chart_service import ForexChartService
from app.services.mt5_service import MT5Service


def get_instrument_service(session: Session = Depends(get_session)) -> InstrumentService:
    return InstrumentService(session)


def get_bias_service(session: Session = Depends(get_session)) -> BiasService:
    return BiasService(session)


def get_forexfactory_service(session: Session = Depends(get_session)) -> ForexFactoryService:
    return ForexFactoryService(session)


def get_news_service() -> NewsService:
    """Stateless — no DB session required."""
    return NewsService()


def get_forex_chart_service() -> ForexChartService:
    """Stateless — no DB session required."""
    return ForexChartService()


def get_mt5_service() -> MT5Service:
    """Returns the class-level singleton. Connection is lazy and persists."""
    return MT5Service.instance()
