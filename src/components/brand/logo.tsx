import Link from "next/link";
import { cn } from "@/lib/utils";
import { site } from "@/lib/site";

/** Фирменный знак СРО «СССС»: лаконичная «арка/портал» в золоте на navy. */
export function LogoMark({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 48 48"
      className={className}
      role="img"
      aria-label={site.name}
      fill="none"
    >
      <rect width="48" height="48" rx="11" fill="var(--color-navy-800)" />
      <rect
        x="0.6"
        y="0.6"
        width="46.8"
        height="46.8"
        rx="10.4"
        stroke="var(--color-gold-500)"
        strokeOpacity="0.35"
        strokeWidth="1.2"
      />
      {/* Колонны/портал */}
      <g fill="var(--color-gold-400)">
        <path d="M11 34V20l5-3v17h-5Z" />
        <path d="M21.5 34V15l5-3v22h-5Z" opacity="0.92" />
        <path d="M32 34V18l5-3v19h-5Z" opacity="0.84" />
      </g>
      <rect x="9" y="35.5" width="30" height="2.6" rx="1.3" fill="var(--color-gold-500)" />
    </svg>
  );
}

export function Logo({
  className,
  variant = "dark",
  withText = true,
}: {
  className?: string;
  variant?: "dark" | "light";
  withText?: boolean;
}) {
  return (
    <Link
      href="/"
      className={cn("group inline-flex items-center gap-3", className)}
      aria-label={`${site.name} — на главную`}
    >
      <LogoMark className="h-11 w-11 shrink-0 transition-transform duration-300 group-hover:scale-[1.04]" />
      {withText && (
        <span className="flex flex-col leading-none">
          <span
            className={cn(
              "font-display text-xl font-extrabold tracking-tight",
              variant === "dark" ? "text-navy-900" : "text-white",
            )}
          >
            {site.name}
          </span>
          <span
            className={cn(
              "mt-1 text-[0.68rem] font-medium leading-tight tracking-tight",
              variant === "dark" ? "text-slate-500" : "text-slate-300",
            )}
          >
            Строительный союз
            <br />
            Северной столицы
          </span>
        </span>
      )}
    </Link>
  );
}
