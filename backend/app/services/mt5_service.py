from __future__ import annotations

from datetime import datetime
from typing import List

from mt5linux import MetaTrader5

from app.core.config import settings
from app.core.exceptions import MT5ConnectionError, MT5OrderError
from app.schemas.mt5 import (
    AccountInfo, Position, Order, OrderResult,
    CancelResult, Deal, MarketOrderRequest, PendingOrderRequest,
)

_ORDER_TYPE_MAP = {
    "BUY":             MetaTrader5.ORDER_TYPE_BUY,
    "SELL":            MetaTrader5.ORDER_TYPE_SELL,
    "BUY_LIMIT":       MetaTrader5.ORDER_TYPE_BUY_LIMIT,
    "SELL_LIMIT":      MetaTrader5.ORDER_TYPE_SELL_LIMIT,
    "BUY_STOP":        MetaTrader5.ORDER_TYPE_BUY_STOP,
    "SELL_STOP":       MetaTrader5.ORDER_TYPE_SELL_STOP,
    "BUY_STOP_LIMIT":  MetaTrader5.ORDER_TYPE_BUY_STOP_LIMIT,
    "SELL_STOP_LIMIT": MetaTrader5.ORDER_TYPE_SELL_STOP_LIMIT,
}

_RETCODE_DESC: dict[int, str] = {
    10008: "Request confirmed",
    10009: "Request completed",
    10010: "Request partially completed",
    10013: "Invalid request",
    10014: "Invalid volume",
    10015: "Invalid price",
    10016: "Invalid stops",
    10017: "Trade disabled",
    10018: "Market closed",
    10019: "Not enough money",
    10020: "Price changed",
    10021: "No quotes to process",
    10027: "Auto-trading disabled by server",
    10028: "Auto-trading disabled by client",
    10030: "Close order already exists",
}


