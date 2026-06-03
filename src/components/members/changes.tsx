import { Section, SectionHeading } from "@/components/ui/section";
import { Card } from "@/components/ui/card";
import { Icon } from "@/lib/icons";

/**
 * Раздел «Внесение изменений в реестр членов СРО» (с исходного сайта).
 * Содержит реальную форму со скачиванием — заявление от ЮЛ.
 */
export function MembersChanges() {
  return (
    <Section tone="white" id="changes">
      <SectionHeading
        align="left"
        eyebrow="Изменения в реестре"
        title="Внесение изменений в реестр членов СРО"
        description="Для актуализации сведений о компании в реестре подайте заполненное заявление по форме."
      />

      <Card className="mt-8 overflow-hidden">
        <div className="hidden items-center gap-4 border-b border-slate-100 bg-slate-50/60 px-5 py-2.5 text-[0.65rem] font-semibold uppercase tracking-wider text-slate-400 md:flex">
          <span className="h-12 w-12 shrink-0" />
          <span className="flex-1">Документ</span>
          <span className="w-24 text-center">Размещено</span>
          <span className="w-24 text-center">Редакция</span>
          <span className="w-28 text-center">Файл</span>
        </div>
        <a
          href="/docs/zayavlenie-izmenenia.pdf"
          target="_blank"
          rel="noopener"
          className="group flex flex-wrap items-center gap-4 px-5 py-4 transition-colors hover:bg-gold-50/40"
        >
          <span className="inline-flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-red-50 text-xs font-bold text-red-600 ring-1 ring-red-100">
            PDF
          </span>
          <span className="min-w-0 flex-1">
            <span className="block font-medium text-navy-900 group-hover:text-navy-700">
              Заявление ЮЛ. Внесение изменений в реестр членов СРО
            </span>
          </span>
          <span className="hidden w-24 text-center text-sm font-medium text-slate-600 md:inline-block">
            16.01.2026
          </span>
          <span className="hidden w-24 text-center text-sm font-medium text-slate-600 md:inline-block">
            16.01.2026
          </span>
          <span className="inline-flex w-28 shrink-0 items-center justify-center gap-1.5 rounded-xl bg-navy-50 py-2 text-sm font-semibold text-navy-800 transition-colors group-hover:bg-gold-100 group-hover:text-gold-800">
            <Icon name="Download" className="h-4 w-4" />
            Скачать
          </span>
        </a>
      </Card>

      <p className="mt-4 text-xs text-slate-500">
        Дата публикации: 16.01.2026 · Последнее изменение: 19.01.2026
      </p>
    </Section>
  );
}
