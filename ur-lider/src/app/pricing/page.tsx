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
    "Стоимость вступления в СРО в «ЮРЛИДЕР»: оплата только взноса в компенсационный фонд, подготовка документов бесплатно, первый год без ежемесячных взносов.",
};

const plans = [
  {
    name: "СРО проектировщиков",
    price: "от 50 000 ₽",
    note: "взнос в компенсационный фонд",
    features: [
      "Подбор аккредитованной СРО",
      "Подготовка документов — бесплатно",
      "Допуск за 24 часа",
      "Помощь с внесением в НРС",
      "Электронная выписка из реестра",
    ],
    cta: "Рассчитать",
    featured: false,
  },
  {
    name: "СРО строителей",
    price: "от 100 000 ₽",
    note: "взнос в компенсационный фонд",
    features: [
      "Подбор аккредитованной СРО",
      "Подготовка документов — бесплатно",
      "Допуск за 24 часа",
      "Первый год без ежемесячных взносов",
      "Помощь с внесением в НРС",
      "Выписка для тендеров",
    ],
    cta: "Рассчитать",
    featured: true,
  },
  {
    name: "СРО изыскателей",
    price: "от 50 000 ₽",
    note: "взнос в компенсационный фонд",
    features: [
      "Подбор аккредитованной СРО",
      "Подготовка документов — бесплатно",
      "Допуск за 24 часа",
      "Подбор уровня ответственности",
      "Электронная выписка из реестра",
    ],
    cta: "Рассчитать",
    featured: false,
  },
];

const faq = [
  {
    q: "Из чего складывается стоимость вступления в СРО?",
    a: "Основная сумма — это взнос в компенсационный фонд, размер которого установлен законом и зависит от вида СРО и уровня ответственности. Подготовку документов мы берём на себя бесплатно.",
  },
  {
    q: "Есть ли скрытые платежи и комиссии?",
    a: "Нет. Вы оплачиваете только взнос в компенсационный фонд. Никаких скрытых комиссий за наши услуги по подготовке и подаче документов.",
  },
  {
    q: "Что значит «первый год без ежемесячных взносов»?",
    a: "По ряду аккредитованных СРО членские взносы за первый период уже включены в условия вступления, поэтому в первый год вы не платите их отдельно.",
  },
];

export default function PricingPage() {
  return (
    <>
      <PageHeader
        eyebrow="Стоимость"
        title="Оплата только компенсационного фонда"
        subtitle="Подготовку документов берём на себя бесплатно. Вы платите лишь установленный законом взнос в компенсационный фонд — без скрытых комиссий."
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
