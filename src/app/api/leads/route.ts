import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { leadSchema } from "@/lib/validation";
import { notifyLead } from "@/lib/notify";

export async function POST(req: Request) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Некорректный запрос" }, { status: 400 });
  }

  const parsed = leadSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { error: "Проверьте корректность полей", issues: parsed.error.flatten().fieldErrors },
      { status: 422 },
    );
  }

  const data = parsed.data;
  try {
    const lead = await prisma.lead.create({
      data: {
        type: data.type,
        name: data.name,
        phone: data.phone,
        email: data.email || null,
        company: data.company || null,
        message: data.message || null,
        source: data.source || null,
        payload: data.payload ? JSON.stringify(data.payload) : null,
      },
    });
    // Уведомление в Telegram (если настроено) — не блокирует ответ при сбое
    await notifyLead(data);
    return NextResponse.json({ ok: true, id: lead.id }, { status: 201 });
  } catch {
    return NextResponse.json({ error: "Не удалось сохранить заявку" }, { status: 500 });
  }
}
