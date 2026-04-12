// ─── Interfaces ───────────────────────────────────────────────────────────────

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

export interface Candle {
  timestamp: number
  open: number
  high: number
  low: number
  close: number
  volume: number
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

// ─── Watchlist ─────────────────────────────────────────────────────────────────

export const MOCK_WATCHLIST: Asset[] = [
  {
    symbol: "AAPL",
    name: "Apple Inc.",
    price: 189.43,
    change: 2.14,
    changePct: 1.14,
    sparkline: [184.2, 185.1, 184.8, 186.3, 187.0, 186.5, 188.1, 188.9, 187.8, 189.0, 189.4],
  },
  {
    symbol: "NVDA",
    name: "NVIDIA Corp.",
    price: 875.32,
    change: 21.08,
    changePct: 2.47,
    sparkline: [845.0, 848.2, 852.1, 855.0, 860.3, 858.7, 865.4, 868.0, 871.2, 873.8, 875.3],
  },
  {
    symbol: "TSLA",
    name: "Tesla Inc.",
    price: 172.18,
    change: -4.32,
    changePct: -2.45,
    sparkline: [180.1, 179.3, 177.8, 178.2, 176.5, 175.9, 174.3, 173.8, 173.1, 172.5, 172.2],
  },
  {
    symbol: "MSFT",
    name: "Microsoft Corp.",
    price: 415.60,
    change: 3.28,
    changePct: 0.80,
    sparkline: [410.2, 411.0, 411.8, 412.5, 413.1, 413.8, 414.2, 414.9, 415.1, 415.4, 415.6],
  },
  {
    symbol: "META",
    name: "Meta Platforms",
    price: 528.90,
    change: -6.12,
    changePct: -1.14,
    sparkline: [538.0, 536.2, 535.8, 534.1, 533.2, 532.0, 531.1, 530.2, 529.8, 529.1, 528.9],
  },
  {
    symbol: "AMZN",
    name: "Amazon.com Inc.",
    price: 198.72,
    change: 1.93,
    changePct: 0.98,
    sparkline: [194.8, 195.3, 195.9, 196.4, 196.8, 197.2, 197.5, 197.9, 198.2, 198.5, 198.7],
  },
  {
    symbol: "BTC",
    name: "Bitcoin / USD",
    price: 68420.50,
    change: 1240.30,
    changePct: 1.85,
    sparkline: [64800, 65200, 65800, 66100, 66800, 67200, 67500, 67800, 68000, 68200, 68420],
  },
  {
    symbol: "ETH",
    name: "Ethereum / USD",
    price: 3512.80,
    change: -48.20,
    changePct: -1.35,
    sparkline: [3620, 3605, 3590, 3578, 3565, 3555, 3545, 3538, 3528, 3520, 3513],
  },
]

// ─── Portfolio Metrics ─────────────────────────────────────────────────────────

export const MOCK_PORTFOLIO_METRICS: PortfolioMetric[] = [
  {
    label: "Total Portfolio",
    value: "$124,830.00",
    change: "+$1,432.20",
    changePct: 1.16,
    positive: true,
  },
  {
    label: "Daily P&L",
    value: "+$1,432.20",
    change: "Today",
    changePct: 1.16,
    positive: true,
  },
  {
    label: "Total Return",
    value: "+18.42%",
    change: "+$19,380.00",
    changePct: 18.42,
    positive: true,
  },
  {
    label: "Available Cash",
    value: "$23,540.00",
    positive: undefined,
  },
]

// ─── Candles (60 x 1-min OHLCV around $189) ──────────────────────────────────

function generateCandles(): Candle[] {
  const candles: Candle[] = []
  const baseTime = Date.now() - 60 * 60 * 1000 // 1 hour ago
  let price = 187.50

  for (let i = 0; i < 60; i++) {
    const direction = Math.random() > 0.48 ? 1 : -1
    const move = Math.random() * 1.2
    const open = price
    const close = parseFloat((price + direction * move).toFixed(2))
    const high = parseFloat((Math.max(open, close) + Math.random() * 0.6).toFixed(2))
    const low = parseFloat((Math.min(open, close) - Math.random() * 0.6).toFixed(2))
    const volume = Math.floor(80000 + Math.random() * 420000)

    candles.push({
      timestamp: baseTime + i * 60 * 1000,
      open,
      high,
      low,
      close,
      volume,
    })

    price = close
  }

  return candles
}

export const MOCK_CANDLES: Candle[] = generateCandles()

// ─── Orders ───────────────────────────────────────────────────────────────────

export const MOCK_ORDERS: Order[] = [
  { id: "o1", asset: "AAPL",  side: "BUY",  qty: 50,   price: 187.20, status: "FILLED",    timestamp: "14:32:01" },
  { id: "o2", asset: "NVDA",  side: "BUY",  qty: 10,   price: 862.50, status: "FILLED",    timestamp: "14:28:47" },
  { id: "o3", asset: "TSLA",  side: "SELL", qty: 25,   price: 175.80, status: "FILLED",    timestamp: "14:21:15" },
  { id: "o4", asset: "META",  side: "SELL", qty: 15,   price: 532.00, status: "PARTIAL",   timestamp: "14:18:30" },
  { id: "o5", asset: "MSFT",  side: "BUY",  qty: 20,   price: 414.00, status: "OPEN",      timestamp: "14:15:02" },
  { id: "o6", asset: "AMZN",  side: "BUY",  qty: 30,   price: 197.50, status: "FILLED",    timestamp: "14:10:44" },
  { id: "o7", asset: "BTC",   side: "BUY",  qty: 0.5,  price: 67200.00, status: "CANCELLED", timestamp: "13:58:11" },
  { id: "o8", asset: "ETH",   side: "SELL", qty: 2,    price: 3560.00, status: "FILLED",   timestamp: "13:45:28" },
]

// ─── Positions ────────────────────────────────────────────────────────────────

// ─── Fundamental Bias ─────────────────────────────────────────────────────────

export const MOCK_OVERALL_SENTIMENT: OverallSentiment = {
  label: "Moderately Bullish",
  direction: "bullish",
  confidenceIndex: 74,
  lastUpdate: "1s ago",
}

export const MOCK_FUNDAMENTAL_BIAS: FundamentalBiasEntry[] = [
  {
    symbol: "XAUUSD",
    name: "Gold / US Dollar",
    changePct: -0.06,
    direction: "bullish",
    confidence: 68,
    lastUpdate: "27m ago",
    analysis:
      "Haven demand is firm: CME FedWatch shows 95.6% odds of a March hold at 3.50–3.75%, while geopolitical tension keeps bids supported. Main near-term risk is today's US CPI downside surprise.",
    bullets: [
      "CME FedWatch prices a 95.6% chance Fed holds at 3.50–3.75% in March, keeping policy restrictive and supporting gold.",
      "Geopolitical tensions in Eastern Europe and Middle East continue to fuel safe-haven demand.",
    ],
  },
  {
    symbol: "GBPUSD",
    name: "British Pound / US Dollar",
    changePct: 0.08,
    direction: "bearish",
    confidence: 64,
    lastUpdate: "27m ago",
    analysis:
      "Sterling is pressured by UK policy/political noise and unclear BoE guidance this week, while traders sit tight for Friday's UK labour and growth releases as the next real direction trigger.",
    bullets: [
      "Political and policy uncertainty is the dominant UK story this week, keeping sterling demand weak vs. the dollar.",
      "Friday's UK labour and growth data are the key catalyst — a miss would confirm the bearish setup.",
    ],
  },
  {
    symbol: "US100",
    name: "Nasdaq 100",
    changePct: -0.27,
    direction: "neutral",
    confidence: 64,
    lastUpdate: "27m ago",
    analysis:
      "Market is in wait-and-see mode before today's US CPI. Inflation expectations held at 3.1%, but conflict-driven oil gains keep upside inflation risk alive and cap risk appetite.",
    bullets: [
      "US consumer inflation expectations held at 3.1%, calming immediate panic but not resolving structural concerns.",
      "Conflict-driven oil price gains create upside inflation risk, limiting equity upside potential near-term.",
    ],
  },
  {
    symbol: "USDJPY",
    name: "US Dollar / Japanese Yen",
    changePct: 0.21,
    direction: "neutral",
    confidence: 64,
    lastUpdate: "27m ago",
    analysis:
      "Pair is caught between BoJ normalisation narrative and USD strength from Fed hold expectations. Positioning is mixed ahead of Japanese CPI and US inflation data later this week.",
    bullets: [
      "BoJ rate normalisation narrative provides yen support, limiting USD/JPY upside extension.",
      "Fed hold expectations keep USD well-bid, creating a directional tug-of-war with mixed near-term bias.",
    ],
  },
  {
    symbol: "EURGBP",
    name: "Euro / British Pound",
    changePct: -0.13,
    direction: "bearish",
    confidence: 82,
    lastUpdate: "27m ago",
    analysis:
      "EUR/GBP bias is the highest-conviction bearish call this session. ECB dovish pivot expectations weigh heavily on the euro while UK inflation stickiness supports relative GBP strength.",
    bullets: [
      "ECB is expected to cut rates more aggressively than BoE, driving EUR underperformance versus GBP.",
      "UK CPI stickiness is a key driver — stronger UK inflation prints support GBP relative to EUR near-term.",
    ],
  },
  {
    symbol: "US30",
    name: "Dow Jones Industrial",
    changePct: -0.34,
    direction: "neutral",
    confidence: 66,
    lastUpdate: "27m ago",
    analysis:
      "Blue-chip index reflects cautious positioning ahead of the CPI print. Defensive sector rotation is evident but not decisive. Rate-sensitive components face headwinds from elevated yield expectations.",
    bullets: [
      "Defensive rotation into utilities and consumer staples signals risk-off without full bearish commitment.",
      "Elevated rate expectations continue to pressure rate-sensitive components, capping index upside.",
    ],
  },
]

// ─── Positions ────────────────────────────────────────────────────────────────

export const MOCK_POSITIONS: Position[] = [
  {
    asset: "AAPL",
    qty: 150,
    entryPrice: 174.80,
    currentPrice: 189.43,
    pnl: 2194.50,
    pnlPct: 8.37,
  },
  {
    asset: "NVDA",
    qty: 20,
    entryPrice: 620.00,
    currentPrice: 875.32,
    pnl: 5106.40,
    pnlPct: 41.18,
  },
  {
    asset: "TSLA",
    qty: 40,
    entryPrice: 185.30,
    currentPrice: 172.18,
    pnl: -524.80,
    pnlPct: -7.08,
  },
  {
    asset: "MSFT",
    qty: 35,
    entryPrice: 398.50,
    currentPrice: 415.60,
    pnl: 598.50,
    pnlPct: 4.29,
  },
]
