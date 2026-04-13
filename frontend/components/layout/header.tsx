"use client"

import { useEffect, useState } from "react"
import { ChevronDown } from "lucide-react"
import { Button } from "@/components/ui/button"

export function Header() {
  const [time, setTime] = useState("")

  useEffect(() => {
    const tick = () =>
      setTime(new Date().toLocaleTimeString("en-US", { hour12: false }))
    tick()
    const id = setInterval(tick, 1000)
    return () => clearInterval(id)
  }, [])

  return (
    <header className="flex h-11 shrink-0 items-center justify-between border-b border-surface-border bg-surface-1 px-4">
      {/* Asset selector */}
      <Button variant="outline" size="sm" className="gap-1.5 font-mono text-xs">
        AAPL / USD
        <ChevronDown size={12} className="text-muted-foreground" />
      </Button>

      {/* Market status */}
      <div className="flex items-center gap-2">
        <span className="relative flex h-2 w-2">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-profit opacity-60" />
          <span className="relative inline-flex h-2 w-2 rounded-full bg-profit" />
        </span>
        <span className="font-mono text-xs text-profit tracking-wide">NYSE · OPEN</span>
      </div>

      {/* Clock */}
      <span className="font-mono text-sm text-muted-foreground tabular-nums">
        {time}
      </span>
    </header>
  )
}
