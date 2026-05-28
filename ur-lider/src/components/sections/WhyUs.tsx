import { Clock, Banknote, FileCheck2, ShieldCheck } from "lucide-react";
import { Section } from "@/components/ui/Section";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Reveal } from "@/components/ui/Reveal";

const reasons = [
  {
    icon: Clock,
    title: "Допуск за 24 часа",
    text: "Подбираем СРО и оформляем членство в кратчайший срок — вы успеваете к тендеру и не теряете контракты.",
  },
  {
    icon: Banknote,
    title: "Оплата только компфонда",
    text: "Вы платите лишь взнос в компенсационный фонд, установленный законом. Без скрытых комиссий и переплат.",
  },
  {
    icon: FileCheck2,
    title: "Документы — бесплатно",
    text: "Полный пакет документов для вступления в СРО готовим за свой счёт. От вас — только реквизиты.",
  },
  {
    icon: ShieldCheck,
    title: "Надёжные СРО",
    text: "Официальная аккредитация в проверенных СРО Санкт-Петербурга — без риска исключения из реестра.",
  },
];

export function WhyUs() {
  return (
    <Section tone="white">
      <div className="grid gap-12 lg:grid-cols-[0.85fr_1.15fr] lg:gap-16">
        <SectionHeading
          eyebrow="Почему ЮРЛИДЕР"
          title="Допуск СРО без переплат и нервов"
          subtitle="Берём бюрократию на себя: вы получаете готовый допуск, а не пачку требований и счетов."
        />

        <div className="grid gap-x-10 gap-y-9 sm:grid-cols-2">
          {reasons.map((r, i) => (
            <Reveal key={r.title} delay={(i % 2) * 80}>
              <div className="flex flex-col">
                <span className="grid h-12 w-12 place-items-center rounded-xl border border-line bg-paper text-accent">
                  <r.icon className="h-6 w-6" strokeWidth={1.6} aria-hidden />
                </span>
                <h3 className="mt-5 text-lg text-ink">{r.title}</h3>
                <p className="mt-2 text-[15px] leading-relaxed text-muted">
                  {r.text}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </Section>
  );
}