class MT5Service:
    _instance: MT5Service | None = None

    @classmethod
    def instance(cls) -> MT5Service:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        self._mt5: MetaTrader5 | None = None

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _conn(self) -> MetaTrader5:
        if self._mt5 is None:
            self._mt5 = MetaTrader5()
        return self._mt5

    def _ensure_connected(self) -> None:
        mt5 = self._conn()
        mt5.initialize(host=settings.MT5_HOST, port=settings.MT5_PORT)
        if not mt5.terminal_info():
            raise MT5ConnectionError(
                "MT5",
                "terminal not reachable — ensure the Wine MT5 terminal and mt5linux server are running",
            )
        if settings.MT5_LOGIN and settings.MT5_PASSWORD and settings.MT5_SERVER:
            ok = mt5.login(
                login=settings.MT5_LOGIN,
                password=settings.MT5_PASSWORD,
                server=settings.MT5_SERVER,
            )
            if not ok:
                raise MT5ConnectionError("MT5", f"login failed: {mt5.last_error()}")

    def _retcode_desc(self, code: int) -> str:
        return _RETCODE_DESC.get(code, f"retcode {code}")

    def _build_order_result(self, result) -> OrderResult:
        return OrderResult(
            retcode=result.retcode,
            retcode_description=self._retcode_desc(result.retcode),
            deal=result.deal,
            order=result.order,
            volume=result.volume,
            price=result.price,
            bid=result.bid,
            ask=result.ask,
            comment=result.comment,
            request_id=result.request_id,
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def get_account_info(self) -> AccountInfo:
        self._ensure_connected()
        mt5 = self._conn()
        info = mt5.account_info()
        if info is None:
            raise MT5ConnectionError("MT5", f"account_info() failed: {mt5.last_error()}")
        return AccountInfo(
            login=info.login,
            name=info.name,
            server=info.server,
            currency=info.currency,
            balance=info.balance,
            equity=info.equity,
            margin=info.margin,
            free_margin=info.margin_free,
            margin_level=info.margin_level,
            leverage=info.leverage,
            profit=info.profit,
        )

    def get_positions(self) -> List[Position]:
        self._ensure_connected()
        mt5 = self._conn()
        positions = mt5.positions_get()
        if positions is None:
            return []
        return [
            Position(
                ticket=p.ticket,
                symbol=p.symbol,
                type="buy" if p.type == MetaTrader5.POSITION_TYPE_BUY else "sell",
                volume=p.volume,
                price_open=p.price_open,
                price_current=p.price_current,
                sl=p.sl,
                tp=p.tp,
                profit=p.profit,
                swap=p.swap,
                comment=p.comment,
                time=p.time,
            )
            for p in positions
        ]

    def get_orders(self) -> List[Order]:
        self._ensure_connected()
        mt5 = self._conn()
        orders = mt5.orders_get()
        if orders is None:
            return []
        return [
            Order(
                ticket=o.ticket,
                symbol=o.symbol,
                type=str(o.type),
                volume_initial=o.volume_initial,
                volume_current=o.volume_current,
                price_open=o.price_open,
                sl=o.sl,
                tp=o.tp,
                comment=o.comment,
                time_setup=o.time_setup,
            )
            for o in orders
        ]

    def place_market_order(self, req: MarketOrderRequest) -> OrderResult:
        self._ensure_connected()
        mt5 = self._conn()
        symbol_info = mt5.symbol_info(req.symbol)
        if symbol_info is None:
            raise MT5OrderError("MT5", f"symbol '{req.symbol}' not found")
        if not symbol_info.visible:
            mt5.symbol_select(req.symbol, True)

        tick = mt5.symbol_info_tick(req.symbol)
        price = tick.ask if req.order_type.value == "BUY" else tick.bid

        request_dict = {
            "action":       MetaTrader5.TRADE_ACTION_DEAL,
            "symbol":       req.symbol,
            "volume":       req.volume,
            "type":         _ORDER_TYPE_MAP[req.order_type.value],
            "price":        price,
            "sl":           req.sl or 0.0,
            "tp":           req.tp or 0.0,
            "deviation":    req.deviation,
            "magic":        req.magic,
            "comment":      req.comment,
            "type_time":    MetaTrader5.ORDER_TIME_GTC,
            "type_filling": MetaTrader5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request_dict)
        if result is None:
            raise MT5OrderError("MT5", f"order_send returned None: {mt5.last_error()}")
        return self._build_order_result(result)

    def place_pending_order(self, req: PendingOrderRequest) -> OrderResult:
        self._ensure_connected()
        mt5 = self._conn()
        symbol_info = mt5.symbol_info(req.symbol)
        if symbol_info is None:
            raise MT5OrderError("MT5", f"symbol '{req.symbol}' not found")
        if not symbol_info.visible:
            mt5.symbol_select(req.symbol, True)

        request_dict = {
            "action":       MetaTrader5.TRADE_ACTION_PENDING,
            "symbol":       req.symbol,
            "volume":       req.volume,
            "type":         _ORDER_TYPE_MAP[req.order_type.value],
            "price":        req.price,
            "sl":           req.sl or 0.0,
            "tp":           req.tp or 0.0,
            "magic":        req.magic,
            "comment":      req.comment,
            "type_time":    MetaTrader5.ORDER_TIME_SPECIFIED if req.expiration else MetaTrader5.ORDER_TIME_GTC,
            "expiration":   req.expiration or 0,
            "type_filling": MetaTrader5.ORDER_FILLING_RETURN,
        }
        result = mt5.order_send(request_dict)
        if result is None:
            raise MT5OrderError("MT5", f"order_send returned None: {mt5.last_error()}")
        return self._build_order_result(result)

    def cancel_order(self, ticket: int) -> CancelResult:
        self._ensure_connected()
        mt5 = self._conn()
        request_dict = {
            "action": MetaTrader5.TRADE_ACTION_REMOVE,
            "order":  ticket,
        }
        result = mt5.order_send(request_dict)
        if result is None:
            raise MT5OrderError("MT5", f"order_send returned None: {mt5.last_error()}")
        return CancelResult(
            retcode=result.retcode,
            retcode_description=self._retcode_desc(result.retcode),
            ticket=ticket,
        )

    def get_deals_history(
        self, from_timestamp: int, to_timestamp: int, group: str = "*"
    ) -> List[Deal]:
        self._ensure_connected()
        mt5 = self._conn()
        deals = mt5.history_deals_get(
            datetime.utcfromtimestamp(from_timestamp),
            datetime.utcfromtimestamp(to_timestamp),
            group=group,
        )
        if deals is None:
            return []
        return [
            Deal(
                ticket=d.ticket,
                order=d.order,
                symbol=d.symbol,
                type=str(d.type),
                volume=d.volume,
                price=d.price,
                commission=d.commission,
                swap=d.swap,
                profit=d.profit,
                comment=d.comment,
                time=d.time,
            )
            for d in deals
        ]
