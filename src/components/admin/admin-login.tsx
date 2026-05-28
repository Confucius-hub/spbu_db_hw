"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { LogoMark } from "@/components/brand/logo";
import { Button } from "@/components/ui/button";
import { Icon } from "@/lib/icons";

export function AdminLogin() {
  const router = useRouter();
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.error ?? "Ошибка входa");
      }
      router.refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка");
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-[80vh] items-center justify-center bg-slate-50 px-5 py-16">
      <div className="w-full max-w-sm rounded-3xl border border-slate-200 bg-white p-8 shadow-card">
        <div className="flex flex-col items-center text-center">
          <LogoMark className="h-14 w-14" />
          <h1 className="mt-4 text-xl font-bold text-navy-900">Панель управления</h1>
          <p className="mt-1 text-sm text-slate-500">Войдите, чтобы управлять контентом</p>
        </div>

        <form onSubmit={submit} className="mt-7 space-y-4">
          <div>
            <label htmlFor="admin-pass" className="mb-1.5 block text-sm font-medium text-slate-600">
              Пароль
            </label>
            <input
              id="admin-pass"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoFocus
              className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-navy-900 focus:border-gold-400 focus:outline-none focus:ring-2 focus:ring-gold-200"
              placeholder="••••••••"
            />
          </div>
          {error && <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
          <Button type="submit" variant="primary" size="lg" className="w-full" disabled={loading}>
            {loading ? "Вход…" : "Войти"}
            {!loading && <Icon name="ArrowRight" className="h-4 w-4" />}
          </Button>
        </form>

        <p className="mt-5 text-center text-xs text-slate-400">
          Пароль задаётся в переменной <code>ADMIN_PASSWORD</code> в файле <code>.env</code>
        </p>
      </div>
    </div>
  );
}
