import Link from "next/link";
import { cn } from "@/lib/utils";

type Category = { slug: string; title: string };

const chip = (active: boolean) =>
  cn(
    "inline-flex items-center rounded-full px-4 py-2 text-sm font-medium transition-colors",
    active
      ? "bg-navy-800 text-white"
      : "bg-white text-slate-600 ring-1 ring-slate-200 hover:ring-gold-300 hover:text-navy-900",
  );

/** Навигация по рубрикам — чистые SEO-маршруты /news/category/[slug]. */
export function CategoryNav({
  categories,
  activeSlug,
}: {
  categories: Category[];
  activeSlug?: string;
}) {
  return (
    <div className="flex flex-wrap gap-2">
      <Link href="/news" className={chip(!activeSlug)}>
        Все
      </Link>
      {categories.map((c) => (
        <Link
          key={c.slug}
          href={`/news/category/${c.slug}`}
          className={chip(activeSlug === c.slug)}
        >
          {c.title}
        </Link>
      ))}
    </div>
  );
}
