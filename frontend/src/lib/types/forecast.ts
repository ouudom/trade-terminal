export type BiasLevel = "bullish" | "bearish" | "neutral"
export type ConfidenceLevel = "HIGH" | "MEDIUM" | "LOW"

export interface HighImpactEvent {
  event: string
  date: string
  could_flip?: boolean
}

export interface WeeklyForecastRow {
  id: string
  instrument_id: number
  symbol: string
  week_of: string
  generated_by: string
  // Technical
  technical_bias: BiasLevel | null
  technical_ai_analysis: string | null
  technical_key_drivers: string[] | null
  technical_invalidation: string | null
  key_zone_high: number | null
  key_zone_low: number | null
  invalidation_level: number | null
  trend_structure: string | null
  premium_discount: string | null
  weekly_high: number | null
  weekly_low: number | null
  // Sentimental
  sentiment_bias: BiasLevel | null
  sentiment_ai_analysis: string | null
  sentiment_key_drivers: string[] | null
  sentiment_invalidation: string | null
  retail_long_pct: number | null
  retail_short_pct: number | null
  cot_net_position: number | null
  cot_change_week: number | null
  // Composite
  overall_bias: BiasLevel | null
  confidence: ConfidenceLevel | null
  high_impact_events: HighImpactEvent[] | null
}
