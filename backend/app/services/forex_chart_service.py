from __future__ import annotations

import yfinance as yf

from app.core.exceptions import ExternalServiceError, NotFoundError
from app.schemas.forex_charts import Candle, FOREX_PAIRS, TIMEFRAME_MAP


class ForexChartService:
    def get_pairs(self) -> list[str]:
        return FOREX_PAIRS

    def get_chart(self, symbol: str, timeframe: str) -> list[Candle]:
        if timeframe not in TIMEFRAME_MAP:
            raise NotFoundError("timeframe", timeframe)

        period, interval = TIMEFRAME_MAP[timeframe]
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
        except Exception as e:
            raise ExternalServiceError("yfinance", str(e)) from e

        if df.empty:
            raise NotFoundError("forex symbol", symbol)

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
