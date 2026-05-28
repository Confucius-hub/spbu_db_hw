import { Section } from "@/components/ui/Section";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Reveal } from "@/components/ui/Reveal";

const steps = [
  {
    n: "01",
    title: "Заявка и консультация",
    text: "Определяем нужный вид СРО и уровень ответственности под ваши контракты. Бесплатно.",
  },
  {
    n: "02",
    title: "Подготовка документов",
    text: "Готовим полный пакет за свой счёт и при необходимости вносим специалистов в НРС.",
  },
  {
    n: "03",
    title: "Оплата компфонда",
    text: "Вы оплачиваете только взнос в компенсационный фонд, установленный законом.",
  },
  {
    n: "04",
    title: "Допуск за 24 часа",
    text: "Получаете членство в СРО и электронную выписку для участия в тендерах.",
  },
];

export function Process() {
  return (
    <Section tone="ink">
      <SectionHeading
        tone="onDark"
        eyebrow="Как вступить в СРО"
        title="Четыре шага до допуска СРО"
        subtitle="Всю работу с документами и СРО берём на себя — от вас нужны только реквизиты компании."
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
