/**
 * Живая лента реальных отраслевых новостей через RSS Google Новостей.
 * Это НЕ выдуманный контент: реальные свежие заголовки сторонних СМИ
 * с указанием источника и ссылкой на оригинал.
 *
 * Отказоустойчивость: при любой ошибке/недоступности возвращается [],
 * и блок на странице просто не показывается (сайт не ломается).
 *
 * Запрос настраивается через NEXT_PUBLIC_NEWS_QUERY (по умолчанию — тема СРО).
 */

export type IndustryItem = {
  title: string;
  link: string;
  source: string;
  pubDate: string | null;
};

const DEFAULT_QUERY = "СРО строительство НОСТРОЙ саморегулирование";

function decodeEntities(input: string): string {
  return input
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .trim();
}

function tag(block: string, name: string): string | null {
  const m = block.match(new RegExp(`<${name}[^>]*>([\\s\\S]*?)</${name}>`, "i"));
  return m ? decodeEntities(m[1]) : null;
}

/** Парсит RSS 2.0 (в т.ч. формат Google Новостей). Экспортируется для тестов. */
export function parseRss(xml: string, limit = 8): IndustryItem[] {
  const items: IndustryItem[] = [];
  const blocks = xml.match(/<item[\s\S]*?<\/item>/gi) ?? [];

  for (const block of blocks) {
    const rawTitle = tag(block, "title");
    const link = tag(block, "link");
    if (!rawTitle || !link) continue;

    const source = tag(block, "source") ?? "Источник";
    // У Google Новостей заголовок часто оканчивается на « - Издание» — убираем дубликат
    const title = rawTitle.replace(new RegExp(`\\s*[-–—]\\s*${escapeRe(source)}\\s*$`), "").trim();

    items.push({
      title: title || rawTitle,
      link,
      source,
      pubDate: tag(block, "pubDate"),
    });
    if (items.length >= limit) break;
  }
  return items;
}

function escapeRe(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

export function googleNewsUrl(query = process.env.NEXT_PUBLIC_NEWS_QUERY || DEFAULT_QUERY): string {
  const q = encodeURIComponent(query);
  return `https://news.google.com/rss/search?q=${q}&hl=ru&gl=RU&ceid=RU:ru`;
}

/** Загружает живую отраслевую ленту. Никогда не бросает — при ошибке возвращает []. */
export async function fetchIndustryNews(limit = 6): Promise<IndustryItem[]> {
  try {
    const res = await fetch(googleNewsUrl(), {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
        Accept: "application/rss+xml, application/xml, text/xml",
      },
      signal: AbortSignal.timeout(6000),
      // Кэшируем на 30 минут, чтобы лента была свежей, но не дёргать источник на каждый запрос
      next: { revalidate: 1800 },
    });
    if (!res.ok) return [];
    const xml = await res.text();
    return parseRss(xml, limit);
  } catch {
    return [];
  }
}
