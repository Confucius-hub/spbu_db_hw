import type { Metadata } from "next";
import { Section, SectionHeading } from "@/components/ui/section";
import { PageHeader } from "@/components/layout/page-header";
import { Card } from "@/components/ui/card";
import { Cta } from "@/components/sections/cta";
import { LeadForm } from "@/components/forms/lead-form";
import { Icon, type IconName } from "@/lib/icons";
import { pageMetadata } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "НРС — Национальный реестр специалистов",
  description:
    "Внесение специалистов в Национальный реестр специалистов (НРС) НОСТРОЙ: требования, документы, сроки. Подготовим пакет под ключ.",
  path: "/nrs",
});

const requirements: { icon: IconName; title: string; text: string }[] = [
  { icon: "Award", title: "Профильное образование", text: "Высшее образование по специальности или направлению подготовки в области строительства." },
  { icon: "Clock", title: "Стаж работы", text: "Стаж по специальности не менее установленного срока, в том числе на инженерных должностях." },
  { icon: "BadgeCheck", title: "Повышение квалификации", text: "Документ о повышении квалификации в установленные периоды." },
  { icon: "Scale", title: "Отсутствие судимости", text: "Отсутствие непогашенной судимости за отдельные категории преступлений." },
];

const docs = [
  "Документы об образовании и повышении квалификации",
  "Трудовая книжка или сведения о трудовой деятельности",
  "СНИЛС и удостоверение личности",
  "Заявление по установленной форме",
];

export default function NrsPage() {
  return (
    <>
      <PageHeader
        eyebrow="Услуги · НРС"
        title="Национальный реестр специалистов (НРС)"
        description="Для членства в СРО компания должна иметь не менее двух специалистов по организации строительства, внесённых в НРС НОСТРОЙ. Поможем внести специалистов без замечаний."
        breadcrumbs={[{ label: "НРС" }]}
      />

      <Section tone="white">
        <div className="grid items-start gap-12 lg:grid-cols-2">
          <div>
            <SectionHeading
              align="left"
              eyebrow="Что это"
              title="Зачем нужен НРС"
              description="Национальный реестр специалистов — это реестр НОСТРОЙ, подтверждающий квалификацию инженеров — организаторов строительства."
            />
            <div className="mt-6 space-y-4 leading-relaxed text-slate-600">
              <p>
                Сведения о специалистах в НРС — обязательное условие членства в СРО. Именно эти
                специалисты несут ответственность за организацию работ и подписание ключевых
                документов на объекте.
              </p>
              <p>
                Мы берём подготовку документов на себя: проверяем соответствие требованиям, исключаем
                типичные ошибки и сопровождаем заявление до получения результата.
              </p>
            </div>
            <div className="mt-6 rounded-2xl border border-gold-200 bg-gold-50 p-5">
              <p className="flex items-center gap-2 font-semibold text-navy-900">
                <Icon name="Users" className="h-5 w-5 text-gold-600" />
                Минимум 2 специалиста
              </p>
              <p className="mt-1.5 text-sm text-slate-600">
                Для членства в СРО требуется не менее двух специалистов, внесённых в НРС.
              </p>
            </div>
          </div>

          <Card className="p-6 sm:p-8">
            <h3 className="text-lg font-bold text-navy-900">Внести специалиста в НРС</h3>
            <p className="mt-1 text-sm text-slate-500">
              Оставьте заявку — проверим документы и подготовим пакет.
            </p>
            <div className="mt-5">
              <LeadForm
                type="CONSULTATION"
                source="nrs-page"
                fields={["company", "email"]}
                submitLabel="Получить консультацию"
              />
            </div>
          </Card>
        </div>
      </Section>

      <Section tone="muted">
        <SectionHeading eyebrow="Требования" title="Требования к специалисту" />
        <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {requirements.map((r) => (
            <Card key={r.title} hover className="p-6">
              <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-navy-800 text-gold-400">
                <Icon name={r.icon} className="h-6 w-6" />
              </span>
              <h3 className="mt-4 font-bold text-navy-900">{r.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600">{r.text}</p>
            </Card>
          ))}
        </div>
      </Section>

      <Section tone="white">
        <div className="grid items-center gap-10 lg:grid-cols-2">
          <div>
            <SectionHeading
              align="left"
              eyebrow="Документы"
              title="Какие документы потребуются"
            />
            <ul className="mt-6 space-y-3">
              {docs.map((d) => (
                <li key={d} className="flex items-start gap-3 text-slate-700">
                  <span className="mt-0.5 inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
                    <Icon name="Check" className="h-4 w-4" strokeWidth={2.5} />
                  </span>
                  {d}
                </li>
              ))}
            </ul>
          </div>
          <Card className="bg-navy-900 p-8 text-white">
            <Icon name="ClipboardList" className="h-12 w-12 text-gold-400" />
            <p className="mt-4 text-xl font-bold text-white">Сделаем всю работу за вас</p>
            <p className="mt-3 text-slate-300">
              Проверим комплектность, оформим заявление и доведём до внесения в реестр. Вы получаете
              результат без погружения в бюрократию.
            </p>
          </Card>
        </div>
      </Section>

      <Cta title="Нужно внести специалистов в НРС?" text="Оставьте заявку — подготовим документы и сопроводим до результата." />
    </>
  );
}
