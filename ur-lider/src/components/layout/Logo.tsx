import Link from "next/link";
import { cn } from "@/lib/utils";
import { site } from "@/lib/site";

export function Logo({
  tone = "default",
  className,
}: {
  tone?: "default" | "onDark";
  className?: string;
}) {
  return (
    <Link
      href="/"
      aria-label={site.legalName}
      className={cn("group inline-flex items-center gap-2.5", className)}
    >
      <span
        className={cn(
          "grid h-9 w-9 place-items-center rounded-lg transition-colors",
          tone === "onDark" ? "bg-white/10 ring-1 ring-white/15" : "bg-ink",
        )}
      >
        <svg viewBox="0 0 24 24" className="h-5 w-5" aria-hidden>
          <path
            d="M6 4v13a3 3 0 0 0 3 3h9"
            fill="none"
            stroke="var(--color-accent)"
            strokeWidth="2.1"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </span>
      <span className="flex flex-col leading-none">
        <span
          className={cn(
            "font-serif text-[19px] font-semibold tracking-tight",
            tone === "onDark" ? "text-white" : "text-ink",
          )}
        >
          Лидер
        </span>
        <span
          className={cn(
            "text-[10px] font-medium uppercase tracking-[0.2em]",
            tone === "onDark" ? "text-white/55" : "text-faint",
          )}
        >
          Юридическая компания
        </span>
      </span>
    </Link>
  );
}
