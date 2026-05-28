import Link from "next/link";
import { prisma } from "@/lib/prisma";
import { Icon, type IconName } from "@/lib/icons";
import { formatDateShort } from "@/lib/utils";

export const dynamic = "force-dynamic";

const leadTypeLabels: Record<string, string> = {
  CALLBACK: "Обратный звонок",
  CONSULTATION: "Консультация",
  APPLICATION: "Заявка на вступление",
  CALCULATOR: "Расчёт стоимости",
};

export default async function AdminDashboard() {
  const [articles, published, featured, leads, newLeads, recentLeads] = await Promise.all([
    prisma.article.count(),
    prisma.article.count({ where: { published: true } }),
    prisma.article.count({ where: { featured: true } }),
    prisma.lead.count(),
    prisma.lead.count({ where: { status: "NEW" } }),
    prisma.lead.findMany({ orderBy: { createdAt: "desc" }, take: 8 }),
  ]);

  const stats: { label: string; value: number; icon: IconName; tone: string }[] = [
    { label: "Всего статей", value: articles, icon: "Newspaper", tone: "bg-navy-50 text-navy-700" },
    { label: "Опубликовано", value: published, icon: "CheckCircle2", tone: "bg-emerald-50 text-emerald-600" },
    { label: "В избранном", value: featured, icon: "Sparkles", tone: "bg-gold-100 text-gold-700" },
    { label: "Новых заявок", value: newLeads, icon: "Send", tone: "bg-red-50 text-red-600" },
  ];

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-navy-900">Дашборд</h1>
          <p className="mt-1 text-slate-500">Обзор контента и заявок с сайта</p>
        </div>
        <Link
          href="/admin/news/new"
          className="inline-flex h-11 items-center gap-2 rounded-xl bg-navy-800 px-5 font-semibold text-white transition-colors hover:bg-navy-700"
        >
          <Icon name="Plus" className="h-4 w-4" strokeWidth={2.5} />
          Новая статья
        </Link>
      </div>

      <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((s) => (
          <div key={s.label} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-soft">
            <span className={`inline-flex h-11 w-11 items-center justify-center rounded-xl ${s.tone}`}>
              <Icon name={s.icon} className="h-5 w-5" />
            </span>
            <p className="mt-4 font-display text-3xl font-extrabold text-navy-900">{s.value}</p>
            <p className="text-sm text-slate-500">{s.label}</p>
          </div>
        ))}
      </div>

      <div className="mt-8 rounded-2xl border border-slate-200 bg-white shadow-soft">
        <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">
          <h2 className="font-bold text-navy-900">Последние заявки</h2>
          <span className="text-sm text-slate-500">Всего: {leads}</span>
        </div>
        {recentLeads.length === 0 ? (
          <p className="px-5 py-10 text-center text-slate-500">Заявок пока нет</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs uppercase tracking-wider text-slate-400">
                  <th className="px-5 py-3 font-semibold">Тип</th>
                  <th className="px-5 py-3 font-semibold">Имя</th>
                  <th className="px-5 py-3 font-semibold">Телефон</th>
                  <th className="px-5 py-3 font-semibold">Компания</th>
                  <th className="px-5 py-3 font-semibold">Дата</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {recentLeads.map((l) => (
                  <tr key={l.id} className="hover:bg-slate-50">
                    <td className="px-5 py-3.5">
                      <span className="inline-flex rounded-full bg-navy-50 px-2.5 py-1 text-xs font-semibold text-navy-700">
                        {leadTypeLabels[l.type] ?? l.type}
                      </span>
                    </td>
                    <td className="px-5 py-3.5 font-medium text-navy-900">{l.name}</td>
                    <td className="px-5 py-3.5 text-slate-600">{l.phone}</td>
                    <td className="px-5 py-3.5 text-slate-600">{l.company ?? "—"}</td>
                    <td className="px-5 py-3.5 text-slate-500">{formatDateShort(l.createdAt)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
