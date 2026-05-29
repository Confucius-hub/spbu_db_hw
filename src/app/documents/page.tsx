import type { Metadata } from "next";
import { Section } from "@/components/ui/section";
import { PageHeader } from "@/components/layout/page-header";
import { DocumentsExplorer } from "@/components/documents/documents-explorer";
import { Cta } from "@/components/sections/cta";
import { Icon } from "@/lib/icons";
import { documents, documentCategories } from "@/lib/documents";
import { pageMetadata } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "Документы",
  description:
    "Уставные документы, положения, стандарты, формы и реестры СРО «Строительный союз Северной столицы».",
  path: "/documents",
});

export default function DocumentsPage() {
  return (
    <>
      <PageHeader
        eyebrow="Раскрытие информации"
        title="Документы"
        description="Уставные документы, положения, стандарты, формы и реестры организации. Доступны для скачивания."
        breadcrumbs={[{ label: "Документы" }]}
      />

      <Section tone="muted">
        <div className="mb-8 flex items-start gap-3 rounded-2xl border border-navy-100 bg-navy-50 p-5">
          <Icon name="Layers" className="mt-0.5 h-5 w-5 shrink-0 text-navy-700" />
          <p className="text-sm text-slate-600">
            Здесь публикуются документы, подлежащие обязательному раскрытию. Если нужный документ
            или выписка ещё не выложены — нажмите «Запросить», и мы направим актуальную версию.
          </p>
        </div>
        <DocumentsExplorer documents={documents} categories={documentCategories} />
      </Section>

      <Cta title="Не нашли нужный документ?" text="Свяжитесь с нами — подскажем и направим актуальную форму или выписку." />
    </>
  );
}
