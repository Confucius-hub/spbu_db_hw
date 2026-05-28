import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Container } from "@/components/ui/container";
import { Breadcrumbs } from "@/components/layout/breadcrumbs";
import { ArticleCover } from "@/components/news/cover";
import { ArticleBody } from "@/components/news/article-body";
import { ShareButtons } from "@/components/news/share-buttons";
import { NewsCard } from "@/components/news/news-card";
import { Cta } from "@/components/sections/cta";
import { Badge } from "@/components/ui/badge";
import { Icon } from "@/lib/icons";
import { formatDate } from "@/lib/utils";
import { getArticleBySlug, getRelatedArticles, incrementViews } from "@/lib/news";
import { site } from "@/lib/site";

export const dynamic = "force-dynamic";

type Params = Promise<{ slug: string }>;

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { slug } = await params;
  const article = await getArticleBySlug(slug);
  if (!article) return { title: "Материал не найден" };
  return {
    title: article.seoTitle || article.title,
    description: article.seoDescription || article.excerpt,
    alternates: { canonical: `/news/${article.slug}` },
    openGraph: {
      type: "article",
      title: article.title,
      description: article.excerpt,
      url: `${site.url}/news/${article.slug}`,
      publishedTime: article.publishedAt.toISOString(),
    },
  };
}

export default async function ArticlePage({ params }: { params: Params }) {
  const { slug } = await params;
  const article = await getArticleBySlug(slug);
  if (!article) notFound();

  await incrementViews(article.id);
  const related = await getRelatedArticles(article, 3);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    headline: article.title,
    description: article.excerpt,
    datePublished: article.publishedAt.toISOString(),
    dateModified: article.updatedAt.toISOString(),
    author: { "@type": "Organization", name: article.author },
    publisher: { "@type": "Organization", name: site.legalName },
    mainEntityOfPage: `${site.url}/news/${article.slug}`,
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <article>
        {/* Шапка статьи */}
        <header className="border-b border-slate-200 bg-white">
          <Container size="narrow" className="py-8 sm:py-12">
            <Breadcrumbs
              items={[
                { label: "Новости", href: "/news" },
                { label: article.category.title, href: `/news/category/${article.category.slug}` },
              ]}
            />
            <div className="mt-6 flex flex-wrap items-center gap-3">
              <Link href={`/news/category/${article.category.slug}`}>
                <Badge variant="navy">{article.category.title}</Badge>
              </Link>
              <span className="inline-flex items-center gap-1.5 text-sm text-slate-500">
                <Icon name="Calendar" className="h-4 w-4" />
                {formatDate(article.publishedAt)}
              </span>
              <span className="inline-flex items-center gap-1.5 text-sm text-slate-500">
                <Icon name="Clock" className="h-4 w-4" />
                {article.readingTime} мин чтения
              </span>
              <span className="inline-flex items-center gap-1.5 text-sm text-slate-500">
                <Icon name="Eye" className="h-4 w-4" />
                {article.views}
              </span>
            </div>
            <h1 className="mt-4 font-display text-3xl font-extrabold leading-tight text-navy-900 sm:text-4xl">
              {article.title}
            </h1>
            <p className="mt-4 text-lg leading-relaxed text-slate-600">{article.excerpt}</p>
          </Container>
        </header>

        {/* Обложка */}
        <Container size="narrow" className="py-8">
          <ArticleCover
            categorySlug={article.category.slug}
            categoryTitle={article.category.title}
            size="hero"
            className="aspect-[16/8] rounded-2xl"
          />
        </Container>

        {/* Тело */}
        <Container size="narrow" className="pb-12">
          <ArticleBody content={article.content} />

          {/* Теги + поделиться */}
          <div className="mt-10 flex flex-col gap-5 border-t border-slate-200 pt-6 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex flex-wrap gap-2">
              {article.tags.map((t) => (
                <Link
                  key={t.id}
                  href={`/news?tag=${t.slug}`}
                  className="inline-flex items-center gap-1.5 rounded-full bg-slate-100 px-3 py-1.5 text-sm text-slate-600 transition-colors hover:bg-gold-100 hover:text-gold-800"
                >
                  <Icon name="Tag" className="h-3.5 w-3.5" />
                  {t.title}
                </Link>
              ))}
            </div>
            <ShareButtons slug={article.slug} title={article.title} />
          </div>

          {/* Автор */}
          <div className="mt-8 flex items-center gap-4 rounded-2xl bg-slate-50 p-5">
            <span className="inline-flex h-12 w-12 items-center justify-center rounded-full bg-navy-800 text-gold-400">
              <Icon name="BadgeCheck" className="h-6 w-6" />
            </span>
            <div>
              <p className="font-semibold text-navy-900">{article.author}</p>
              <p className="text-sm text-slate-500">
                Официальная публикация СРО «Строительный союз Северной столицы»
              </p>
            </div>
          </div>
        </Container>
      </article>

      {/* Похожие материалы */}
      {related.length > 0 && (
        <section className="bg-slate-50 py-16">
          <Container>
            <div className="flex items-end justify-between">
              <h2 className="text-2xl font-bold text-navy-900 sm:text-3xl">Похожие материалы</h2>
              <Link
                href="/news"
                className="inline-flex items-center gap-1.5 text-sm font-semibold text-navy-800 hover:text-gold-700"
              >
                Все новости
                <Icon name="ArrowRight" className="h-4 w-4" />
              </Link>
            </div>
            <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
              {related.map((a) => (
                <NewsCard key={a.id} article={a} />
              ))}
            </div>
          </Container>
        </section>
      )}

      <Cta />
    </>
  );
}
