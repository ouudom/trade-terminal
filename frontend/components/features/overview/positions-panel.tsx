import { ArrowRight } from "lucide-react"
import type { Position } from "@/lib/types"
import { cn } from "@/lib/utils"

interface PositionsPanelProps {
  positions: Position[]
}

export function PositionsPanel({ positions }: PositionsPanelProps) {
  const totalPnl = positions.reduce((sum, p) => sum + p.pnl, 0)

  return (
    <div className="rounded-lg border border-surface-border bg-surface-2">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-surface-border px-4 py-2.5">
        <span className="font-mono text-xs font-semibold uppercase tracking-wider text-muted-foreground/80">
          Open Positions
        </span>
        <span
          className={cn(
            "font-mono text-xs tabular-nums font-semibold",
            totalPnl >= 0 ? "text-profit" : "text-loss",
          )}
        >
          {totalPnl >= 0 ? "+" : ""}$
          {totalPnl.toLocaleString("en-US", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })}
        </span>
      </div>

      {/* Column labels */}
      <div className="grid grid-cols-[1fr_auto_auto] items-center gap-2 border-b border-surface-border px-4 py-1.5">
        <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground/50">Position</span>
        <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground/50 w-32 text-center">
          Entry → Current
        </span>
        <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground/50 w-24 text-right">P&L</span>
      </div>

      {/* Positions */}
      <div className="overflow-y-auto">
        {positions.map((pos) => {
          const positive = pos.pnl >= 0
          return (
            <div
              key={pos.asset}
              className="grid grid-cols-[1fr_auto_auto] items-center gap-2 border-b border-surface-border px-4 py-2.5 transition-colors last:border-0 hover:bg-surface-3 cursor-pointer"
            >
              {/* Symbol + qty */}
              <div className="flex flex-col">
                <span className="font-mono text-xs font-semibold">{pos.asset}</span>
                <span className="font-mono text-[10px] text-muted-foreground/60">
                  {pos.qty} shares
                </span>
              </div>

              {/* Entry → Current */}
              <div className="flex items-center gap-1 w-32 justify-center">
                <span className="font-mono text-[11px] text-muted-foreground tabular-nums">
                  {pos.entryPrice.toFixed(2)}
                </span>
                <ArrowRight size={9} className="text-muted-foreground/40 shrink-0" />
                <span className="font-mono text-[11px] tabular-nums">
                  {pos.currentPrice.toFixed(2)}
                </span>
              </div>

              {/* P&L */}
              <div
                className={cn(
                  "flex flex-col items-end w-24",
                  positive ? "text-profit" : "text-loss",
                )}
              >
                <span className="font-mono text-xs font-semibold tabular-nums">
                  {positive ? "+" : ""}${Math.abs(pos.pnl).toFixed(2)}
                </span>
                <span className="font-mono text-[10px] tabular-nums opacity-80">
                  {positive ? "+" : ""}
                  {pos.pnlPct.toFixed(2)}%
                </span>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
