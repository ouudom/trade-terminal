from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import yfinance as yf

router = APIRouter(prefix="/forex", tags=["forex"])

FOREX_PAIRS = [
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

# Maps UI timeframe -> (yfinance period, yfinance interval)
TIMEFRAME_MAP = {
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


@router.get("/pairs")
def get_forex_pairs():
    return {"pairs": FOREX_PAIRS}


@router.get("/chart/{symbol}", response_model=list[Candle])
def get_forex_chart(
    symbol: str,
    timeframe: str = Query(default="1h", enum=list(TIMEFRAME_MAP.keys())),
):
    period, interval = TIMEFRAME_MAP[timeframe]
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"yfinance error: {e}")

    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data for {symbol}")

    candles = []
    for ts, row in df.iterrows():
        candles.append(
            Candle(
                time=int(ts.timestamp()),
                open=round(float(row["Open"]), 6),
                high=round(float(row["High"]), 6),
                low=round(float(row["Low"]), 6),
                close=round(float(row["Close"]), 6),
                volume=round(float(row.get("Volume", 0)), 2),
            )
        )

    return candles
