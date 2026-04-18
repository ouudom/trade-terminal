"use client"
import { useState, useEffect } from "react"
import { forecastApi } from "@/lib/api"
import type { WeeklyForecastRow } from "@/lib/types/forecast"

export function useWeeklyForecasts(week?: string) {
  const [data, setData] = useState<WeeklyForecastRow[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function fetch() {
      try {
        setLoading(true)
        setError(null)

        let weekStr = week
        if (!weekStr) {
          const latest = await forecastApi.getLatestWeek()
          weekStr = latest.week_of
          if (!weekStr) {
            throw new Error("No forecasts available")
          }
        }

        const forecasts = await forecastApi.getWeeklyForecasts(weekStr)
        if (!cancelled) {
          setData(forecasts)
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to fetch forecasts")
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    fetch()
    return () => { cancelled = true }
  }, [week])

  return { data, loading, error }
}
