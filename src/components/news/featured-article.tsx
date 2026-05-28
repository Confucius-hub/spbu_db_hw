import Link from "next/link";
import { ArticleCover } from "./cover";
import { Badge } from "@/components/ui/badge";
import { Icon } from "@/lib/icons";
import { formatDate } from "@/lib/utils";
import type { ArticleWithRelations } from "@/lib/news";

export function FeaturedArticle({ article }: { article: ArticleWithRelations }) {
  return (
    <article className="group overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-card lg:grid lg:grid-cols-2">
      <Link href={`/news/${article.slug}`} className="block">
        <ArticleCover
          categorySlug={article.category.slug}
          categoryTitle={article.category.title}
          size="hero"
          className="aspect-[16/10] lg:h-full lg:aspect-auto"
        />
      </Link>
      <div className="flex flex-col justify-center p-7 sm:p-9">
        <div className="flex items-center gap-3">
          <Badge variant="gold">
            <Icon name="Sparkles" className="h-3.5 w-3.5" />
            Главное
          </Badge>
          <span className="text-sm text-slate-500">{article.category.title}</span>
        </div>
        <h2 className="mt-4 font-display text-2xl font-extrabold leading-tight text-navy-900 sm:text-3xl">
          <Link href={`/news/${article.slug}`} className="transition-colors group-hover:text-navy-700">
            {article.title}
          </Link>
        </h2>
        <p className="mt-3 text-[1.02rem] leading-relaxed text-slate-600">{article.excerpt}</p>
        <div className="mt-5 flex items-center gap-4 text-sm text-slate-500">
          <span className="inline-flex items-center gap-1.5">
            <Icon name="Calendar" className="h-4 w-4" />
            {formatDate(article.publishedAt)}
          </span>
          <span className="inline-flex items-center gap-1.5">
            <Icon name="Clock" className="h-4 w-4" />
            {article.readingTime} мин чтения
          </span>
        </div>
        <Link
          href={`/news/${article.slug}`}
          className="mt-6 inline-flex w-fit items-center gap-2 rounded-xl bg-navy-800 px-5 py-3 text-sm font-semibold text-white transition-colors hover:bg-navy-700"
        >
          Читать материал
          <Icon name="ArrowRight" className="h-4 w-4" />
        </Link>
      </div>
    </article>
  );
}
