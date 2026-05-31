import { Photo } from "@/components/ui/photo";
import { Icon, type IconName } from "@/lib/icons";
import { cn } from "@/lib/utils";
import { newsCategoryImages } from "@/lib/site";

type CoverStyle = { gradient: string; icon: IconName; pattern: "grid" | "dots" };

const STYLES: Record<string, CoverStyle> = {
  legislation: { gradient: "from-navy-800 to-navy-950", icon: "ScrollText", pattern: "grid" },
  industry: { gradient: "from-navy-700 via-navy-800 to-navy-950", icon: "TrendingUp", pattern: "dots" },
  sro: { gradient: "from-navy-800 to-navy-900", icon: "Building2", pattern: "grid" },
  nostroy: { gradient: "from-navy-700 to-navy-900", icon: "Landmark", pattern: "dots" },
  guides: { gradient: "from-navy-800 to-navy-950", icon: "FileText", pattern: "grid" },
};

const FALLBACK: CoverStyle = { gradient: "from-navy-800 to-navy-950", icon: "Newspaper", pattern: "grid" };

/**
 * Обложка статьи: фото по рубрике с фирменным затемнением.
 * Если фото не загрузится — остаётся фирменный градиент с иконкой.
 */
export function ArticleCover({
  categorySlug,
  categoryTitle,
  className,
  size = "card",
}: {
  categorySlug: string;
  categoryTitle: string;
  className?: string;
  size?: "card" | "hero";
}) {
  const s = STYLES[categorySlug] ?? FALLBACK;
  const photo = newsCategoryImages[categorySlug];

  return (
    <div
      className={cn(
        "relative overflow-hidden bg-gradient-to-br",
        s.gradient,
        className,
      )}
    >
      {/* Фото — снизу, чтобы фолбэк-градиент остался при ошибке */}
      {photo && (
        <Photo
          src={photo}
          className="absolute inset-0"
          imgClassName="opacity-70"
          priority={size === "hero"}
        />
      )}
      {/* Затемнение для читаемости категории */}
      <div
        className="absolute inset-0 bg-gradient-to-t from-navy-950/85 via-navy-900/40 to-navy-900/20"
        aria-hidden
      />
      {/* Тонкая фирменная сетка */}
      <div
        className={cn("absolute inset-0 opacity-30", s.pattern === "grid" ? "bg-grid" : "bg-dots")}
        aria-hidden
      />
      {/* Декоративный градиентный круг */}
      <div
        className="absolute -bottom-8 -right-6 h-40 w-40 rounded-full bg-gold-500/10 blur-2xl"
        aria-hidden
      />
      {/* Иконка-«водяной знак» — на случай отсутствия фото остаётся узнаваемой */}
      <Icon
        name={s.icon}
        className={cn(
          "absolute text-white/10",
          size === "hero" ? "-bottom-8 -right-4 h-52 w-52" : "-bottom-6 -right-3 h-32 w-32",
        )}
        strokeWidth={1.25}
      />
      {/* Чип рубрики */}
      <span className="absolute left-4 top-4 inline-flex items-center gap-1.5 rounded-full bg-navy-900/70 px-3 py-1 text-xs font-semibold text-gold-200 ring-1 ring-white/15 backdrop-blur-sm">
        <span className="h-1.5 w-1.5 rounded-full bg-gold-400" />
        {categoryTitle}
      </span>
    </div>
  );
}
