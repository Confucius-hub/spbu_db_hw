import type { Metadata } from "next";
import { Section, SectionHeading } from "@/components/ui/section";
import { PageHeader } from "@/components/layout/page-header";
import { Card } from "@/components/ui/card";
import { LeadForm } from "@/components/forms/lead-form";
import { Icon, type IconName } from "@/lib/icons";
import { site } from "@/lib/site";
import { pageMetadata } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "Контакты",
  description:
    "Контакты СРО «Строительный союз Северной столицы»: телефон, e-mail, адрес офиса в Санкт-Петербурге и форма обратной связи.",
  path: "/contacts",
});

const contacts: { icon: IconName; label: string; value: string; href?: string }[] = [
  { icon: "Phone", label: "Телефон", value: site.phone, href: site.phoneHref },
  { icon: "Mail", label: "E-mail", value: site.email, href: site.emailHref },
  { icon: "MapPin", label: "Адрес", value: site.address },
  { icon: "Clock", label: "Режим работы", value: site.workHours },
];

export default function ContactsPage() {
  return (
    <>
      <PageHeader
        eyebrow="Связаться с нами"
        title="Контакты"
        description="Ответим на вопросы о вступлении, рассчитаем стоимость и поможем с документами."
        breadcrumbs={[{ label: "Контакты" }]}
      />

      <Section tone="white">
        <div className="grid gap-10 lg:grid-cols-2">
          {/* Контактные данные */}
          <div>
            <SectionHeading
              align="left"
              eyebrow="Реквизиты связи"
              title="Как с нами связаться"
            />
            <div className="mt-8 grid gap-4 sm:grid-cols-2">
              {contacts.map((c) => {
                const inner = (
                  <Card hover={!!c.href} className="flex h-full items-start gap-4 p-5">
                    <span className="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-gold-100 text-gold-700">
                      <Icon name={c.icon} className="h-5 w-5" />
                    </span>
                    <div>
                      <p className="text-sm text-slate-500">{c.label}</p>
                      <p className="mt-0.5 font-semibold text-navy-900">{c.value}</p>
                    </div>
                  </Card>
                );
                return c.href ? (
                  <a key={c.label} href={c.href} className="block">
                    {inner}
                  </a>
                ) : (
                  <div key={c.label}>{inner}</div>
                );
              })}
            </div>

            {/* Карта (заглушка) */}
            <div className="mt-6 overflow-hidden rounded-2xl border border-slate-200">
              <div className="relative flex aspect-[16/10] items-center justify-center bg-gradient-to-br from-navy-800 to-navy-950">
                <div className="absolute inset-0 bg-grid opacity-40" aria-hidden />
                <div className="relative text-center text-white">
                  <Icon name="MapPin" className="mx-auto h-10 w-10 text-gold-400" />
                  <p className="mt-2 font-semibold">{site.address}</p>
                  <p className="text-sm text-slate-300">Санкт-Петербург</p>
                </div>
              </div>
            </div>
          </div>

          {/* Форма */}
          <Card className="h-fit p-6 sm:p-8 lg:sticky lg:top-28">
            <h2 className="text-xl font-bold text-navy-900">Напишите нам</h2>
            <p className="mt-1.5 text-sm text-slate-500">
              Заполните форму — менеджер свяжется с вами в рабочее время.
            </p>
            <div className="mt-6">
              <LeadForm
                type="CONSULTATION"
                source="contacts-page"
                fields={["company", "email", "message"]}
                submitLabel="Отправить сообщение"
              />
            </div>
          </Card>
        </div>
      </Section>
    </>
  );
}
