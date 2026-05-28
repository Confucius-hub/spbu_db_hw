import type { MetadataRoute } from "next";
import { site } from "@/lib/site";
import { getAllArticleSlugs, getCategories } from "@/lib/news";

export const dynamic = "force-dynamic";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const base = site.url;
  const now = new Date();

  const staticRoutes = [
    "",
    "/about",
    "/membership",
    "/nrs",
    "/documents",
    "/members",
    "/news",
    "/contacts",
    "/privacy",
  ].map((path) => ({
    url: `${base}${path}`,
    lastModified: now,
    changeFrequency: "weekly" as const,
    priority: path === "" ? 1 : 0.7,
  }));

  let articleRoutes: MetadataRoute.Sitemap = [];
  let categoryRoutes: MetadataRoute.Sitemap = [];
  try {
    const [articles, categories] = await Promise.all([getAllArticleSlugs(), getCategories()]);
    articleRoutes = articles.map((a) => ({
      url: `${base}/news/${a.slug}`,
      lastModified: a.updatedAt,
      changeFrequency: "monthly" as const,
      priority: 0.6,
    }));
    categoryRoutes = categories.map((c) => ({
      url: `${base}/news/category/${c.slug}`,
      lastModified: now,
      changeFrequency: "weekly" as const,
      priority: 0.5,
    }));
  } catch {
    // БД может быть недоступна во время сборки — отдаём статические маршруты
  }

  return [...staticRoutes, ...articleRoutes, ...categoryRoutes];
}
