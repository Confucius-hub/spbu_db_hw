import { Section } from "@/components/ui/Section";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Reveal } from "@/components/ui/Reveal";

const steps = [
  {
    n: "01",
    title: "Консультация",
    text: "Изучаем ситуацию и документы, отвечаем на вопросы. Бесплатно и конфиденциально.",
  },
  {
    n: "02",
    title: "Анализ и стратегия",
    text: "Оцениваем перспективы, формируем план действий и прозрачную смету.",
  },
  {
    n: "03",
    title: "Договор и работа",
    text: "Фиксируем условия. Профильный юрист ведёт дело и держит вас в курсе.",
  },
  {
    n: "04",
    title: "Результат",
    text: "Доводим до цели и сопровождаем исполнение решения.",
  },
];

export function Process() {
  return (
    <Section tone="ink">
      <SectionHeading
        tone="onDark"
        eyebrow="Как мы работаем"
        title="Понятный процесс от первого звонка до результата"
        subtitle="Никакой неопределённости: вы всегда знаете, что происходит и что будет дальше."
      />

      <ol className="mt-14 grid gap-px overflow-hidden rounded-2xl border border-white/10 bg-white/10 sm:grid-cols-2 lg:grid-cols-4">
        {steps.map((s, i) => (
          <Reveal as="li" key={s.n} delay={i * 70} className="bg-ink">
            <div className="flex h-full flex-col p-7 lg:p-8">
              <span className="font-serif text-4xl font-semibold text-accent">
                {s.n}
              </span>
              <h3 className="mt-5 text-lg text-white">{s.title}</h3>
              <p className="mt-2 text-[15px] leading-relaxed text-white/60">
                {s.text}
              </p>
            </div>
          </Reveal>
        ))}
      </ol>
    </Section>
  );
}
