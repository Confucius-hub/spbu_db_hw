import { NextResponse, type NextRequest } from "next/server";
import { contactSchema, type ContactErrors } from "@/lib/validation/contact";
import { submitLead } from "@/lib/services/contact-service";

export const runtime = "nodejs";

/**
 * HTTP layer for contact leads:
 *   parse → rate-limit → validate (zod) → service → response
 * Keeps transport concerns out of the service layer.
 */

// --- Naive in-memory rate limiter (swap for Redis in production) ---
const WINDOW_MS = 60_000;
const MAX_PER_WINDOW = 5;
const hits = new Map<string, { count: number; resetAt: number }>();

function rateLimit(key: string): boolean {
  const now = Date.now();
  const entry = hits.get(key);
  if (!entry || now > entry.resetAt) {
    hits.set(key, { count: 1, resetAt: now + WINDOW_MS });
    return true;
  }
  if (entry.count >= MAX_PER_WINDOW) return false;
  entry.count += 1;
  return true;
}

function clientKey(req: NextRequest): string {
  const fwd = req.headers.get("x-forwarded-for");
  return fwd?.split(",")[0]?.trim() || "local";
}

export async function POST(req: NextRequest) {
  if (!rateLimit(clientKey(req))) {
    return NextResponse.json(
      { ok: false, message: "Слишком много запросов. Попробуйте позже." },
      { status: 429 },
    );
  }

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json(
      { ok: false, message: "Некорректный запрос." },
      { status: 400 },
    );
  }

  const parsed = contactSchema.safeParse(body);
  if (!parsed.success) {
    const errors: ContactErrors = {};
    for (const issue of parsed.error.issues) {
      const field = issue.path[0] as keyof ContactErrors;
      if (field && !errors[field]) errors[field] = issue.message;
    }
    return NextResponse.json(
      { ok: false, message: "Проверьте корректность полей.", errors },
      { status: 422 },
    );
  }

  // Honeypot triggered — pretend success, drop silently.
  if (parsed.data.company) {
    return NextResponse.json({ ok: true });
  }

  try {
    const lead = await submitLead(parsed.data);
    return NextResponse.json({ ok: true, id: lead.id }, { status: 201 });
  } catch {
    return NextResponse.json(
      { ok: false, message: "Не удалось отправить заявку. Позвоните нам." },
      { status: 500 },
    );
  }
}
