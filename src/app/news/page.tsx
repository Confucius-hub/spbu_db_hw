import type { Metadata } from "next";
import { Container } from "@/components/ui/container";
import { PageHeader } from "@/components/layout/page-header";
import { NewsCard } from "@/components/news/news-card";
import { CategoryNav } from "@/components/news/category-nav";
import { SearchBox } from "@/components/news/search-box";
import { FeaturedArticle } from "@/components/news/featured-article";
import { Pagination } from "@/components/news/pagination";
import { Cta } from "@/components/sections/cta";
import { Icon } from "@/lib/icons";
import { getCategories, getFeaturedArticle, getTags, listArticles } from "@/lib/news";
import { pageMetadata } from "@/lib/seo";

export const dynamic = "force-dynamic";

export const metadata: Metadata = pageMetadata({
  title: "Новости",
  description:
    "Изменения в законодательстве, реформа саморегулирования 2026, цифровизация (ТИМ), новости НОСТРОЙ и события СРО «Строительный союз Северной столицы».",
  path: "/news",
});

type SearchParams = Promise<{ page?: string; q?: string; tag?: string }>;

export default async function NewsPage({ searchParams }: { searchParams: SearchParams }) {
  const sp = await searchParams;
  const page = Number(sp.page ?? "1") || 1;
  const query = sp.q;
  const tag = sp.tag;

  const [categories, featured, list, tags] = await Promise.all([
    getCategories(),
    !query && !tag && page === 1 ? getFeaturedArticle() : Promise.resolve(null),
    listArticles({ page, query, tag }),
    getTags(),
  ]);

  const activeTag = tag ? tags.find((t) => t.slug === tag) : undefined;
  const items = featured ? list.items.filter((a) => a.id !== featured.id) : list.items;

  return (
    <>
      <PageHeader
        eyebrow="Медиацентр"
        title="Новости и аналитика"
        description="Следим за изменениями в саморегулировании, разбираем реформу 2026 года, цифровизацию отрасли и рассказываем о жизни СРО."
        breadcrumbs={[{ label: "Новости" }]}
      />

      <section className="bg-slate-50 py-12 sm:py-16">
        <Container>
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <CategoryNav categories={categories} />
            <SearchBox initial={query} />
          </div>

          {query && (
            <p className="mt-6 text-sm text-slate-600">
              Результаты по запросу{" "}
              <span className="font-semibold text-navy-900">«{query}»</span>: {list.total} материалов
            </p>
          )}
          {activeTag && (
            <p className="mt-6 inline-flex items-center gap-2 text-sm text-slate-600">
              <Icon name="Tag" className="h-4 w-4 text-gold-600" />
              Тег <span className="font-semibold text-navy-900">«{activeTag.title}»</span>:{" "}
              {list.total} материалов
            </p>
          )}

          {featured && (
            <div className="mt-8">
              <FeaturedArticle article={featured} />
            </div>
          )}

          {items.length > 0 ? (
            <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
              {items.map((a) => (
                <NewsCard key={a.id} article={a} />
              ))}
            </div>
          ) : (
            !featured && (
              <div className="mt-10 rounded-2xl border border-dashed border-slate-300 bg-white py-16 text-center">
                <Icon name="Search" className="mx-auto h-10 w-10 text-slate-300" />
                <p className="mt-3 font-semibold text-navy-900">Ничего не найдено</p>
                <p className="mt-1 text-sm text-slate-500">
                  Попробуйте изменить запрос или выбрать рубрику.
                </p>
              </div>
            )
          )}

          <Pagination
            page={list.page}
            totalPages={list.totalPages}
            params={{ q: query, tag }}
          />
        </Container>
      </section>

      <Cta
        title="Не пропускайте важные изменения"
        text="Оставьте контакты — сообщим о ключевых нововведениях в саморегулировании и поможем подготовиться."
      />
    </>
  );
}
