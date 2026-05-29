"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { mainNav, site } from "@/lib/site";
import { Logo } from "@/components/brand/logo";
import { Button } from "@/components/ui/button";
import { Icon } from "@/lib/icons";
import { CallbackButton } from "@/components/forms/callback-modal";

export function Header() {
  const pathname = usePathname();
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [lastPath, setLastPath] = useState(pathname);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Закрываем мобильное меню при смене маршрута (обновление состояния на этапе рендера —
  // рекомендованный React паттерн вместо setState внутри эффекта).
  if (pathname !== lastPath) {
    setLastPath(pathname);
    setMenuOpen(false);
  }

  useEffect(() => {
    document.body.style.overflow = menuOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [menuOpen]);

  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <header className="sticky top-0 z-50">
      {/* Верхняя информационная полоса */}
      <div className="hidden border-b border-white/10 bg-navy-950 text-slate-300 lg:block">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-8 py-2 text-[0.8rem]">
          <a
            href={site.nostroyUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 transition-colors hover:text-gold-300"
          >
            <Icon name="BadgeCheck" className="h-4 w-4 text-gold-400" />
            Реестр НОСТРОЙ: <span className="font-medium text-white">{site.registryNumber}</span>
          </a>
          <div className="flex items-center gap-6">
            <span className="inline-flex items-center gap-2">
              <Icon name="Clock" className="h-4 w-4 text-slate-400" />
              {site.workHours}
            </span>
            <a
              href={site.emailHref}
              className="inline-flex items-center gap-2 transition-colors hover:text-gold-300"
            >
              <Icon name="Mail" className="h-4 w-4 text-slate-400" />
              {site.email}
            </a>
            <a
              href={site.phoneHref}
              className="inline-flex items-center gap-2 whitespace-nowrap font-medium text-white transition-colors hover:text-gold-300 2xl:hidden"
            >
              <Icon name="Phone" className="h-4 w-4 text-gold-400" />
              {site.phone}
            </a>
          </div>
        </div>
      </div>

      {/* Основная строка */}
      <div
        className={cn(
          "border-b bg-white/90 backdrop-blur-md transition-all duration-300",
          scrolled ? "border-slate-200 shadow-soft" : "border-transparent",
        )}
      >
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-5 sm:px-6 lg:px-8">
          <div className={cn("transition-all duration-300", scrolled ? "py-2.5" : "py-3.5")}>
            <Logo />
          </div>

          <nav className="hidden items-center gap-0.5 xl:flex">
            {mainNav.map((item) =>
              item.children ? (
                <div key={item.href} className="group relative">
                  <Link
                    href={item.href}
                    aria-current={isActive(item.href) ? "page" : undefined}
                    aria-haspopup="true"
                    className={cn(
                      "relative inline-flex items-center gap-1 whitespace-nowrap rounded-lg px-3 py-2 text-[0.95rem] font-medium transition-colors",
                      isActive(item.href) ? "text-navy-900" : "text-slate-600 hover:text-navy-900",
                    )}
                  >
                    {item.label}
                    <Icon
                      name="ChevronDown"
                      className="h-3.5 w-3.5 text-slate-400 transition-transform duration-200 group-hover:rotate-180"
                    />
                    {isActive(item.href) && (
                      <span className="absolute inset-x-3.5 -bottom-0.5 h-0.5 rounded-full bg-gold-500" />
                    )}
                  </Link>

                  {/* Панель подменю (pt-3 — невидимый «мостик» для наведения) */}
                  <div className="invisible absolute left-0 top-full z-50 w-72 translate-y-1 pt-3 opacity-0 transition-all duration-200 ease-[cubic-bezier(0.22,1,0.36,1)] group-hover:visible group-hover:translate-y-0 group-hover:opacity-100 group-focus-within:visible group-focus-within:translate-y-0 group-focus-within:opacity-100">
                    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white p-2 shadow-lift">
                      {item.children.map((child) => (
                        <Link
                          key={child.href}
                          href={child.href}
                          className="group/sub flex items-start gap-3 rounded-xl px-3 py-2.5 transition-colors hover:bg-navy-50"
                        >
                          <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-gold-400 transition-transform group-hover/sub:scale-125" />
                          <span>
                            <span className="block text-sm font-semibold text-navy-900">
                              {child.label}
                            </span>
                            {child.description && (
                              <span className="block text-xs text-slate-500">{child.description}</span>
                            )}
                          </span>
                        </Link>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <Link
                  key={item.href}
                  href={item.href}
                  aria-current={isActive(item.href) ? "page" : undefined}
                  className={cn(
                    "relative whitespace-nowrap rounded-lg px-3 py-2 text-[0.95rem] font-medium transition-colors",
                    isActive(item.href) ? "text-navy-900" : "text-slate-600 hover:text-navy-900",
                  )}
                >
                  {item.label}
                  {isActive(item.href) && (
                    <span className="absolute inset-x-3.5 -bottom-0.5 h-0.5 rounded-full bg-gold-500" />
                  )}
                </Link>
              ),
            )}
          </nav>

          <div className="flex items-center gap-2 sm:gap-3">
            <a
              href={site.phoneHref}
              className="hidden items-center gap-2 whitespace-nowrap text-sm font-bold text-navy-900 transition-colors hover:text-gold-700 2xl:inline-flex"
            >
              <Icon name="Phone" className="h-4 w-4 text-gold-600" />
              {site.phone}
            </a>
            <CallbackButton className="hidden sm:inline-flex" />
            <button
              type="button"
              onClick={() => setMenuOpen((v) => !v)}
              className="inline-flex h-11 w-11 items-center justify-center rounded-xl border border-slate-200 text-navy-800 transition-colors hover:bg-navy-50 xl:hidden"
              aria-label={menuOpen ? "Закрыть меню" : "Открыть меню"}
              aria-expanded={menuOpen}
            >
              <Icon name={menuOpen ? "X" : "Menu"} className="h-5 w-5" strokeWidth={2} />
            </button>
          </div>
        </div>
      </div>

      {/* Мобильное меню */}
      <MobileMenu open={menuOpen} isActive={isActive} onClose={() => setMenuOpen(false)} />
    </header>
  );
}

function MobileMenu({
  open,
  isActive,
  onClose,
}: {
  open: boolean;
  isActive: (href: string) => boolean;
  onClose: () => void;
}) {
  const [expanded, setExpanded] = useState<string | null>(null);
  return (
    <div
      className={cn(
        "fixed inset-0 top-0 z-40 xl:hidden",
        open ? "pointer-events-auto" : "pointer-events-none",
      )}
      aria-hidden={!open}
    >
      <div
        className={cn(
          "absolute inset-0 bg-navy-950/40 backdrop-blur-sm transition-opacity duration-300",
          open ? "opacity-100" : "opacity-0",
        )}
        onClick={onClose}
      />
      <div
        className={cn(
          "absolute right-0 top-0 flex h-[100dvh] w-[min(22rem,88vw)] flex-col bg-white shadow-lift transition-transform duration-300 ease-[cubic-bezier(0.22,1,0.36,1)]",
          open ? "translate-x-0" : "translate-x-full",
        )}
      >
        <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">
          <Logo />
          <button
            type="button"
            onClick={onClose}
            className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 text-navy-800"
            aria-label="Закрыть меню"
          >
            <Icon name="X" className="h-5 w-5" strokeWidth={2} />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto px-3 py-4">
          {mainNav.map((item) =>
            item.children ? (
              <div key={item.href}>
                <button
                  type="button"
                  onClick={() => setExpanded((v) => (v === item.href ? null : item.href))}
                  aria-expanded={expanded === item.href}
                  className={cn(
                    "flex w-full items-center justify-between rounded-xl px-4 py-3.5 text-left text-base font-medium transition-colors",
                    isActive(item.href) ? "bg-navy-50 text-navy-900" : "text-slate-700 hover:bg-slate-50",
                  )}
                >
                  <span>{item.label}</span>
                  <Icon
                    name="ChevronDown"
                    className={cn(
                      "h-4 w-4 text-slate-400 transition-transform duration-200",
                      expanded === item.href && "rotate-180",
                    )}
                  />
                </button>
                <div
                  className={cn(
                    "grid transition-all duration-300 ease-[cubic-bezier(0.22,1,0.36,1)]",
                    expanded === item.href ? "grid-rows-[1fr] opacity-100" : "grid-rows-[0fr] opacity-0",
                  )}
                >
                  <div className="overflow-hidden">
                    <div className="ml-4 border-l border-slate-100 py-1 pl-3">
                      {item.children.map((child) => (
                        <Link
                          key={child.href}
                          href={child.href}
                          onClick={onClose}
                          className="block rounded-lg px-3 py-2.5 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-50 hover:text-navy-900"
                        >
                          {child.label}
                        </Link>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <Link
                key={item.href}
                href={item.href}
                onClick={onClose}
                aria-current={isActive(item.href) ? "page" : undefined}
                className={cn(
                  "flex items-center justify-between rounded-xl px-4 py-3.5 text-base font-medium transition-colors",
                  isActive(item.href) ? "bg-navy-50 text-navy-900" : "text-slate-700 hover:bg-slate-50",
                )}
              >
                <span>{item.label}</span>
                <Icon name="ChevronRight" className="h-4 w-4 text-slate-300" />
              </Link>
            ),
          )}
        </nav>

        <div className="space-y-3 border-t border-slate-100 p-5">
          <a
            href={site.phoneHref}
            className="flex items-center gap-3 text-lg font-bold text-navy-900"
          >
            <Icon name="Phone" className="h-5 w-5 text-gold-600" />
            {site.phone}
          </a>
          <Button href="/membership" variant="gold" className="w-full" size="lg">
            Рассчитать стоимость
          </Button>
          <p className="text-center text-xs text-slate-400">{site.workHours}</p>
        </div>
      </div>
    </div>
  );
}
