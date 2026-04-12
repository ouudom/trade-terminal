"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  LayoutDashboard,
  PieChart,
  TrendingUp,
  ClipboardList,
  Settings,
  Compass,
  CalendarDays,
  BarChart2,
} from "lucide-react"
import { cn } from "@/lib/utils"

const NAV_SECTIONS = [
  {
    items: [
      { label: "Overview",          href: "/dashboard",                   icon: LayoutDashboard },
      { label: "Portfolio",         href: "/dashboard/portfolio",         icon: PieChart },
      { label: "Markets",           href: "/dashboard/markets",           icon: TrendingUp },
      { label: "Fundamental Bias",  href: "/dashboard/fundamental-bias",  icon: Compass },
      { label: "Forex Charts",      href: "/dashboard/forex-charts",      icon: BarChart2 },
      { label: "Orders",            href: "/dashboard/orders",            icon: ClipboardList },
    ],
  },
  {
    label: "Data",
    items: [
      { label: "ForexFactory Events", href: "/dashboard/data/forex-events", icon: CalendarDays },
    ],
  },
  {
    items: [
      { label: "Settings", href: "/dashboard/settings", icon: Settings },
    ],
  },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="flex h-screen w-52 shrink-0 flex-col border-r border-surface-border bg-surface-1">
      {/* Logo */}
      <div className="flex h-11 items-center gap-2.5 border-b border-surface-border px-4">
        <img src="/logo.svg" alt="Trade Terminal" className="h-7 w-7" />
        <span className="text-sm font-semibold tracking-tight text-foreground">
          Trade Terminal
        </span>
      </div>

      {/* Nav */}
      <nav className="flex flex-col gap-3 p-2 flex-1">
        {NAV_SECTIONS.map((section, si) => (
          <div key={si} className="flex flex-col gap-0.5">
            {section.label && (
              <span className="px-3 pb-0.5 pt-1 font-mono text-[10px] uppercase tracking-wider text-muted-foreground/50">
                {section.label}
              </span>
            )}
            {section.items.map(({ label, href, icon: Icon }) => {
              const isActive = pathname === href || (href !== "/dashboard" && pathname.startsWith(href + "/"))
              return (
                <Link
                  key={href}
                  href={href}
                  className={cn(
                    "relative flex items-center gap-2.5 rounded-md px-3 py-2 text-sm transition-colors",
                    isActive
                      ? "bg-surface-3 text-foreground before:absolute before:left-0 before:top-1.5 before:bottom-1.5 before:w-0.5 before:rounded-full before:bg-teal"
                      : "text-muted-foreground hover:bg-surface-3 hover:text-foreground"
                  )}
                >
                  <Icon size={15} strokeWidth={isActive ? 2 : 1.5} />
                  <span>{label}</span>
                </Link>
              )
            })}
          </div>
        ))}
      </nav>

      {/* Bottom */}
      <div className="border-t border-surface-border px-3 py-3">
        <div className="flex items-center gap-2.5">
          <div className="flex h-7 w-7 items-center justify-center rounded-full bg-surface-3 text-xs font-mono font-medium text-muted-foreground">
            JD
          </div>
          <div className="flex flex-col">
            <span className="text-xs font-medium text-foreground">John Doe</span>
            <span className="font-mono text-[10px] text-muted-foreground/60">v0.1.0</span>
          </div>
        </div>
      </div>
    </aside>
  )
}
