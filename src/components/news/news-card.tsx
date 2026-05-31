import Link from "next/link";
import { ArticleCover } from "./cover";
import { Icon } from "@/lib/icons";
import { formatDate, isRecent, pluralize } from "@/lib/utils";
import type { ArticleWithRelations } from "@/lib/news";

export function NewsCard({
  article,
  className,
}: {
  article: ArticleWithRelations;
  className?: string;
}) {
  return (
    <article
      className={
        "group flex flex-col overflow-hidden rounded-2xl border border-slate-200/80 bg-white shadow-soft transition-all duration-300 ease-[cubic-bezier(0.22,1,0.36,1)] hover:-translate-y-1 hover:border-gold-200 hover:shadow-lift " +
        (className ?? "")
      }
    >
      <Link href={`/news/${article.slug}`} className="relative block">
        <ArticleCover
          categorySlug={article.category.slug}
          categoryTitle={article.category.title}
          seed={article.slug}
          className="aspect-[16/9]"
        />
        {isRecent(article.publishedAt) && (
          <span className="absolute right-4 top-4 inline-flex items-center gap-1 rounded-full bg-gold-500 px-2.5 py-1 text-xs font-bold text-navy-950 shadow-sm">
            <span className="h-1.5 w-1.5 rounded-full bg-navy-900" />
            Свежее
          </span>
        )}
      </Link>
      <div className="flex flex-1 flex-col p-5">
        <div className="flex items-center gap-3 text-xs text-slate-500">
          <span className="inline-flex items-center gap-1.5">
            <Icon name="Calendar" className="h-3.5 w-3.5" />
            {formatDate(article.publishedAt)}
          </span>
          <span className="inline-flex items-center gap-1.5">
            <Icon name="Clock" className="h-3.5 w-3.5" />
            {article.readingTime} мин
          </span>
        </div>
        <h3 className="mt-2.5 text-lg font-bold leading-snug text-navy-900">
          <Link
            href={`/news/${article.slug}`}
            className="transition-colors after:absolute group-hover:text-navy-700"
          >
            {article.title}
          </Link>
        </h3>
        <p className="mt-2 line-clamp-3 flex-1 text-[0.92rem] leading-relaxed text-slate-600">
          {article.excerpt}
        </p>
        <span className="mt-4 inline-flex items-center gap-1.5 text-sm font-semibold text-navy-800 transition-colors group-hover:text-gold-700">
          Читать
          <Icon name="ArrowRight" className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
        </span>
      </div>
    </article>
  );
}

export function articleMetaLabel(count: number) {
  return `${count} ${pluralize(count, ["статья", "статьи", "статей"])}`;
}
