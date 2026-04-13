from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_forex_chart_service
from app.schemas.forex_charts import Candle, TIMEFRAME_MAP
from app.services.forex_chart_service import ForexChartService

router = APIRouter(prefix="/forex", tags=["forex"])


@router.get("/pairs")
def get_forex_pairs(svc: ForexChartService = Depends(get_forex_chart_service)):
    return {"pairs": svc.get_pairs()}


@router.get("/chart/{symbol}", response_model=list[Candle])
def get_forex_chart(
    symbol: str,
    timeframe: str = Query(default="1h", enum=list(TIMEFRAME_MAP.keys())),
    svc: ForexChartService = Depends(get_forex_chart_service),
):
    return svc.get_chart(symbol, timeframe)
