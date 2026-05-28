"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Icon } from "@/lib/icons";
import { slugify, cn } from "@/lib/utils";

type Category = { id: string; title: string };

export type ArticleInitial = {
  id?: string;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  categoryId: string;
  author?: string;
  tags: string[];
  featured: boolean;
  published: boolean;
  seoTitle?: string;
  seoDescription?: string;
};

const field =
  "w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-[0.95rem] text-navy-900 focus:border-gold-400 focus:outline-none focus:ring-2 focus:ring-gold-200";
const label = "mb-1.5 block text-sm font-medium text-slate-700";

export function ArticleEditor({
  categories,
  initial,
}: {
  categories: Category[];
  initial?: ArticleInitial;
}) {
  const router = useRouter();
  const isEdit = Boolean(initial?.id);

  const [form, setForm] = useState<ArticleInitial>(
    initial ?? {
      title: "",
      slug: "",
      excerpt: "",
      content: "",
      categoryId: categories[0]?.id ?? "",
      author: "",
      tags: [],
      featured: false,
      published: true,
      seoTitle: "",
      seoDescription: "",
    },
  );
  const [tagsText, setTagsText] = useState((initial?.tags ?? []).join(", "));
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const set = <K extends keyof ArticleInitial>(key: K, value: ArticleInitial[K]) =>
    setForm((f) => ({ ...f, [key]: value }));

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const payload = {
      ...form,
      slug: form.slug || slugify(form.title),
      author: form.author || undefined,
      tags: tagsText
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean),
    };

    const url = isEdit ? `/api/admin/articles/${initial!.id}` : "/api/admin/articles";
    try {
      const res = await fetch(url, {
        method: isEdit ? "PUT" : "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.error ?? "Не удалось сохранить");
      }
      router.push("/admin/news");
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка");
      setLoading(false);
    }
  }

  return (
    <form onSubmit={submit} className="grid gap-6 lg:grid-cols-[1fr_18rem]">
      {/* Основное */}
      <div className="space-y-5">
        <div>
          <label className={label}>Заголовок</label>
          <input
            className={field}
            value={form.title}
            onChange={(e) => {
              const title = e.target.value;
              set("title", title);
              if (!isEdit && (!form.slug || form.slug === slugify(form.title)))
                set("slug", slugify(title));
            }}
            placeholder="Заголовок статьи"
            required
          />
        </div>

        <div>
          <label className={label}>Slug (URL)</label>
          <div className="flex gap-2">
            <input
              className={field}
              value={form.slug}
              onChange={(e) => set("slug", e.target.value)}
              placeholder="slug-stati"
              required
            />
            <button
              type="button"
              onClick={() => set("slug", slugify(form.title))}
              className="shrink-0 rounded-xl border border-slate-200 px-3 text-sm font-medium text-navy-700 hover:bg-slate-50"
            >
              Из заголовка
            </button>
          </div>
        </div>

        <div>
          <label className={label}>Краткое описание</label>
          <textarea
            className={cn(field, "resize-none")}
            rows={2}
            value={form.excerpt}
            onChange={(e) => set("excerpt", e.target.value)}
            placeholder="1–2 предложения для карточки и SEO"
            required
          />
        </div>

        <div>
          <label className={label}>Текст статьи (Markdown)</label>
          <textarea
            className={cn(field, "min-h-[24rem] resize-y font-mono text-sm leading-relaxed")}
            value={form.content}
            onChange={(e) => set("content", e.target.value)}
            placeholder={"## Подзаголовок\n\nАбзац текста…\n\n- Пункт списка"}
            required
          />
          <p className="mt-1.5 text-xs text-slate-400">
            Поддерживается Markdown: ## заголовки, **жирный**, списки, &gt; цитаты.
          </p>
        </div>
      </div>

      {/* Сайдбар настроек */}
      <div className="space-y-5">
        <div className="rounded-2xl border border-slate-200 bg-white p-5">
          {error && (
            <p className="mb-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>
          )}
          <Button type="submit" variant="primary" className="w-full" disabled={loading}>
            <Icon name="Check" className="h-4 w-4" strokeWidth={2.5} />
            {loading ? "Сохранение…" : isEdit ? "Сохранить" : "Опубликовать"}
          </Button>
          <button
            type="button"
            onClick={() => router.push("/admin/news")}
            className="mt-2 w-full rounded-xl px-4 py-2 text-sm font-medium text-slate-500 hover:bg-slate-50"
          >
            Отмена
          </button>
        </div>

        <div className="space-y-4 rounded-2xl border border-slate-200 bg-white p-5">
          <div>
            <label className={label}>Рубрика</label>
            <select
              className={field}
              value={form.categoryId}
              onChange={(e) => set("categoryId", e.target.value)}
              required
            >
              {categories.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.title}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className={label}>Теги (через запятую)</label>
            <input
              className={field}
              value={tagsText}
              onChange={(e) => setTagsText(e.target.value)}
              placeholder="309-ФЗ, НОСТРОЙ"
            />
          </div>

          <div>
            <label className={label}>Автор</label>
            <input
              className={field}
              value={form.author ?? ""}
              onChange={(e) => set("author", e.target.value)}
              placeholder="Пресс-служба СРО «СССС»"
            />
          </div>

          <label className="flex cursor-pointer items-center gap-3">
            <input
              type="checkbox"
              checked={form.featured}
              onChange={(e) => set("featured", e.target.checked)}
              className="h-4 w-4 accent-gold-500"
            />
            <span className="text-sm text-slate-700">В избранное (на главную)</span>
          </label>

          <label className="flex cursor-pointer items-center gap-3">
            <input
              type="checkbox"
              checked={form.published}
              onChange={(e) => set("published", e.target.checked)}
              className="h-4 w-4 accent-gold-500"
            />
            <span className="text-sm text-slate-700">Опубликовано</span>
          </label>
        </div>

        <details className="rounded-2xl border border-slate-200 bg-white p-5">
          <summary className="cursor-pointer text-sm font-semibold text-navy-900">
            SEO (необязательно)
          </summary>
          <div className="mt-4 space-y-4">
            <div>
              <label className={label}>SEO Title</label>
              <input
                className={field}
                value={form.seoTitle ?? ""}
                onChange={(e) => set("seoTitle", e.target.value)}
              />
            </div>
            <div>
              <label className={label}>SEO Description</label>
              <textarea
                className={cn(field, "resize-none")}
                rows={3}
                value={form.seoDescription ?? ""}
                onChange={(e) => set("seoDescription", e.target.value)}
              />
            </div>
          </div>
        </details>
      </div>
    </form>
  );
}
