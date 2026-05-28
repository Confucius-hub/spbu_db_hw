import { Target, Banknote, UserCheck, FileSearch } from "lucide-react";
import { Section } from "@/components/ui/Section";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Reveal } from "@/components/ui/Reveal";

const reasons = [
  {
    icon: Target,
    title: "Берёмся за результат",
    text: "Честно оцениваем перспективы дела. Если шансов нет — скажем прямо и не возьмём деньги за пустую работу.",
  },
  {
    icon: Banknote,
    title: "Прозрачная стоимость",
    text: "Фиксируем цену и объём в договоре до старта. Без скрытых платежей и доплат «по ходу».",
  },
  {
    icon: UserCheck,
    title: "Персональный юрист",
    text: "За вами закрепляется профильный специалист и куратор. Вы всегда знаете статус по делу.",
  },
  {
    icon: FileSearch,
    title: "Глубокая проработка",
    text: "Стратегию строим на доказательствах и судебной практике, а не на обещаниях.",
  },
];

export function WhyUs() {
  return (
    <Section tone="white">
      <div className="grid gap-12 lg:grid-cols-[0.85fr_1.15fr] lg:gap-16">
        <SectionHeading
          eyebrow="Почему «Лидер»"
          title="Подход, который вызывает доверие"
          subtitle="Мы строим долгосрочные отношения с клиентами — поэтому ценим репутацию выше разовой выгоды."
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
