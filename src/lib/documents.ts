/**
 * Перечень официальных документов СРО (стандартный набор для СРО в реестре НОСТРОЙ).
 *
 * Прямые скачивания работают по принципу «положил файл — появилась кнопка Скачать»:
 *   1) скачайте PDF со своего сайта sro-ssss.ru (раздел «Учредительные документы»,
 *      «Протоколы» и т.д.) — у вас есть к нему доступ;
 *   2) положите файл в каталог public/docs/ с именем из поля `file` ниже;
 *   3) страница «Документы» сама определит наличие файла и покажет «Скачать»
 *      (см. логику в src/app/documents/page.tsx). Править код не нужно.
 *
 * Пока файла нет — документ помечен «Готовится», строка кликабельна и ведёт на
 * запрос актуальной версии. Содержимое документов НЕ выдумывается.
 */

export type DocItem = {
  title: string;
  category: string;
  format: "PDF" | "DOC" | "XLS";
  /** Имя файла в public/docs/. Если файл присутствует — появится кнопка «Скачать». */
  file: string;
  /** Опциональная подпись под названием. */
  note?: string;
  /** Заполняется автоматически на сервере, если файл найден в public/docs/. */
  href?: string | null;
};

export const documentCategories = [
  "Учредительные документы",
  "Положения",
  "Стандарты",
  "Протоколы",
  "Формы и бланки",
] as const;

export const documents: DocItem[] = [
  // Учредительные документы
  { title: "Устав Ассоциации «Строительный союз Северной столицы»", category: "Учредительные документы", format: "PDF", file: "ustav.pdf" },
  { title: "Выписка из реестра НОСТРОЙ", category: "Учредительные документы", format: "PDF", file: "vypiska-nostroy.pdf", note: "СРО-С-335-25122025 · 25.12.2025" },
  { title: "Свидетельство о государственной регистрации", category: "Учредительные документы", format: "PDF", file: "svidetelstvo.pdf" },

  // Положения
  { title: "Положение о компенсационном фонде возмещения вреда", category: "Положения", format: "PDF", file: "polozhenie-kf-vv.pdf" },
  { title: "Положение о компенсационном фонде обеспечения договорных обязательств", category: "Положения", format: "PDF", file: "polozhenie-kf-odo.pdf" },
  { title: "Положение о членстве, размере и порядке уплаты взносов", category: "Положения", format: "PDF", file: "polozhenie-chlenstvo.pdf" },
  { title: "Положение о контроле за деятельностью членов СРО", category: "Положения", format: "PDF", file: "polozhenie-kontrol.pdf" },
  { title: "Положение о мерах дисциплинарного воздействия", category: "Положения", format: "PDF", file: "polozhenie-disciplina.pdf" },

  // Стандарты
  { title: "Квалификационные стандарты специалистов", category: "Стандарты", format: "PDF", file: "standarty-kvalifikacia.pdf" },
  { title: "Стандарты и правила саморегулирования", category: "Стандарты", format: "PDF", file: "standarty-pravila.pdf" },

  // Протоколы
  { title: "Протоколы общих собраний членов", category: "Протоколы", format: "PDF", file: "protokoly-sobrania.pdf" },
  { title: "Протоколы заседаний коллегиального органа управления", category: "Протоколы", format: "PDF", file: "protokoly-kollegial.pdf" },

  // Формы и бланки
  { title: "Заявление о приёме в члены СРО", category: "Формы и бланки", format: "PDF", file: "zayavlenie-priem.pdf" },
  { title: "Анкета члена СРО", category: "Формы и бланки", format: "PDF", file: "anketa.pdf" },
  { title: "Форма уведомления о заключённом договоре подряда", category: "Формы и бланки", format: "PDF", file: "uvedomlenie-dogovor.pdf" },
];
