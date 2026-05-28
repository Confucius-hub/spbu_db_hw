import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Container } from "@/components/ui/container";
import { PageHeader } from "@/components/layout/page-header";
import { NewsCard } from "@/components/news/news-card";
import { CategoryNav } from "@/components/news/category-nav";
import { Pagination } from "@/components/news/pagination";
import { Cta } from "@/components/sections/cta";
import { Icon } from "@/lib/icons";
import { getCategories, getCategoryBySlug, listArticles } from "@/lib/news";
import { pageMetadata } from "@/lib/seo";

export const dynamic = "force-dynamic";

type Params = Promise<{ slug: string }>;
type SearchParams = Promise<{ page?: string }>;

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { slug } = await params;
  const category = await getCategoryBySlug(slug);
  if (!category) return { title: "Рубрика не найдена" };
  return pageMetadata({
    title: `${category.title} — Новости`,
    description: category.description ?? `Новости рубрики «${category.title}» СРО «СССС».`,
    path: `/news/category/${category.slug}`,
  });
}

export default async function CategoryPage({
  params,
  searchParams,
}: {
  params: Params;
  searchParams: SearchParams;
}) {
  const { slug } = await params;
  const sp = await searchParams;
  const page = Number(sp.page ?? "1") || 1;

  const category = await getCategoryBySlug(slug);
  if (!category) notFound();

  const [categories, list] = await Promise.all([
    getCategories(),
    listArticles({ page, category: slug }),
  ]);

  return (
    <>
      <PageHeader
        eyebrow="Рубрика"
        title={category.title}
        description={category.description ?? undefined}
        breadcrumbs={[{ label: "Новости", href: "/news" }, { label: category.title }]}
      />

      <section className="bg-slate-50 py-12 sm:py-16">
        <Container>
          <CategoryNav categories={categories} activeSlug={slug} />

          {list.items.length > 0 ? (
            <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
              {list.items.map((a) => (
                <NewsCard key={a.id} article={a} />
              ))}
            </div>
          ) : (
            <div className="mt-10 rounded-2xl border border-dashed border-slate-300 bg-white py-16 text-center">
              <Icon name="Newspaper" className="mx-auto h-10 w-10 text-slate-300" />
              <p className="mt-3 font-semibold text-navy-900">В этой рубрике пока нет материалов</p>
            </div>
          )}

          <Pagination
            page={list.page}
            totalPages={list.totalPages}
            base={`/news/category/${slug}`}
          />
        </Container>
      </section>

      <Cta />
    </>
  );
}
