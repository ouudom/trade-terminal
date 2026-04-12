"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { BarChart2, SlidersHorizontal, Database, Bell } from "lucide-react"
import { cn } from "@/lib/utils"

const SETTINGS_NAV = [
  { label: "Instruments",   href: "/dashboard/settings/instruments",   icon: BarChart2 },
  { label: "General",       href: "/dashboard/settings/general",       icon: SlidersHorizontal },
  { label: "Data Sources",  href: "/dashboard/settings/data-sources",  icon: Database },
  { label: "Notifications", href: "/dashboard/settings/notifications", icon: Bell },
]

function SettingsSidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-44 shrink-0 flex flex-col gap-0.5 border-r border-surface-border p-2">
      <p className="px-3 pb-2 pt-1 font-mono text-[10px] uppercase tracking-wider text-muted-foreground/60">
        Settings
      </p>
      {SETTINGS_NAV.map(({ label, href, icon: Icon }) => {
        const isActive = pathname === href
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
            <Icon size={14} strokeWidth={isActive ? 2 : 1.5} />
            <span>{label}</span>
          </Link>
        )
      })}
    </aside>
  )
}

export default function SettingsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-full gap-0">
      <SettingsSidebar />
      <main className="flex-1 overflow-y-auto p-6">
        {children}
      </main>
    </div>
  )
}
