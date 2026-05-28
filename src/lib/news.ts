import { Prisma } from "@prisma/client";
import { prisma } from "./prisma";

export type ArticleWithRelations = Prisma.ArticleGetPayload<{
  include: { category: true; tags: true };
}>;

export const PER_PAGE = 6;

export function getCategories() {
  return prisma.category.findMany({ orderBy: { title: "asc" } });
}

export function getCategoryBySlug(slug: string) {
  return prisma.category.findUnique({ where: { slug } });
}

export function getTags() {
  return prisma.tag.findMany({ orderBy: { title: "asc" } });
}

export async function getFeaturedArticle(): Promise<ArticleWithRelations | null> {
  return prisma.article.findFirst({
    where: { published: true, featured: true },
    orderBy: { publishedAt: "desc" },
    include: { category: true, tags: true },
  });
}

export async function getRecentArticles(limit = 3): Promise<ArticleWithRelations[]> {
  return prisma.article.findMany({
    where: { published: true },
    orderBy: { publishedAt: "desc" },
    take: limit,
    include: { category: true, tags: true },
  });
}

type ListParams = {
  page?: number;
  category?: string; // slug
  tag?: string; // slug
  query?: string;
  perPage?: number;
};

export async function listArticles({
  page = 1,
  category,
  tag,
  query,
  perPage = PER_PAGE,
}: ListParams): Promise<{
  items: ArticleWithRelations[];
  total: number;
  totalPages: number;
  page: number;
}> {
  const where: Prisma.ArticleWhereInput = {
    published: true,
    ...(category ? { category: { slug: category } } : {}),
    ...(tag ? { tags: { some: { slug: tag } } } : {}),
  };

  // Поиск по кириллице: SQLite LIKE не регистронезависим для не-ASCII,
  // поэтому фильтруем в памяти (объём данных небольшой).
  if (query && query.trim()) {
    const q = query.trim().toLowerCase();
    const all = await prisma.article.findMany({
      where,
      orderBy: [{ featured: "desc" }, { publishedAt: "desc" }],
      include: { category: true, tags: true },
    });
    const filtered = all.filter((a) =>
      [a.title, a.excerpt, a.content, a.category.title].some((f) =>
        f.toLowerCase().includes(q),
      ),
    );
    const total = filtered.length;
    const totalPages = Math.max(1, Math.ceil(total / perPage));
    const safePage = Math.min(Math.max(1, page), totalPages);
    const items = filtered.slice((safePage - 1) * perPage, safePage * perPage);
    return { items, total, totalPages, page: safePage };
  }

  const total = await prisma.article.count({ where });
  const totalPages = Math.max(1, Math.ceil(total / perPage));
  const safePage = Math.min(Math.max(1, page), totalPages);
  const items = await prisma.article.findMany({
    where,
    orderBy: [{ featured: "desc" }, { publishedAt: "desc" }],
    skip: (safePage - 1) * perPage,
    take: perPage,
    include: { category: true, tags: true },
  });
  return { items, total, totalPages, page: safePage };
}

export async function getArticleBySlug(slug: string): Promise<ArticleWithRelations | null> {
  return prisma.article.findFirst({
    where: { slug, published: true },
    include: { category: true, tags: true },
  });
}

export async function getRelatedArticles(
  article: ArticleWithRelations,
  limit = 3,
): Promise<ArticleWithRelations[]> {
  const tagIds = article.tags.map((t) => t.id);
  return prisma.article.findMany({
    where: {
      published: true,
      id: { not: article.id },
      OR: [
        { categoryId: article.categoryId },
        ...(tagIds.length ? [{ tags: { some: { id: { in: tagIds } } } }] : []),
      ],
    },
    orderBy: { publishedAt: "desc" },
    take: limit,
    include: { category: true, tags: true },
  });
}

export async function getAllArticleSlugs(): Promise<{ slug: string; updatedAt: Date }[]> {
  return prisma.article.findMany({
    where: { published: true },
    select: { slug: true, updatedAt: true },
  });
}

export async function incrementViews(id: string) {
  try {
    await prisma.article.update({ where: { id }, data: { views: { increment: 1 } } });
  } catch {
    // не критично
  }
}
