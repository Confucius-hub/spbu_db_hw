import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/** Объединяет классы Tailwind, корректно разрешая конфликты. */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const dateFmt = new Intl.DateTimeFormat("ru-RU", {
  day: "numeric",
  month: "long",
  year: "numeric",
});

const dateFmtShort = new Intl.DateTimeFormat("ru-RU", {
  day: "2-digit",
  month: "2-digit",
  year: "numeric",
});

export function formatDate(date: Date | string): string {
  return dateFmt.format(new Date(date));
}

export function formatDateShort(date: Date | string): string {
  return dateFmtShort.format(new Date(date));
}

/** Опубликовано недавно (по умолчанию ≤ 10 дней) — для бейджа «Свежее». */
export function isRecent(date: Date | string, days = 10): boolean {
  const diff = Date.now() - new Date(date).getTime();
  return diff >= 0 && diff <= days * 24 * 60 * 60 * 1000;
}

/** Относительная дата: «сегодня», «вчера», «N дней назад» или полная дата. */
export function relativeDate(date: Date | string): string {
  const d = new Date(date);
  const days = Math.floor((Date.now() - d.getTime()) / (24 * 60 * 60 * 1000));
  if (days < 0) return formatDate(d);
  if (days === 0) return "сегодня";
  if (days === 1) return "вчера";
  if (days < 7) return `${days} ${pluralize(days, ["день", "дня", "дней"])} назад`;
  return formatDate(d);
}

/** Форматирует число в рубли без копеек: 300000 -> «300 000 ₽». */
export function formatCurrency(value: number): string {
  return new Intl.NumberFormat("ru-RU", {
    style: "currency",
    currency: "RUB",
    maximumFractionDigits: 0,
  }).format(value);
}

/** Детерминированный хеш строки в положительное число (для стабильного выбора фото). */
export function hashToInt(input: string, max = 100000): number {
  let h = 2166136261;
  for (let i = 0; i < input.length; i++) {
    h ^= input.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (Math.abs(h) % max) + 1;
}

/**
 * Маска российского телефона: форматирует ввод в «+7 (XXX) XXX-XX-XX».
 * Корректно обрабатывает ведущую 7/8 и частичный ввод.
 */
export function formatRuPhone(input: string): string {
  let digits = input.replace(/\D/g, "");
  if (!digits) return "";
  // Нормализуем код страны: ведущие 7 или 8 -> код «7»
  if (digits[0] === "8") digits = "7" + digits.slice(1);
  if (digits[0] !== "7") digits = "7" + digits;
  digits = digits.slice(0, 11); // 7 + 10 цифр

  const a = digits.slice(1, 4); // код
  const b = digits.slice(4, 7);
  const c = digits.slice(7, 9);
  const d = digits.slice(9, 11);

  let out = "+7";
  if (a) out += ` (${a}`;
  if (a.length === 3) out += ")";
  if (b) out += ` ${b}`;
  if (c) out += `-${c}`;
  if (d) out += `-${d}`;
  return out;
}

/** Русские склонения: pluralize(2, ['день','дня','дней']) -> 'дня'. */
export function pluralize(n: number, forms: [string, string, string]): string {
  const abs = Math.abs(n) % 100;
  const n1 = abs % 10;
  if (abs > 10 && abs < 20) return forms[2];
  if (n1 > 1 && n1 < 5) return forms[1];
  if (n1 === 1) return forms[0];
  return forms[2];
}

/** Оценка времени чтения по числу слов. */
export function readingTimeFromText(text: string): number {
  const words = text.trim().split(/\s+/).length;
  return Math.max(1, Math.round(words / 180));
}

/** Транслитерация и slug из произвольной строки (для админки). */
export function slugify(input: string): string {
  const map: Record<string, string> = {
    а: "a", б: "b", в: "v", г: "g", д: "d", е: "e", ё: "e", ж: "zh",
    з: "z", и: "i", й: "y", к: "k", л: "l", м: "m", н: "n", о: "o",
    п: "p", р: "r", с: "s", т: "t", у: "u", ф: "f", х: "h", ц: "ts",
    ч: "ch", ш: "sh", щ: "sch", ъ: "", ы: "y", ь: "", э: "e", ю: "yu", я: "ya",
  };
  return input
    .toLowerCase()
    .split("")
    .map((ch) => map[ch] ?? ch)
    .join("")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}
