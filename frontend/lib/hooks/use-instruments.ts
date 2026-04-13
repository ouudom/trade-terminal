"use client"

import { useState, useEffect, useCallback } from "react"
import { instrumentsApi } from "@/lib/api"
import type { Instrument } from "@/lib/api"

export function useInstruments() {
  const [instruments, setInstruments] = useState<Instrument[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchInstruments = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await instrumentsApi.list()
      setInstruments(data)
    } catch {
      setError("Could not load instruments — is the backend running?")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchInstruments()
  }, [fetchInstruments])

  const toggleActive = useCallback((id: number) => {
    setInstruments((prev) =>
      prev.map((i) => (i.id === id ? { ...i, is_active: !i.is_active } : i)),
    )
  }, [])

  return { instruments, loading, error, refetch: fetchInstruments, toggleActive }
}
