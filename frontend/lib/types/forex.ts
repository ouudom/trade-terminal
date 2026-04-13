export interface Candle {
  timestamp: number
  open: number
  high: number
  low: number
  close: number
  volume: number
}

export interface RawCandle {
  time: number
  open: number
  high: number
  low: number
  close: number
  volume: number
}

export type ForexEvent = {
  id: number
  currency: string
  event_name: string
  date: string | null
  time: string | null
  impact: "High" | "Medium"
  actual: string | null
  forecast: string | null
  previous: string | null
  fetched_at: string
}
