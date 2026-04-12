"use client"

import { useState } from "react"
import { cn } from "@/lib/utils"

export function GeneralSettings() {
  const [timeframe, setTimeframe] = useState("1h")
  const [timezone, setTimezone] = useState("UTC")
  const [compact, setCompact] = useState(false)

  return (
    <div className="max-w-3xl space-y-5">
      {/* Header */}
      <div className="border-b border-surface-border pb-4">
        <h2 className="text-sm font-semibold text-foreground">General</h2>
        <p className="mt-0.5 text-xs text-muted-foreground">
          Display preferences and default behaviour for the terminal.
        </p>
      </div>

      {/* Settings rows */}
      <div className="divide-y divide-surface-border rounded-lg border border-surface-border overflow-hidden">
        <SettingRow
          label="Default Timeframe"
          description="Timeframe used when opening a new chart."
        >
          <select
            value={timeframe}
            onChange={e => setTimeframe(e.target.value)}
            className="h-7 rounded-md border border-surface-border bg-surface-1 px-2 font-mono text-xs text-foreground focus:outline-none focus:ring-1 focus:ring-teal/50"
          >
            {["1m", "5m", "15m", "1h", "4h", "1d"].map(tf => (
              <option key={tf}>{tf}</option>
            ))}
          </select>
        </SettingRow>

        <SettingRow
          label="Timezone"
          description="Timestamps and session times are displayed in this timezone."
        >
          <select
            value={timezone}
            onChange={e => setTimezone(e.target.value)}
            className="h-7 rounded-md border border-surface-border bg-surface-1 px-2 font-mono text-xs text-foreground focus:outline-none focus:ring-1 focus:ring-teal/50"
          >
            {["UTC", "UTC+1", "UTC+7", "UTC+8"].map(tz => (
              <option key={tz}>{tz}</option>
            ))}
          </select>
        </SettingRow>

        <SettingRow
          label="Compact Mode"
          description="Reduce row height and font size across tables."
        >
          <button
            onClick={() => setCompact(v => !v)}
            role="switch"
            aria-checked={compact}
            className={cn(
              "relative inline-flex h-4.5 w-8 shrink-0 cursor-pointer rounded-full border border-transparent transition-colors",
              compact ? "bg-teal" : "bg-surface-3"
            )}
          >
            <span
              className={cn(
                "pointer-events-none inline-block h-3.5 w-3.5 translate-y-[0.5px] rounded-full bg-white shadow-sm transition-transform",
                compact ? "translate-x-[14px]" : "translate-x-[1px]"
              )}
            />
          </button>
        </SettingRow>
      </div>
    </div>
  )
}

function SettingRow({
  label,
  description,
  children,
}: {
  label: string
  description: string
  children: React.ReactNode
}) {
  return (
    <div className="flex items-center justify-between gap-4 bg-surface-1 px-4 py-3">
      <div>
        <p className="text-xs font-medium text-foreground">{label}</p>
        <p className="text-[11px] text-muted-foreground">{description}</p>
      </div>
      {children}
    </div>
  )
}
