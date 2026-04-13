import { Search } from "lucide-react"
import type { Asset } from "@/lib/types"
import { cn } from "@/lib/utils"

interface SparklineProps {
  data: number[]
  positive: boolean
  width?: number
  height?: number
}

function Sparkline({ data, positive, width = 64, height = 24 }: SparklineProps) {
  const min = Math.min(...data)
  const max = Math.max(...data)
  const range = max - min || 1

  const points = data
    .map((v, i) => {
      const x = (i / (data.length - 1)) * width
      const y = height - ((v - min) / range) * (height - 2) - 1
      return `${x},${y}`
    })
    .join(" ")

  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      className="shrink-0"
    >
      <polyline
        points={points}
        fill="none"
        stroke={positive ? "var(--profit)" : "var(--loss)"}
        strokeWidth={1.5}
        strokeLinejoin="round"
        strokeLinecap="round"
      />
    </svg>
  )
}

interface WatchlistProps {
  assets: Asset[]
}

export function Watchlist({ assets }: WatchlistProps) {
  return (
    <div className="rounded-lg border border-surface-border bg-surface-2">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-surface-border px-4 py-2.5">
        <span className="font-mono text-xs font-semibold uppercase tracking-wider text-muted-foreground/80">
          Watchlist
        </span>
        <button className="flex h-6 w-6 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-surface-3 hover:text-foreground">
          <Search size={13} />
        </button>
      </div>

      {/* Column headers */}
      <div className="grid grid-cols-[1fr_auto_auto] items-center gap-2 border-b border-surface-border px-4 py-1.5">
        <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground/50">Asset</span>
        <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground/50 w-16 text-center">Trend</span>
        <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground/50 w-24 text-right">Price / Chg</span>
      </div>

      {/* Asset rows */}
      <div className="overflow-y-auto max-h-52">
        {assets.map((asset) => {
          const positive = asset.changePct >= 0
          return (
            <div
              key={asset.symbol}
              className="grid grid-cols-[1fr_auto_auto] items-center gap-2 border-b border-surface-border px-4 py-2 transition-colors last:border-0 hover:bg-surface-3 cursor-pointer"
            >
              {/* Symbol + name */}
              <div className="flex flex-col min-w-0">
                <span className="font-mono text-xs font-semibold">{asset.symbol}</span>
                <span className="truncate font-mono text-[10px] text-muted-foreground/60">
                  {asset.name}
                </span>
              </div>

              {/* Sparkline */}
              <div className="w-16 flex justify-center">
                <Sparkline data={asset.sparkline} positive={positive} />
              </div>

              {/* Price + change */}
              <div className="flex flex-col items-end w-24">
                <span className="font-mono text-xs tabular-nums">
                  {asset.price >= 1000
                    ? asset.price.toLocaleString("en-US", {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                      })
                    : asset.price.toFixed(2)}
                </span>
                <span
                  className={cn(
                    "font-mono text-[10px] tabular-nums",
                    positive ? "text-profit" : "text-loss",
                  )}
                >
                  {positive ? "+" : ""}
                  {asset.changePct.toFixed(2)}%
                </span>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
