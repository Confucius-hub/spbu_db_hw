"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Icon } from "@/lib/icons";
import { cn, formatRuPhone } from "@/lib/utils";

export type LeadType = "CALLBACK" | "CONSULTATION" | "APPLICATION" | "CALCULATOR";
type ExtraField = "email" | "company" | "message";

const inputCls =
  "w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-[0.95rem] text-navy-900 placeholder:text-slate-400 transition-colors focus:border-gold-400 focus:outline-none focus:ring-2 focus:ring-gold-200";

export function LeadForm({
  type,
  fields = [],
  submitLabel = "Отправить заявку",
  source,
  tone = "light",
  payload,
  className,
}: {
  type: LeadType;
  fields?: ExtraField[];
  submitLabel?: string;
  source?: string;
  tone?: "light" | "dark";
  payload?: Record<string, unknown>;
  className?: string;
}) {
  const [state, setState] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [error, setError] = useState<string | null>(null);
  const [phone, setPhone] = useState("");

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const data = new FormData(form);
    if (data.get("website")) return; // honeypot

    setState("loading");
    setError(null);
    try {
      const res = await fetch("/api/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type,
          name: data.get("name"),
          phone: data.get("phone"),
          email: data.get("email") || undefined,
          company: data.get("company") || undefined,
          message: data.get("message") || undefined,
          source,
          payload,
        }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.error ?? "Не удалось отправить заявку");
      }
      setState("success");
      form.reset();
      setPhone("");
    } catch (err) {
      setState("error");
      setError(err instanceof Error ? err.message : "Ошибка отправки");
    }
  }

  if (state === "success") {
    return (
      <div
        className={cn(
          "flex flex-col items-center gap-3 rounded-2xl border border-emerald-200 bg-emerald-50 p-6 text-center",
          className,
        )}
      >
        <span className="inline-flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
          <Icon name="CheckCircle2" className="h-7 w-7" strokeWidth={2} />
        </span>
        <p className="text-lg font-bold text-navy-900">Заявка отправлена!</p>
        <p className="text-sm text-slate-600">
          Менеджер свяжется с вами в течение 15 минут в рабочее время.
        </p>
        <button
          type="button"
          onClick={() => setState("idle")}
          className="text-sm font-semibold text-navy-700 underline underline-offset-4"
        >
          Отправить ещё одну
        </button>
      </div>
    );
  }

  const labelCls = cn(
    "mb-1.5 block text-sm font-medium",
    tone === "dark" ? "text-slate-300" : "text-slate-600",
  );

  return (
    <form onSubmit={handleSubmit} className={cn("space-y-3.5", className)} noValidate>
      <div className="hidden" aria-hidden>
        <label>
          Не заполняйте
          <input type="text" name="website" tabIndex={-1} autoComplete="off" />
        </label>
      </div>

      <div>
        <label className={labelCls} htmlFor={`name-${type}`}>
          Ваше имя
        </label>
        <input
          id={`name-${type}`}
          name="name"
          required
          minLength={2}
          placeholder="Иван Иванов"
          className={inputCls}
          autoComplete="name"
        />
      </div>

      <div>
        <label className={labelCls} htmlFor={`phone-${type}`}>
          Телефон
        </label>
        <input
          id={`phone-${type}`}
          name="phone"
          type="tel"
          required
          inputMode="tel"
          value={phone}
          onChange={(e) => setPhone(formatRuPhone(e.target.value))}
          placeholder="+7 (___) ___-__-__"
          className={inputCls}
          autoComplete="tel"
        />
      </div>

      {fields.includes("company") && (
        <div>
          <label className={labelCls} htmlFor={`company-${type}`}>
            Компания
          </label>
          <input
            id={`company-${type}`}
            name="company"
            placeholder="ООО «Ваша компания»"
            className={inputCls}
            autoComplete="organization"
          />
        </div>
      )}

      {fields.includes("email") && (
        <div>
          <label className={labelCls} htmlFor={`email-${type}`}>
            E-mail
          </label>
          <input
            id={`email-${type}`}
            name="email"
            type="email"
            placeholder="mail@company.ru"
            className={inputCls}
            autoComplete="email"
          />
        </div>
      )}

      {fields.includes("message") && (
        <div>
          <label className={labelCls} htmlFor={`message-${type}`}>
            Сообщение
          </label>
          <textarea
            id={`message-${type}`}
            name="message"
            rows={4}
            placeholder="Кратко опишите ваш вопрос"
            className={cn(inputCls, "resize-none")}
          />
        </div>
      )}

      {error && (
        <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>
      )}

      <Button type="submit" variant="gold" size="lg" className="w-full" disabled={state === "loading"}>
        {state === "loading" ? "Отправляем…" : submitLabel}
        {state !== "loading" && <Icon name="ArrowRight" className="h-4 w-4" />}
      </Button>

      <p className={cn("text-center text-xs", tone === "dark" ? "text-slate-400" : "text-slate-400")}>
        Нажимая кнопку, вы соглашаетесь с{" "}
        <a href="/privacy" className="underline underline-offset-2 hover:text-gold-600">
          политикой обработки персональных данных
        </a>
        .
      </p>
    </form>
  );
}
