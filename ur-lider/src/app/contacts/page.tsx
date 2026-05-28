import type { Metadata } from "next";
import { Phone, Mail, MapPin, Clock } from "lucide-react";
import { PageHeader } from "@/components/ui/PageHeader";
import { Section } from "@/components/ui/Section";
import { ContactForm } from "@/components/sections/ContactForm";
import { site } from "@/lib/site";

export const metadata: Metadata = {
  title: "Контакты",
  description:
    "Свяжитесь с юридической компанией «Лидер»: телефон, email, адрес офиса в Москве. Запишитесь на бесплатную консультацию.",
};

const contactItems = [
  { icon: Phone, label: "Телефон", value: site.phone, href: `tel:${site.phoneHref}` },
  { icon: Mail, label: "Email", value: site.email, href: `mailto:${site.email}` },
  { icon: MapPin, label: "Офис", value: site.address },
  { icon: Clock, label: "Часы работы", value: site.workingHours },
];

export default function ContactsPage() {
  return (
    <>
      <PageHeader
        eyebrow="Контакты"
        title="Получите расчёт стоимости допуска СРО"
        subtitle="Опишите задачу — специалист по СРО свяжется с вами в течение 30 минут в рабочее время. Консультация бесплатна."
        crumbs={[{ label: "Главная", href: "/" }, { label: "Контакты" }]}
      />

      <Section tone="paper">
        <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:gap-14">
          {/* Contact info */}
          <div>
            <div className="grid gap-4 sm:grid-cols-2">
              {contactItems.map((c) => {
                const body = (
                  <div className="flex h-full flex-col rounded-2xl border border-line bg-white p-6">
                    <span className="grid h-11 w-11 place-items-center rounded-xl bg-accent-soft text-accent-strong">
                      <c.icon className="h-5 w-5" strokeWidth={1.7} aria-hidden />
                    </span>
                    <span className="mt-4 text-[13px] font-medium uppercase tracking-wider text-faint">
                      {c.label}
                    </span>
                    <span className="mt-1 text-[15px] font-semibold text-ink">
                      {c.value}
                    </span>
                  </div>
                );
                return c.href ? (
                  <a key={c.label} href={c.href} className="transition-transform hover:-translate-y-0.5">
                    {body}
                  </a>
                ) : (
                  <div key={c.label}>{body}</div>
                );
              })}
            </div>

            {/* Map placeholder */}
            <div className="mt-4 overflow-hidden rounded-2xl border border-line bg-paper-2">
              <div className="relative grid h-64 place-items-center bg-grid-dark/0">
                <div
                  aria-hidden
                  className="absolute inset-0 opacity-[0.5]"
                  style={{
                    backgroundImage:
                      "linear-gradient(to right, rgba(15,28,36,0.06) 1px, transparent 1px), linear-gradient(to bottom, rgba(15,28,36,0.06) 1px, transparent 1px)",
                    backgroundSize: "32px 32px",
                  }}
                />
                <div className="relative flex flex-col items-center text-center">
                  <MapPin className="h-8 w-8 text-accent" aria-hidden />
                  <span className="mt-2 max-w-xs text-sm text-muted">
                    {site.address}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Form */}
          <div className="rounded-2xl border border-line bg-white p-7 shadow-[var(--shadow-card)] sm:p-9">
            <h2 className="text-2xl text-ink">Оставить заявку</h2>
            <p className="mt-2 text-[15px] text-muted">
              Поля со звёздочкой обязательны. Остальное поможет нам подготовиться
              к разговору.
            </p>
            <div className="mt-7">
              <ContactForm variant="full" />
            </div>
          </div>
        </div>
      </Section>
    </>
  );
}
