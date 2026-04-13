from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends

from app.core.dependencies import get_bias_service
from app.models.bias_snapshot import Timeframe
from app.schemas.bias import BiasPayload, BiasSnapshotResponse, InsertBiasResponse
from app.services.bias_service import BiasService

router = APIRouter(prefix="/bias", tags=["bias"])


@router.get("/snapshots", response_model=list[BiasSnapshotResponse])
def get_snapshots(
    timeframe: Optional[Timeframe] = None,
    svc: BiasService = Depends(get_bias_service),
):
    return svc.get_snapshots(timeframe)


@router.post("/insert-bias", response_model=InsertBiasResponse)
def insert_bias(
    payloads: list[BiasPayload],
    svc: BiasService = Depends(get_bias_service),
):
    return svc.insert_bias(payloads)
