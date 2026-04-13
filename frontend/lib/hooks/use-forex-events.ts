"use client"

import { useState, useEffect, useCallback } from "react"
import { forexFactoryApi, ApiError } from "@/lib/api"
import type { ForexEvent } from "@/lib/types"

export function useForexEvents() {
  const [events, setEvents] = useState<ForexEvent[]>([])
  const [loading, setLoading] = useState(true)
  const [fetching, setFetching] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadStored = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await forexFactoryApi.getEvents()
      setEvents(data)
    } catch (e) {
      setError(e instanceof ApiError ? `${e.status}: ${e.statusText}` : "Failed to load events")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadStored()
  }, [loadStored])

  const fetchWeek = useCallback(
    async (week: string) => {
      setFetching(true)
      setError(null)
      try {
        await forexFactoryApi.fetchCalendar(week)
        await loadStored()
      } catch (e) {
        setError(e instanceof ApiError ? `Fetch failed: ${e.status}` : `Fetch failed for "${week}"`)
      } finally {
        setFetching(false)
      }
    },
    [loadStored],
  )

  return { events, loading, fetching, error, loadStored, fetchWeek }
}
