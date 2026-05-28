"use client";

import { useMemo, useState } from "react";
import { Icon } from "@/lib/icons";
import { formatDate, cn } from "@/lib/utils";
import type { DocItem } from "@/lib/documents";

const formatColors: Record<DocItem["format"], string> = {
  PDF: "bg-red-50 text-red-600 ring-red-100",
  DOC: "bg-blue-50 text-blue-600 ring-blue-100",
  XLS: "bg-emerald-50 text-emerald-600 ring-emerald-100",
};

export function DocumentsExplorer({
  documents,
  categories,
}: {
  documents: DocItem[];
  categories: readonly string[];
}) {
  const [active, setActive] = useState<string | null>(null);
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return documents.filter(
      (d) =>
        (!active || d.category === active) &&
        (!q || d.title.toLowerCase().includes(q)),
    );
  }, [documents, active, query]);

  const chip = (isActive: boolean) =>
    cn(
      "inline-flex items-center rounded-full px-4 py-2 text-sm font-medium transition-colors",
      isActive
        ? "bg-navy-800 text-white"
        : "bg-white text-slate-600 ring-1 ring-slate-200 hover:ring-gold-300 hover:text-navy-900",
    );

  return (
    <div>
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex flex-wrap gap-2">
          <button onClick={() => setActive(null)} className={chip(!active)}>
            Все
          </button>
          {categories.map((c) => (
            <button key={c} onClick={() => setActive(c)} className={chip(active === c)}>
              {c}
            </button>
          ))}
        </div>
        <div className="relative w-full lg:w-72">
          <Icon
            name="Search"
            className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
          />
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Поиск документа"
            className="w-full rounded-xl border border-slate-200 bg-white py-2.5 pl-10 pr-4 text-sm text-navy-900 placeholder:text-slate-400 focus:border-gold-400 focus:outline-none focus:ring-2 focus:ring-gold-200"
          />
        </div>
      </div>

      <div className="mt-8 space-y-3">
        {filtered.map((d, i) => (
          <a
            key={i}
            href={d.href}
            className="group flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-soft transition-all hover:border-gold-200 hover:shadow-card"
          >
            <span
              className={cn(
                "inline-flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-xs font-bold ring-1",
                formatColors[d.format],
              )}
            >
              {d.format}
            </span>
            <div className="min-w-0 flex-1">
              <p className="truncate font-semibold text-navy-900 group-hover:text-navy-700">
                {d.title}
              </p>
              <p className="mt-0.5 text-sm text-slate-500">
                {d.category} · {d.size} · обновлено {formatDate(d.date)}
              </p>
            </div>
            <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-navy-700 transition-colors group-hover:bg-gold-100 group-hover:text-gold-700">
              <Icon name="Download" className="h-5 w-5" />
            </span>
          </a>
        ))}

        {filtered.length === 0 && (
          <div className="rounded-2xl border border-dashed border-slate-300 bg-white py-14 text-center">
            <Icon name="Search" className="mx-auto h-10 w-10 text-slate-300" />
            <p className="mt-3 font-semibold text-navy-900">Документы не найдены</p>
            <p className="mt-1 text-sm text-slate-500">Измените запрос или категорию.</p>
          </div>
        )}
      </div>
    </div>
  );
}
