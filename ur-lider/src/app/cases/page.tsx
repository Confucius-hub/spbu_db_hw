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
    "Результаты дел юридической компании «Лидер»: налоговые споры, банкротство, арбитраж, корпоративные и семейные споры — с конкретными цифрами.",
};

export default function CasesPage() {
  return (
    <>
      <PageHeader
        eyebrow="Результаты"
        title="Кейсы, измеримые в цифрах"
        subtitle="Подборка дел из разных практик. Имена клиентов скрыты ради конфиденциальности, результаты — реальные."
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

      <CtaBand title="Похожая ситуация?" subtitle="Расскажите о деле — оценим перспективы и предложим стратегию." />
    </>
  );
}
