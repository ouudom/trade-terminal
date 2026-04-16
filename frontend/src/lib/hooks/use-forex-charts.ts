"use client"

import { useState, useEffect } from "react"
import { forexApi } from "@/lib/api"
import type { Candle } from "@/lib/types"

export const FOREX_PAIRS = [
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
] as const

function toCandle(r: { time: number; open: number; high: number; low: number; close: number; volume: number }): Candle {
  return {
    timestamp: r.time,
    open: r.open,
    high: r.high,
    low: r.low,
    close: r.close,
    volume: r.volume,
  }
}

export function useForexCharts(timeframe: string) {
  const [candleMap, setCandleMap] = useState<Record<string, Candle[]>>({})
  const [loading, setLoading] = useState(true)
  const [errors, setErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    let cancelled = false

    async function fetchAll() {
      setLoading(true)
      setErrors({})

      const results = await Promise.allSettled(
        FOREX_PAIRS.map((symbol) =>
          forexApi.getChartCandles(symbol, timeframe).then((raw) => ({
            symbol,
            candles: raw.map(toCandle),
          })),
        ),
      )

      if (cancelled) return

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
    }

    fetchAll()
    return () => {
      cancelled = true
    }
  }, [timeframe])

  return { candleMap, loading, errors }
}
