import Link from "next/link";
import { Container } from "@/components/ui/container";

export type TocItem = { label: string; href: string };

/**
 * Якорная навигация по странице. Горизонтальные «чипы» под шапкой страницы,
 * плавный скролл к разделам. На мобильных переносится в несколько строк.
 */
export function PageToc({
  items,
  title = "На этой странице",
}: {
  items: TocItem[];
  title?: string;
}) {
  if (items.length === 0) return null;
  return (
    <nav aria-label={title} className="border-b border-slate-200 bg-white">
      <Container>
        <div className="flex flex-col gap-3 py-4 lg:flex-row lg:items-center lg:gap-6">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            {title}
          </span>
          <ul className="-mx-1 flex flex-wrap gap-2 overflow-x-auto px-1">
            {items.map((it) => (
              <li key={it.href}>
                <Link
                  href={it.href}
                  className="inline-flex shrink-0 items-center rounded-full bg-slate-100 px-3.5 py-1.5 text-sm font-medium text-slate-700 transition-colors hover:bg-gold-100 hover:text-gold-800"
                >
                  {it.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </Container>
    </nav>
  );
}
