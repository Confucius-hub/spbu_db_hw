import type { Metadata } from "next";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { PageHeader } from "@/components/ui/PageHeader";
import { Section } from "@/components/ui/Section";
import { Reveal } from "@/components/ui/Reveal";
import { PracticeIcon } from "@/components/ui/PracticeIcon";
import { CtaBand } from "@/components/sections/CtaBand";
import { practices } from "@/lib/practices";

export const metadata: Metadata = {
  title: "Практики",
  description:
    "Направления работы юридической компании «Лидер»: сопровождение бизнеса, банкротство, налоговые споры, арбитраж, недвижимость и услуги частным клиентам.",
};

export default function PracticesPage() {
  return (
    <>
      <PageHeader
        eyebrow="Практики"
        title="Направления, в которых мы сильны"
        subtitle="Выберите практику, чтобы увидеть состав услуг, результаты и ответы на частые вопросы."
        crumbs={[{ label: "Главная", href: "/" }, { label: "Практики" }]}
      />

      <Section tone="paper">
        <div className="grid gap-4 lg:grid-cols-2">
          {practices.map((p, i) => (
            <Reveal key={p.slug} delay={(i % 2) * 80}>
              <Link
                href={`/practices/${p.slug}`}
                className="group flex h-full flex-col rounded-2xl border border-line bg-white p-8 transition-[transform,box-shadow,border-color] duration-300 hover:-translate-y-1 hover:border-line-strong hover:shadow-[var(--shadow-lift)]"
              >
                <div className="flex items-start justify-between gap-4">
                  <span className="grid h-13 w-13 place-items-center rounded-xl bg-accent-soft text-accent-strong transition-colors group-hover:bg-accent group-hover:text-white">
                    <PracticeIcon name={p.icon} className="h-6 w-6" />
                  </span>
                  <ArrowUpRight className="h-5 w-5 text-faint transition-all duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 group-hover:text-accent" />
                </div>
                <h2 className="mt-6 text-2xl text-ink">{p.title}</h2>
                <p className="mt-3 flex-1 text-[15px] leading-relaxed text-muted">
                  {p.summary}
                </p>
                <div className="mt-6 flex flex-wrap gap-2">
                  {p.services.slice(0, 3).map((s) => (
                    <span
                      key={s}
                      className="rounded-full border border-line bg-paper px-3 py-1 text-[13px] text-graphite"
                    >
                      {s}
                    </span>
                  ))}
                </div>
              </Link>
            </Reveal>
          ))}
        </div>
      </Section>

      <CtaBand />
    </>
  );
}
