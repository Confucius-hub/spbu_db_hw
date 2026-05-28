import Link from "next/link";
import { footerNav, site } from "@/lib/site";
import { Logo } from "@/components/brand/logo";
import { Icon } from "@/lib/icons";

export function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="bg-navy-950 text-slate-300">
      <div className="mx-auto max-w-7xl px-5 sm:px-6 lg:px-8">
        {/* Верхняя CTA-полоса */}
        <div className="flex flex-col gap-5 border-b border-white/10 py-10 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white">Готовы вступить в СРО?</h2>
            <p className="mt-1 text-slate-400">
              Рассчитайте стоимость или получите бесплатную консультацию.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/membership#calculator"
              className="inline-flex h-12 items-center gap-2 rounded-xl bg-gold-500 px-6 font-semibold text-navy-950 transition-colors hover:bg-gold-400"
            >
              <Icon name="Calculator" className="h-5 w-5" />
              Рассчитать стоимость
            </Link>
            <a
              href={site.phoneHref}
              className="inline-flex h-12 items-center gap-2 rounded-xl border border-white/20 px-6 font-semibold text-white transition-colors hover:bg-white/10"
            >
              <Icon name="Phone" className="h-5 w-5 text-gold-400" />
              {site.phone}
            </a>
          </div>
        </div>

        {/* Основная сетка */}
        <div className="grid gap-10 py-12 md:grid-cols-2 lg:grid-cols-12">
          <div className="lg:col-span-4">
            <Logo variant="light" />
            <p className="mt-4 max-w-sm text-sm leading-relaxed text-slate-400">
              {site.legalName}. Допуск к строительным работам, внесение специалистов в НРС и
              сопровождение членов СРО с {site.founded} года.
            </p>
            <div className="mt-5 inline-flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-3.5 py-2.5 text-xs">
              <Icon name="BadgeCheck" className="h-5 w-5 text-gold-400" />
              <span>
                Реестр НОСТРОЙ
                <span className="ml-1 font-semibold text-white">{site.registryNumber}</span>
                <span className="block text-slate-500">от {site.registryDate}</span>
              </span>
            </div>
          </div>

          {footerNav.map((col) => (
            <div key={col.title} className="lg:col-span-2">
              <h3 className="text-sm font-semibold uppercase tracking-wider text-white">
                {col.title}
              </h3>
              <ul className="mt-4 space-y-2.5">
                {col.items.map((item) => (
                  <li key={item.href + item.label}>
                    <Link
                      href={item.href}
                      className="text-sm text-slate-400 transition-colors hover:text-gold-300"
                    >
                      {item.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}

          <div className="lg:col-span-2">
            <h3 className="text-sm font-semibold uppercase tracking-wider text-white">Контакты</h3>
            <ul className="mt-4 space-y-3 text-sm text-slate-400">
              <li>
                <a href={site.phoneHref} className="inline-flex items-center gap-2 hover:text-gold-300">
                  <Icon name="Phone" className="h-4 w-4 text-gold-400" />
                  {site.phone}
                </a>
              </li>
              <li>
                <a href={site.emailHref} className="inline-flex items-center gap-2 hover:text-gold-300">
                  <Icon name="Mail" className="h-4 w-4 text-gold-400" />
                  {site.email}
                </a>
              </li>
              <li className="flex items-start gap-2">
                <Icon name="MapPin" className="mt-0.5 h-4 w-4 shrink-0 text-gold-400" />
                {site.address}
              </li>
              <li className="flex items-start gap-2">
                <Icon name="Clock" className="mt-0.5 h-4 w-4 shrink-0 text-gold-400" />
                {site.workHours}
              </li>
            </ul>
          </div>
        </div>

        {/* Нижняя полоса */}
        <div className="flex flex-col gap-3 border-t border-white/10 py-6 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between">
          <p>
            © {site.founded}—{year} {site.legalName}. Все права защищены.
          </p>
          <div className="flex flex-wrap items-center gap-x-5 gap-y-2">
            <Link href="/privacy" className="transition-colors hover:text-gold-300">
              Политика конфиденциальности
            </Link>
            <Link href="/documents" className="transition-colors hover:text-gold-300">
              Документы
            </Link>
            <Link href="/sitemap.xml" className="transition-colors hover:text-gold-300">
              Карта сайта
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
