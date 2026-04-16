import type { LucideIcon } from "lucide-react"
import {
  LayoutDashboard,
  PieChart,
  TrendingUp,
  ClipboardList,
  Settings,
  Compass,
  CalendarDays,
  BarChart2,
  SlidersHorizontal,
  Database,
  Bell,
} from "lucide-react"

export type NavItem = {
  label: string
  href: string
  icon: LucideIcon
}

export type NavSection = {
  label?: string
  items: NavItem[]
}

export const DASHBOARD_NAV: NavSection[] = [
  {
    items: [
      { label: "Overview",          href: "/overview",         icon: LayoutDashboard },
      { label: "Portfolio",         href: "/portfolio",        icon: PieChart },
      { label: "Markets",           href: "/markets",          icon: TrendingUp },
      { label: "Fundamental Bias",  href: "/fundamental-bias", icon: Compass },
      { label: "Forex Charts",      href: "/forex-charts",     icon: BarChart2 },
      { label: "Orders",            href: "/orders",           icon: ClipboardList },
    ],
  },
  {
    label: "Data",
    items: [
      { label: "ForexFactory Events", href: "/forex-events", icon: CalendarDays },
    ],
  },
  {
    items: [
      { label: "Settings", href: "/settings", icon: Settings },
    ],
  },
]

export const SETTINGS_NAV: NavItem[] = [
  { label: "Instruments",   href: "/settings/instruments",   icon: BarChart2 },
  { label: "General",       href: "/settings/general",       icon: SlidersHorizontal },
  { label: "Data Sources",  href: "/settings/data-sources",  icon: Database },
  { label: "Notifications", href: "/settings/notifications", icon: Bell },
]
