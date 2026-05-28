import { createHmac, timingSafeEqual } from "crypto";
import { cookies } from "next/headers";

export const ADMIN_COOKIE = "sro_admin";
export const COOKIE_MAX_AGE = 60 * 60 * 24 * 7; // 7 дней

const SECRET = process.env.ADMIN_SESSION_SECRET ?? "dev-insecure-secret-change-me";

function sign(payload: string): string {
  return createHmac("sha256", SECRET).update(payload).digest("base64url");
}

function safeEqual(a: string, b: string): boolean {
  const bufA = Buffer.from(a);
  const bufB = Buffer.from(b);
  if (bufA.length !== bufB.length) return false;
  return timingSafeEqual(bufA, bufB);
}

export function createSessionToken(): string {
  const exp = String(Date.now() + COOKIE_MAX_AGE * 1000);
  return `${exp}.${sign(exp)}`;
}

export function verifySessionToken(token?: string | null): boolean {
  if (!token) return false;
  const [payload, signature] = token.split(".");
  if (!payload || !signature) return false;
  if (!safeEqual(signature, sign(payload))) return false;
  const exp = Number(payload);
  return Number.isFinite(exp) && exp > Date.now();
}

export function checkPassword(input: string): boolean {
  const expected = process.env.ADMIN_PASSWORD ?? "";
  if (!expected) return false;
  return safeEqual(input, expected);
}

/** Проверка сессии администратора (для server-компонентов и API). */
export async function isAdmin(): Promise<boolean> {
  const store = await cookies();
  return verifySessionToken(store.get(ADMIN_COOKIE)?.value);
}
