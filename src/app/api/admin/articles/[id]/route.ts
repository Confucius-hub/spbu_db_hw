import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { isAdmin } from "@/lib/auth";
import { articleSchema } from "@/lib/validation";
import { readingTimeFromText, slugify } from "@/lib/utils";

export async function PUT(req: Request, { params }: { params: Promise<{ id: string }> }) {
  if (!(await isAdmin())) {
    return NextResponse.json({ error: "Требуется авторизация" }, { status: 401 });
  }
  const { id } = await params;

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

  const clash = await prisma.article.findFirst({
    where: { slug: d.slug, NOT: { id } },
  });
  if (clash) {
    return NextResponse.json({ error: "Slug занят другой статьёй" }, { status: 409 });
  }

  try {
    await prisma.article.update({
      where: { id },
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
          set: [],
          connectOrCreate: (d.tags ?? []).map((t) => ({
            where: { slug: slugify(t) },
            create: { slug: slugify(t), title: t },
          })),
        },
      },
    });
    return NextResponse.json({ ok: true });
  } catch {
    return NextResponse.json({ error: "Статья не найдена" }, { status: 404 });
  }
}

export async function DELETE(_req: Request, { params }: { params: Promise<{ id: string }> }) {
  if (!(await isAdmin())) {
    return NextResponse.json({ error: "Требуется авторизация" }, { status: 401 });
  }
  const { id } = await params;
  try {
    await prisma.article.delete({ where: { id } });
    return NextResponse.json({ ok: true });
  } catch {
    return NextResponse.json({ error: "Статья не найдена" }, { status: 404 });
  }
}
