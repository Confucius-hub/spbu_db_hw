"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { Icon } from "@/lib/icons";
import { cn } from "@/lib/utils";
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
  const [query, setQuery] = useState("");
  const q = query.trim().toLowerCase();

  const filtered = useMemo(
    () => documents.filter((d) => !q || d.title.toLowerCase().includes(q)),
    [documents, q],
  );

  const byCategory = useMemo(() => {
    const map = new Map<string, DocItem[]>();
    for (const cat of categories) map.set(cat, []);
    for (const d of filtered) {
      if (!map.has(d.category)) map.set(d.category, []);
      map.get(d.category)!.push(d);
    }
    return map;
  }, [filtered, categories]);

  return (
    <div>
      {/* Поиск */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h2 className="text-2xl font-bold text-navy-900 sm:text-3xl">Реестр документов</h2>
        <div className="relative w-full sm:w-80">
          <Icon
            name="Search"
            className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
          />
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Поиск по названию"
            className="w-full rounded-xl border border-slate-200 bg-white py-2.5 pl-10 pr-4 text-sm text-navy-900 placeholder:text-slate-400 focus:border-gold-400 focus:outline-none focus:ring-2 focus:ring-gold-200"
          />
        </div>
      </div>

      {/* Секции по категориям */}
      <div className="mt-10 space-y-10">
        {categories.map((cat) => {
          const items = byCategory.get(cat) ?? [];
          if (items.length === 0) return null;
          return (
            <section key={cat}>
              <h3 className="mb-4 inline-flex items-center gap-3 text-sm font-semibold uppercase tracking-[0.14em] text-gold-700">
                <span className="h-px w-6 bg-gold-400/70" />
                {cat}
                <span className="text-xs font-normal normal-case tracking-normal text-slate-400">
                  · {items.length}
                </span>
              </h3>
              <div className="divide-y divide-slate-100 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-soft">
                {items.map((d, i) => (
                  <DocumentRow key={i} doc={d} />
                ))}
              </div>
            </section>
          );
        })}
      </div>

      {filtered.length === 0 && (
        <div className="mt-10 rounded-2xl border border-dashed border-slate-300 bg-white py-14 text-center">
          <Icon name="Search" className="mx-auto h-10 w-10 text-slate-300" />
          <p className="mt-3 font-semibold text-navy-900">Документы не найдены</p>
          <p className="mt-1 text-sm text-slate-500">Попробуйте изменить запрос.</p>
        </div>
      )}
    </div>
  );
}

function DocumentRow({ doc }: { doc: DocItem }) {
  const available = !!doc.href;

  const content = (
    <>
      <span
        className={cn(
          "inline-flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-xs font-bold ring-1",
          formatColors[doc.format],
        )}
      >
        {doc.format}
      </span>
      <div className="min-w-0 flex-1">
        <p className="font-medium text-navy-900 group-hover:text-navy-700">{doc.title}</p>
        {doc.note && <p className="mt-0.5 text-xs text-slate-500">{doc.note}</p>}
      </div>
      {available ? (
        <span className="inline-flex shrink-0 items-center gap-1.5 text-sm font-semibold text-navy-700 transition-colors group-hover:text-gold-700">
          Скачать
          <Icon name="Download" className="h-4 w-4" />
        </span>
      ) : (
        <span className="inline-flex shrink-0 items-center gap-1.5 rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-500 transition-colors group-hover:bg-gold-100 group-hover:text-gold-800">
          <Icon name="Clock" className="h-3.5 w-3.5" />
          <span className="group-hover:hidden">Готовится</span>
          <span className="hidden group-hover:inline">Запросить</span>
        </span>
      )}
    </>
  );

  if (available) {
    return (
      <a
        href={doc.href!}
        target="_blank"
        rel="noopener"
        className="group flex items-center gap-4 px-5 py-4 transition-colors hover:bg-gold-50/40"
      >
        {content}
      </a>
    );
  }

  // Документа ещё нет в свободном доступе — строка ведёт на запрос актуальной версии
  return (
    <Link
      href="/contacts"
      title={`Запросить документ: ${doc.title}`}
      className="group flex items-center gap-4 px-5 py-4 transition-colors hover:bg-gold-50/40"
    >
      {content}
    </Link>
  );
}
