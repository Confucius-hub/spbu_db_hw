import Link from "next/link";
import { Icon } from "@/lib/icons";
import { site } from "@/lib/site";
import { cn } from "@/lib/utils";

export type Crumb = { label: string; href?: string };

/** Хлебные крошки + JSON-LD BreadcrumbList для SEO. */
export function Breadcrumbs({
  items,
  tone = "light",
}: {
  items: Crumb[];
  tone?: "light" | "dark";
}) {
  const all: Crumb[] = [{ label: "Главная", href: "/" }, ...items];

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: all.map((c, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: c.label,
      ...(c.href ? { item: `${site.url}${c.href}` } : {}),
    })),
  };

  const linkCls =
    tone === "dark"
      ? "text-slate-300 transition-colors hover:text-gold-300"
      : "text-slate-500 transition-colors hover:text-gold-700";
  const currentCls = tone === "dark" ? "font-medium text-white" : "font-medium text-navy-800";
  const sepCls = tone === "dark" ? "text-slate-500" : "text-slate-300";

  return (
    <nav aria-label="Хлебные крошки">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <ol className="flex flex-wrap items-center gap-1.5 text-sm">
        {all.map((c, i) => {
          const last = i === all.length - 1;
          return (
            <li key={i} className="flex items-center gap-1.5">
              {c.href && !last ? (
                <Link href={c.href} className={linkCls}>
                  {c.label}
                </Link>
              ) : (
                <span className={cn(last ? currentCls : linkCls)}>{c.label}</span>
              )}
              {!last && <Icon name="ChevronRight" className={cn("h-3.5 w-3.5", sepCls)} />}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
