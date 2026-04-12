import { TrendingUp, TrendingDown } from "lucide-react"
import { Card, CardHeader, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import type { PortfolioMetric } from "@/lib/mock-data"
import { cn } from "@/lib/utils"

interface PortfolioCardsProps {
  metrics: PortfolioMetric[]
}

export function PortfolioCards({ metrics }: PortfolioCardsProps) {
  return (
    <div className="grid grid-cols-4 gap-3">
      {metrics.map((metric) => (
        <Card key={metric.label}>
          <CardHeader>
            <span className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground/70">
              {metric.label}
            </span>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex flex-col gap-1.5">
              <span
                className={cn(
                  "font-mono text-2xl font-semibold tabular-nums",
                  metric.positive === true && "text-profit",
                  metric.positive === false && "text-loss"
                )}
              >
                {metric.value}
              </span>

              {metric.change !== undefined && (
                <div className="flex items-center gap-1.5">
                  {metric.changePct !== undefined && (
                    <>
                      {metric.positive !== undefined ? (
                        metric.positive ? (
                          <TrendingUp size={11} className="text-profit" />
                        ) : (
                          <TrendingDown size={11} className="text-loss" />
                        )
                      ) : null}
                      <Badge variant={metric.positive ? "profit" : metric.positive === false ? "loss" : "default"}>
                        {metric.positive ? "+" : ""}{metric.changePct?.toFixed(2)}%
                      </Badge>
                    </>
                  )}
                  <span className="font-mono text-[11px] text-muted-foreground">
                    {metric.change}
                  </span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
