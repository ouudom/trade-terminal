import { FundamentalBiasDashboard } from "@/components/dashboard/fundamental-bias"
import type { FundamentalBiasEntry, OverallSentiment, BiasDirection } from "@/lib/mock-data"

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

interface SnapshotRow {
  snapshot_id: string
  instrument_id: number
  symbol: string
  name: string
  timeframe: string
  bias: string
  confidence: number
  summary: string
  key_drivers: string | null
  invalidation_notes: string | null
  valid_from: string
  valid_until: string | null
  macro: unknown
}

function normalizeDirection(bias: string): BiasDirection {
  if (bias === "bullish" || bias === "bullish_bias") return "bullish"
  if (bias === "bearish" || bias === "bearish_bias") return "bearish"
  return "neutral"
}

function relativeTime(iso: string): string {
  const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 1000)
  if (diff < 60) return `${diff}s ago`
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}

function toBullets(key_drivers: string | null, invalidation_notes: string | null): string[] {
  const lines: string[] = []
  if (key_drivers) lines.push(...key_drivers.split("\n").map((s) => s.trim()).filter(Boolean))
  if (invalidation_notes) lines.push(...invalidation_notes.split("\n").map((s) => s.trim()).filter(Boolean))
  return lines
}

function deriveOverallSentiment(entries: FundamentalBiasEntry[]): OverallSentiment {
  if (entries.length === 0) {
    return { label: "No Data", direction: "neutral", confidenceIndex: 0, lastUpdate: "—" }
  }

  const counts = { bullish: 0, bearish: 0, neutral: 0 }
  for (const e of entries) counts[e.direction]++

  const direction: BiasDirection =
    counts.bullish > counts.bearish && counts.bullish > counts.neutral
      ? "bullish"
      : counts.bearish > counts.bullish && counts.bearish > counts.neutral
      ? "bearish"
      : "neutral"

  const avgConfidence = Math.round(entries.reduce((s, e) => s + e.confidence, 0) / entries.length)

  const label =
    direction === "bullish"
      ? avgConfidence >= 70
        ? "Strongly Bullish"
        : "Moderately Bullish"
      : direction === "bearish"
      ? avgConfidence >= 70
        ? "Strongly Bearish"
        : "Moderately Bearish"
      : "Mixed / Neutral"

  return {
    label,
    direction,
    confidenceIndex: avgConfidence,
    lastUpdate: relativeTime(new Date().toISOString()),
  }
}

export default async function FundamentalBiasPage() {
  let entries: FundamentalBiasEntry[] = []

  try {
    const res = await fetch(`${API_BASE}/bias/snapshots`, { cache: "no-store" })
    if (res.ok) {
      const rows: SnapshotRow[] = await res.json()
      entries = rows.map((r) => ({
        symbol: r.symbol,
        name: r.name,
        changePct: 0,
        direction: normalizeDirection(r.bias),
        confidence: Math.round((r.confidence / 5) * 100),
        lastUpdate: relativeTime(r.valid_from),
        analysis: r.summary,
        bullets: toBullets(r.key_drivers, r.invalidation_notes),
      }))
    }
  } catch {
    // Backend unavailable — render with empty state
  }

  const sentiment = deriveOverallSentiment(entries)

  return <FundamentalBiasDashboard entries={entries} sentiment={sentiment} />
}
