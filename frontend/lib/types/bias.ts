export type BiasDirection = "bullish" | "bearish" | "neutral"

export interface FundamentalBiasEntry {
  symbol: string
  name: string
  changePct: number
  direction: BiasDirection
  confidence: number
  lastUpdate: string
  analysis: string
  bullets: string[]
}

export interface OverallSentiment {
  label: string
  direction: BiasDirection
  confidenceIndex: number
  lastUpdate: string
}
