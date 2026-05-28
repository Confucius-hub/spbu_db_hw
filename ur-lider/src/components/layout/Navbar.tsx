"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Phone, Menu, X, ChevronDown, Clock } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Logo } from "./Logo";
import { nav, site } from "@/lib/site";
import { cn } from "@/lib/utils";

export function Navbar() {
  const pathname = usePathname();
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const [openGroup, setOpenGroup] = useState<string | null>(null);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Lock body scroll while the mobile sheet is open.
  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  const closeMenu = () => setOpen(false);

  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <header className="sticky top-0 z-50">
      {/* Utility bar */}
      <div className="hidden border-b border-line/70 bg-paper/80 backdrop-blur lg:block">
        <Container className="flex h-10 items-center justify-between text-[13px] text-muted">
          <span className="inline-flex items-center gap-2">
            <Clock className="h-3.5 w-3.5 text-accent" aria-hidden />
            {site.workingHours}
          </span>
          <span className="inline-flex items-center gap-5">
            <span>{site.address}</span>
            <a href={`mailto:${site.email}`} className="hover:text-ink">
              {site.email}
            </a>
          </span>
        </Container>
      </div>

      {/* Main bar */}
      <div
        className={cn(
          "border-b transition-colors duration-300",
          scrolled || open
            ? "border-line bg-paper/90 backdrop-blur-md"
            : "border-transparent bg-paper/60 backdrop-blur",
        )}
      >
        <Container className="flex h-16 items-center justify-between gap-4 lg:h-18">
          <Logo />

          {/* Desktop nav */}
          <nav className="hidden items-center gap-1 lg:flex">
            {nav.map((item) =>
              item.children ? (
                <div key={item.href} className="group relative">
                  <Link
                    href={item.href}
                    className={cn(
                      "inline-flex items-center gap-1 rounded-full px-3.5 py-2 text-[15px] font-medium transition-colors",
                      isActive(item.href)
                        ? "text-ink"
                        : "text-graphite hover:text-ink",
                    )}
                  >
                    {item.label}
                    <ChevronDown
                      className="h-4 w-4 text-faint transition-transform duration-200 group-hover:rotate-180"
                      aria-hidden
                    />
                  </Link>
                  {/* Mega-menu */}
                  <div className="invisible absolute left-1/2 top-full w-[min(620px,90vw)] -translate-x-1/2 pt-3 opacity-0 transition-all duration-200 group-focus-within:visible group-focus-within:opacity-100 group-hover:visible group-hover:opacity-100">
                    <div className="grid grid-cols-2 gap-1 rounded-2xl border border-line bg-white p-2.5 shadow-[var(--shadow-lift)]">
                      {item.children.map((child) => (
                        <Link
                          key={child.href}
                          href={child.href}
                          className="rounded-xl px-3.5 py-3 transition-colors hover:bg-paper"
                        >
                          <span className="block text-[15px] font-semibold text-ink">
                            {child.label}
                          </span>
                          {child.description && (
                            <span className="mt-0.5 block text-[13px] leading-snug text-muted">
                              {child.description}
                            </span>
                          )}
                        </Link>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "rounded-full px-3.5 py-2 text-[15px] font-medium transition-colors",
                    isActive(item.href)
                      ? "text-ink"
                      : "text-graphite hover:text-ink",
                  )}
                >
                  {item.label}
                </Link>
              ),
            )}
          </nav>

          {/* Right actions */}
          <div className="flex items-center gap-2">
            <a
              href={`tel:${site.phoneHref}`}
              className="hidden items-center gap-2 text-[15px] font-semibold text-ink xl:inline-flex"
            >
              <Phone className="h-4 w-4 text-accent" aria-hidden />
              {site.phone}
            </a>
            <Button href="/contacts" variant="accent" className="hidden sm:inline-flex">
              Консультация
            </Button>
            <button
              type="button"
              onClick={() => setOpen((v) => !v)}
              aria-label={open ? "Закрыть меню" : "Открыть меню"}
              aria-expanded={open}
              className="grid h-11 w-11 place-items-center rounded-full border border-line-strong text-ink transition-colors hover:bg-white lg:hidden"
            >
              {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </Container>
      </div>

      {/* Mobile sheet */}
      {open && (
        <div className="fixed inset-x-0 bottom-0 top-16 z-40 overflow-y-auto bg-paper lg:hidden">
          <Container className="flex flex-col gap-1 py-6">
            {nav.map((item) => (
              <div key={item.href} className="border-b border-line/70 py-1">
                {item.children ? (
                  <MobileGroup
                    item={item}
                    open={openGroup === item.href}
                    onToggle={() =>
                      setOpenGroup((g) => (g === item.href ? null : item.href))
                    }
                    onNavigate={closeMenu}
                  />
                ) : (
                  <Link
                    href={item.href}
                    onClick={closeMenu}
                    className="block py-3 text-lg font-semibold text-ink"
                  >
                    {item.label}
                  </Link>
                )}
              </div>
            ))}

            <div className="mt-6 flex flex-col gap-3">
              <Button href="/contacts" onClick={closeMenu} variant="accent" size="lg">
                Записаться на консультацию
              </Button>
              <a
                href={`tel:${site.phoneHref}`}
                className="inline-flex h-12 items-center justify-center gap-2 rounded-full border border-line-strong text-[15px] font-semibold text-ink"
              >
                <Phone className="h-4 w-4 text-accent" aria-hidden />
                {site.phone}
              </a>
            </div>
          </Container>
        </div>
      )}
    </header>
  );
}

function MobileGroup({
  item,
  open,
  onToggle,
  onNavigate,
}: {
  item: (typeof nav)[number];
  open: boolean;
  onToggle: () => void;
  onNavigate: () => void;
}) {
  return (
    <div>
      <div className="flex items-center justify-between">
        <Link
          href={item.href}
          onClick={onNavigate}
          className="py-3 text-lg font-semibold text-ink"
        >
          {item.label}
        </Link>
        <button
          type="button"
          onClick={onToggle}
          aria-label={open ? "Свернуть" : "Развернуть"}
          aria-expanded={open}
          className="grid h-9 w-9 place-items-center rounded-full text-faint"
        >
          <ChevronDown
            className={cn("h-5 w-5 transition-transform", open && "rotate-180")}
          />
        </button>
      </div>
      {open && item.children && (
        <ul className="mb-2 ml-1 flex flex-col gap-1 border-l border-line pl-4">
          {item.children.map((child) => (
            <li key={child.href}>
              <Link
                href={child.href}
                onClick={onNavigate}
                className="block py-2 text-[15px] text-graphite"
              >
                {child.label}
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
