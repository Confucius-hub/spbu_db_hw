import Link from "next/link";
import { cn } from "@/lib/utils";
import { site } from "@/lib/site";

/**
 * "ЮРЛИДЕР" brand lockup — faithful recreation of the original logo:
 * an A-frame emblem ("UR" over a reversed "LIDER" band) + bold wordmark.
 */
export function Logo({
  tone = "default",
  className,
}: {
  tone?: "default" | "onDark";
  className?: string;
}) {
  const fg = tone === "onDark" ? "#ffffff" : "#0f1c24";
  const bg = tone === "onDark" ? "#0f1c24" : "#ffffff";

  return (
    <Link
      href="/"
      aria-label={site.legalName}
      className={cn("group inline-flex items-center gap-2.5", className)}
    >
      <svg
        viewBox="0 0 84 64"
        className="h-9 w-auto shrink-0"
        role="img"
        aria-hidden
      >
        {/* A-frame roof */}
        <path
          d="M6 58 L42 7 L78 58"
          fill="none"
          stroke={fg}
          strokeWidth="8"
          strokeLinejoin="round"
          strokeLinecap="round"
        />
        {/* UR */}
        <text
          x="42"
          y="35"
          textAnchor="middle"
          fontFamily="var(--font-inter), sans-serif"
          fontSize="15"
          fontWeight="800"
          fill={fg}
        >
          UR
        </text>
        {/* LIDER band */}
        <rect x="13" y="41" width="58" height="17" rx="2.5" fill={fg} />
        <text
          x="42"
          y="53.5"
          textAnchor="middle"
          fontFamily="var(--font-inter), sans-serif"
          fontSize="12"
          fontWeight="800"
          letterSpacing="1"
          fill={bg}
        >
          LIDER
        </text>
      </svg>

      <span className="flex flex-col leading-none">
        <span
          className={cn(
            "text-[21px] font-extrabold tracking-tight",
            tone === "onDark" ? "text-white" : "text-ink",
          )}
        >
          ЮРЛИДЕР
        </span>
        <span
          className={cn(
            "mt-1 text-[10px] tracking-[0.16em]",
            tone === "onDark" ? "text-white/55" : "text-faint",
          )}
        >
          юридическая компания
        </span>
      </span>
    </Link>
  );
}
