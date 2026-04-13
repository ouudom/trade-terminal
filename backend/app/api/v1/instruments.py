from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.dependencies import get_instrument_service
from app.models.instrument import Instrument
from app.services.instrument_service import InstrumentService

router = APIRouter(prefix="/instruments", tags=["instruments"])


@router.get("", response_model=list[Instrument])
def list_instruments(svc: InstrumentService = Depends(get_instrument_service)):
    return svc.list_all()
