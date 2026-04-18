"use client"

import { useState } from "react"
import { ChevronDown } from "lucide-react"
import { cn } from "@/lib/utils"
import type { WeeklyForecastRow, BiasLevel, ConfidenceLevel } from "@/lib/types/forecast"

// ── Direction helpers ──────────────────────────────────────────────────────────

type DirStyles = { text: string; bg: string; bar: string; label: string; cssVar: string }

function dirStyles(d: BiasLevel | null): DirStyles {
  if (d === "bullish")
    return { text: "text-profit", bg: "bg-profit/10", bar: "bg-profit", label: "BULLISH", cssVar: "var(--profit)" }
  if (d === "bearish")
    return { text: "text-loss", bg: "bg-loss/10", bar: "bg-loss", label: "BEARISH", cssVar: "var(--loss)" }
  return { text: "text-teal", bg: "bg-teal/10", bar: "bg-teal", label: "NEUTRAL", cssVar: "var(--teal)" }
}

function BiasBadge({ bias, size = "sm" }: { bias: BiasLevel | null; size?: "xs" | "sm" }) {
  const ds = dirStyles(bias)
  return (
    <span
      className={cn(
        "font-mono font-bold tracking-[0.12em] rounded-sm",
        ds.text, ds.bg,
        size === "xs" ? "text-[8px] px-1 py-[2px]" : "text-[9px] px-1.5 py-[3px]",
      )}
    >
      {ds.label}
    </span>
  )
}

function ConfidenceBadge({ level }: { level: ConfidenceLevel | null }) {
  const styles =
    level === "HIGH"
      ? "text-profit/80 bg-profit/5 border border-profit/20"
      : level === "MEDIUM"
        ? "text-yellow-400/80 bg-yellow-400/5 border border-yellow-400/20"
        : "text-muted-foreground/50 bg-surface-3 border border-surface-border"
  return (
    <span className={cn("font-mono text-[8px] font-bold tracking-[0.15em] px-1.5 py-[3px] rounded-sm", styles)}>
      {level ?? "—"}
    </span>
  )
}

// ── Bias distribution strip ────────────────────────────────────────────────────

function BiasDistribution({ rows }: { rows: WeeklyForecastRow[] }) {
  if (!rows.length) return null
  const bull = rows.filter((r) => r.overall_bias === "bullish").length
  const bear = rows.filter((r) => r.overall_bias === "bearish").length
  const neut = rows.filter((r) => r.overall_bias === "neutral").length
  const total = rows.length

  return (
    <div className="flex items-center gap-2.5">
      <div className="flex h-[3px] w-24 overflow-hidden rounded-full bg-surface-3">
        <div className="bg-profit h-full" style={{ width: `${(bull / total) * 100}%` }} />
        <div className="bg-teal h-full" style={{ width: `${(neut / total) * 100}%` }} />
        <div className="bg-loss h-full" style={{ width: `${(bear / total) * 100}%` }} />
      </div>
      <div className="flex items-center gap-2 font-mono text-[9px] text-muted-foreground/40">
        {bull > 0 && <span><span className="text-profit">{bull}</span> bull</span>}
        {neut > 0 && <span><span className="text-teal">{neut}</span> neutral</span>}
        {bear > 0 && <span><span className="text-loss">{bear}</span> bear</span>}
      </div>
    </div>
  )
}

// ── Price zone display ─────────────────────────────────────────────────────────

function ZoneRow({ label, value }: { label: string; value: number | null }) {
  if (value == null) return null
  return (
    <div className="flex items-center justify-between gap-3">
      <span className="font-mono text-[9px] uppercase tracking-[0.15em] text-muted-foreground/35">{label}</span>
      <span className="font-mono text-xs tabular-nums text-foreground/70">{value.toFixed(4)}</span>
    </div>
  )
}

function COTChange({ change }: { change: number | null }) {
  if (change == null) return <span className="text-muted-foreground/30">—</span>
  const pos = change > 0
  return (
    <span className={cn("font-mono text-xs tabular-nums font-semibold", pos ? "text-profit" : "text-loss")}>
      {pos ? "+" : ""}{change.toLocaleString()}
    </span>
  )
}

// ── Instrument row ─────────────────────────────────────────────────────────────

