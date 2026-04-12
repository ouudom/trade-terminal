"use client"

import { useEffect, useState } from "react"
import { Plus, RefreshCw, Search } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table"

interface Instrument {
  id: number
  symbol: string
  name: string
  asset_class: string
  is_active: boolean
}

const ASSET_CLASSES = ["all", "forex", "equity", "crypto", "index", "commodity"]

const assetClassStyle: Record<string, string> = {
  forex:     "bg-blue-500/15 text-blue-400",
  crypto:    "bg-amber-500/15 text-amber-400",
  equity:    "bg-teal/15 text-teal",
  index:     "bg-purple-500/15 text-purple-400",
  commodity: "bg-orange-500/15 text-orange-400",
}

function Toggle({ active, onToggle }: { active: boolean; onToggle: () => void }) {
  return (
    <button
      onClick={onToggle}
      className={cn(
        "relative inline-flex h-4.5 w-8 shrink-0 cursor-pointer rounded-full border border-transparent transition-colors",
        active ? "bg-teal" : "bg-surface-3"
      )}
      aria-checked={active}
      role="switch"
    >
      <span
        className={cn(
          "pointer-events-none inline-block h-3.5 w-3.5 translate-y-[0.5px] rounded-full bg-white shadow-sm transition-transform",
          active ? "translate-x-[14px]" : "translate-x-[1px]"
        )}
      />
    </button>
  )
}

export function InstrumentsSettings() {
  const [instruments, setInstruments] = useState<Instrument[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState("")
  const [assetFilter, setAssetFilter] = useState("all")

  async function fetchInstruments() {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch("http://localhost:8000/instruments")
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data: Instrument[] = await res.json()
      setInstruments(data)
    } catch {
      setError("Could not load instruments — is the backend running?")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchInstruments() }, [])

  function toggleActive(id: number) {
    setInstruments(prev =>
      prev.map(i => i.id === id ? { ...i, is_active: !i.is_active } : i)
    )
  }

  const filtered = instruments.filter(i => {
    const matchesSearch =
      i.symbol.toLowerCase().includes(search.toLowerCase()) ||
      i.name.toLowerCase().includes(search.toLowerCase())
    const matchesClass = assetFilter === "all" || i.asset_class === assetFilter
    return matchesSearch && matchesClass
  })

  const activeCount = instruments.filter(i => i.is_active).length

  return (
    <div className="max-w-3xl space-y-5">
      {/* Header */}
      <div className="flex items-start justify-between border-b border-surface-border pb-4">
        <div>
          <h2 className="text-sm font-semibold text-foreground">Instruments</h2>
          <p className="mt-0.5 text-xs text-muted-foreground">
            Manage the instruments tracked and analysed by the terminal.
          </p>
        </div>
        <Button variant="outline" size="sm" className="gap-1.5">
          <Plus size={12} />
          Add Instrument
        </Button>
      </div>

      {/* Filters */}
      <div className="flex flex-col gap-2.5">
        {/* Search */}
        <div className="relative">
          <Search size={12} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-muted-foreground/60" />
          <input
            type="text"
            placeholder="Search symbol or name…"
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="h-7 w-full rounded-md border border-surface-border bg-surface-1 pl-7 pr-3 font-mono text-xs text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-1 focus:ring-teal/50"
          />
        </div>

        {/* Asset class pills */}
        <div className="flex flex-wrap gap-1">
          {ASSET_CLASSES.map(cls => (
            <button
              key={cls}
              onClick={() => setAssetFilter(cls)}
              className={cn(
                "rounded-md px-2.5 py-1 font-mono text-[10px] uppercase tracking-wide transition-colors",
                assetFilter === cls
                  ? "bg-surface-3 text-foreground"
                  : "text-muted-foreground hover:bg-surface-3 hover:text-foreground"
              )}
            >
              {cls}
            </button>
          ))}
        </div>
      </div>

      {/* Table */}
      {loading ? (
        <div className="space-y-px rounded-lg border border-surface-border overflow-hidden">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="flex items-center gap-3 px-3 py-2.5 bg-surface-1">
              <div className="h-4 w-14 rounded bg-surface-3 animate-pulse" />
              <div className="h-4 w-40 rounded bg-surface-3 animate-pulse" />
              <div className="ml-auto h-4 w-16 rounded bg-surface-3 animate-pulse" />
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="flex flex-col items-center gap-3 rounded-lg border border-surface-border bg-surface-1 py-10 text-center">
          <p className="text-xs text-muted-foreground">{error}</p>
          <Button variant="outline" size="sm" className="gap-1.5" onClick={fetchInstruments}>
            <RefreshCw size={11} />
            Retry
          </Button>
        </div>
      ) : filtered.length === 0 ? (
        <div className="flex items-center justify-center rounded-lg border border-surface-border bg-surface-1 py-10">
          <p className="text-xs text-muted-foreground">No instruments found.</p>
        </div>
      ) : (
        <div className="rounded-lg border border-surface-border overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Symbol</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Class</TableHead>
                <TableHead className="text-right">Active</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map(instrument => (
                <TableRow
                  key={instrument.id}
                  className={cn(!instrument.is_active && "opacity-50")}
                >
                  <TableCell>
                    <span className="font-mono text-[11px] font-medium uppercase text-foreground">
                      {instrument.symbol}
                    </span>
                  </TableCell>
                  <TableCell className="text-muted-foreground">
                    {instrument.name}
                  </TableCell>
                  <TableCell>
                    <span
                      className={cn(
                        "inline-flex items-center rounded px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wide",
                        assetClassStyle[instrument.asset_class] ?? "bg-surface-3 text-muted-foreground"
                      )}
                    >
                      {instrument.asset_class}
                    </span>
                  </TableCell>
                  <TableCell className="text-right">
                    <Toggle
                      active={instrument.is_active}
                      onToggle={() => toggleActive(instrument.id)}
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}

      {/* Footer */}
      {!loading && !error && (
        <p className="text-[11px] text-muted-foreground/60">
          Showing {filtered.length} of {instruments.length} · {activeCount} active
        </p>
      )}
    </div>
  )
}
