"use client"

import { useState } from "react"
import { MarketChart } from "@/components/features/forex-charts/market-chart"
import { useForexCharts, FOREX_PAIRS } from "@/lib/hooks/use-forex-charts"

const TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d"] as const
type Timeframe = (typeof TIMEFRAMES)[number]

function displaySymbol(ticker: string) {
  return ticker.replace("=X", "")
}

export default function ForexChartsPage() {
  const [timeframe, setTimeframe] = useState<Timeframe>("1h")
  const { candleMap, loading, errors } = useForexCharts(timeframe)

  return (
    <div className="flex flex-col gap-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-base font-semibold text-foreground">Forex Charts</h1>
          <p className="font-mono text-[11px] text-muted-foreground/60">
            Live OHLCV via yfinance · {FOREX_PAIRS.length} pairs
          </p>
        </div>
        {/* Global timeframe selector */}
        <div className="flex gap-1 rounded-md border border-surface-border bg-surface-1 p-1">
          {TIMEFRAMES.map((tf) => (
            <button
              key={tf}
              onClick={() => setTimeframe(tf)}
              className={`rounded px-2.5 py-1 font-mono text-[11px] transition-colors ${
                timeframe === tf
                  ? "bg-surface-3 text-foreground"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      {/* Grid */}
      {loading ? (
        <div className="grid grid-cols-1 gap-3">
          {FOREX_PAIRS.map((symbol) => (
            <div
              key={symbol}
              className="h-[300px] animate-pulse rounded-lg border border-surface-border bg-surface-1"
            />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-3">
          {FOREX_PAIRS.map((symbol) => {
            const candles = candleMap[symbol]
            const error = errors[symbol]
            const display = displaySymbol(symbol)

            if (error) {
              return (
                <div
                  key={symbol}
                  className="flex h-[300px] flex-col items-center justify-center rounded-lg border border-surface-border bg-surface-1 text-muted-foreground"
                >
                  <span className="font-mono text-xs">{display}</span>
                  <span className="mt-1 font-mono text-[10px] text-red-400/70">{error}</span>
                </div>
              )
            }

            return (
              <div
                key={symbol}
                className="rounded-lg border border-surface-border bg-surface-1 overflow-hidden"
              >
                <MarketChart candles={candles ?? []} symbol={display} />
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
