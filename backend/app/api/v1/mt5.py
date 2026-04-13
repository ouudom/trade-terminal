from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, Path, Query

from app.core.dependencies import get_mt5_service
from app.schemas.mt5 import (
    AccountInfo, Position, Order,
    MarketOrderRequest, PendingOrderRequest, OrderResult,
    CancelResult, Deal,
)
from app.services.mt5_service import MT5Service

router = APIRouter(prefix="/mt5", tags=["MT5"])


@router.get("/account", response_model=AccountInfo, summary="MT5 account info")
def get_account(svc: MT5Service = Depends(get_mt5_service)):
    return svc.get_account_info()


@router.get("/positions", response_model=List[Position], summary="Open positions")
def get_positions(svc: MT5Service = Depends(get_mt5_service)):
    return svc.get_positions()


@router.get("/orders", response_model=List[Order], summary="Open pending orders")
def get_orders(svc: MT5Service = Depends(get_mt5_service)):
    return svc.get_orders()


@router.post("/orders/market", response_model=OrderResult, summary="Execute a market order")
def place_market_order(
    req: MarketOrderRequest,
    svc: MT5Service = Depends(get_mt5_service),
):
    return svc.place_market_order(req)


@router.post("/orders/pending", response_model=OrderResult, summary="Place a pending order")
def place_pending_order(
    req: PendingOrderRequest,
    svc: MT5Service = Depends(get_mt5_service),
):
    return svc.place_pending_order(req)


@router.delete(
    "/orders/{ticket}",
    response_model=CancelResult,
    summary="Cancel a pending order by ticket",
)
def cancel_order(
    ticket: int = Path(..., description="MT5 order ticket number"),
    svc: MT5Service = Depends(get_mt5_service),
):
    return svc.cancel_order(ticket)


@router.get("/history/deals", response_model=List[Deal], summary="Deal history in a time range")
def get_deal_history(
    from_timestamp: int = Query(..., description="Range start as Unix timestamp"),
    to_timestamp: int = Query(..., description="Range end as Unix timestamp"),
    group: str = Query(default="*", description="Symbol filter, e.g. *USD*"),
    svc: MT5Service = Depends(get_mt5_service),
):
    return svc.get_deals_history(from_timestamp, to_timestamp, group)
