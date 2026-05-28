"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Icon } from "@/lib/icons";
import { cn } from "@/lib/utils";

type Category = { slug: string; title: string };

export function NewsFilters({
  categories,
  activeCategory,
  query,
}: {
  categories: Category[];
  activeCategory?: string;
  query?: string;
}) {
  const router = useRouter();
  const [value, setValue] = useState(query ?? "");

  function submit(e: React.FormEvent) {
    e.preventDefault();
    const sp = new URLSearchParams();
    if (value.trim()) sp.set("q", value.trim());
    if (activeCategory) sp.set("category", activeCategory);
    const qs = sp.toString();
    router.push(qs ? `/news?${qs}` : "/news");
  }

  const chip = (active: boolean) =>
    cn(
      "inline-flex items-center rounded-full px-4 py-2 text-sm font-medium transition-colors",
      active
        ? "bg-navy-800 text-white"
        : "bg-white text-slate-600 ring-1 ring-slate-200 hover:ring-gold-300 hover:text-navy-900",
    );

  const withQuery = (category?: string) => {
    const sp = new URLSearchParams();
    if (category) sp.set("category", category);
    if (query) sp.set("q", query);
    const qs = sp.toString();
    return qs ? `/news?${qs}` : "/news";
  };

  return (
    <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
      <div className="flex flex-wrap gap-2">
        <Link href={withQuery(undefined)} className={chip(!activeCategory)}>
          Все
        </Link>
        {categories.map((c) => (
          <Link key={c.slug} href={withQuery(c.slug)} className={chip(activeCategory === c.slug)}>
            {c.title}
          </Link>
        ))}
      </div>

      <form onSubmit={submit} className="relative w-full lg:w-72">
        <Icon
          name="Search"
          className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
        />
        <input
          type="search"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Поиск по новостям"
          className="w-full rounded-xl border border-slate-200 bg-white py-2.5 pl-10 pr-4 text-sm text-navy-900 placeholder:text-slate-400 transition-colors focus:border-gold-400 focus:outline-none focus:ring-2 focus:ring-gold-200"
        />
      </form>
    </div>
  );
}
