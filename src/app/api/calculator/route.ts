import { NextResponse } from "next/server";
import { calculatorSchema } from "@/lib/validation";
import { computeCalculator } from "@/lib/calculator";

export async function POST(req: Request) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Некорректный запрос" }, { status: 400 });
  }

  const parsed = calculatorSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      { error: "Проверьте входные данные", issues: parsed.error.flatten().fieldErrors },
      { status: 422 },
    );
  }

  return NextResponse.json({ ok: true, result: computeCalculator(parsed.data) });
}
