import type { Metadata } from "next";
import { Section, SectionHeading } from "@/components/ui/section";
import { PageHeader } from "@/components/layout/page-header";
import { PageToc } from "@/components/layout/page-toc";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Calculator } from "@/components/home/calculator";
import { Steps } from "@/components/sections/steps";
import { MembershipDocs } from "@/components/membership/docs";
import { Faq } from "@/components/sections/faq";
import { Cta } from "@/components/sections/cta";
import { LeadForm } from "@/components/forms/lead-form";
import { Icon } from "@/lib/icons";
import { formatCurrency } from "@/lib/utils";
import { VV_LEVELS, ODO_LEVELS } from "@/lib/calculator";
import { pageMetadata, serviceJsonLd } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "Вступление в СРО",
  description:
    "Вступление в СРО строителей за 1 день: условия, стоимость, уровни ответственности, допуск на ОПО. Онлайн-калькулятор взносов.",
  path: "/membership",
});

const included = [
  "Подбор уровня ответственности под ваши договоры",
  "Подготовка полного пакета документов",
  "Внесение специалистов в НРС при необходимости",
  "Сопровождение до записи в реестре",
  "Фиксированная стоимость в договоре",
  "Личный менеджер на всех этапах",
];

export default function MembershipPage() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(
            serviceJsonLd({
              name: "Вступление в СРО строителей",
              description:
                "Сопровождение вступления в СРО строителей под ключ: подбор уровня ответственности, подготовка документов, внесение специалистов в НРС, допуск на ОПО.",
              path: "/membership",
              serviceType: "Допуск к строительным работам через членство в СРО",
            }),
          ),
        }}
      />
      <PageHeader
        eyebrow="Услуги · Вступление"
        title="Вступление в СРО строителей за 1 день"
        description="Поможем получить допуск к строительным, монтажным и ремонтным работам под ключ — без скрытых платежей и сложных процедур."
        breadcrumbs={[{ label: "Вступление" }]}
      >
        <div className="flex flex-wrap gap-3">
          <Button href="#calculator" variant="gold" size="lg">
            <Icon name="Calculator" className="h-5 w-5" />
            Рассчитать стоимость
          </Button>
          <Button href="#application" variant="white" size="lg">
            Оставить заявку
          </Button>
        </div>
      </PageHeader>

      <PageToc
        items={[
          { label: "Условия и калькулятор", href: "#calculator" },
          { label: "Уровни ответственности", href: "#levels" },
          { label: "Допуск на ОПО", href: "#opo" },
          { label: "Документы для вступления", href: "#documents" },
          { label: "Как вступить", href: "#steps" },
          { label: "Оставить заявку", href: "#application" },
          { label: "Вопросы и ответы", href: "#faq" },
        ]}
      />

      {/* Что входит + калькулятор */}
      <Section tone="white" id="calculator">
        <div className="grid items-start gap-10 lg:grid-cols-2">
          <div>
            <SectionHeading
              align="left"
              eyebrow="Под ключ"
              title="Что входит в сопровождение вступления"
              description="Берём на себя всю работу — от расчёта до получения допуска. Вы получаете прозрачную фиксированную стоимость."
            />
            <ul className="mt-8 space-y-3.5">
              {included.map((item) => (
                <li key={item} className="flex items-start gap-3">
                  <span className="mt-0.5 inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
                    <Icon name="Check" className="h-4 w-4" strokeWidth={2.5} />
                  </span>
                  <span className="text-slate-700">{item}</span>
                </li>
              ))}
            </ul>
            <div className="mt-8 rounded-2xl border border-gold-200 bg-gold-50 p-5">
              <p className="flex items-center gap-2 font-semibold text-navy-900">
                <Icon name="Zap" className="h-5 w-5 text-gold-600" />
                Решение о приёме — за 1 рабочий день
              </p>
              <p className="mt-1.5 text-sm text-slate-600">
                При полном пакете документов. Полное оформление с внесением в реестр — до 3 рабочих
                дней.
              </p>
            </div>
          </div>

          <div className="lg:sticky lg:top-28">
            <Calculator variant="full" />
          </div>
        </div>
      </Section>

      {/* Уровни ответственности */}
      <Section tone="muted" id="levels">
        <SectionHeading
          eyebrow="Стоимость"
          title="Уровни ответственности и взносы в компенсационные фонды"
          description="Размер взноса зависит от максимальной стоимости одного договора (ст. 55.16 Градостроительного кодекса РФ)."
        />
        <div className="mt-10 grid gap-6 lg:grid-cols-2">
          <FundTable
            title="КФ возмещения вреда (КФ ВВ)"
            subtitle="Обязателен для всех членов СРО"
            levels={VV_LEVELS}
          />
          <FundTable
            title="КФ обеспечения договорных обязательств (КФ ОДО)"
            subtitle="Для участия в конкурсах и закупках"
            levels={ODO_LEVELS}
          />
        </div>
      </Section>

      {/* Допуск на ОПО */}
      <Section tone="white" id="opo">
        <div className="grid items-center gap-10 lg:grid-cols-2">
          <div>
            <SectionHeading
              align="left"
              eyebrow="Особо опасные объекты"
              title="Допуск на ОПО и технически сложные объекты"
              description="Для работ на особо опасных, технически сложных и уникальных объектах действуют повышенные требования к кадровому составу и системе контроля качества."
            />
            <ul className="mt-6 space-y-3">
              {[
                "Дополнительные специалисты с квалификацией и стажем на ОПО",
                "Наличие необходимого имущества и оборудования",
                "Внедрённая система контроля качества",
                "Соблюдение требований промышленной безопасности",
              ].map((t) => (
                <li key={t} className="flex items-start gap-3 text-slate-700">
                  <Icon name="HardHat" className="mt-0.5 h-5 w-5 shrink-0 text-gold-600" />
                  {t}
                </li>
              ))}
            </ul>
            <Button href="#application" variant="primary" className="mt-7">
              Получить консультацию по ОПО
            </Button>
          </div>
          <Card className="bg-navy-900 p-8 text-white">
            <Icon name="HardHat" className="h-12 w-12 text-gold-400" />
            <p className="mt-4 text-xl font-bold text-white">
              Отдельного взноса за допуск ОПО не требуется
            </p>
            <p className="mt-3 text-slate-300">
              Допуск оформляется в рамках членства при подтверждении соответствия требованиям. Мы
              поможем привести кадровый состав и документацию в порядок.
            </p>
          </Card>
        </div>
      </Section>

      <MembershipDocs />

      <Steps />

      {/* Заявка */}
      <Section tone="muted" id="application">
        <div className="grid items-start gap-10 lg:grid-cols-2">
          <div>
            <SectionHeading
              align="left"
              eyebrow="Заявка на вступление"
              title="Оставьте заявку — рассчитаем и подготовим документы"
              description="Менеджер свяжется с вами в течение 15 минут, уточнит детали и сформирует индивидуальный расчёт и перечень документов."
            />
            <div className="mt-6 space-y-3 text-slate-700">
              {[
                "Бесплатно и без обязательств",
                "Индивидуальный расчёт под ваши договоры",
                "Перечень документов под ваш вид работ",
              ].map((t) => (
                <p key={t} className="flex items-center gap-2.5">
                  <Icon name="CheckCircle2" className="h-5 w-5 text-emerald-600" />
                  {t}
                </p>
              ))}
            </div>
          </div>
          <Card className="p-6 sm:p-8">
            <LeadForm
              type="APPLICATION"
              source="membership-page"
              fields={["company", "email", "message"]}
              submitLabel="Отправить заявку"
            />
          </Card>
        </div>
      </Section>

      <Faq />
      <Cta />
    </>
  );
}

function FundTable({
  title,
  subtitle,
  levels,
}: {
  title: string;
  subtitle: string;
  levels: { level: number; label: string; fee: number }[];
}) {
  return (
    <Card className="overflow-hidden">
      <div className="border-b border-slate-100 p-5">
        <h3 className="font-bold text-navy-900">{title}</h3>
        <p className="text-sm text-slate-500">{subtitle}</p>
      </div>
      <table className="w-full text-sm">
        <thead>
          <tr className="bg-slate-50 text-left text-xs uppercase tracking-wider text-slate-500">
            <th className="px-5 py-3 font-semibold">Уровень</th>
            <th className="px-5 py-3 font-semibold">Стоимость договора</th>
            <th className="px-5 py-3 text-right font-semibold">Взнос</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {levels.map((l) => (
            <tr key={l.level} className="transition-colors hover:bg-gold-50/50">
              <td className="px-5 py-3.5 font-semibold text-navy-800">{l.level}</td>
              <td className="px-5 py-3.5 text-slate-600">{l.label}</td>
              <td className="px-5 py-3.5 text-right font-semibold text-navy-900">
                {formatCurrency(l.fee)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </Card>
  );
}
