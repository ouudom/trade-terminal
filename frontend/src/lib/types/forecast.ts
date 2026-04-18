export type BiasLevel = "bullish" | "bearish" | "neutral"
export type ConfidenceLevel = "HIGH" | "MEDIUM" | "LOW"

// Technical section
export interface PremiumDiscount {
  context: "premium" | "discount" | "equilibrium"
  current_price: number
  note?: string
}

export interface TrendStructure {
  weekly: string
  daily: string
  h4: string
  aligned: boolean
}

export interface SupplyDemandZone {
  type: "supply" | "demand"
  high: number
  low: number
  timeframe: string
  freshness: "fresh" | "tested" | "broken"
  tested_count: number
  strength: "strong" | "moderate" | "weak"
  confluence_notes?: string
}

export interface SupportResistanceLevel {
  level: number
  type: "support" | "resistance"
  strength: "strong" | "moderate" | "weak"
  note?: string
}

export interface VolumeProfile {
  timeframe: string
  poc: number | null
  vah: number | null
  val: number | null
  price_vs_value_area: string | null
}

export interface LiquiditySweep {
  side: "buy_side" | "sell_side"
  level: number
  swept: boolean
  implication?: string
}

export interface Imbalance {
  type: "buy" | "sell"
  price: number
  timeframe: string
}

export interface OrderFlowData {
  volume_profile?: VolumeProfile | null
  cumulative_delta_4h?: string | null
  delta_at_key_zone?: string | null
  liquidity_sweeps?: LiquiditySweep[] | null
  imbalances?: Imbalance[] | null
  data_quality?: string | null
  summary?: string | null
}

export interface TechnicalSection {
  bias: BiasLevel | null
  ai_analysis: string | null
  invalidation: string | null
  weekly_high: number | null
  weekly_low: number | null
  weekly_midpoint: number | null
  premium_discount: PremiumDiscount | null
  trend_structure: TrendStructure | null
  supply_demand_zones: SupplyDemandZone[] | null
  support_resistance_levels: SupportResistanceLevel[] | null
  order_flow: OrderFlowData | null
}

// Fundamental section
export interface NewsEvent {
  day: string
  event: string
  currency: string
  impact: "high" | "medium" | "low"
  forecast?: string
  previous?: string
  actual?: string
  bias_impact_if_above?: string
  bias_impact_if_below?: string
}

export interface FundamentalSection {
  bias: BiasLevel | null
  ai_analysis: string | null
  invalidation: string | null
  key_drivers: string[] | null
  dxy_bias: BiasLevel | null
  news: NewsEvent[] | null
}

// Sentimental section
export interface SentimentalSection {
  bias: BiasLevel | null
  ai_analysis: string | null
  invalidation: string | null
  retail_long_pct: number | null
  retail_short_pct: number | null
  retail_extreme: boolean | null
  retail_signal: string | null
  cot_net_position: number | null
  cot_change_week: number | null
  cot_trend_direction: string | null
  cot_trend_weeks: number | null
  smart_money_vs_retail: string | null
}

// Confluence section
export interface ConfluenceData {
  factors_aligned: string[] | null
  factor_count: number
  score: "HIGH" | "MEDIUM" | "LOW"
}

// Setup scenarios
export interface SetupScenario {
  entry_zone?: [number, number]
  stop: number
  target_1r2: number
  target_1r3: number
  sl_pips: number
  lot_size: number | null
  r_ratio_min: number
  narrative: string
  valid_if: string
}

export interface SetupScenarios {
  primary: "buy" | "sell" | null
  buy: SetupScenario | null
  sell: SetupScenario | null
}

// High-impact events
export interface HighImpactEvent {
  day: string
  event: string
  currency: string
  risk?: string
}

// Main weekly forecast row
export interface WeeklyForecastRow {
  id: string
  instrument_id: number
  instrument: string
  week_of: string
  generated_by: string
  technical: TechnicalSection | null
  fundamental: FundamentalSection | null
  sentimental: SentimentalSection | null
  confluence: ConfluenceData | null
  overall_bias: BiasLevel | null
  overall_ai_analysis: string | null
  overall_key_drivers: string[] | null
  overall_bias_invalidation_reasons: string[] | null
  overall_setup_scenarios: SetupScenarios | null
  confidence: ConfidenceLevel | null
  correlation_warning: string | null
  high_impact_events: HighImpactEvent[] | null
}

// Daily validation
export interface EntryTrigger {
  liquidity_sweep?: boolean
  sweep_level?: number
  sweep_side?: string
  adds_strength?: boolean
  engulfing_15m?: boolean
  bos_choch_15m?: string
  bos_choch_level?: number
  pullback_entry?: Record<string, any>
}

export interface DailyValidationRow {
  id: string
  forecast_id: string
  instrument_id: number
  instrument: string
  date: string
  session?: string
  price_at_zone?: boolean
  weekly_bias_intact?: boolean
  overnight_news_invalidation?: boolean
  entry_trigger?: EntryTrigger
  tp_path_clear?: boolean
  tp_path_blockers?: string[]
  output?: string
  output_reason?: string
}
