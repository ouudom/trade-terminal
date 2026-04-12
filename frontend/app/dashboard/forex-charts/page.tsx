"use client"

import { useState, useEffect, useCallback } from "react"
import { MarketChart } from "@/components/dashboard/market-chart"
import type { Candle } from "@/lib/mock-data"

const FOREX_PAIRS = [
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

const TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d"] as const
type Timeframe = (typeof TIMEFRAMES)[number]

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

interface RawCandle {
  time: number
  open: number
  high: number
  low: number
  close: number
  volume: number
}

function toCandle(r: RawCandle): Candle {
  return {
    timestamp: r.time,
    open: r.open,
    high: r.high,
    low: r.low,
    close: r.close,
    volume: r.volume,
  }
}

function displaySymbol(ticker: string) {
  return ticker.replace("=X", "")
}

export default function ForexChartsPage() {
  const [timeframe, setTimeframe] = useState<Timeframe>("1h")
  const [candleMap, setCandleMap] = useState<Record<string, Candle[]>>({})
  const [loading, setLoading] = useState(true)
  const [errors, setErrors] = useState<Record<string, string>>({})

  const fetchAll = useCallback(async (tf: Timeframe) => {
    setLoading(true)
    setErrors({})

    const results = await Promise.allSettled(
      FOREX_PAIRS.map(async (symbol) => {
        const res = await fetch(
          `${API_BASE}/forex/chart/${symbol}?timeframe=${tf}`
        )
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data: RawCandle[] = await res.json()
        return { symbol, candles: data.map(toCandle) }
      })
    )

    const newMap: Record<string, Candle[]> = {}
    const newErrors: Record<string, string> = {}

    results.forEach((result, i) => {
      const symbol = FOREX_PAIRS[i]
      if (result.status === "fulfilled") {
        newMap[symbol] = result.value.candles
      } else {
        newErrors[symbol] = result.reason?.message ?? "Failed"
      }
    })

    setCandleMap(newMap)
    setErrors(newErrors)
    setLoading(false)
  }, [])

  useEffect(() => {
    fetchAll(timeframe)
  }, [timeframe, fetchAll])

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
