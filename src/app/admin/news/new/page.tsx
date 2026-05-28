import Link from "next/link";
import { prisma } from "@/lib/prisma";
import { ArticleEditor } from "@/components/admin/article-editor";
import { Icon } from "@/lib/icons";

export const dynamic = "force-dynamic";

export default async function NewArticlePage() {
  const categories = await prisma.category.findMany({ orderBy: { title: "asc" } });

  return (
    <div>
      <Link
        href="/admin/news"
        className="inline-flex items-center gap-1.5 text-sm font-medium text-slate-500 hover:text-navy-900"
      >
        <Icon name="ChevronRight" className="h-4 w-4 rotate-180" />
        К списку новостей
      </Link>
      <h1 className="mt-3 text-2xl font-bold text-navy-900">Новая статья</h1>
      <div className="mt-6">
        <ArticleEditor categories={categories} />
      </div>
    </div>
  );
}