function InstrumentRow({ row, index }: { row: WeeklyForecastRow; index: number }) {
  const [open, setOpen] = useState(false)
  const ds = dirStyles(row.overall_bias)

  return (
    <div
      className={cn(
        "relative border-b border-surface-border last:border-b-0 transition-colors duration-150",
        open ? "bg-surface-2" : "bg-surface-1 hover:bg-surface-2",
      )}
    >
      {/* Left accent bar */}
      <div className="absolute left-0 top-0 bottom-0 w-0.5 overflow-hidden bg-surface-3">
        <div className={cn("w-full h-full", ds.bar)} />
      </div>

      <button className="w-full text-left focus:outline-none" onClick={() => setOpen((v) => !v)}>
        <div className="flex items-center gap-4 pl-5 pr-4 py-3.5">
          <span className="font-mono text-[10px] text-muted-foreground/25 w-5 shrink-0 tabular-nums">
            {String(index + 1).padStart(2, "0")}
          </span>

          <div className="w-28 shrink-0">
            <div className="font-mono text-sm font-bold tracking-tight text-foreground leading-none">
              {row.symbol}
            </div>
            {row.trend_structure && (
              <div className="font-mono text-[9px] text-muted-foreground/35 mt-[3px] leading-none">
                {row.trend_structure.replace(/_/g, "/")}
              </div>
            )}
          </div>

          <div className="w-20 shrink-0">
            <BiasBadge bias={row.overall_bias} />
          </div>

          <div className="w-14 shrink-0">
            <ConfidenceBadge level={row.confidence} />
          </div>

          <div className="flex items-center gap-2 w-36 shrink-0">
            <div className="flex items-center gap-1">
              <span className="font-mono text-[8px] text-muted-foreground/30 tracking-wider">T</span>
              <BiasBadge bias={row.technical_bias} size="xs" />
            </div>
            <div className="flex items-center gap-1">
              <span className="font-mono text-[8px] text-muted-foreground/30 tracking-wider">S</span>
              <BiasBadge bias={row.sentiment_bias} size="xs" />
            </div>
          </div>

          <p className="flex-1 font-mono text-[11px] text-muted-foreground/50 leading-relaxed truncate hidden sm:block">
            {row.technical_ai_analysis ?? row.sentiment_ai_analysis ?? "—"}
          </p>

          <ChevronDown
            size={12}
            className={cn(
              "text-muted-foreground/30 transition-transform duration-200 shrink-0",
              open && "rotate-180",
            )}
          />
        </div>
      </button>

      {/* Expanded panel */}
      {open && (
        <div className="pl-14 pr-5 pb-5 border-t border-surface-border/60">
          <div className="pt-4 grid grid-cols-1 lg:grid-cols-2 gap-6">

            {/* Technical */}
            <div className="space-y-3">
              <p className="font-mono text-[9px] uppercase tracking-[0.2em] text-muted-foreground/35">
                Technical Analysis
              </p>
              {row.technical_ai_analysis && (
                <p className="text-sm text-muted-foreground leading-relaxed">{row.technical_ai_analysis}</p>
              )}

              {(row.key_zone_high != null || row.key_zone_low != null || row.invalidation_level != null) && (
                <div className="mt-3 rounded-md border border-surface-border bg-surface-2 px-3 py-2.5 space-y-1.5">
                  <ZoneRow label="Zone high" value={row.key_zone_high} />
                  <ZoneRow label="Zone low" value={row.key_zone_low} />
                  <ZoneRow label="Weekly high" value={row.weekly_high} />
                  <ZoneRow label="Weekly low" value={row.weekly_low} />
                  {row.invalidation_level != null && (
                    <div className="pt-1 border-t border-surface-border">
                      <ZoneRow label="Invalidation" value={row.invalidation_level} />
                    </div>
                  )}
                </div>
              )}

              <div className="flex items-center gap-3 flex-wrap">
                {row.premium_discount && (
                  <span className="font-mono text-[8px] font-bold tracking-[0.12em] px-1.5 py-[2px] rounded-sm bg-surface-3 text-muted-foreground/60">
                    {row.premium_discount}
                  </span>
                )}
              </div>

              {row.technical_key_drivers && row.technical_key_drivers.length > 0 && (
                <div>
                  <p className="font-mono text-[9px] uppercase tracking-[0.15em] text-muted-foreground/30 mb-1.5">
                    Key Drivers
                  </p>
                  <ul className="space-y-1.5">
                    {row.technical_key_drivers.map((d, i) => (
                      <li key={i} className="flex gap-2 text-xs text-muted-foreground/65 leading-relaxed">
                        <span className={cn("mt-[5px] h-[4px] w-[4px] rounded-sm shrink-0", dirStyles(row.technical_bias).bar)} />
                        {d}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {row.technical_invalidation && (
                <p className="font-mono text-[10px] text-loss/50 leading-relaxed">
                  ⚠ {row.technical_invalidation}
                </p>
              )}
            </div>

            {/* Sentimental */}
            <div className="space-y-3">
              <p className="font-mono text-[9px] uppercase tracking-[0.2em] text-muted-foreground/35">
                Sentimental Analysis
              </p>
              {row.sentiment_ai_analysis && (
                <p className="text-sm text-muted-foreground leading-relaxed">{row.sentiment_ai_analysis}</p>
              )}

              {(row.retail_long_pct != null || row.cot_net_position != null) && (
                <div className="rounded-md border border-surface-border bg-surface-2 px-3 py-2.5 space-y-2">
                  {row.retail_long_pct != null && row.retail_short_pct != null && (
                    <div className="space-y-1">
                      <div className="flex justify-between font-mono text-[9px] text-muted-foreground/40">
                        <span>Retail Long</span>
                        <span className="text-profit">{row.retail_long_pct.toFixed(1)}%</span>
                      </div>
                      <div className="flex h-[3px] w-full overflow-hidden rounded-full bg-surface-3">
                        <div className="bg-profit h-full" style={{ width: `${row.retail_long_pct}%` }} />
                        <div className="bg-loss h-full" style={{ width: `${row.retail_short_pct}%` }} />
                      </div>
                      <div className="flex justify-between font-mono text-[9px] text-muted-foreground/40">
                        <span>Retail Short</span>
                        <span className="text-loss">{row.retail_short_pct.toFixed(1)}%</span>
                      </div>
                    </div>
                  )}

                  {row.cot_net_position != null && (
                    <div className="flex items-center justify-between border-t border-surface-border pt-2">
                      <span className="font-mono text-[9px] text-muted-foreground/35 uppercase tracking-wider">COT Net</span>
                      <span className="font-mono text-xs tabular-nums text-foreground/70">
                        {row.cot_net_position.toLocaleString()}
                      </span>
                    </div>
                  )}

                  {row.cot_change_week != null && (
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-[9px] text-muted-foreground/35 uppercase tracking-wider">COT Δ Week</span>
                      <COTChange change={row.cot_change_week} />
                    </div>
                  )}
                </div>
              )}

              {row.sentiment_key_drivers && row.sentiment_key_drivers.length > 0 && (
                <div>
                  <p className="font-mono text-[9px] uppercase tracking-[0.15em] text-muted-foreground/30 mb-1.5">
                    Key Drivers
                  </p>
                  <ul className="space-y-1.5">
                    {row.sentiment_key_drivers.map((d, i) => (
                      <li key={i} className="flex gap-2 text-xs text-muted-foreground/65 leading-relaxed">
                        <span className={cn("mt-[5px] h-[4px] w-[4px] rounded-sm shrink-0", dirStyles(row.sentiment_bias).bar)} />
                        {d}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {row.sentiment_invalidation && (
                <p className="font-mono text-[10px] text-loss/50 leading-relaxed">
                  ⚠ {row.sentiment_invalidation}
                </p>
              )}
            </div>
          </div>

          {/* High-impact events */}
          {row.high_impact_events && row.high_impact_events.length > 0 && (
            <div className="mt-4 pt-4 border-t border-surface-border/60">
              <p className="font-mono text-[9px] uppercase tracking-[0.2em] text-muted-foreground/35 mb-2">
                High-Impact Events
              </p>
              <div className="flex flex-wrap gap-2">
                {row.high_impact_events.map((ev, i) => (
                  <div
                    key={i}
                    className={cn(
                      "flex items-center gap-2 rounded-sm border px-2 py-1",
                      ev.could_flip
                        ? "border-loss/20 bg-loss/5"
                        : "border-surface-border bg-surface-2",
                    )}
                  >
                    <span className="font-mono text-[10px] text-foreground/70">{ev.event}</span>
                    <span className="font-mono text-[9px] text-muted-foreground/40">{ev.date}</span>
                    {ev.could_flip && (
                      <span className="font-mono text-[8px] text-loss/60 font-bold">FLIP RISK</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// ── Main dashboard ─────────────────────────────────────────────────────────────

interface WeeklyForecastDashboardProps {
  rows: WeeklyForecastRow[]
  weekOf: string
}

export function WeeklyForecastDashboard({ rows, weekOf }: WeeklyForecastDashboardProps) {
  const weekDate = new Date(weekOf + "T00:00:00Z")
  const weekEnd = new Date(weekDate)
  weekEnd.setUTCDate(weekEnd.getUTCDate() + 4)

  const fmt = (d: Date) =>
    d.toLocaleDateString("en-US", { month: "short", day: "2-digit", timeZone: "UTC" }).toUpperCase()

  const weekLabel = `${fmt(weekDate)} – ${fmt(weekEnd)}, ${weekDate.getUTCFullYear()}`

  const dominantBias: BiasLevel =
    rows.filter((r) => r.overall_bias === "bullish").length > rows.filter((r) => r.overall_bias === "bearish").length
      ? "bullish"
      : rows.filter((r) => r.overall_bias === "bearish").length > rows.filter((r) => r.overall_bias === "bullish").length
        ? "bearish"
        : "neutral"

  const ds = dirStyles(dominantBias)

  return (
    <div className="flex min-h-full flex-col gap-3">
      {/* Header */}
      <div className="rounded-lg border border-surface-border bg-surface-1 px-5 py-4">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
              <span className="font-mono text-[9px] uppercase tracking-[0.25em] text-muted-foreground/35">
                Weekly Outlook
              </span>
              <span className="h-px w-4 bg-surface-border" />
              <span className="font-mono text-[9px] text-muted-foreground/25 tracking-wide">
                {weekLabel}
              </span>
            </div>

            <h1
              className="text-[26px] font-extrabold leading-none text-foreground"
              style={{ fontFamily: "var(--font-syne)", letterSpacing: "-0.02em" }}
            >
              Weekly Forecast
            </h1>

            <div className="mt-0.5">
              {rows.length === 0 ? (
                <span className="font-mono text-sm text-muted-foreground/40">No forecast data for this week</span>
              ) : (
                <span className={cn("font-mono text-sm font-semibold", ds.text)}>
                  {dominantBias.charAt(0).toUpperCase() + dominantBias.slice(1)} bias dominant
                </span>
              )}
            </div>
          </div>

          <div className="flex flex-col items-end gap-3 pt-0.5">
            <div className="flex items-center gap-1.5">
              <div className="h-1.5 w-1.5 rounded-full bg-profit animate-pulse" />
              <span className="font-mono text-[9px] uppercase tracking-widest text-profit">Live</span>
            </div>
            <BiasDistribution rows={rows} />
            <span className="font-mono text-[9px] text-muted-foreground/25">
              {rows.length} instrument{rows.length !== 1 ? "s" : ""}
            </span>
          </div>
        </div>
      </div>

      {/* Column headers */}
      <div className="flex items-center gap-4 px-5 py-1">
        <span className="w-5 shrink-0" />
        <span className="w-28 shrink-0 font-mono text-[9px] uppercase tracking-[0.18em] text-muted-foreground/30">
          Instrument
        </span>
        <span className="w-20 shrink-0 font-mono text-[9px] uppercase tracking-[0.18em] text-muted-foreground/30">
          Bias
        </span>
        <span className="w-14 shrink-0 font-mono text-[9px] uppercase tracking-[0.18em] text-muted-foreground/30">
          Conf
        </span>
        <span className="w-36 shrink-0 font-mono text-[9px] uppercase tracking-[0.18em] text-muted-foreground/30">
          T / S
        </span>
        <span className="flex-1 font-mono text-[9px] uppercase tracking-[0.18em] text-muted-foreground/30 hidden sm:block">
          Analysis
        </span>
      </div>

      {/* Instrument list */}
      <div className="overflow-hidden rounded-lg border border-surface-border">
        {rows.length === 0 ? (
          <div className="flex flex-col items-center justify-center gap-2 py-16">
            <span className="font-mono text-[9px] uppercase tracking-widest text-muted-foreground/25">
              No Data
            </span>
            <span className="font-mono text-xs text-muted-foreground/40">
              Run the weekly forecast routine to populate this week
            </span>
          </div>
        ) : (
          rows.map((row, i) => <InstrumentRow key={row.id} row={row} index={i} />)
        )}
      </div>
    </div>
  )
}
