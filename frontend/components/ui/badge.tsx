import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded px-1.5 py-0.5 text-[10px] font-mono font-medium uppercase tracking-wide transition-colors",
  {
    variants: {
      variant: {
        default:    "bg-muted text-muted-foreground",
        profit:     "bg-profit-muted text-profit",
        loss:       "bg-loss-muted text-loss",
        filled:     "bg-profit-muted text-profit",
        partial:    "bg-amber-500/15 text-amber-400",
        open:       "bg-blue-500/15 text-blue-400",
        cancelled:  "bg-muted text-muted-foreground/60",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <span className={cn(badgeVariants({ variant, className }))} {...props} />
  )
}

export { Badge, badgeVariants }
