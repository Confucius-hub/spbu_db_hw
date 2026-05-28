import { cn } from "@/lib/utils";

type Variant = "gold" | "navy" | "muted" | "outline" | "success";

const variants: Record<Variant, string> = {
  gold: "bg-gold-100 text-gold-800 ring-1 ring-gold-200",
  navy: "bg-navy-800 text-white",
  muted: "bg-slate-100 text-slate-600 ring-1 ring-slate-200",
  outline: "bg-white/70 text-navy-700 ring-1 ring-navy-200",
  success: "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-200",
};

export function Badge({
  children,
  variant = "muted",
  className,
}: {
  children: React.ReactNode;
  variant?: Variant;
  className?: string;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold",
        variants[variant],
        className,
      )}
    >
      {children}
    </span>
  );
}
