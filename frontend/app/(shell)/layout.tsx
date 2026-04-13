import { Sidebar } from "@/components/layout/sidebar"
import { Header } from "@/components/layout/header"

export default function ShellLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="dark flex h-screen overflow-hidden bg-surface-0 text-foreground">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-auto p-3">{children}</main>
      </div>
    </div>
  )
}
