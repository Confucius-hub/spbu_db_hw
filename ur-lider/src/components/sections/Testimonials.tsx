import { Quote } from "lucide-react";
import { Section } from "@/components/ui/Section";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Reveal } from "@/components/ui/Reveal";

const items = [
  {
    quote:
      "Нужен был допуск СРО строителей под тендер — оформили буквально за день. Документы готовили сами, мы только подписали. Огромная экономия времени.",
    name: "Игорь Северин",
    role: "Директор, строительная компания",
  },
  {
    quote:
      "Наша СРО попала под исключение из реестра. ЮРЛИДЕР перевёл компенсационный фонд в надёжную организацию без остановки работ по контрактам.",
    name: "Марина Кольцова",
    role: "Руководитель проектного бюро",
  },
  {
    quote:
      "Внесли двух специалистов в НРС после отказа, который мы получили сами. Разобрались с причинами и сделали всё с первого раза. Рекомендую.",
    name: "Алексей Громов",
    role: "Главный инженер, изыскания",
  },
];

export function Testimonials() {
  return (
    <Section tone="white">
      <SectionHeading
        align="center"
        eyebrow="Отзывы"
        title="Клиенты возвращаются и рекомендуют"
      />

      <div className="mt-12 grid gap-4 lg:grid-cols-3">
        {items.map((t, i) => (
          <Reveal key={t.name} delay={(i % 3) * 70}>
            <figure className="flex h-full flex-col rounded-2xl border border-line bg-paper p-7">
              <Quote className="h-7 w-7 text-accent" aria-hidden />
              <blockquote className="mt-4 flex-1 text-[15px] leading-relaxed text-graphite">
                {t.quote}
              </blockquote>
              <figcaption className="mt-6 border-t border-line pt-4">
                <span className="block font-semibold text-ink">{t.name}</span>
                <span className="text-[13px] text-muted">{t.role}</span>
              </figcaption>
            </figure>
          </Reveal>
        ))}
      </div>
    </Section>
  );
}
