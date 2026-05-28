import { Section } from "@/components/ui/section";
import { Button } from "@/components/ui/button";
import { NewsCard } from "@/components/news/news-card";
import { Icon } from "@/lib/icons";
import { getRecentArticles } from "@/lib/news";

export async function NewsTeaser() {
  const articles = await getRecentArticles(3);
  if (articles.length === 0) return null;

  return (
    <Section tone="white">
      <div className="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <div className="mb-3 inline-flex items-center gap-2 text-sm font-semibold uppercase tracking-[0.14em] text-gold-700">
            <span className="h-px w-6 bg-gold-400/70" />
            Новости и события
          </div>
          <h2 className="max-w-xl text-3xl font-bold text-navy-900 sm:text-4xl">
            Изменения в отрасли и жизнь СРО
          </h2>
        </div>
        <Button href="/news" variant="outline">
          Все новости
          <Icon name="ArrowRight" className="h-4 w-4" />
        </Button>
      </div>

      <div className="mt-10 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
        {articles.map((a) => (
          <NewsCard key={a.id} article={a} />
        ))}
      </div>

      <div className="mt-8 sm:hidden">
        <Button href="/news" variant="outline" className="w-full">
          Все новости
          <Icon name="ArrowRight" className="h-4 w-4" />
        </Button>
      </div>
    </Section>
  );
}
