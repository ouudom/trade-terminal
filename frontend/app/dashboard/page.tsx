import { PortfolioCards } from "@/components/dashboard/portfolio-cards"
import { MarketChart } from "@/components/dashboard/market-chart"
import { Watchlist } from "@/components/dashboard/watchlist"
import { OrdersTable } from "@/components/dashboard/orders-table"
import { PositionsPanel } from "@/components/dashboard/positions-panel"
import {
  MOCK_PORTFOLIO_METRICS,
  MOCK_CANDLES,
  MOCK_WATCHLIST,
  MOCK_ORDERS,
  MOCK_POSITIONS,
} from "@/lib/mock-data"

export default function DashboardPage() {
  return (
    <div className="flex min-h-full flex-col gap-3">
      {/* Portfolio summary row */}
      <PortfolioCards metrics={MOCK_PORTFOLIO_METRICS} />

      {/* Main content: 60/40 split */}
      <div className="flex min-h-0 flex-1 gap-3">
        {/* Left column — chart + watchlist */}
        <div className="flex min-w-0 flex-col gap-3" style={{ flex: 3 }}>
          <MarketChart candles={MOCK_CANDLES} symbol="AAPL" />
          <Watchlist assets={MOCK_WATCHLIST} />
        </div>

        {/* Right column — orders + positions */}
        <div className="flex min-w-0 flex-col gap-3" style={{ flex: 2 }}>
          <OrdersTable orders={MOCK_ORDERS} />
          <PositionsPanel positions={MOCK_POSITIONS} />
        </div>
      </div>
    </div>
  )
}
