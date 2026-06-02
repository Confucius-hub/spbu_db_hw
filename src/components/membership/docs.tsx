import Link from "next/link";
import { Section, SectionHeading } from "@/components/ui/section";
import { Icon } from "@/lib/icons";

type DocLine = {
  text: string;
  /** Если задано — рядом со строкой будет ссылка «Скачать». */
  download?: string;
  /** Помечает строки, актуальные только для ИП / только для юр.лиц. */
  for?: "ИП" | "ЮЛ";
};

/**
 * Реальный список «Документы для вступления» с sro-ssss.ru/vsro/Dokumenty-dlja-vstuplenija.
 * Содержание не выдумано. Ссылки «Скачать» подставляются только там, где у нас есть
 * соответствующий PDF в /public/docs/.
 */
const COMMON: DocLine[] = [
  { text: "Заявление на вступление", download: "/docs/zayavlenie-priem.pdf" },
  { text: "Копия свидетельства ОГРН или копия свидетельства о внесении записи в ЕГРЮЛ о юридическом лице, зарегистрированном до 01.07.2002 г." },
  { text: "Копия свидетельства о постановке на учёт в налоговом органе (ИНН)" },
  { text: "Копия последней редакции Устава" },
  { text: "Доверенность на ведение дел, связанных с приёмом в Ассоциацию, либо иной документ, подтверждающий полномочия заявителя", download: "/docs/doverennost.pdf" },
  { text: "Решение, подтверждающее полномочия руководителя" },
  { text: "Копии Свидетельства о государственной регистрации физического лица в качестве индивидуального предпринимателя", for: "ИП" },
  { text: "Копии Свидетельства о постановке на учёт в налоговом органе физического лица в качестве индивидуального предпринимателя", for: "ИП" },
  { text: "Копия паспорта", for: "ИП" },
  { text: "Согласие на обработку персональных данных (для индивидуального предпринимателя)", download: "/docs/soglasie-pdn.pdf" },
  { text: "Копии Уведомлений о включении не менее двух специалистов в Национальный реестр специалистов Ассоциации «Национальное объединение строителей» (НРС)" },
  { text: "Копии дипломов о высшем образовании работников, осуществляющих строительство, реконструкцию, капитальный ремонт объектов капитального строительства" },
  { text: "Копии трудовых книжек (выписки)" },
  { text: "Копии свидетельств о прохождении Независимой оценки квалификации" },
  { text: "Сведения о квалификации специалистов", download: "/docs/svedenia-kvalifikacia.pdf" },
];

const OPO: DocLine[] = [
  { text: "Документ, подтверждающий наличие системы контроля качества: положение, приказы на ответственных лиц, инструкция либо иной документ, регламентирующий систему контроля качества в организации" },
  { text: "Документ, подтверждающий наличие необходимого имущества и оборудования для выполнения работ на ОПО" },
  { text: "Копии Уведомлений о включении специалистов в НРС с соответствующим стажем работы на особо опасных, технически сложных и уникальных объектах" },
];

function ForBadge({ kind }: { kind: "ИП" | "ЮЛ" }) {
  return (
    <span className="ml-2 inline-flex items-center rounded-full bg-gold-100 px-2 py-0.5 text-[0.65rem] font-semibold text-gold-800 ring-1 ring-gold-200">
      только для {kind}
    </span>
  );
}

function Row({ line, n }: { line: DocLine; n: number }) {
  return (
    <li className="flex items-start gap-4 border-t border-slate-100 py-3.5 first:border-t-0">
      <span className="mt-0.5 inline-flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-navy-50 text-xs font-bold text-navy-800">
        {n}
      </span>
      <div className="flex-1">
        <span className="text-[0.95rem] leading-relaxed text-slate-700">{line.text}</span>
        {line.for && <ForBadge kind={line.for} />}
      </div>
      {line.download ? (
        <a
          href={line.download}
          target="_blank"
          rel="noopener"
          className="inline-flex shrink-0 items-center gap-1.5 rounded-xl bg-navy-50 px-3 py-1.5 text-xs font-semibold text-navy-800 transition-colors hover:bg-gold-100 hover:text-gold-800"
        >
          <Icon name="Download" className="h-3.5 w-3.5" />
          Скачать
        </a>
      ) : (
        <span className="hidden shrink-0 sm:inline-block sm:w-[5.5rem]" />
      )}
    </li>
  );
}

export function MembershipDocs() {
  return (
    <Section tone="muted" id="documents">
      <SectionHeading
        align="left"
        eyebrow="Документы для вступления"
        title="Что нужно подготовить"
        description="Перечень документов для подачи заявки на вступление в Ассоциацию. Формы со ссылкой «Скачать» можно сразу заполнить."
      />

      {/* Основной список */}
      <div className="mt-8 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-soft">
        <div className="border-b border-slate-100 bg-slate-50/60 px-6 py-3">
          <p className="text-sm font-semibold text-navy-900">
            Общий пакет
            <span className="ml-2 text-xs font-normal text-slate-500">{COMMON.length} пунктов</span>
          </p>
        </div>
        <ol className="px-6 py-2">
          {COMMON.map((line, i) => (
            <Row key={i} line={line} n={i + 1} />
          ))}
        </ol>
      </div>

      {/* Дополнительный пакет для ОПО */}
      <div className="mt-6 overflow-hidden rounded-2xl border border-gold-200 bg-gradient-to-br from-gold-50/40 to-white shadow-soft">
        <div className="flex items-center gap-3 border-b border-gold-100 bg-gold-50/60 px-6 py-3">
          <Icon name="HardHat" className="h-5 w-5 text-gold-700" />
          <p className="text-sm font-semibold text-navy-900">
            Дополнительно для работ на ОПО, технически сложных и объектах атомной энергии
          </p>
        </div>
        <ol className="px-6 py-2">
          {OPO.map((line, i) => (
            <Row key={i} line={line} n={COMMON.length + i + 1} />
          ))}
        </ol>
      </div>

      {/* Помощь */}
      <div className="mt-6 flex flex-col gap-3 rounded-2xl border border-navy-100 bg-navy-50/60 p-5 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-start gap-3">
          <Icon name="MessagesSquare" className="mt-0.5 h-5 w-5 shrink-0 text-navy-700" />
          <p className="text-sm text-slate-700">
            Поможем подготовить полный пакет и проверим комплектность до подачи — без скрытых платежей.
          </p>
        </div>
        <Link
          href="/contacts"
          className="inline-flex shrink-0 items-center gap-1.5 rounded-xl bg-navy-800 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-navy-700"
        >
          Связаться с менеджером
          <Icon name="ArrowRight" className="h-4 w-4" />
        </Link>
      </div>
    </Section>
  );
}
