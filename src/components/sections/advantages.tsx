import { Section, SectionHeading } from "@/components/ui/section";
import { Card } from "@/components/ui/card";
import { Icon, type IconName } from "@/lib/icons";
import { advantages } from "@/lib/site";

export function Advantages() {
  return (
    <Section tone="muted">
      <SectionHeading
        eyebrow="Почему мы"
        title="Преимущества работы с СРО «СССС»"
        description="Сопровождаем на всех этапах и отвечаем за результат. Прозрачно, быстро и надёжно."
      />
      <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {advantages.map((a) => (
          <Card key={a.title} hover className="p-6">
            <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gold-100 text-gold-700">
              <Icon name={a.icon as IconName} className="h-6 w-6" />
            </span>
            <h3 className="mt-4 text-lg font-bold text-navy-900">{a.title}</h3>
            <p className="mt-2 text-[0.95rem] leading-relaxed text-slate-600">{a.text}</p>
          </Card>
        ))}
      </div>
    </Section>
  );
}
