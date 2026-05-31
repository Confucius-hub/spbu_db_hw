import type { Metadata } from "next";
import { existsSync } from "node:fs";
import { join } from "node:path";
import { Section } from "@/components/ui/section";
import { PageHeader } from "@/components/layout/page-header";
import { DocumentsExplorer } from "@/components/documents/documents-explorer";
import { Button } from "@/components/ui/button";
import { Cta } from "@/components/sections/cta";
import { Icon } from "@/lib/icons";
import { documents, documentCategories } from "@/lib/documents";
import { pageMetadata } from "@/lib/seo";

export const dynamic = "force-dynamic";

export const metadata: Metadata = pageMetadata({
  title: "Документы",
  description:
    "Уставные документы, положения, стандарты, формы и протоколы СРО «Строительный союз Северной столицы».",
  path: "/documents",
});

export default function DocumentsPage() {
  // Авто-определение: если файл реально лежит в public/docs/ — показываем «Скачать».
  const docsDir = join(process.cwd(), "public", "docs");
  const docs = documents.map((d) => ({
    ...d,
    href: existsSync(join(docsDir, d.file)) ? `/docs/${d.file}` : null,
  }));
  const availableCount = docs.filter((d) => d.href).length;
  return (
    <>
      <PageHeader
        eyebrow="Раскрытие информации"
        title="Документы"
        description="Уставные документы, положения, стандарты, протоколы и формы организации."
        breadcrumbs={[{ label: "Документы" }]}
      />

      <Section tone="muted">
        {/* Единый блок с пояснением и кнопкой запроса (вместо «Запросить» в каждой строке) */}
        <div className="mb-10 overflow-hidden rounded-2xl border border-navy-100 bg-gradient-to-br from-navy-50 to-white">
          <div className="flex flex-col gap-5 p-6 sm:flex-row sm:items-center sm:justify-between sm:p-7">
            <div className="flex items-start gap-4">
              <span className="inline-flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-navy-800 text-gold-400">
                <Icon name="Layers" className="h-6 w-6" />
              </span>
              <div>
                <p className="font-semibold text-navy-900">Не нашли нужный документ?</p>
                <p className="mt-1 text-sm text-slate-600">
                  {availableCount > 0
                    ? "Не все документы выложены в открытый доступ. Актуальную версию пришлёт менеджер по запросу."
                    : "Документы готовятся к публикации. Актуальную версию пришлёт менеджер по запросу."}
                </p>
              </div>
            </div>
            <Button href="/contacts" variant="primary" className="shrink-0">
              <Icon name="Mail" className="h-4 w-4" />
              Запросить документ
            </Button>
          </div>
        </div>

        <DocumentsExplorer documents={docs} categories={documentCategories} />
      </Section>

      <Cta />
    </>
  );
}
