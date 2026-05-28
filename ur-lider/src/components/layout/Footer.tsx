import Link from "next/link";
import { Phone, Mail, MapPin } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Logo } from "./Logo";
import { nav, site } from "@/lib/site";
import { practices } from "@/lib/practices";

export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="bg-ink text-white/70">
      <Container className="py-16 lg:py-20">
        <div className="grid gap-12 lg:grid-cols-[1.4fr_1fr_1fr_1.1fr]">
          <div>
            <Logo tone="onDark" />
            <p className="mt-5 max-w-xs text-[15px] leading-relaxed text-white/55">
              {site.description}
            </p>
          </div>

          <FooterCol title="Практики">
            {practices.map((p) => (
              <FooterLink key={p.slug} href={`/practices/${p.slug}`}>
                {p.title}
              </FooterLink>
            ))}
          </FooterCol>

          <FooterCol title="Компания">
            {nav
              .filter((n) => n.href !== "/practices")
              .map((n) => (
                <FooterLink key={n.href} href={n.href}>
                  {n.label}
                </FooterLink>
              ))}
          </FooterCol>

          <FooterCol title="Контакты">
            <a
              href={`tel:${site.phoneHref}`}
              className="flex items-center gap-2.5 py-1.5 text-white transition-colors hover:text-accent"
            >
              <Phone className="h-4 w-4 text-accent" aria-hidden />
              {site.phone}
            </a>
            <a
              href={`mailto:${site.email}`}
              className="flex items-center gap-2.5 py-1.5 transition-colors hover:text-white"
            >
              <Mail className="h-4 w-4 text-accent" aria-hidden />
              {site.email}
            </a>
            <span className="flex items-start gap-2.5 py-1.5 text-[15px] leading-snug">
              <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-accent" aria-hidden />
              {site.address}
            </span>
          </FooterCol>
        </div>

        <div className="mt-14 flex flex-col gap-3 border-t border-white/10 pt-7 text-[13px] text-white/45 sm:flex-row sm:items-center sm:justify-between">
          <span>
            © {year} {site.legalName}. ИНН {site.inn}.
          </span>
          <div className="flex flex-wrap gap-x-6 gap-y-2">
            <Link href="/privacy" className="hover:text-white/80">
              Политика конфиденциальности
            </Link>
            <Link href="/contacts" className="hover:text-white/80">
              Согласие на обработку данных
            </Link>
          </div>
        </div>
      </Container>
    </footer>
  );
}

function FooterCol({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <h4 className="font-sans text-[13px] font-semibold uppercase tracking-[0.16em] text-white/40">
        {title}
      </h4>
      <div className="mt-4 flex flex-col">{children}</div>
    </div>
  );
}

function FooterLink({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) {
  return (
    <Link
      href={href}
      className="py-1.5 text-[15px] text-white/65 transition-colors hover:text-white"
    >
      {children}
    </Link>
  );
}
