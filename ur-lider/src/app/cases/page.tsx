import type { Metadata } from "next";
import { PageHeader } from "@/components/ui/PageHeader";
import { Section } from "@/components/ui/Section";
import { Reveal } from "@/components/ui/Reveal";
import { CaseCard } from "@/components/sections/CaseCard";
import { CtaBand } from "@/components/sections/CtaBand";
import { cases } from "@/lib/cases";

export const metadata: Metadata = {
  title: "Кейсы",
  description:
    "Примеры оформления допусков СРО компанией «ЮРЛИДЕР»: строители, проектировщики, изыскатели, НРС, выписки и переход СРО — с реальными сроками.",
};

export default function CasesPage() {
  return (
    <>
      <PageHeader
        eyebrow="Кейсы"
        title="Допуски, оформленные в срок"
        subtitle="Подборка примеров по разным видам СРО. Названия клиентов скрыты, результаты и сроки — реальные."
        crumbs={[{ label: "Главная", href: "/" }, { label: "Кейсы" }]}
      />

      <Section tone="paper">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {cases.map((c, i) => (
            <Reveal key={c.id} delay={(i % 3) * 70}>
              <CaseCard item={c} />
            </Reveal>
          ))}
        </div>
      </Section>

      <CtaBand title="Нужен такой же допуск?" subtitle="Расскажите о задаче — подберём СРО и рассчитаем стоимость бесплатно." />
    </>
  );
}
