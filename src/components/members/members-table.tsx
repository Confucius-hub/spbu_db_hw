"use client";

import { useMemo, useState } from "react";
import { Icon } from "@/lib/icons";
import { cn, formatCurrency } from "@/lib/utils";
import type { MemberItem } from "@/lib/members-registry";

type Filter = "all" | "ul" | "ip";

export function MembersTable({ members }: { members: MemberItem[] }) {
  const [q, setQ] = useState("");
  const [filter, setFilter] = useState<Filter>("all");

  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase();
    return members.filter((m) => {
      if (filter === "ul" && m.type !== "ЮЛ") return false;
      if (filter === "ip" && m.type !== "ИП") return false;
      if (!needle) return true;
      return (
        m.name.toLowerCase().includes(needle) ||
        m.reg.includes(needle) ||
        m.inn.includes(needle) ||
        m.ogrn.includes(needle)
      );
    });
  }, [members, q, filter]);

  const chip = (active: boolean) =>
    cn(
      "inline-flex items-center rounded-full px-3.5 py-1.5 text-sm font-medium transition-colors",
      active
        ? "bg-navy-800 text-white"
        : "bg-white text-slate-600 ring-1 ring-slate-200 hover:ring-gold-300 hover:text-navy-900",
    );

  return (
    <div>
      {/* Тулбар: поиск + фильтр-чипы + экспорт */}
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex flex-wrap gap-2">
          <button onClick={() => setFilter("all")} className={chip(filter === "all")}>
            Все <span className="ml-1.5 text-xs opacity-70">{members.length}</span>
          </button>
          <button onClick={() => setFilter("ul")} className={chip(filter === "ul")}>
            Юр. лица
          </button>
          <button onClick={() => setFilter("ip")} className={chip(filter === "ip")}>
            ИП
          </button>
        </div>
        <div className="flex items-center gap-2">
          <div className="relative w-full sm:w-72">
            <Icon
              name="Search"
              className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
            />
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Поиск: ИНН, ОГРН, № или название"
              className="w-full rounded-xl border border-slate-200 bg-white py-2.5 pl-10 pr-4 text-sm text-navy-900 placeholder:text-slate-400 focus:border-gold-400 focus:outline-none focus:ring-2 focus:ring-gold-200"
            />
          </div>
          <a
            href="/api/members/csv"
            className="inline-flex h-10 shrink-0 items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-3.5 text-sm font-semibold text-navy-700 transition-colors hover:border-gold-300 hover:bg-gold-50"
            title="Скачать реестр (CSV)"
          >
            <Icon name="Download" className="h-4 w-4" />
            CSV
          </a>
        </div>
      </div>

      <p className="mt-4 text-sm text-slate-500">
        Показано: <span className="font-semibold text-navy-900">{filtered.length}</span> из {members.length}
      </p>

      {/* Десктоп: таблица */}
      <div className="mt-6 hidden overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-soft md:block">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-slate-50/80 text-left text-[0.65rem] font-semibold uppercase tracking-wider text-slate-500">
              <tr>
                <th className="px-5 py-3 font-semibold">Наименование</th>
                <th className="px-3 py-3 font-semibold">Статус</th>
                <th className="px-3 py-3 font-semibold">№</th>
                <th className="px-3 py-3 font-semibold">Дата</th>
                <th className="px-3 py-3 font-semibold">ОГРН/ОГРНИП</th>
                <th className="px-3 py-3 font-semibold">ИНН</th>
                <th className="px-3 py-3 text-right font-semibold">КФ ВВ</th>
                <th className="px-5 py-3 font-semibold">Лимит работ</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filtered.map((m, i) => (
                <tr key={i} className="transition-colors hover:bg-gold-50/40">
                  <td className="max-w-xs px-5 py-3.5 font-medium text-navy-900">
                    <span className="block">{m.name}</span>
                    <span className="mt-0.5 inline-block rounded bg-slate-100 px-1.5 py-0.5 text-[0.65rem] font-semibold text-slate-500">
                      {m.type}
                    </span>
                  </td>
                  <td className="px-3 py-3.5">
                    <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700 ring-1 ring-emerald-100">
                      <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                      {m.status}
                    </span>
                  </td>
                  <td className="px-3 py-3.5 font-mono text-slate-700">{m.reg}</td>
                  <td className="px-3 py-3.5 text-slate-600">{m.date}</td>
                  <td className="px-3 py-3.5 font-mono text-xs text-slate-700">{m.ogrn}</td>
                  <td className="px-3 py-3.5 font-mono text-xs text-slate-700">{m.inn}</td>
                  <td className="px-3 py-3.5 text-right font-semibold text-navy-900">
                    {formatCurrency(m.kfVv)}
                  </td>
                  <td className="max-w-[14rem] px-5 py-3.5 text-slate-600">{m.maxContract}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Мобильный: карточки */}
      <div className="mt-6 grid gap-3 md:hidden">
        {filtered.map((m, i) => (
          <article
            key={i}
            className="rounded-2xl border border-slate-200 bg-white p-4 shadow-soft"
          >
            <div className="flex items-start justify-between gap-3">
              <p className="flex-1 font-semibold text-navy-900">{m.name}</p>
              <span className="rounded bg-slate-100 px-2 py-0.5 text-[0.65rem] font-semibold text-slate-500">
                {m.type}
              </span>
            </div>
            <span className="mt-2 inline-flex items-center gap-1.5 rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700 ring-1 ring-emerald-100">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
              {m.status}
            </span>
            <dl className="mt-3 grid grid-cols-2 gap-x-4 gap-y-2 text-xs">
              <div>
                <dt className="text-slate-400">№ в реестре</dt>
                <dd className="font-mono font-medium text-slate-700">{m.reg}</dd>
              </div>
              <div>
                <dt className="text-slate-400">Дата</dt>
                <dd className="text-slate-700">{m.date}</dd>
              </div>
              <div>
                <dt className="text-slate-400">ИНН</dt>
                <dd className="font-mono text-slate-700">{m.inn}</dd>
              </div>
              <div>
                <dt className="text-slate-400">ОГРН/ОГРНИП</dt>
                <dd className="font-mono text-slate-700">{m.ogrn}</dd>
              </div>
              <div className="col-span-2 border-t border-slate-100 pt-2">
                <dt className="text-slate-400">КФ возмещения вреда</dt>
                <dd className="font-semibold text-navy-900">{formatCurrency(m.kfVv)}</dd>
              </div>
              <div className="col-span-2">
                <dt className="text-slate-400">Лимит работ</dt>
                <dd className="text-slate-600">{m.maxContract}</dd>
              </div>
            </dl>
          </article>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="mt-6 rounded-2xl border border-dashed border-slate-300 bg-white py-12 text-center">
          <Icon name="Search" className="mx-auto h-10 w-10 text-slate-300" />
          <p className="mt-3 font-semibold text-navy-900">Ничего не найдено</p>
          <p className="mt-1 text-sm text-slate-500">Попробуйте изменить запрос или фильтр.</p>
        </div>
      )}
    </div>
  );
}
