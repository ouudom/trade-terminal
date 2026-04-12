"use client"

import { useState, useRef, useEffect, useCallback } from "react"
import { Button } from "@/components/ui/button"
import type { Candle } from "@/lib/mock-data"

const TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d"] as const
type Timeframe = (typeof TIMEFRAMES)[number]

const PAD = { top: 16, bottom: 8, left: 60, right: 8 }
const VOL_RATIO = 0.20
const PRICE_RATIO = 0.72
const GAP = 6

interface MarketChartProps {
  candles: Candle[]
  symbol: string
}

export function MarketChart({ candles, symbol }: MarketChartProps) {
  const [timeframe, setTimeframe] = useState<Timeframe>("1m")
  const [hoveredIdx, setHoveredIdx] = useState<number | null>(null)
  const [dims, setDims] = useState({ width: 800, height: 380 })
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const el = containerRef.current
    if (!el) return
    const ro = new ResizeObserver(([entry]) => {
      setDims({
        width: entry.contentRect.width,
        height: entry.contentRect.height,
      })
    })
    ro.observe(el)
    return () => ro.disconnect()
  }, [])

  const { width, height } = dims
  const priceH = height * PRICE_RATIO
  const volH = height * VOL_RATIO
  const volY = priceH + GAP

  const prices = candles.flatMap((c) => [c.high, c.low])
  const priceMin = Math.min(...prices)
  const priceMax = Math.max(...prices)
  const priceRange = priceMax - priceMin || 1

  const vols = candles.map((c) => c.volume)
  const volMax = Math.max(...vols)

  const innerW = width - PAD.left - PAD.right
  const candleW = innerW / candles.length
  const bodyW = Math.max(candleW * 0.6, 1)

  const toY = (p: number) =>
    PAD.top + ((priceMax - p) / priceRange) * (priceH - PAD.top - PAD.bottom)

  const candleX = (i: number) => PAD.left + i * candleW + candleW / 2

  const handleMouseMove = useCallback(
    (e: React.MouseEvent<SVGRectElement>) => {
      const rect = e.currentTarget.getBoundingClientRect()
      const x = e.clientX - rect.left - PAD.left
      const idx = Math.floor(x / candleW)
      setHoveredIdx(Math.max(0, Math.min(idx, candles.length - 1)))
    },
    [candles.length, candleW]
  )

  // Grid lines (5 horizontal)
  const gridPrices = Array.from({ length: 5 }, (_, i) =>
    priceMin + (priceRange / 4) * i
  ).reverse()

  const hovered = hoveredIdx !== null ? candles[hoveredIdx] : null
  const tooltipX = hoveredIdx !== null ? candleX(hoveredIdx) : 0
  const tooltipRight = hoveredIdx !== null && hoveredIdx > candles.length / 2

  const lastCandle = candles[candles.length - 1]
  const priceChange = lastCandle.close - candles[0].open
  const priceChangePct = (priceChange / candles[0].open) * 100

  return (
    <div className="flex flex-col rounded-lg border border-surface-border bg-surface-2">
      {/* Panel header */}
      <div className="flex items-center justify-between border-b border-surface-border px-4 py-2.5">
        <div className="flex items-center gap-3">
          <span className="font-mono text-sm font-semibold">{symbol}</span>
          <span className="font-mono text-xl font-semibold tabular-nums">
            ${lastCandle.close.toFixed(2)}
          </span>
          <span
            className={`font-mono text-xs tabular-nums ${
              priceChange >= 0 ? "text-profit" : "text-loss"
            }`}
          >
            {priceChange >= 0 ? "+" : ""}
            {priceChange.toFixed(2)} ({priceChangePct >= 0 ? "+" : ""}
            {priceChangePct.toFixed(2)}%)
          </span>
        </div>

        {/* Timeframe buttons */}
        <div className="flex items-center gap-0.5">
          {TIMEFRAMES.map((tf) => (
            <Button
              key={tf}
              variant={timeframe === tf ? "outline" : "ghost"}
              size="xs"
              onClick={() => setTimeframe(tf)}
              className="font-mono text-[11px]"
            >
              {tf}
            </Button>
          ))}
        </div>
      </div>

      {/* SVG Chart */}
      <div ref={containerRef} className="flex-1 min-h-0" style={{ height: 340 }}>
        <svg
          width={width}
          height={height}
          className="block"
          onMouseLeave={() => setHoveredIdx(null)}
        >
          {/* Price grid lines */}
          {gridPrices.map((p) => {
            const y = toY(p)
            return (
              <g key={p}>
                <line
                  x1={PAD.left}
                  x2={width - PAD.right}
                  y1={y}
                  y2={y}
                  stroke="var(--surface-border)"
                  strokeWidth={1}
                />
                <text
                  x={PAD.left - 6}
                  y={y + 4}
                  textAnchor="end"
                  fill="var(--color-muted-foreground)"
                  fontSize={9}
                  fontFamily="'Geist Mono', monospace"
                >
                  {p.toFixed(2)}
                </text>
              </g>
            )
          })}

          {/* Candles */}
          {candles.map((c, i) => {
            const x = candleX(i)
            const isUp = c.close >= c.open
            const color = isUp ? "var(--profit)" : "var(--loss)"
            const bodyTop = toY(Math.max(c.open, c.close))
            const bodyBot = toY(Math.min(c.open, c.close))
            const bodyHeight = Math.max(bodyBot - bodyTop, 1)
            const isHovered = hoveredIdx === i

            return (
              <g key={i} opacity={hoveredIdx !== null && !isHovered ? 0.5 : 1}>
                {/* Wick */}
                <line
                  x1={x}
                  x2={x}
                  y1={toY(c.high)}
                  y2={toY(c.low)}
                  stroke="var(--candle-wick)"
                  strokeWidth={1}
                />
                {/* Body */}
                <rect
                  x={x - bodyW / 2}
                  y={bodyTop}
                  width={bodyW}
                  height={bodyHeight}
                  fill={color}
                  rx={1}
                />
              </g>
            )
          })}

          {/* Volume bars */}
          {candles.map((c, i) => {
            const x = candleX(i)
            const isUp = c.close >= c.open
            const barH = (c.volume / volMax) * (volH - 4)
            return (
              <rect
                key={`v${i}`}
                x={x - bodyW / 2}
                y={volY + (volH - barH)}
                width={bodyW}
                height={barH}
                fill={isUp ? "var(--profit)" : "var(--loss)"}
                opacity={0.4}
                rx={1}
              />
            )
          })}

          {/* Volume separator line */}
          <line
            x1={PAD.left}
            x2={width - PAD.right}
            y1={volY}
            y2={volY}
            stroke="var(--surface-border)"
            strokeWidth={1}
          />

          {/* Hover overlay */}
          <rect
            x={PAD.left}
            y={0}
            width={innerW}
            height={height}
            fill="transparent"
            onMouseMove={handleMouseMove}
            style={{ cursor: "crosshair" }}
          />

          {/* Crosshair + tooltip */}
          {hovered && hoveredIdx !== null && (
            <g>
              {/* Vertical line */}
              <line
                x1={tooltipX}
                x2={tooltipX}
                y1={PAD.top}
                y2={height}
                stroke="var(--color-muted-foreground)"
                strokeWidth={1}
                strokeDasharray="3,3"
                opacity={0.5}
              />

              {/* Tooltip box */}
              {(() => {
                const tw = 148
                const th = 84
                const tx = tooltipRight ? tooltipX - tw - 8 : tooltipX + 8
                const ty = PAD.top + 4
                const isUp = hovered.close >= hovered.open
                const color = isUp ? "var(--profit)" : "var(--loss)"
                return (
                  <g>
                    <rect
                      x={tx}
                      y={ty}
                      width={tw}
                      height={th}
                      fill="var(--surface-3)"
                      stroke="var(--surface-border)"
                      strokeWidth={1}
                      rx={4}
                    />
                    {[
                      ["O", hovered.open.toFixed(2)],
                      ["H", hovered.high.toFixed(2)],
                      ["L", hovered.low.toFixed(2)],
                      ["C", hovered.close.toFixed(2)],
                    ].map(([label, val], idx) => (
                      <g key={label}>
                        <text
                          x={tx + 10}
                          y={ty + 18 + idx * 16}
                          fill="var(--color-muted-foreground)"
                          fontSize={10}
                          fontFamily="'Geist Mono', monospace"
                        >
                          {label}
                        </text>
                        <text
                          x={tx + tw - 10}
                          y={ty + 18 + idx * 16}
                          textAnchor="end"
                          fill={label === "C" ? color : "var(--color-foreground)"}
                          fontSize={10}
                          fontFamily="'Geist Mono', monospace"
                          fontWeight={label === "C" ? "600" : "400"}
                        >
                          {val}
                        </text>
                      </g>
                    ))}
                  </g>
                )
              })()}
            </g>
          )}
        </svg>
      </div>
    </div>
  )
}
