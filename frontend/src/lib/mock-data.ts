import type { Asset, PortfolioMetric, Order, Position } from "@/lib/types"

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

// ─── Orders ───────────────────────────────────────────────────────────────────

export const MOCK_ORDERS: Order[] = [
  { id: "o1", asset: "AAPL",  side: "BUY",  qty: 50,   price: 187.20,   status: "FILLED",    timestamp: "14:32:01" },
  { id: "o2", asset: "NVDA",  side: "BUY",  qty: 10,   price: 862.50,   status: "FILLED",    timestamp: "14:28:47" },
  { id: "o3", asset: "TSLA",  side: "SELL", qty: 25,   price: 175.80,   status: "FILLED",    timestamp: "14:21:15" },
  { id: "o4", asset: "META",  side: "SELL", qty: 15,   price: 532.00,   status: "PARTIAL",   timestamp: "14:18:30" },
  { id: "o5", asset: "MSFT",  side: "BUY",  qty: 20,   price: 414.00,   status: "OPEN",      timestamp: "14:15:02" },
  { id: "o6", asset: "AMZN",  side: "BUY",  qty: 30,   price: 197.50,   status: "FILLED",    timestamp: "14:10:44" },
  { id: "o7", asset: "BTC",   side: "BUY",  qty: 0.5,  price: 67200.00, status: "CANCELLED", timestamp: "13:58:11" },
  { id: "o8", asset: "ETH",   side: "SELL", qty: 2,    price: 3560.00,  status: "FILLED",    timestamp: "13:45:28" },
]

// ─── Positions ────────────────────────────────────────────────────────────────

export const MOCK_POSITIONS: Position[] = [
  { asset: "AAPL", qty: 150, entryPrice: 174.80, currentPrice: 189.43, pnl: 2194.50,  pnlPct: 8.37  },
  { asset: "NVDA", qty: 20,  entryPrice: 620.00, currentPrice: 875.32, pnl: 5106.40,  pnlPct: 41.18 },
  { asset: "TSLA", qty: 40,  entryPrice: 185.30, currentPrice: 172.18, pnl: -524.80,  pnlPct: -7.08 },
  { asset: "MSFT", qty: 35,  entryPrice: 398.50, currentPrice: 415.60, pnl: 598.50,   pnlPct: 4.29  },
]
