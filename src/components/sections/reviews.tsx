import { Section, SectionHeading } from "@/components/ui/section";
import { Card } from "@/components/ui/card";
import { Icon } from "@/lib/icons";
import { reviews } from "@/lib/site";

export function Reviews() {
  return (
    <Section tone="muted">
      <SectionHeading
        eyebrow="Отзывы"
        title="Что говорят о работе с нами"
        description="Опыт компаний, которые проходили вступление и сопровождение в СРО «СССС»."
      />
      <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {reviews.map((r) => (
          <Card key={r.company} className="flex flex-col p-6">
            <Icon name="Quote" className="h-8 w-8 text-gold-300" />
            <p className="mt-3 flex-1 text-[0.95rem] leading-relaxed text-slate-700">{r.text}</p>
            <div className="mt-5 flex items-center gap-1 text-gold-500">
              {Array.from({ length: r.rating }).map((_, i) => (
                <Icon key={i} name="Star" className="h-4 w-4 fill-gold-400 text-gold-400" />
              ))}
            </div>
            <div className="mt-3 border-t border-slate-100 pt-3">
              <p className="font-semibold text-navy-900">{r.company}</p>
              <p className="text-sm text-slate-500">{r.person}</p>
            </div>
          </Card>
        ))}
      </div>
    </Section>
  );
}
