"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LogoMark } from "@/components/brand/logo";
import { LogoutButton } from "@/components/admin/logout-button";
import { Icon, type IconName } from "@/lib/icons";
import { cn } from "@/lib/utils";

const nav: { href: string; label: string; icon: IconName }[] = [
  { href: "/admin", label: "Дашборд", icon: "LayoutDashboard" },
  { href: "/admin/news", label: "Новости", icon: "Newspaper" },
];

export function AdminShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isActive = (href: string) =>
    href === "/admin" ? pathname === "/admin" : pathname.startsWith(href);

  return (
    <div className="min-h-screen bg-slate-50 lg:grid lg:grid-cols-[16rem_1fr]">
      {/* Сайдбар */}
      <aside className="flex flex-col gap-1 bg-navy-950 p-4 text-white lg:min-h-screen">
        <div className="flex items-center gap-3 px-2 py-3">
          <LogoMark className="h-9 w-9" />
          <div className="leading-tight">
            <p className="text-sm font-bold text-white">СССС</p>
            <p className="text-xs text-slate-400">Админ-панель</p>
          </div>
        </div>

        <nav className="mt-4 flex gap-1 lg:flex-col">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "inline-flex items-center gap-2.5 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors",
                isActive(item.href)
                  ? "bg-white/10 text-white"
                  : "text-slate-300 hover:bg-white/5 hover:text-white",
              )}
            >
              <Icon name={item.icon} className="h-5 w-5" />
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="mt-auto hidden flex-col gap-1 border-t border-white/10 pt-3 lg:flex">
          <Link
            href="/"
            target="_blank"
            className="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-slate-300 transition-colors hover:bg-white/10 hover:text-white"
          >
            <Icon name="ExternalLink" className="h-4 w-4" />
            Открыть сайт
          </Link>
          <LogoutButton />
        </div>
      </aside>

      {/* Контент */}
      <div className="flex flex-col">
        <header className="flex items-center justify-between border-b border-slate-200 bg-white px-5 py-3 lg:hidden">
          <span className="font-semibold text-navy-900">Админ-панель</span>
          <LogoutButton />
        </header>
        <main className="flex-1 p-5 sm:p-8">{children}</main>
      </div>
    </div>
  );
}
