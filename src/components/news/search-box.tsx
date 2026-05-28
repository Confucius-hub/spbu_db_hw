"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Icon } from "@/lib/icons";

/** Поле поиска по новостям — переходит на /news?q=… */
export function SearchBox({ initial }: { initial?: string }) {
  const router = useRouter();
  const [value, setValue] = useState(initial ?? "");

  function submit(e: React.FormEvent) {
    e.preventDefault();
    const q = value.trim();
    router.push(q ? `/news?q=${encodeURIComponent(q)}` : "/news");
  }

  return (
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
  );
}
