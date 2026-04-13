"use client"

import { useState } from "react"
import { ChevronDown } from "lucide-react"
import { cn } from "@/lib/utils"
import type { FundamentalBiasEntry, OverallSentiment, BiasDirection } from "@/lib/types"

// ── Direction helpers ──────────────────────────────────────────────────────────

type DirStyles = {
  text: string
  bg: string
  bar: string
  label: string
  cssVar: string
}

function dirStyles(d: BiasDirection): DirStyles {
  if (d === "bullish")
    return { text: "text-profit", bg: "bg-profit/10", bar: "bg-profit", label: "BULLISH", cssVar: "var(--profit)" }
  if (d === "bearish")
    return { text: "text-loss", bg: "bg-loss/10", bar: "bg-loss", label: "BEARISH", cssVar: "var(--loss)" }
  return { text: "text-teal", bg: "bg-teal/10", bar: "bg-teal", label: "NEUTRAL", cssVar: "var(--teal)" }
}

// ── Signal bars (confidence) ───────────────────────────────────────────────────

function SignalBars({ pct, ds }: { pct: number; ds: DirStyles }) {
  const filled = Math.max(1, Math.round(pct / 20))
  return (
    <div className="flex items-end gap-[3px]" style={{ height: "15px" }}>
      {[1, 2, 3, 4, 5].map((i) => (
        <div
          key={i}
          className={cn("w-[5px] rounded-[2px]", i <= filled ? ds.bar : "bg-surface-3")}
          style={{ height: `${(i / 5) * 100}%` }}
        />
      ))}
    </div>
  )
}

// ── Bias distribution strip ────────────────────────────────────────────────────

function BiasDistribution({ entries }: { entries: FundamentalBiasEntry[] }) {
  if (!entries.length) return null
  const bull = entries.filter((e) => e.direction === "bullish").length
  const bear = entries.filter((e) => e.direction === "bearish").length
  const neut = entries.filter((e) => e.direction === "neutral").length
  const total = entries.length

  return (
    <div className="flex items-center gap-2.5">
      <div className="flex h-[3px] w-24 overflow-hidden rounded-full bg-surface-3">
        <div className="bg-profit h-full" style={{ width: `${(bull / total) * 100}%` }} />
        <div className="bg-teal h-full" style={{ width: `${(neut / total) * 100}%` }} />
        <div className="bg-loss h-full" style={{ width: `${(bear / total) * 100}%` }} />
      </div>
      <div className="flex items-center gap-2 font-mono text-[9px] text-muted-foreground/40">
        {bull > 0 && (
          <span>
            <span className="text-profit">{bull}</span> bull
          </span>
        )}
        {neut > 0 && (
          <span>
            <span className="text-teal">{neut}</span> neutral
          </span>
        )}
        {bear > 0 && (
          <span>
            <span className="text-loss">{bear}</span> bear
          </span>
        )}
      </div>
    </div>
  )
}

// ── Spectrum meter ─────────────────────────────────────────────────────────────

function SpectrumMeter({ sentiment }: { sentiment: OverallSentiment }) {
  const pos =
    sentiment.direction === "bullish"
      ? Math.min(95, 50 + sentiment.confidenceIndex * 0.44)
      : sentiment.direction === "bearish"
        ? Math.max(5, 50 - sentiment.confidenceIndex * 0.44)
        : 50
  const ds = dirStyles(sentiment.direction)

  return (
    <div className="flex items-center gap-2">
      <span className="font-mono text-[9px] uppercase tracking-widest text-loss/50">Bear</span>
      <div className="relative h-[3px] w-24 rounded-full bg-surface-3">
        <div
          className="absolute top-1/2 -translate-y-1/2 h-2.5 w-2.5 rounded-full border-2 border-surface-1 -translate-x-1/2 transition-all duration-700"
          style={{
            left: `${pos}%`,
            backgroundColor: ds.cssVar,
            boxShadow: `0 0 8px ${ds.cssVar}`,
          }}
        />
      </div>
      <span className="font-mono text-[9px] uppercase tracking-widest text-profit/50">Bull</span>
    </div>
  )
}

