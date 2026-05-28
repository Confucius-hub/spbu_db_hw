/** Реестр документов организации (демо-данные; файлы подключаются в /public). */

export type DocItem = {
  title: string;
  category: string;
  format: "PDF" | "DOC" | "XLS";
  size: string;
  date: string;
  href: string;
};

export const documentCategories = [
  "Уставные документы",
  "Положения",
  "Стандарты",
  "Формы и бланки",
  "Реестры и отчётность",
] as const;

export const documents: DocItem[] = [
  {
    title: "Устав СРО «Строительный союз Северной столицы»",
    category: "Уставные документы",
    format: "PDF",
    size: "1,2 МБ",
    date: "2025-01-20",
    href: "#",
  },
  {
    title: "Свидетельство о регистрации в реестре НОСТРОЙ",
    category: "Уставные документы",
    format: "PDF",
    size: "640 КБ",
    date: "2010-06-30",
    href: "#",
  },
  {
    title: "Положение о компенсационном фонде возмещения вреда",
    category: "Положения",
    format: "PDF",
    size: "880 КБ",
    date: "2025-03-01",
    href: "#",
  },
  {
    title: "Положение о компенсационном фонде обеспечения договорных обязательств",
    category: "Положения",
    format: "PDF",
    size: "910 КБ",
    date: "2025-03-01",
    href: "#",
  },
  {
    title: "Положение о членстве, размере и порядке уплаты взносов",
    category: "Положения",
    format: "PDF",
    size: "1,0 МБ",
    date: "2026-03-01",
    href: "#",
  },
  {
    title: "Положение о контроле за деятельностью членов",
    category: "Положения",
    format: "PDF",
    size: "720 КБ",
    date: "2026-03-01",
    href: "#",
  },
  {
    title: "Стандарты и внутренние документы СРО",
    category: "Стандарты",
    format: "PDF",
    size: "2,4 МБ",
    date: "2025-09-15",
    href: "#",
  },
  {
    title: "Квалификационные стандарты специалистов",
    category: "Стандарты",
    format: "PDF",
    size: "1,1 МБ",
    date: "2025-09-15",
    href: "#",
  },
  {
    title: "Заявление о приёме в члены СРО",
    category: "Формы и бланки",
    format: "DOC",
    size: "85 КБ",
    date: "2026-03-01",
    href: "#",
  },
  {
    title: "Анкета члена СРО",
    category: "Формы и бланки",
    format: "DOC",
    size: "72 КБ",
    date: "2026-03-01",
    href: "#",
  },
  {
    title: "Форма уведомления о заключённом договоре подряда",
    category: "Формы и бланки",
    format: "DOC",
    size: "64 КБ",
    date: "2026-03-01",
    href: "#",
  },
  {
    title: "Реестр членов СРО (актуальная выписка)",
    category: "Реестры и отчётность",
    format: "XLS",
    size: "3,1 МБ",
    date: "2026-05-01",
    href: "#",
  },
  {
    title: "Годовой отчёт о деятельности за 2025 год",
    category: "Реестры и отчётность",
    format: "PDF",
    size: "4,5 МБ",
    date: "2026-04-10",
    href: "#",
  },
];
