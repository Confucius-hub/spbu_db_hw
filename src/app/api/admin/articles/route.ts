import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { isAdmin } from "@/lib/auth";
import { articleSchema } from "@/lib/validation";
import { readingTimeFromText, slugify } from "@/lib/utils";

export async function POST(req: Request) {
  if (!(await isAdmin())) {
    return NextResponse.json({ error: "Требуется авторизация" }, { status: 401 });
  }

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Некорректный запрос" }, { status: 400 });
  }

  const parsed = articleSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { error: "Проверьте поля", issues: parsed.error.flatten().fieldErrors },
      { status: 422 },
    );
  }
  const d = parsed.data;

  const exists = await prisma.article.findUnique({ where: { slug: d.slug } });
  if (exists) {
    return NextResponse.json({ error: "Статья с таким slug уже существует" }, { status: 409 });
  }

  const article = await prisma.article.create({
    data: {
      slug: d.slug,
      title: d.title,
      excerpt: d.excerpt,
      content: d.content,
      categoryId: d.categoryId,
      author: d.author || undefined,
      featured: d.featured,
      published: d.published,
      readingTime: readingTimeFromText(d.content),
      seoTitle: d.seoTitle || null,
      seoDescription: d.seoDescription || null,
      tags: {
        connectOrCreate: (d.tags ?? []).map((t) => ({
          where: { slug: slugify(t) },
          create: { slug: slugify(t), title: t },
        })),
      },
    },
  });

  return NextResponse.json({ ok: true, id: article.id }, { status: 201 });
}
