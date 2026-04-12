from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


# ── Enumerations ──────────────────────────────────────────────────────────────

class OrderType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class PendingOrderType(str, Enum):
    BUY_LIMIT = "BUY_LIMIT"
    SELL_LIMIT = "SELL_LIMIT"
    BUY_STOP = "BUY_STOP"
    SELL_STOP = "SELL_STOP"
    BUY_STOP_LIMIT = "BUY_STOP_LIMIT"
    SELL_STOP_LIMIT = "SELL_STOP_LIMIT"


# ── Account ───────────────────────────────────────────────────────────────────

class AccountInfo(BaseModel):
    login: int
    name: str
    server: str
    currency: str
    balance: float
    equity: float
    margin: float
    free_margin: float
    margin_level: Optional[float]
    leverage: int
    profit: float


# ── Positions ─────────────────────────────────────────────────────────────────

class Position(BaseModel):
    ticket: int
    symbol: str
    type: str
    volume: float
    price_open: float
    price_current: float
    sl: float
    tp: float
    profit: float
    swap: float
    comment: str
    time: int


# ── Open Orders ───────────────────────────────────────────────────────────────

class Order(BaseModel):
    ticket: int
    symbol: str
    type: str
    volume_initial: float
    volume_current: float
    price_open: float
    sl: float
    tp: float
    comment: str
    time_setup: int


# ── Market Order ──────────────────────────────────────────────────────────────

class MarketOrderRequest(BaseModel):
    symbol: str = Field(..., description="Instrument symbol, e.g. EURUSD")
    order_type: OrderType = Field(..., description="BUY or SELL")
    volume: float = Field(..., gt=0, description="Lot size, e.g. 0.01")
    sl: Optional[float] = Field(default=None, description="Stop loss price (omit for none)")
    tp: Optional[float] = Field(default=None, description="Take profit price (omit for none)")
    deviation: int = Field(default=20, description="Max price deviation in points")
    comment: str = Field(default="", description="Order comment")
    magic: int = Field(default=0, description="Expert Advisor magic number")


class OrderResult(BaseModel):
    retcode: int
    retcode_description: str
    deal: int
    order: int
    volume: float
    price: float
    bid: float
    ask: float
    comment: str
    request_id: int


# ── Pending Order ─────────────────────────────────────────────────────────────

class PendingOrderRequest(BaseModel):
    symbol: str = Field(..., description="Instrument symbol, e.g. EURUSD")
    order_type: PendingOrderType = Field(..., description="BUY_LIMIT, SELL_LIMIT, BUY_STOP, SELL_STOP")
    volume: float = Field(..., gt=0, description="Lot size, e.g. 0.01")
    price: float = Field(..., description="Pending order trigger price")
    sl: Optional[float] = Field(default=None, description="Stop loss price")
    tp: Optional[float] = Field(default=None, description="Take profit price")
    expiration: Optional[int] = Field(default=None, description="Expiration as Unix timestamp (omit for GTC)")
    comment: str = Field(default="")
    magic: int = Field(default=0)


# ── Cancel Order ──────────────────────────────────────────────────────────────

class CancelResult(BaseModel):
    retcode: int
    retcode_description: str
    ticket: int


# ── History Deals ─────────────────────────────────────────────────────────────

class Deal(BaseModel):
    ticket: int
    order: int
    symbol: str
    type: str
    volume: float
    price: float
    commission: float
    swap: float
    profit: float
    comment: str
    time: int
