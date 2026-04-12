from __future__ import annotations
from typing import List
from fastapi import APIRouter, HTTPException, Path, Query

from app.models.mt5 import (
    AccountInfo, Position, Order,
    MarketOrderRequest, PendingOrderRequest, OrderResult,
    CancelResult, Deal,
)
import app.services.mt5_service as mt5_svc

router = APIRouter(prefix="/mt5", tags=["MT5"])


def _mt5_error(exc: Exception, status: int = 503) -> HTTPException:
    return HTTPException(status_code=status, detail=str(exc))


@router.get("/account", response_model=AccountInfo, summary="MT5 account info")
def get_account():
    try:
        return mt5_svc.get_account_info()
    except Exception as e:
        raise _mt5_error(e)


@router.get("/positions", response_model=List[Position], summary="Open positions")
def get_positions():
    try:
        return mt5_svc.get_positions()
    except Exception as e:
        raise _mt5_error(e)


@router.get("/orders", response_model=List[Order], summary="Open pending orders")
def get_orders():
    try:
        return mt5_svc.get_orders()
    except Exception as e:
        raise _mt5_error(e)


@router.post("/orders/market", response_model=OrderResult, summary="Execute a market order")
def place_market_order(req: MarketOrderRequest):
    try:
        return mt5_svc.place_market_order(req)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise _mt5_error(e)


@router.post("/orders/pending", response_model=OrderResult, summary="Place a pending order")
def place_pending_order(req: PendingOrderRequest):
    try:
        return mt5_svc.place_pending_order(req)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise _mt5_error(e)


@router.delete(
    "/orders/{ticket}",
    response_model=CancelResult,
    summary="Cancel a pending order by ticket",
)
def cancel_order(ticket: int = Path(..., description="MT5 order ticket number")):
    try:
        return mt5_svc.cancel_order(ticket)
    except Exception as e:
        raise _mt5_error(e)


@router.get("/history/deals", response_model=List[Deal], summary="Deal history in a time range")
def get_deal_history(
    from_timestamp: int = Query(..., description="Range start as Unix timestamp"),
    to_timestamp: int = Query(..., description="Range end as Unix timestamp"),
    group: str = Query(default="*", description="Symbol filter, e.g. *USD*"),
):
    try:
        return mt5_svc.get_deals_history(from_timestamp, to_timestamp, group)
    except Exception as e:
        raise _mt5_error(e)
