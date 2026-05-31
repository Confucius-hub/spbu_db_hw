/**
 * Реестр документов СРО. Структура и названия адаптированы с официального сайта
 * sro-ssss.ru (разделы «Учредительные документы» и «Протоколы»), оформление
 * улучшено: карточки, группировка, даты размещения/редакции, прямые скачивания.
 *
 * Файлы лежат в /public/docs/. Имя файла — поле `file`. Реальные PDF можно
 * заменить, положив одноимённые файлы. Содержимое НЕ выдумывается: PDF —
 * официальные информационные листы с реквизитами и пометкой о запросе.
 */

export type DocItem = {
  title: string;
  category: string;
  format: "PDF" | "DOC" | "XLS";
  file: string;
  /** Дата размещения (как на исходном сайте). */
  date?: string;
  /** Дата последней редакции. */
  edition?: string;
  /** Доп. подпись. */
  note?: string;
  /** Заполняется автоматически на сервере, если файл найден в public/docs/. */
  href?: string | null;
};

export const documentCategories = [
  "Учредительные документы",
  "Протоколы общего собрания",
  "Протоколы совета ассоциации",
  "Формы и бланки",
] as const;

const C = "Учредительные документы";
const OS = "Протоколы общего собрания";
const SA = "Протоколы совета ассоциации";
const F = "Формы и бланки";

export const documents: DocItem[] = [
  // ——— Учредительные документы (реальные названия с sro-ssss.ru) ———
  { title: "Устав Ассоциации", category: C, format: "PDF", file: "ustav.pdf", date: "16.01.2026", edition: "16.01.2026" },
  { title: "ИНН СССС", category: C, format: "PDF", file: "inn.pdf", date: "16.01.2026", edition: "16.01.2026" },
  { title: "Свидетельство Минюст", category: C, format: "PDF", file: "svidetelstvo-minust.pdf", date: "16.01.2026", edition: "16.01.2026" },
  { title: "С-335. Уведомление о включении в реестр РТН", category: C, format: "PDF", file: "s335-uvedomlenie-rtn.pdf", date: "16.01.2026", edition: "16.01.2026" },
  { title: "С-335. Выписка из реестра РТН", category: C, format: "PDF", file: "s335-vypiska-rtn.pdf", date: "16.01.2026", edition: "16.01.2026" },
  { title: "Лист записи Ассоциация СССС", category: C, format: "PDF", file: "list-zapisi.pdf", date: "16.01.2026", edition: "16.01.2026" },
  { title: "Домен", category: C, format: "PDF", file: "domen.pdf", date: "16.01.2026", edition: "16.01.2026" },

  // ——— Протоколы общего собрания (реальные номера и даты) ———
  { title: "Протокол ОС № 5 от 10.04.2026", category: OS, format: "PDF", file: "protokol-os-5.pdf", date: "10.04.2026", edition: "10.04.2026" },
  { title: "Протокол ОС № 4 от 14.01.2026", category: OS, format: "PDF", file: "protokol-os-4.pdf", date: "14.01.2026", edition: "14.01.2026" },
  { title: "Протокол ОС № 3 от 27.11.2025", category: OS, format: "PDF", file: "protokol-os-3.pdf", date: "27.11.2025", edition: "27.11.2025" },
  { title: "Протокол ОС № 2 от 29.07.2025", category: OS, format: "PDF", file: "protokol-os-2.pdf", date: "29.07.2025", edition: "29.07.2025" },
  { title: "Протокол ОС № 1 от 07.05.2025", category: OS, format: "PDF", file: "protokol-os-1.pdf", date: "07.05.2025", edition: "07.05.2025" },

  // ——— Протоколы совета ассоциации (реальные номера и даты) ———
  { title: "Протокол СА № 27 от 18.05.2026", category: SA, format: "PDF", file: "protokol-sa-27.pdf", date: "18.05.2026", edition: "18.05.2026" },
  { title: "Протокол СА № 26 от 15.05.2026", category: SA, format: "PDF", file: "protokol-sa-26.pdf", date: "15.05.2026", edition: "15.05.2026" },
  { title: "Протокол СА № 25 от 14.05.2026", category: SA, format: "PDF", file: "protokol-sa-25.pdf", date: "14.05.2026", edition: "14.05.2026" },
  { title: "Протокол СА № 24 от 27.04.2026", category: SA, format: "PDF", file: "protokol-sa-24.pdf", date: "27.04.2026", edition: "27.04.2026" },
  { title: "Протокол СА № 23 от 09.04.2026", category: SA, format: "PDF", file: "protokol-sa-23.pdf", date: "09.04.2026", edition: "09.04.2026" },
  { title: "Протокол СА № 22 от 08.04.2026", category: SA, format: "PDF", file: "protokol-sa-22.pdf", date: "08.04.2026", edition: "08.04.2026" },
  { title: "Протокол СА № 21 от 30.03.2026", category: SA, format: "PDF", file: "protokol-sa-21.pdf", date: "30.03.2026", edition: "30.03.2026" },
  { title: "Протокол СА № 20 от 27.03.2026", category: SA, format: "PDF", file: "protokol-sa-20.pdf", date: "27.03.2026", edition: "27.03.2026" },
  { title: "Протокол СА № 19 от 25.03.2026", category: SA, format: "PDF", file: "protokol-sa-19.pdf", date: "25.03.2026", edition: "25.03.2026" },

  // ——— Формы и бланки для вступления (реальные, со «скачать») ———
  { title: "Заявление на вступление", category: F, format: "PDF", file: "zayavlenie-priem.pdf", note: "Форма для заполнения" },
  { title: "Доверенность на ведение дел", category: F, format: "PDF", file: "doverennost.pdf", note: "Форма для заполнения" },
  { title: "Согласие на обработку персональных данных", category: F, format: "PDF", file: "soglasie-pdn.pdf", note: "Форма для заполнения" },
  { title: "Сведения о квалификации специалистов", category: F, format: "PDF", file: "svedenia-kvalifikacia.pdf", note: "Форма для заполнения" },
];
