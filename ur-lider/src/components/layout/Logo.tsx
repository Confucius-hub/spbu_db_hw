import Link from "next/link";
import { cn } from "@/lib/utils";
import { site } from "@/lib/site";

/**
 * "ЮРЛИДЕР" brand lockup — recreation of the original logo:
 * a bold A-frame emblem ("UR" над плашкой "LIDER") + жирная надпись.
 * For a pixel-perfect mark, drop the official SVG into /public and swap here.
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
        viewBox="0 0 92 64"
        className="h-9 w-auto shrink-0"
        role="img"
        aria-hidden
      >
        {/* A-frame: thick legs */}
        <path d="M14 58 L46 8 L78 58 L66 58 L46 27 L26 58 Z" fill={fg} />
        {/* feet */}
        <rect x="6" y="53" width="20" height="6" rx="1" fill={fg} />
        <rect x="66" y="53" width="20" height="6" rx="1" fill={fg} />
        {/* UR */}
        <text
          x="46"
          y="34"
          textAnchor="middle"
          fontFamily="var(--font-inter), sans-serif"
          fontSize="14"
          fontWeight="800"
          fill={fg}
        >
          UR
        </text>
        {/* LIDER band */}
        <rect x="13" y="40" width="66" height="16" rx="2" fill={fg} />
        <text
          x="46"
          y="52"
          textAnchor="middle"
          fontFamily="var(--font-inter), sans-serif"
          fontSize="12"
          fontWeight="800"
          letterSpacing="1.5"
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
