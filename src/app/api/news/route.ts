import { NextResponse } from "next/server";
import { listArticles } from "@/lib/news";

/** Публичный JSON-эндпоинт ленты новостей. */
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const page = Number(searchParams.get("page") ?? "1") || 1;
  const category = searchParams.get("category") ?? undefined;
  const tag = searchParams.get("tag") ?? undefined;
  const query = searchParams.get("q") ?? undefined;

  const { items, total, totalPages, page: current } = await listArticles({
    page,
    category,
    tag,
    query,
  });

  return NextResponse.json({
    page: current,
    totalPages,
    total,
    items: items.map((a) => ({
      slug: a.slug,
      title: a.title,
      excerpt: a.excerpt,
      category: a.category.title,
      categorySlug: a.category.slug,
      tags: a.tags.map((t) => t.title),
      publishedAt: a.publishedAt,
      readingTime: a.readingTime,
      url: `/news/${a.slug}`,
    })),
  });
}
