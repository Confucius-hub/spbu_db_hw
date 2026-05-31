import type { Metadata } from "next";
import Link from "next/link";
import { Section, SectionHeading } from "@/components/ui/section";
import { PageHeader } from "@/components/layout/page-header";
import { PageToc } from "@/components/layout/page-toc";
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
    "СРО «Строительный союз Северной столицы» — саморегулируемая организация строителей Санкт-Петербурга в реестре НОСТРОЙ (СРО-С-335-25122025).",
  path: "/about",
});

const values: { icon: IconName; title: string; text: string }[] = [
  { icon: "ShieldCheck", title: "Надёжность", text: "Компенсационные фонды возмещения вреда и обеспечения договорных обязательств." },
  { icon: "Scale", title: "Прозрачность", text: "Фиксированные условия и понятные правила без скрытых платежей." },
  { icon: "Users", title: "Сообщество", text: "Объединяем строительные компании и ИП Санкт-Петербурга." },
  { icon: "BadgeCheck", title: "Соответствие", text: "Работаем в соответствии с требованиями реестра НОСТРОЙ и № 309-ФЗ." },
];

/** Функции СРО (с официального сайта). */
const functions = [
  "Контроль качества работ членов и выдача допусков",
  "Обучение и аттестация специалистов",
  "Защита интересов членов перед государством и регуляторами",
  "Компенсационные фонды для возмещения ущерба",
  "Разработка стандартов и рекомендаций по отрасли",
  "Консультации по законодательству и страхованию",
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
        description="Саморегулируемая организация строителей Санкт-Петербурга. Внесена в государственный реестр НОСТРОЙ: СРО-С-335-25122025."
        breadcrumbs={[{ label: "О СРО" }]}
      />

      <PageToc
        items={[
          { label: "Кто мы", href: "#mission" },
          { label: "Функции СРО", href: "#functions" },
          { label: "Принципы", href: "#values" },
          { label: "Компенсационные фонды", href: "#fund" },
          { label: "Реквизиты", href: "#requisites" },
        ]}
      />

      {/* Миссия */}
      <Section tone="white" id="mission">
        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div>
            <SectionHeading
              align="left"
              eyebrow="Кто мы"
              title="Объединяем профессионалов строительной отрасли"
            />
            <div className="mt-6 space-y-4 text-[1.02rem] leading-relaxed text-slate-600">
              <p>
                Ассоциация объединяет компании и индивидуальных предпринимателей, работающих в
                области строительства, реконструкции и капитального ремонта капитальных объектов.
              </p>
              <p>
                Основная миссия СРО — отстаивать права и интересы своих участников перед Федеральной
                антимонопольной службой, органами исполнительной власти, местными властями и другими
                регуляторами строительного рынка. Это помогает создать оптимальные условия для
                бизнеса, повысить надёжность и качество работ — особенно в условиях уникальной
                исторической среды Северной столицы.
              </p>
              <p>
                Наша задача — сделать саморегулирование понятным и удобным инструментом, а не
                формальностью, и помочь членам адаптироваться к реформе отрасли 2026 года.
              </p>
            </div>
          </div>
          <Card className="bg-navy-900 p-8 text-white">
            <h3 className="text-lg font-bold text-white">Коротко о главном</h3>
            <dl className="mt-6 space-y-5">
              {[
                ["Статус", "СРО в реестре НОСТРОЙ"],
                ["Регистрационный номер", site.registryNumber],
                ["Дата внесения в реестр", site.registryDate],
                ["Компенсационные фонды", "ВВ и ОДО"],
              ].map(([k, v]) => (
                <div key={k} className="flex items-center justify-between gap-4 border-b border-white/10 pb-4 last:border-0 last:pb-0">
                  <dt className="text-slate-300">{k}</dt>
                  <dd className="text-right font-display text-base font-bold text-gold-gradient">{v}</dd>
                </div>
              ))}
            </dl>
          </Card>
        </div>
      </Section>

      {/* Функции СРО */}
      <Section tone="white" id="functions" className="pt-0">
        <SectionHeading
          align="left"
          eyebrow="Чем мы занимаемся"
          title="Основные функции СРО"
        />
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {functions.map((f) => (
            <div key={f} className="flex items-start gap-3 rounded-2xl border border-slate-200 bg-white p-5">
              <span className="mt-0.5 inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
                <Icon name="Check" className="h-4 w-4" strokeWidth={2.5} />
              </span>
              <span className="text-slate-700">{f}</span>
            </div>
          ))}
        </div>
      </Section>

      {/* Ценности */}
      <Section tone="muted" id="values">
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
              <p className="mt-4 font-display text-3xl font-extrabold text-gold-gradient">2 фонда</p>
              <p className="mt-1 text-slate-300">компенсационные фонды СРО</p>
            </div>
            <div className="grid grid-cols-2 divide-x divide-slate-100">
              <div className="p-6 text-center">
                <p className="font-display text-lg font-extrabold text-navy-900">КФ ВВ</p>
                <p className="mt-1 text-sm text-slate-500">возмещение вреда</p>
              </div>
              <div className="p-6 text-center">
                <p className="font-display text-lg font-extrabold text-navy-900">КФ ОДО</p>
                <p className="mt-1 text-sm text-slate-500">договорные обязательства</p>
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
