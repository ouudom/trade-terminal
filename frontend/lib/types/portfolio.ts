export interface Asset {
  symbol: string
  name: string
  price: number
  change: number
  changePct: number
  sparkline: number[]
}

export interface PortfolioMetric {
  label: string
  value: string
  change?: string
  changePct?: number
  positive?: boolean
}

export type OrderSide = "BUY" | "SELL"
export type OrderStatus = "FILLED" | "PARTIAL" | "OPEN" | "CANCELLED"

export interface Order {
  id: string
  asset: string
  side: OrderSide
  qty: number
  price: number
  status: OrderStatus
  timestamp: string
}

export interface Position {
  asset: string
  qty: number
  entryPrice: number
  currentPrice: number
  pnl: number
  pnlPct: number
}