// ── Instrument row ─────────────────────────────────────────────────────────────

function InstrumentRow({ entry, index }: { entry: FundamentalBiasEntry; index: number }) {
  const [open, setOpen] = useState(false)
  const ds = dirStyles(entry.direction)

  return (
    <div
      className={cn(
        "relative border-b border-surface-border last:border-b-0 transition-colors duration-150",
        open ? "bg-surface-2" : "bg-surface-1 hover:bg-surface-2",
      )}
    >
      {/* Left accent bar */}
      <div className="absolute left-0 top-0 bottom-0 w-0.5 overflow-hidden bg-surface-3">
        <div
          className={cn("w-full transition-[height] duration-700 ease-out", ds.bar)}
          style={{ height: `${entry.confidence}%` }}
        />
      </div>

      {/* Clickable row */}
      <button className="w-full text-left focus:outline-none" onClick={() => setOpen((v) => !v)}>
        <div className="flex items-center gap-4 pl-5 pr-4 py-3.5">
          <span className="font-mono text-[10px] text-muted-foreground/25 w-5 shrink-0 select-none tabular-nums">
            {String(index + 1).padStart(2, "0")}
          </span>

          <div className="w-32 shrink-0">
            <div className="font-mono text-sm font-bold tracking-tight text-foreground leading-none">
              {entry.symbol}
            </div>
            <div className="font-mono text-[9px] text-muted-foreground/35 mt-[3px] leading-none truncate">
              {entry.name}
            </div>
          </div>

          <div className="w-20 shrink-0">
            <span
              className={cn(
                "font-mono text-[9px] font-bold tracking-[0.15em] px-1.5 py-[3px] rounded-sm",
                ds.text,
                ds.bg,
              )}
            >
              {ds.label}
            </span>
          </div>

          <div className="flex items-center gap-2 w-[90px] shrink-0">
            <SignalBars pct={entry.confidence} ds={ds} />
            <span className={cn("font-mono text-xs font-semibold tabular-nums", ds.text)}>
              {entry.confidence}%
            </span>
          </div>

          <p className="flex-1 font-mono text-[11px] text-muted-foreground/50 leading-relaxed truncate hidden sm:block">
            {entry.analysis}
          </p>

          <div className="flex items-center gap-3 shrink-0">
            <span className="font-mono text-[9px] text-muted-foreground/25 tabular-nums hidden md:block">
              {entry.lastUpdate}
            </span>
            <ChevronDown
              size={12}
              className={cn(
                "text-muted-foreground/30 transition-transform duration-200 shrink-0",
                open && "rotate-180",
              )}
            />
          </div>
        </div>
      </button>

      {/* Expanded analysis */}
      {open && (
        <div className="pl-14 pr-5 pb-5 border-t border-surface-border/60">
          <div
            className="pt-4 grid gap-6"
            style={{
              gridTemplateColumns: entry.bullets.length > 0 ? "1fr 18rem" : "1fr",
            }}
          >
            <div>
              <p className="font-mono text-[9px] uppercase tracking-[0.2em] text-muted-foreground/35 mb-2">
                Analysis
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">{entry.analysis}</p>
              <div className="mt-3 flex items-center gap-2">
                <div className={cn("h-px flex-1 opacity-15", ds.bar)} />
                <span className="font-mono text-[9px] text-muted-foreground/30 tabular-nums">
                  {entry.lastUpdate}
                </span>
              </div>
            </div>

            {entry.bullets.length > 0 && (
              <div>
                <p className="font-mono text-[9px] uppercase tracking-[0.2em] text-muted-foreground/35 mb-2">
                  Key Drivers
                </p>
                <ul className="space-y-2.5">
                  {entry.bullets.map((b, i) => (
                    <li
                      key={i}
                      className="flex gap-2.5 text-xs text-muted-foreground/65 leading-relaxed"
                    >
                      <span
                        className={cn("mt-[5px] h-[4px] w-[4px] rounded-sm shrink-0", ds.bar)}
                      />
                      {b}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

// ── Main dashboard ─────────────────────────────────────────────────────────────

interface FundamentalBiasDashboardProps {
  entries: FundamentalBiasEntry[]
  sentiment: OverallSentiment
}

export function FundamentalBiasDashboard({ entries, sentiment }: FundamentalBiasDashboardProps) {
  const ds = dirStyles(sentiment.direction)
  const dateStr = new Date()
    .toLocaleDateString("en-US", { month: "short", day: "2-digit", year: "numeric" })
    .toUpperCase()

  return (
    <div className="flex min-h-full flex-col gap-3">
      {/* Briefing header */}
      <div className="rounded-lg border border-surface-border bg-surface-1 px-5 py-4">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
              <span className="font-mono text-[9px] uppercase tracking-[0.25em] text-muted-foreground/35">
                Intelligence Brief
              </span>
              <span className="h-px w-4 bg-surface-border" />
              <span className="font-mono text-[9px] text-muted-foreground/25 tracking-wide">
                {dateStr}
              </span>
            </div>

            <h1
              className="text-[26px] font-extrabold leading-none text-foreground"
              style={{ fontFamily: "var(--font-syne)", letterSpacing: "-0.02em" }}
            >
              Fundamental Bias
            </h1>

            <div className="flex items-center gap-3 mt-0.5">
              <span className={cn("font-mono text-sm font-semibold", ds.text)}>
                {sentiment.label}
              </span>
              <SpectrumMeter sentiment={sentiment} />
              <span className={cn("font-mono text-xs font-bold tabular-nums", ds.text)}>
                {sentiment.confidenceIndex}%
              </span>
            </div>
          </div>

          <div className="flex flex-col items-end gap-3 pt-0.5">
            <div className="flex items-center gap-1.5">
              <div className="h-1.5 w-1.5 rounded-full bg-profit animate-pulse" />
              <span className="font-mono text-[9px] uppercase tracking-widest text-profit">Live</span>
            </div>
            <BiasDistribution entries={entries} />
            <span className="font-mono text-[9px] text-muted-foreground/25">
              {entries.length} instrument{entries.length !== 1 ? "s" : ""}
            </span>
          </div>
        </div>
      </div>

      {/* Column headers */}
      <div className="flex items-center gap-4 px-5 py-1">
        <span className="w-5 shrink-0" />
        <span className="w-32 shrink-0 font-mono text-[9px] uppercase tracking-[0.18em] text-muted-foreground/30">
          Instrument
        </span>
        <span className="w-20 shrink-0 font-mono text-[9px] uppercase tracking-[0.18em] text-muted-foreground/30">
          Bias
        </span>
        <span className="w-[90px] shrink-0 font-mono text-[9px] uppercase tracking-[0.18em] text-muted-foreground/30">
          Signal
        </span>
        <span className="flex-1 font-mono text-[9px] uppercase tracking-[0.18em] text-muted-foreground/30 hidden sm:block">
          Analysis
        </span>
        <span className="shrink-0 font-mono text-[9px] uppercase tracking-[0.18em] text-muted-foreground/30 pr-[18px] hidden md:block">
          Updated
        </span>
      </div>

      {/* Instrument list */}
      <div className="overflow-hidden rounded-lg border border-surface-border">
        {entries.length === 0 ? (
          <div className="flex flex-col items-center justify-center gap-2 py-16">
            <span className="font-mono text-[9px] uppercase tracking-widest text-muted-foreground/25">
              No Data
            </span>
            <span className="font-mono text-xs text-muted-foreground/40">
              No bias records found in the database
            </span>
          </div>
        ) : (
          entries.map((entry, i) => (
            <InstrumentRow key={entry.symbol} entry={entry} index={i} />
          ))
        )}
      </div>
    </div>
  )
}
