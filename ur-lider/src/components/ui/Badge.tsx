import { cn } from "@/lib/utils";

/** Eyebrow / pill label. `tone="onDark"` for dark sections. */
export function Badge({
  children,
  tone = "default",
  className,
}: {
  children: React.ReactNode;
  tone?: "default" | "onDark";
  className?: string;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-2 rounded-full px-3.5 py-1.5 text-xs font-semibold uppercase tracking-[0.14em]",
        tone === "default"
          ? "bg-accent-soft text-accent-strong"
          : "bg-white/10 text-white/80 ring-1 ring-white/15",
        className,
      )}
    >
      <span
        aria-hidden
        className={cn(
          "h-1.5 w-1.5 rounded-full",
          tone === "default" ? "bg-accent" : "bg-accent",
        )}
      />
      {children}
    </span>
  );
}
