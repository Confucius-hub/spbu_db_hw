import Link from "next/link";
import { Icon } from "@/lib/icons";
import { cn } from "@/lib/utils";

function buildHref(base: string, params: Record<string, string | undefined>, page: number) {
  const sp = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) if (v) sp.set(k, v);
  if (page > 1) sp.set("page", String(page));
  const qs = sp.toString();
  return qs ? `${base}?${qs}` : base;
}

export function Pagination({
  page,
  totalPages,
  base = "/news",
  params = {},
}: {
  page: number;
  totalPages: number;
  base?: string;
  params?: Record<string, string | undefined>;
}) {
  if (totalPages <= 1) return null;

  const pages = Array.from({ length: totalPages }, (_, i) => i + 1).filter(
    (p) => p === 1 || p === totalPages || Math.abs(p - page) <= 1,
  );

  const items: (number | "…")[] = [];
  let prev = 0;
  for (const p of pages) {
    if (prev && p - prev > 1) items.push("…");
    items.push(p);
    prev = p;
  }

  const linkBase =
    "inline-flex h-10 min-w-10 items-center justify-center rounded-xl px-3 text-sm font-semibold transition-colors";

  return (
    <nav className="mt-12 flex items-center justify-center gap-1.5" aria-label="Пагинация">
      {page > 1 && (
        <Link
          href={buildHref(base, params, page - 1)}
          className={cn(linkBase, "border border-slate-200 text-navy-800 hover:bg-navy-50")}
          aria-label="Предыдущая страница"
        >
          <Icon name="ChevronRight" className="h-4 w-4 rotate-180" strokeWidth={2} />
        </Link>
      )}

      {items.map((it, i) =>
        it === "…" ? (
          <span key={`gap-${i}`} className="px-1 text-slate-400">
            …
          </span>
        ) : (
          <Link
            key={it}
            href={buildHref(base, params, it)}
            aria-current={it === page ? "page" : undefined}
            className={cn(
              linkBase,
              it === page
                ? "bg-navy-800 text-white"
                : "border border-slate-200 text-navy-800 hover:bg-navy-50",
            )}
          >
            {it}
          </Link>
        ),
      )}

      {page < totalPages && (
        <Link
          href={buildHref(base, params, page + 1)}
          className={cn(linkBase, "border border-slate-200 text-navy-800 hover:bg-navy-50")}
          aria-label="Следующая страница"
        >
          <Icon name="ChevronRight" className="h-4 w-4" strokeWidth={2} />
        </Link>
      )}
    </nav>
  );
}
