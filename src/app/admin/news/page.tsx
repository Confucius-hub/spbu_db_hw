import Link from "next/link";
import { prisma } from "@/lib/prisma";
import { Icon } from "@/lib/icons";
import { formatDateShort } from "@/lib/utils";
import { ArticleDeleteButton } from "@/components/admin/article-delete-button";
import { Badge } from "@/components/ui/badge";

export const dynamic = "force-dynamic";

export default async function AdminNewsList() {
  const articles = await prisma.article.findMany({
    orderBy: { publishedAt: "desc" },
    include: { category: true },
  });

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-navy-900">Новости</h1>
          <p className="mt-1 text-slate-500">{articles.length} материалов</p>
        </div>
        <Link
          href="/admin/news/new"
          className="inline-flex h-11 items-center gap-2 rounded-xl bg-navy-800 px-5 font-semibold text-white transition-colors hover:bg-navy-700"
        >
          <Icon name="Plus" className="h-4 w-4" strokeWidth={2.5} />
          Новая статья
        </Link>
      </div>

      <div className="mt-8 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-soft">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-100 text-left text-xs uppercase tracking-wider text-slate-400">
                <th className="px-5 py-3 font-semibold">Заголовок</th>
                <th className="px-5 py-3 font-semibold">Рубрика</th>
                <th className="px-5 py-3 font-semibold">Статус</th>
                <th className="px-5 py-3 font-semibold">Дата</th>
                <th className="px-5 py-3 text-right font-semibold">Просмотры</th>
                <th className="px-5 py-3 text-right font-semibold">Действия</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {articles.map((a) => (
                <tr key={a.id} className="hover:bg-slate-50">
                  <td className="max-w-sm px-5 py-3.5">
                    <Link href={`/admin/news/${a.id}`} className="font-medium text-navy-900 hover:text-gold-700">
                      {a.title}
                    </Link>
                    {a.featured && (
                      <span className="ml-2 inline-flex">
                        <Badge variant="gold">
                          <Icon name="Sparkles" className="h-3 w-3" />
                          Главное
                        </Badge>
                      </span>
                    )}
                  </td>
                  <td className="px-5 py-3.5 text-slate-600">{a.category.title}</td>
                  <td className="px-5 py-3.5">
                    {a.published ? (
                      <Badge variant="success">Опубликовано</Badge>
                    ) : (
                      <Badge variant="muted">Черновик</Badge>
                    )}
                  </td>
                  <td className="px-5 py-3.5 text-slate-500">{formatDateShort(a.publishedAt)}</td>
                  <td className="px-5 py-3.5 text-right text-slate-500">{a.views}</td>
                  <td className="px-5 py-3.5">
                    <div className="flex items-center justify-end gap-1">
                      <Link
                        href={`/admin/news/${a.id}`}
                        className="inline-flex h-9 w-9 items-center justify-center rounded-lg text-slate-400 transition-colors hover:bg-navy-50 hover:text-navy-700"
                        aria-label="Редактировать"
                        title="Редактировать"
                      >
                        <Icon name="Pencil" className="h-4 w-4" />
                      </Link>
                      <ArticleDeleteButton id={a.id} title={a.title} />
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
