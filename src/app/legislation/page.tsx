import type { Metadata } from "next";
import { Section } from "@/components/ui/section";
import { PageHeader } from "@/components/layout/page-header";
import { Cta } from "@/components/sections/cta";
import { Icon } from "@/lib/icons";
import { laws } from "@/lib/legislation";
import { media } from "@/lib/site";
import { pageMetadata } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "Законодательство",
  description:
    "Нормативно-правовая база саморегулирования в строительстве: законы о СРО, Градостроительный кодекс, требования к членам СРО и перечни видов работ.",
  path: "/legislation",
});

export default function LegislationPage() {
  return (
    <>
      <PageHeader
        eyebrow="Нормативная база"
        title="Законодательство"
        description="Основные федеральные законы и нормативные акты, регулирующие деятельность саморегулируемых организаций в строительстве."
        breadcrumbs={[{ label: "Законодательство" }]}
        image={media.documents}
      />

      <Section tone="muted">
        <div className="mx-auto max-w-4xl space-y-3">
          {laws.map((law, i) => (
            <a
              key={i}
              href={law.href}
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-start gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-soft transition-all hover:-translate-y-0.5 hover:border-gold-200 hover:shadow-card"
            >
              <span className="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-navy-800 text-gold-400">
                <Icon name="Scale" className="h-5 w-5" />
              </span>
              <div className="min-w-0 flex-1">
                <p className="font-semibold leading-snug text-navy-900 group-hover:text-navy-700">
                  {law.title}
                </p>
                {law.note && <p className="mt-1 text-sm text-slate-500">{law.note}</p>}
              </div>
              <span className="mt-1 inline-flex shrink-0 items-center gap-1.5 text-sm font-semibold text-navy-700 transition-colors group-hover:text-gold-700">
                <span className="hidden sm:inline">Читать</span>
                <Icon name="ExternalLink" className="h-4 w-4" />
              </span>
            </a>
          ))}
        </div>

        <p className="mx-auto mt-6 max-w-4xl text-xs text-slate-500">
          Ссылки ведут на официальные тексты нормативных актов. Актуальную редакцию документов и
          разъяснения по применению можно запросить у специалистов СРО.
        </p>
      </Section>

      <Cta
        title="Нужна помощь с применением требований?"
        text="Юристы СРО «СССС» проконсультируют по нормативной базе и помогут привести документацию в соответствие."
      />
    </>
  );
}
