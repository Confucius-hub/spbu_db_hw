import Link from "next/link";
import { cn } from "@/lib/utils";
import { site } from "@/lib/site";

/**
 * Фирменный знак СРО «СССС»: классический портал/колоннада (символ строительства
 * и архитектурного наследия Северной столицы). Использует currentColor, поэтому
 * перекрашивается в любой цвет через text-* у родителя (navy на светлом фоне,
 * белый на тёмном). Чтобы заменить на свою PNG/SVG — положите файл в
 * /public/brand/logo.svg и используйте <img src="/brand/logo.svg" />.
 */
export function LogoMark({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 100 84"
      className={className}
      role="img"
      aria-label={site.name}
      fill="currentColor"
    >
      {/* Фронтон (треугольник) с многослойной обводкой */}
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M50 2 L98 27 L2 27 Z M50 9 L86 27 L14 27 Z"
      />
      <path d="M50 13 L78 27 L22 27 Z" />

      {/* Антаблемент (карниз + фриз + архитрав) */}
      <rect x="2" y="29" width="96" height="3" />
      <rect x="5" y="33.5" width="90" height="1.8" />
      <rect x="2" y="37" width="96" height="3" />

      {/* 6 колонн */}
      <g>
        <rect x="11" y="41" width="6" height="22" />
        <rect x="25" y="41" width="6" height="22" />
        <rect x="39" y="41" width="6" height="22" />
        <rect x="53" y="41" width="6" height="22" />
        <rect x="67" y="41" width="6" height="22" />
        <rect x="81" y="41" width="6" height="22" />
      </g>

      {/* Стилобат (ступени) */}
      <rect x="5" y="65" width="90" height="3" />
      <rect x="2" y="70" width="96" height="3" />
      <rect x="0" y="75" width="100" height="5" />
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
      <LogoMark
        className={cn(
          "h-11 w-auto shrink-0 transition-transform duration-300 group-hover:scale-[1.04]",
          variant === "dark" ? "text-navy-900" : "text-white",
        )}
      />
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
