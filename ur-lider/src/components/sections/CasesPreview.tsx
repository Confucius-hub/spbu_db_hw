import { Section } from "@/components/ui/Section";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Button } from "@/components/ui/Button";
import { Reveal } from "@/components/ui/Reveal";
import { CaseCard } from "./CaseCard";
import { cases } from "@/lib/cases";

export function CasesPreview() {
  return (
    <Section tone="paper">
      <div className="flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
        <SectionHeading
          eyebrow="Результаты"
          title="Дела, за которые мы отвечаем цифрами"
          subtitle="Каждое дело — это конкретный результат для клиента, а не строчка в портфолио."
          className="max-w-2xl"
        />
        <Reveal>
          <Button href="/cases" variant="outline" className="shrink-0">
            Все кейсы
          </Button>
        </Reveal>
      </div>

      <div className="mt-12 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {cases.slice(0, 3).map((c, i) => (
          <Reveal key={c.id} delay={(i % 3) * 70}>
            <CaseCard item={c} />
          </Reveal>
        ))}
      </div>
    </Section>
  );
}
