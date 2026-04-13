"use client"

import { useState, useMemo, useRef, useEffect } from "react"
import { RefreshCw, ChevronDown, Check } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table"
import { cn } from "@/lib/utils"
import { useForexEvents } from "@/lib/hooks/use-forex-events"

const WEEKS = [
  { label: "Last week", value: "last week" },
  { label: "This week", value: "this week" },
  { label: "Next week", value: "next week" },
] as const
type WeekValue = (typeof WEEKS)[number]["value"]

const IMPACT_FILTERS = ["All", "High", "Medium"] as const
type ImpactFilter = (typeof IMPACT_FILTERS)[number]

function ImpactBadge({ impact }: { impact: string }) {
  return <Badge variant={impact === "High" ? "loss" : "partial"}>{impact}</Badge>
}

function FilterChip({
  label,
  active,
  onClick,
}: {
  label: string
  active: boolean
  onClick: () => void
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "rounded px-2 py-0.5 font-mono text-[10px] uppercase tracking-wide transition-colors",
        active
          ? "bg-surface-3 text-foreground"
          : "text-muted-foreground hover:bg-surface-3 hover:text-foreground",
      )}
    >
      {label}
    </button>
  )
}

export function ForexEventsPanel() {
  const { events, loading, fetching, error, fetchWeek } = useForexEvents()

  const [weekFilter, setWeekFilter] = useState<WeekValue>("this week")
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)
  const [impactFilter, setImpactFilter] = useState<ImpactFilter>("All")
  const [selectedCurrencies, setSelectedCurrencies] = useState<Set<string>>(new Set())

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setDropdownOpen(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  async function handleFetch(week: WeekValue) {
    setDropdownOpen(false)
    await fetchWeek(week)
    setWeekFilter(week)
  }

  const allCurrencies = useMemo(
    () => [...new Set(events.map((e) => e.currency))].sort(),
    [events],
  )

  function toggleCurrency(c: string) {
    setSelectedCurrencies((prev) => {
      const next = new Set(prev)
      next.has(c) ? next.delete(c) : next.add(c)
      return next
    })
  }

  const weekDateRange = useMemo((): [string, string] => {
    const today = new Date()
    const daysSinceSunday = today.getDay() % 7
    const thisSunday = new Date(today)
    thisSunday.setDate(today.getDate() - daysSinceSunday)

    const offset = weekFilter === "last week" ? -7 : weekFilter === "next week" ? 7 : 0

    const start = new Date(thisSunday)
    start.setDate(thisSunday.getDate() + offset)
    const end = new Date(start)
    end.setDate(start.getDate() + 6)

    const fmt = (d: Date) => d.toISOString().slice(0, 10)
    return [fmt(start), fmt(end)]
  }, [weekFilter])

  const filtered = useMemo(() => {
    const [from, to] = weekDateRange
    return events.filter((ev) => {
      if (ev.date) {
        if (ev.date < from || ev.date > to) return false
      }
      if (impactFilter !== "All" && ev.impact !== impactFilter) return false
      if (selectedCurrencies.size > 0 && !selectedCurrencies.has(ev.currency)) return false
      return true
    })
  }, [events, weekDateRange, impactFilter, selectedCurrencies])

  const grouped = useMemo(() => {
    const map: Record<string, typeof events> = {}
    for (const ev of filtered) {
      const key = ev.date ?? "Unknown"
      ;(map[key] ??= []).push(ev)
    }
    return Object.entries(map).sort(([a], [b]) => a.localeCompare(b))
  }, [filtered])

  const weekLabel = WEEKS.find((w) => w.value === weekFilter)?.label ?? "This week"

  return (
    <div className="flex flex-col gap-4 p-6">
      {/* Header row */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-base font-semibold text-foreground">ForexFactory Events</h1>
          <p className="text-xs text-muted-foreground">Medium &amp; High impact · stored in DB</p>
        </div>

        {/* Fetch button with dropdown */}
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => !fetching && setDropdownOpen((o) => !o)}
            disabled={fetching}
            className="flex items-center gap-1.5 rounded-md border border-surface-border bg-surface-2 px-3 py-1.5 text-xs font-medium text-foreground transition-colors hover:bg-surface-3 disabled:opacity-50"
          >
            <RefreshCw size={11} className={fetching ? "animate-spin" : ""} />
            {fetching ? "Fetching…" : "Fetch"}
            {!fetching && (
              <ChevronDown
                size={11}
                className={cn("transition-transform", dropdownOpen && "rotate-180")}
              />
            )}
          </button>

          {dropdownOpen && (
            <div className="absolute right-0 top-full z-20 mt-1 min-w-[130px] rounded-md border border-surface-border bg-surface-2 py-1 shadow-lg">
              {WEEKS.map(({ label, value }) => (
                <button
                  key={value}
                  onClick={() => handleFetch(value)}
                  className="flex w-full items-center gap-2 px-3 py-1.5 text-xs text-foreground transition-colors hover:bg-surface-3"
                >
                  <Check
                    size={10}
                    className={weekFilter === value ? "text-teal" : "invisible"}
                  />
                  {label}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Filter bar */}
      {!loading && events.length > 0 && (
        <div className="flex flex-wrap items-center gap-3 rounded-md border border-surface-border bg-surface-1 px-3 py-2">
          <div className="flex items-center gap-1">
            <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground/50 mr-1">
              Week
            </span>
            {WEEKS.map(({ label, value }) => (
              <FilterChip
                key={value}
                label={label}
                active={weekFilter === value}
                onClick={() => setWeekFilter(value)}
              />
            ))}
          </div>

          <div className="h-3 w-px bg-surface-border" />

          <div className="flex items-center gap-1">
            <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground/50 mr-1">
              Impact
            </span>
            {IMPACT_FILTERS.map((f) => (
              <FilterChip
                key={f}
                label={f}
                active={impactFilter === f}
                onClick={() => setImpactFilter(f)}
              />
            ))}
          </div>

          <div className="h-3 w-px bg-surface-border" />

          <div className="flex flex-wrap items-center gap-1">
            <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground/50 mr-1">
              Currency
            </span>
            <FilterChip
              label="All"
              active={selectedCurrencies.size === 0}
              onClick={() => setSelectedCurrencies(new Set())}
            />
            {allCurrencies.map((c) => (
              <FilterChip
                key={c}
                label={c}
                active={selectedCurrencies.has(c)}
                onClick={() => toggleCurrency(c)}
              />
            ))}
          </div>
        </div>
      )}

      {error && (
        <p className="rounded-md border border-loss/30 bg-loss/10 px-3 py-2 text-xs text-loss">
          {error}
        </p>
      )}

      {/* Table */}
      <div className="rounded-md border border-surface-border bg-surface-1">
        {loading ? (
          <div className="flex h-32 items-center justify-center text-xs text-muted-foreground">
            Loading…
          </div>
        ) : filtered.length === 0 ? (
          <div className="flex h-32 items-center justify-center text-xs text-muted-foreground">
            {events.length === 0
              ? "No events yet — click Fetch to populate."
              : `No ${weekLabel.toLowerCase()} events${
                  impactFilter !== "All" || selectedCurrencies.size > 0
                    ? " matching filters"
                    : ""
                } — try Fetch.`}
          </div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Date</TableHead>
                <TableHead>Time</TableHead>
                <TableHead>Currency</TableHead>
                <TableHead>Impact</TableHead>
                <TableHead className="max-w-56">Event</TableHead>
                <TableHead>Actual</TableHead>
                <TableHead>Forecast</TableHead>
                <TableHead>Previous</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {grouped.map(([date, rows]) =>
                rows.map((ev, i) => (
                  <TableRow key={ev.id}>
                    {i === 0 ? (
                      <TableCell
                        rowSpan={rows.length}
                        className="align-top font-mono text-[10px] text-muted-foreground whitespace-nowrap"
                      >
                        {date}
                      </TableCell>
                    ) : null}
                    <TableCell className="font-mono text-[10px] text-muted-foreground whitespace-nowrap">
                      {ev.time ?? "—"}
                    </TableCell>
                    <TableCell className="font-mono font-medium text-foreground">
                      {ev.currency}
                    </TableCell>
                    <TableCell>
                      <ImpactBadge impact={ev.impact} />
                    </TableCell>
                    <TableCell className="max-w-56 truncate text-foreground">
                      {ev.event_name}
                    </TableCell>
                    <TableCell
                      className={cn(
                        "font-mono",
                        ev.actual ? "text-foreground" : "text-muted-foreground/40",
                      )}
                    >
                      {ev.actual ?? "—"}
                    </TableCell>
                    <TableCell className="font-mono text-muted-foreground">
                      {ev.forecast ?? "—"}
                    </TableCell>
                    <TableCell className="font-mono text-muted-foreground">
                      {ev.previous ?? "—"}
                    </TableCell>
                  </TableRow>
                )),
              )}
            </TableBody>
          </Table>
        )}
      </div>

      {!loading && filtered.length > 0 && (
        <p className="text-right font-mono text-[10px] text-muted-foreground/50">
          {filtered.length} of {events.length} events
        </p>
      )}
    </div>
  )
}
