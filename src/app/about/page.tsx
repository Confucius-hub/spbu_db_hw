import type { Metadata } from "next";
import Link from "next/link";
import { Section, SectionHeading } from "@/components/ui/section";
import { PageHeader } from "@/components/layout/page-header";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Stats } from "@/components/sections/stats";
import { Cta } from "@/components/sections/cta";
import { Icon, type IconName } from "@/lib/icons";
import { site } from "@/lib/site";
import { pageMetadata } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "О СРО",
  description:
    "СРО «Строительный союз Северной столицы» — саморегулируемая организация строителей Санкт-Петербурга в реестре НОСТРОЙ с 2010 года.",
  path: "/about",
});

const values: { icon: IconName; title: string; text: string }[] = [
  { icon: "ShieldCheck", title: "Надёжность", text: "Компенсационный фонд более 300 млн ₽ и нулевые выплаты за всю историю." },
  { icon: "Scale", title: "Прозрачность", text: "Фиксированные условия и понятные правила без скрытых платежей." },
  { icon: "Users", title: "Сообщество", text: "Более 900 строительных компаний Санкт-Петербурга и области." },
  { icon: "BadgeCheck", title: "Соответствие", text: "100% соответствие требованиям реестра НОСТРОЙ." },
];

const requisites = [
  { label: "Полное наименование", value: site.legalName },
  { label: "Сокращённое наименование", value: `СРО Ассоциация «${site.name}»` },
  { label: "Регистрационный номер", value: site.registryNumber },
  { label: "Дата внесения в реестр", value: site.registryDate },
  { label: "Адрес", value: site.address },
  { label: "Телефон", value: site.phone },
  { label: "E-mail", value: site.email },
];

export default function AboutPage() {
  return (
    <>
      <PageHeader
        eyebrow="Об организации"
        title="Строительный союз Северной столицы"
        description="Саморегулируемая организация строителей Санкт-Петербурга. В реестре НОСТРОЙ с 2010 года."
        breadcrumbs={[{ label: "О СРО" }]}
      />

      {/* Миссия */}
      <Section tone="white">
        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div>
            <SectionHeading
              align="left"
              eyebrow="Кто мы"
              title="15 лет развиваем строительный рынок Санкт-Петербурга"
            />
            <div className="mt-6 space-y-4 text-[1.02rem] leading-relaxed text-slate-600">
              <p>
                СРО «Строительный союз Северной столицы» объединяет строительные, монтажные и
                ремонтные компании, обеспечивая их допуск к работам и защищая интересы заказчиков
                через институт компенсационного фонда.
              </p>
              <p>
                Мы помогаем компаниям соответствовать требованиям законодательства, оперативно
                адаптироваться к изменениям — в том числе к реформе саморегулирования 2026 года — и
                развивать бизнес без юридических рисков.
              </p>
              <p>
                Наша задача — сделать саморегулирование понятным и удобным инструментом, а не
                формальностью.
              </p>
            </div>
          </div>
          <Card className="bg-navy-900 p-8 text-white">
            <h3 className="text-lg font-bold text-white">Коротко о главном</h3>
            <dl className="mt-6 space-y-5">
              {[
                ["В реестре НОСТРОЙ", `с ${site.founded} года`],
                ["Компаний в составе", "более 900"],
                ["Компенсационный фонд", "более 300 млн ₽"],
                ["Выплат из фонда", "0 ₽ за всю историю"],
              ].map(([k, v]) => (
                <div key={k} className="flex items-center justify-between border-b border-white/10 pb-4 last:border-0 last:pb-0">
                  <dt className="text-slate-300">{k}</dt>
                  <dd className="font-display text-lg font-bold text-gold-gradient">{v}</dd>
                </div>
              ))}
            </dl>
          </Card>
        </div>
      </Section>

      {/* Ценности */}
      <Section tone="muted">
        <SectionHeading
          eyebrow="Наши принципы"
          title="Ценности, на которых мы работаем"
        />
        <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {values.map((v) => (
            <Card key={v.title} hover className="p-6">
              <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gold-100 text-gold-700">
                <Icon name={v.icon} className="h-6 w-6" />
              </span>
              <h3 className="mt-4 font-bold text-navy-900">{v.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600">{v.text}</p>
            </Card>
          ))}
        </div>
      </Section>

      <Stats />

      {/* Компенсационный фонд */}
      <Section tone="white" id="fund">
        <div className="grid items-center gap-10 lg:grid-cols-2">
          <Card className="order-2 overflow-hidden lg:order-1">
            <div className="bg-gradient-to-br from-navy-800 to-navy-950 p-8 text-white">
              <Icon name="ShieldCheck" className="h-12 w-12 text-gold-400" />
              <p className="mt-4 font-display text-4xl font-extrabold text-gold-gradient">300+ млн ₽</p>
              <p className="mt-1 text-slate-300">размер компенсационного фонда</p>
            </div>
            <div className="grid grid-cols-2 divide-x divide-slate-100">
              <div className="p-6 text-center">
                <p className="font-display text-2xl font-extrabold text-navy-900">0 ₽</p>
                <p className="mt-1 text-sm text-slate-500">выплат за историю</p>
              </div>
              <div className="p-6 text-center">
                <p className="font-display text-2xl font-extrabold text-navy-900">2 фонда</p>
                <p className="mt-1 text-sm text-slate-500">ВВ и ОДО</p>
              </div>
            </div>
          </Card>
          <div className="order-1 lg:order-2">
            <SectionHeading
              align="left"
              eyebrow="Гарантии"
              title="Компенсационный фонд — наша финансовая ответственность"
              description="Фонд гарантирует возмещение вреда и обеспечение договорных обязательств членов СРО. Это главный показатель надёжности организации для заказчика."
            />
            <Button href="/documents" variant="outline" className="mt-7">
              <Icon name="FileText" className="h-4 w-4" />
              Документы о фонде
            </Button>
          </div>
        </div>
      </Section>

      {/* Реквизиты */}
      <Section tone="muted" id="requisites">
        <SectionHeading eyebrow="Реквизиты" title="Сведения об организации" />
        <Card className="mx-auto mt-10 max-w-3xl overflow-hidden">
          <dl className="divide-y divide-slate-100">
            {requisites.map((r) => (
              <div key={r.label} className="grid gap-1 px-6 py-4 sm:grid-cols-3 sm:gap-4">
                <dt className="text-sm text-slate-500">{r.label}</dt>
                <dd className="font-medium text-navy-900 sm:col-span-2">{r.value}</dd>
              </div>
            ))}
          </dl>
        </Card>
        <p className="mt-6 text-center">
          <Link
            href={site.nostroyUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-sm font-semibold text-navy-800 hover:text-gold-700"
          >
            Проверить в едином реестре НОСТРОЙ
            <Icon name="ExternalLink" className="h-4 w-4" />
          </Link>
        </p>
      </Section>

      <Cta />
    </>
  );
}
