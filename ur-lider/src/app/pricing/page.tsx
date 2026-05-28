import type { Metadata } from "next";
import { Check } from "lucide-react";
import { PageHeader } from "@/components/ui/PageHeader";
import { Section } from "@/components/ui/Section";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Button } from "@/components/ui/Button";
import { Reveal } from "@/components/ui/Reveal";
import { Faq } from "@/components/sections/Faq";
import { CtaBand } from "@/components/sections/CtaBand";
import { cn } from "@/lib/utils";

export const metadata: Metadata = {
  title: "Стоимость",
  description:
    "Форматы работы и стоимость услуг юридической компании «Лидер»: разовая консультация, ведение дела под ключ, абонентское обслуживание бизнеса.",
};

const plans = [
  {
    name: "Консультация",
    price: "от 3 000 ₽",
    note: "разовая, зачитывается в стоимость дела",
    features: [
      "Анализ ситуации и документов",
      "Оценка перспектив",
      "Пошаговый план действий",
      "Ответы на вопросы",
    ],
    cta: "Записаться",
    featured: false,
  },
  {
    name: "Ведение дела",
    price: "от 30 000 ₽",
    note: "фиксированная цена под задачу",
    features: [
      "Разработка правовой стратегии",
      "Подготовка всех документов",
      "Полное представительство",
      "Сопровождение до результата",
      "Персональный юрист и куратор",
    ],
    cta: "Обсудить дело",
    featured: true,
  },
  {
    name: "Абонентское",
    price: "от 40 000 ₽/мес",
    note: "для бизнеса, объём по договору",
    features: [
      "Внешний юридический отдел",
      "Договорная работа и экспертиза",
      "Консультации без ограничений",
      "Сопровождение проверок",
      "Выделенный куратор и SLA",
    ],
    cta: "Получить расчёт",
    featured: false,
  },
];

const faq = [
  {
    q: "Почему цена «от» и как формируется итог?",
    a: "Стоимость зависит от сложности дела, объёма работы и инстанций. Точную цену мы фиксируем в договоре после бесплатного анализа — она не меняется в процессе.",
  },
  {
    q: "Берёте ли вы оплату за результат (гонорар успеха)?",
    a: "По ряду дел возможна смешанная модель: фиксированная часть плюс премия за результат. Условия обсуждаются индивидуально.",
  },
  {
    q: "Что входит в бесплатную консультацию?",
    a: "Анализ вашей ситуации, честная оценка перспектив и план действий. Если по итогу заключаем договор — стоимость первичной консультации засчитывается.",
  },
];

export default function PricingPage() {
  return (
    <>
      <PageHeader
        eyebrow="Стоимость"
        title="Прозрачная цена, зафиксированная заранее"
        subtitle="Вы знаете стоимость и объём работы до старта. Без скрытых платежей и доплат «по ходу дела»."
        crumbs={[{ label: "Главная", href: "/" }, { label: "Стоимость" }]}
      />

      <Section tone="paper">
        <div className="grid gap-4 lg:grid-cols-3">
          {plans.map((plan, i) => (
            <Reveal key={plan.name} delay={i * 80}>
              <div
                className={cn(
                  "flex h-full flex-col rounded-2xl border p-8",
                  plan.featured
                    ? "border-ink bg-ink text-white shadow-[var(--shadow-lift)]"
                    : "border-line bg-white",
                )}
              >
                {plan.featured && (
                  <span className="mb-4 inline-flex w-fit items-center rounded-full bg-accent px-3 py-1 text-[12px] font-semibold uppercase tracking-wider text-white">
                    Популярный формат
                  </span>
                )}
                <h2
                  className={cn(
                    "text-xl font-semibold",
                    plan.featured ? "text-white" : "text-ink",
                  )}
                >
                  {plan.name}
                </h2>
                <div className="mt-4 flex items-baseline gap-2">
                  <span
                    className={cn(
                      "font-serif text-4xl font-semibold",
                      plan.featured ? "text-white" : "text-ink",
                    )}
                  >
                    {plan.price}
                  </span>
                </div>
                <p
                  className={cn(
                    "mt-1.5 text-sm",
                    plan.featured ? "text-white/60" : "text-muted",
                  )}
                >
                  {plan.note}
                </p>

                <ul className="mt-7 flex flex-1 flex-col gap-3">
                  {plan.features.map((f) => (
                    <li key={f} className="flex items-start gap-3">
                      <span
                        className={cn(
                          "mt-0.5 grid h-5 w-5 shrink-0 place-items-center rounded-full",
                          plan.featured
                            ? "bg-accent text-white"
                            : "bg-accent-soft text-accent-strong",
                        )}
                      >
                        <Check className="h-3 w-3" strokeWidth={3} aria-hidden />
                      </span>
                      <span
                        className={cn(
                          "text-[15px]",
                          plan.featured ? "text-white/85" : "text-graphite",
                        )}
                      >
                        {f}
                      </span>
                    </li>
                  ))}
                </ul>

                <div className="mt-8">
                  <Button
                    href="/contacts"
                    variant={plan.featured ? "accent" : "outline"}
                    className="w-full"
                  >
                    {plan.cta}
                  </Button>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </Section>

      <Section tone="white">
        <div className="grid gap-10 lg:grid-cols-[0.8fr_1.2fr] lg:gap-16">
          <SectionHeading eyebrow="Вопросы о цене" title="Коротко о стоимости" />
          <Faq items={faq} />
        </div>
      </Section>

      <CtaBand />
    </>
  );
}
