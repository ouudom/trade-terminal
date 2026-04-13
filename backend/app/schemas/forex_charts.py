"""
Schemas and constants for the forex charts endpoints.
Extracted from app/routers/forex_charts.py.
"""
from __future__ import annotations

from pydantic import BaseModel


FOREX_PAIRS: list[str] = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X",
    "USDCHF=X",
    "AUDUSD=X",
    "USDCAD=X",
    "NZDUSD=X",
    "EURGBP=X",
    "EURJPY=X",
    "GBPJPY=X",
]

# Maps UI timeframe → (yfinance period, yfinance interval)
TIMEFRAME_MAP: dict[str, tuple[str, str]] = {
    "1m":  ("1d",  "1m"),
    "5m":  ("5d",  "5m"),
    "15m": ("5d",  "15m"),
    "1h":  ("1mo", "1h"),
    "4h":  ("3mo", "1h"),
    "1d":  ("1y",  "1d"),
}


class Candle(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
