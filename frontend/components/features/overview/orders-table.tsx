import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import type { Order, OrderStatus } from "@/lib/types"
import { cn } from "@/lib/utils"

function statusVariant(s: OrderStatus) {
  if (s === "FILLED") return "filled"
  if (s === "PARTIAL") return "partial"
  if (s === "OPEN") return "open"
  return "cancelled"
}

interface OrdersTableProps {
  orders: Order[]
}

export function OrdersTable({ orders }: OrdersTableProps) {
  return (
    <div className="rounded-lg border border-surface-border bg-surface-2">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-surface-border px-4 py-2.5">
        <span className="font-mono text-xs font-semibold uppercase tracking-wider text-muted-foreground/80">
          Recent Orders
        </span>
        <button className="font-mono text-[10px] text-muted-foreground/60 transition-colors hover:text-foreground">
          View All →
        </button>
      </div>

      {/* Table */}
      <div className="overflow-y-auto max-h-64">
        <Table>
          <TableHeader>
            <TableRow className="hover:bg-transparent">
              <TableHead>Asset</TableHead>
              <TableHead>Side</TableHead>
              <TableHead className="text-right">Qty</TableHead>
              <TableHead className="text-right">Price</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Time</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {orders.map((order) => (
              <TableRow key={order.id}>
                <TableCell>
                  <span className="font-mono font-semibold">{order.asset}</span>
                </TableCell>
                <TableCell>
                  <span
                    className={cn(
                      "font-mono font-semibold",
                      order.side === "BUY" ? "text-profit" : "text-loss",
                    )}
                  >
                    {order.side}
                  </span>
                </TableCell>
                <TableCell className="text-right">
                  <span className="font-mono tabular-nums text-muted-foreground">
                    {order.qty}
                  </span>
                </TableCell>
                <TableCell className="text-right">
                  <span className="font-mono tabular-nums">
                    ${order.price.toLocaleString("en-US", { minimumFractionDigits: 2 })}
                  </span>
                </TableCell>
                <TableCell>
                  <Badge
                    variant={
                      statusVariant(order.status) as Parameters<typeof Badge>[0]["variant"]
                    }
                  >
                    {order.status}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <span className="font-mono tabular-nums text-muted-foreground/70">
                    {order.timestamp}
                  </span>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}
