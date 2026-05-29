import { Section } from "@/components/ui/section";
import { Icon } from "@/lib/icons";
import { relativeDate } from "@/lib/utils";
import { fetchIndustryNews } from "@/lib/industry-news";

/**
 * Живая лента отраслевых новостей (Google Новости RSS).
 * Если фид недоступен — секция не рендерится (никаких пустых блоков).
 */
export async function IndustryFeed() {
  const items = await fetchIndustryNews(6);
  if (items.length === 0) return null;

  return (
    <Section tone="white">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <div className="mb-3 inline-flex items-center gap-2 text-sm font-semibold uppercase tracking-[0.14em] text-gold-700">
            <span className="h-px w-6 bg-gold-400/70" />
            Лента отрасли
          </div>
          <h2 className="text-2xl font-bold text-navy-900 sm:text-3xl">
            Свежие новости строительной отрасли
          </h2>
        </div>
        <p className="inline-flex items-center gap-1.5 text-sm text-slate-500">
          <Icon name="Zap" className="h-4 w-4 text-gold-500" />
          Обновляется автоматически · источник: Google Новости
        </p>
      </div>

      <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {items.map((item, i) => (
          <a
            key={i}
            href={item.link}
            target="_blank"
            rel="noopener noreferrer"
            className="group flex flex-col rounded-2xl border border-slate-200 bg-white p-5 shadow-soft transition-all duration-300 hover:-translate-y-0.5 hover:border-gold-200 hover:shadow-card"
          >
            <div className="flex items-center justify-between gap-2">
              <span className="inline-flex items-center gap-1.5 rounded-full bg-navy-50 px-2.5 py-1 text-xs font-semibold text-navy-700">
                <Icon name="Newspaper" className="h-3.5 w-3.5" />
                {item.source}
              </span>
              <Icon
                name="ArrowUpRight"
                className="h-4 w-4 text-slate-300 transition-colors group-hover:text-gold-500"
              />
            </div>
            <p className="mt-3 flex-1 font-semibold leading-snug text-navy-900 group-hover:text-navy-700">
              {item.title}
            </p>
            {item.pubDate && (
              <p className="mt-3 inline-flex items-center gap-1.5 text-xs text-slate-400">
                <Icon name="Calendar" className="h-3.5 w-3.5" />
                {relativeDate(item.pubDate)}
              </p>
            )}
          </a>
        ))}
      </div>
    </Section>
  );
}
