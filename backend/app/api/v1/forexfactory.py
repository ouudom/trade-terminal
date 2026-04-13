from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_forexfactory_service
from app.models.forexfactory_event import ForexFactoryEvent
from app.schemas.forexfactory import ForexEvent
from app.services.forexfactory_service import ForexFactoryService

router = APIRouter(prefix="/forexfactory", tags=["ForexFactory"])


@router.get("/calendar", response_model=list[ForexEvent])
async def get_calendar(
    week: Optional[str] = Query(
        default="this week",
        description="this week | next week | last week",
    ),
    svc: ForexFactoryService = Depends(get_forexfactory_service),
):
    return await svc.fetch_calendar(week)


@router.get("/events", response_model=list[ForexFactoryEvent])
def get_stored_events(
    currency: Optional[str] = Query(default=None, description="Filter by currency, e.g. USD"),
    impact: Optional[str] = Query(default=None, description="High | Medium"),
    svc: ForexFactoryService = Depends(get_forexfactory_service),
):
    return svc.get_stored_events(currency, impact)
