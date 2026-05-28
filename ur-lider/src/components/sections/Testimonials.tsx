import { Quote } from "lucide-react";
import { Section } from "@/components/ui/Section";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Reveal } from "@/components/ui/Reveal";

const items = [
  {
    quote:
      "Сопровождали сложную налоговую проверку. Доначисления сняли почти полностью. Чёткая работа, всё объясняли понятным языком.",
    name: "Игорь Северин",
    role: "Финансовый директор, производство",
  },
  {
    quote:
      "Помогли пройти банкротство и сохранить квартиру. Поддержка на каждом шаге, без лишнего стресса. Рекомендую.",
    name: "Марина Кольцова",
    role: "Частный клиент",
  },
  {
    quote:
      "Вернули контроль над компанией в корпоративном споре. Стратегия была выверенной, результат — выше ожиданий.",
    name: "Алексей Громов",
    role: "Сооснователь, IT-компания",
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
