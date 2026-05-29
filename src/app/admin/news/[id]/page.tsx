import Link from "next/link";
import { notFound } from "next/navigation";
import { prisma } from "@/lib/prisma";
import { ArticleEditor } from "@/components/admin/article-editor";
import { Icon } from "@/lib/icons";

export const dynamic = "force-dynamic";

export default async function EditArticlePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const [article, categories] = await Promise.all([
    prisma.article.findUnique({ where: { id }, include: { tags: true } }),
    prisma.category.findMany({ orderBy: { title: "asc" } }),
  ]);

  if (!article) notFound();

  return (
    <div>
      <Link
        href="/admin/news"
        className="inline-flex items-center gap-1.5 text-sm font-medium text-slate-500 hover:text-navy-900"
      >
        <Icon name="ChevronRight" className="h-4 w-4 rotate-180" />
        К списку новостей
      </Link>
      <div className="mt-3 flex items-center justify-between gap-4">
        <h1 className="text-2xl font-bold text-navy-900">Редактирование</h1>
        <Link
          href={`/news/${article.slug}`}
          target="_blank"
          rel="noopener"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-navy-700 hover:text-gold-700"
        >
          <Icon name="Eye" className="h-4 w-4" />
          Открыть на сайте
        </Link>
      </div>
      <div className="mt-6">
        <ArticleEditor
          categories={categories}
          initial={{
            id: article.id,
            title: article.title,
            slug: article.slug,
            excerpt: article.excerpt,
            content: article.content,
            categoryId: article.categoryId,
            author: article.author,
            tags: article.tags.map((t) => t.title),
            featured: article.featured,
            published: article.published,
            seoTitle: article.seoTitle ?? "",
            seoDescription: article.seoDescription ?? "",
          }}
        />
      </div>
    </div>
  );
}
