/**
 * Перечень документов организации.
 * Это стандартные документы, обязательные для любой СРО в реестре НОСТРОЙ.
 * Файлы (PDF) добавляются в каталог /public по мере публикации; до этого
 * документ можно запросить через форму обратной связи.
 */

export type DocItem = {
  title: string;
  category: string;
  format: "PDF" | "DOC" | "XLS";
  /** Ссылка на файл; если файла ещё нет — null (показывается кнопка «Запросить»). */
  href: string | null;
};

export const documentCategories = [
  "Учредительные документы",
  "Положения",
  "Стандарты",
  "Протоколы",
  "Формы и бланки",
] as const;

export const documents: DocItem[] = [
  { title: "Устав Ассоциации «Строительный союз Северной столицы»", category: "Учредительные документы", format: "PDF", href: null },
  { title: "Выписка из реестра НОСТРОЙ (СРО-С-335-25122025)", category: "Учредительные документы", format: "PDF", href: null },
  { title: "Свидетельство о государственной регистрации", category: "Учредительные документы", format: "PDF", href: null },

  { title: "Положение о компенсационном фонде возмещения вреда", category: "Положения", format: "PDF", href: null },
  { title: "Положение о компенсационном фонде обеспечения договорных обязательств", category: "Положения", format: "PDF", href: null },
  { title: "Положение о членстве, размере и порядке уплаты взносов", category: "Положения", format: "PDF", href: null },
  { title: "Положение о контроле за деятельностью членов", category: "Положения", format: "PDF", href: null },
  { title: "Положение о мерах дисциплинарного воздействия", category: "Положения", format: "PDF", href: null },

  { title: "Квалификационные стандарты специалистов", category: "Стандарты", format: "PDF", href: null },
  { title: "Стандарты и правила саморегулирования", category: "Стандарты", format: "PDF", href: null },

  { title: "Протоколы общих собраний членов", category: "Протоколы", format: "PDF", href: null },
  { title: "Протоколы заседаний коллегиального органа управления", category: "Протоколы", format: "PDF", href: null },

  { title: "Заявление о приёме в члены СРО", category: "Формы и бланки", format: "DOC", href: null },
  { title: "Анкета члена СРО", category: "Формы и бланки", format: "DOC", href: null },
  { title: "Форма уведомления о заключённом договоре подряда", category: "Формы и бланки", format: "DOC", href: null },
];
